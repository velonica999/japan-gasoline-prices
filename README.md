# japan-gasoline-prices：日本のガソリン・軽油・灯油価格データ（全国平均・47都道府県・週次 CSV）

資源エネルギー庁「石油製品価格調査（給油所小売価格調査）」をもとに [ガソリン価格.com](https://gasoline-kakaku.com/) が整理・集計した、**全国平均と47都道府県**のレギュラー・ハイオク・軽油・灯油（店頭・配達）の価格の CSV です。都道府県別は2004年6月から、全国平均は1990年8月から、毎週の値があります。

- データの説明とダウンロード：https://gasoline-kakaku.com/data/
- サイトで見る（都道府県・油種・週ごとのページ）：https://gasoline-kakaku.com/
- Kaggle：https://www.kaggle.com/datasets/velonica999/japan-weekly-gasoline-prices-by-prefecture （このリポジトリの4ファイルを毎週取り込み）
- 更新：このリポジトリの CSV は、毎日サイトの `/data/` から自動で取り込んでいます。サイトは資源エネルギー庁の公表（原則として毎週水曜日）のあと自動で更新します。

## ファイル

| ファイル | 内容 |
|-|-|
| `data/prefecture_latest.csv` | 今週の全国平均（00）と47都道府県の5油種の価格・前週差・1年前差・高い順の順位 |
| `data/prefecture_weekly_all.csv` | 2004年からの週ごとの値（全国平均と47都道府県・5油種）。下の年別のファイルをつないだもの |
| `data/prefecture_weekly_YYYY.csv` | 同じ値の年別のファイル（2004年〜今年） |
| `data/prefecture_yearly.csv` | 年平均（全国は1990年から、47都道府県は2004年から。今年は途中まで） |
| `data/national_weekly.csv` | 全国平均の週ごとの値（1990年8月27日調査から） |

文字コードは UTF-8（BOM 付き）で、Excel でそのまま開けます。都道府県コードは 01〜47（全国は 00）。価格の単位は、レギュラー・ハイオク・軽油が1Lあたりの円、灯油が18Lあたりの円（店頭現金価格・消費税込み）です。値が無い週・県は空欄です。

## 主な列

| 列名 | 意味 | Description |
|-|-|-|
| 調査日 | 調査日（原則として月曜日。公表は水曜日） | survey date (YYYY-MM-DD) |
| 都道府県コード・都道府県名 | 01〜47、全国は 00 | prefecture code and name |
| レギュラー・ハイオク・軽油 | 1Lあたりの円 | regular / premium gasoline, diesel (yen per liter) |
| 灯油_店頭・灯油_配達 | 18Lあたりの円 | kerosene, store price / home delivery (yen per 18 liters) |
| ○○_前週差・○○_1年前差 | 前の週・約52週前の調査との差（円） | change from previous week / about 52 weeks earlier |
| ○○_順位_高い順 | 47都道府県の中の順位（1＝いちばん高い） | rank among 47 prefectures, 1 = most expensive |
| ○○_年平均・週の数 | その年の週の値の単純平均と、平均した週の数 | annual simple average and number of weeks |

2004年3月までの全国平均は消費税を含まない値で公表されていたため、`national_weekly.csv` の長い推移は2004年の前後で続いていません。全列の説明は https://gasoline-kakaku.com/data/ に、データの読み方は https://gasoline-kakaku.com/guide/how-to-read/ にあります。

## 利用条件（ライセンス）

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja)。商用・非商用を問わず、報道・ブログ・研究・授業・アプリ・AI の学習や回答などに自由に使えます。条件は出典を明記することだけです。

**「出典を明記する」とは？** 使った数字がどこのデータかを、読む人に分かるように書き添えることです。次の1行をコピーして、数字や表・グラフのすぐ下か、記事・資料の最後に貼り付けてください。

```
出典：ガソリン価格.com（資源エネルギー庁「石油製品価格調査」にもとづく集計） https://gasoline-kakaku.com/data/
```

- ブログ・ホームページ：表やグラフのすぐ下に貼る
- 資料・スライド・レポート：そのページの下の端か、最後の「参考資料」に書く
- SNS・動画：投稿文や概要欄の最後に書く
- 表を加工・グラフ化したとき：「出典：ガソリン価格.comのデータをもとに作成 https://gasoline-kakaku.com/data/」と書く
- URL は行の最後に置き、前に空白を入れる（URL のすぐ後ろに文字やカッコを続けると、リンクが切れることがあります）

許可の連絡やお金は要りません。出典さえ書けば、仕事（商用）でも自由に使えます。

元のデータは、資源エネルギー庁「[石油製品価格調査](https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl007/results.html)」で、資源エネルギー庁のウェブサイトの利用規約（公共データ利用規約 第1.0版＝PDL1.0。CC BY 4.0 と互換）に基づき、ガソリン価格.com が整理・集計しています（前週差・1年前差・順位・年平均はガソリン価格.com の計算）。資源エネルギー庁が作成したものではありません。

---

## English

Weekly retail prices of regular and premium gasoline, diesel and kerosene (store and home delivery) in Japan: **national average and all 47 prefectures**, weekly since June 2004 (national average since August 1990). Compiled by [gasoline-kakaku.com](https://gasoline-kakaku.com/) from the Agency for Natural Resources and Energy (ANRE) "Petroleum Products Price Survey". Prices are cash prices at service stations including consumption tax; gasoline and diesel in yen per liter, kerosene in yen per 18 liters. Files are UTF-8 with BOM. License: CC BY 4.0 — please credit "gasoline-kakaku.com, based on ANRE Petroleum Products Price Survey: https://gasoline-kakaku.com/data/". The source data is published under the Public Data License 1.0 (compatible with CC BY 4.0). Not produced by ANRE. Synced daily from https://gasoline-kakaku.com/data/. Also on Kaggle: https://www.kaggle.com/datasets/velonica999/japan-weekly-gasoline-prices-by-prefecture
