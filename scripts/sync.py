"""ガソリン価格.com の /data/ から CSV を取り込む（毎日 GitHub Actions が実行）。

安全のための決まり：
- 取りに行く先は https://gasoline-kakaku.com/data/ の決まったファイルだけ（下の FILES と、2004年から今年までの年別の週の CSV）。
- 1つでも検査に通らなければ、何も書き換えずに終了する（前の CSV がそのまま残る）。
- 検査：HTTP 200・UTF-8（BOM 付き）・1行目が期待どおりの列名・行数が前回の 90% 以上・容量 25MB 以下。
  今年の年別のファイルだけは、年が明けて最初の調査が公表されるまで無い（404）ので、そのときは飛ばす。
- 取り込んだ年別の週の CSV をつないだ data/prefecture_weekly_all.csv もここで作る（Kaggle が1ファイルで読めるように。サイトには無い）。
- 鍵やトークンは使わない（公開ページを読むだけ）。
- 容量の見張り：どれかの CSV が 20MB を超えたら、このリポジトリに Issue を1件立てる（運営者に GitHub からメールが届く）。
  Cloudflare Pages の上限は1ファイル 25MiB。Issue が来たらファイルの分け方を見直す。
"""
import csv
import datetime as dt
import io
import json
import os
import sys
import urllib.error
import urllib.request

BASE = "https://gasoline-kakaku.com/data/"
FILES = {
    "prefecture_latest.csv": "調査日,都道府県コード,都道府県名,地方,レギュラー_価格,",
    "prefecture_yearly.csv": "年,都道府県コード,都道府県名,週の数,レギュラー_年平均,",
    "national_weekly.csv": "調査日,レギュラー,ハイオク,軽油,灯油_店頭,灯油_配達",
}
WEEKLY_HEAD = "調査日,都道府県コード,都道府県名,レギュラー,ハイオク,軽油,灯油_店頭,灯油_配達"
FIRST_YEAR = 2004
ALL_NAME = "prefecture_weekly_all.csv"
MAX_BYTES = 25 * 1024 * 1024
WARN_BYTES = 20_000_000
ISSUE_TITLE = "CSV の容量が 20MB を超えました（構成の見直しが必要）"
UA = "japan-gasoline-prices-sync (+https://github.com/velonica999/japan-gasoline-prices)"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def rows(b):
    return sum(1 for _ in csv.reader(io.StringIO(b.decode("utf-8-sig")))) - 1


def fetch(fn):
    """(バイト列, None) か (None, エラー)。404 は (None, 404)"""
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE + fn, headers={"User-Agent": UA}), timeout=60) as r:
            if r.status != 200:
                return None, f"HTTP {r.status}"
            return r.read(MAX_BYTES + 1), None
    except urllib.error.HTTPError as e:
        return None, 404 if e.code == 404 else f"HTTP {e.code}"
    except Exception as e:
        return None, f"取得失敗 {e}"


def check(fn, b, head):
    if len(b) > MAX_BYTES:
        return "25MB を超えた"
    if not b.startswith(b"\xef\xbb\xbf"):
        return "BOM 付き UTF-8 ではない（HTML のエラーページなどの恐れ）"
    try:
        text = b.decode("utf-8-sig")
    except UnicodeDecodeError:
        return "UTF-8 として読めない"
    if not text.startswith(head):
        return f"列名が想定と違う：{text.splitlines()[0][:120]}"
    old = os.path.join(OUT, fn)
    if os.path.exists(old):
        n, n_old = rows(b), rows(open(old, "rb").read())
        if n < n_old * 0.9:
            return f"行数が急に減った（{n_old:,} → {n:,}）"
    return None


def size_alert(big):
    """20MB を超えた CSV があれば Issue を立てる（同じ題の Issue が開いていれば何もしない）。失敗しても取り込みは止めない"""
    token, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not big or not token or not repo:
        return
    api = f"https://api.github.com/repos/{repo}/issues"
    hd = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "User-Agent": UA}
    try:
        with urllib.request.urlopen(urllib.request.Request(api + "?state=open&per_page=100", headers=hd), timeout=30) as r:
            if any(i.get("title") == ISSUE_TITLE for i in json.load(r)):
                print("容量の Issue は既に開いている")
                return
        body = ("次の CSV が 20MB を超えました。Cloudflare Pages の上限は1ファイル 25MiB です。\n\n"
                + "\n".join(f"- {fn}: {sz / 1e6:.1f}MB" for fn, sz in big)
                + "\n\nファイルの分け方を見直してください。直したらこの Issue を閉じてください。")
        req = urllib.request.Request(api, data=json.dumps({"title": ISSUE_TITLE, "body": body}).encode(), headers=hd, method="POST")
        with urllib.request.urlopen(req, timeout=30):
            print("::warning::容量の Issue を立てた")
    except Exception as e:
        print(f"::warning::容量の Issue を立てられなかった：{e}")


def main():
    this_year = dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).year
    want = dict(FILES)
    for y in range(FIRST_YEAR, this_year + 1):
        want[f"prefecture_weekly_{y}.csv"] = WEEKLY_HEAD
    got, ng = {}, []
    for fn, head in want.items():
        b, err = fetch(fn)
        if err == 404 and fn == f"prefecture_weekly_{this_year}.csv":
            print(f"{fn}: まだ無い（年が明けて最初の公表の前）。飛ばす")
            continue
        if err:
            ng.append(f"{fn}: {err}")
            continue
        e = check(fn, b, head)
        if e:
            ng.append(f"{fn}: {e}")
            continue
        got[fn] = b
    if ng:
        for m in ng:
            print(f"::error::{m}")
        print("取り込みを中止（前の CSV のまま）")
        sys.exit(1)
    # 年別の週の CSV をつないだもの（1行目の列名は1回だけ）
    lines = [WEEKLY_HEAD]
    for fn in sorted(f for f in got if f.startswith("prefecture_weekly_")):
        lines += got[fn].decode("utf-8-sig").replace("\r\n", "\n").rstrip("\n").split("\n")[1:]
    allb = ("﻿" + "\r\n".join(lines) + "\r\n").encode("utf-8")
    e = check(ALL_NAME, allb, WEEKLY_HEAD)
    if e:
        print(f"::error::{ALL_NAME}: {e}")
        sys.exit(1)
    got[ALL_NAME] = allb
    os.makedirs(OUT, exist_ok=True)
    for fn, b in got.items():
        with open(os.path.join(OUT, fn), "wb") as f:
            f.write(b)
        print(f"{fn}: {rows(b):,} 行・{len(b) / 1e6:.2f}MB")
    size_alert([(fn, len(b)) for fn, b in got.items() if len(b) > WARN_BYTES])


if __name__ == "__main__":
    main()
