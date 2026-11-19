# 偉人の言葉帳 AI社員 手順書（RUNBOOK）

インスタアカウント **@meigen_shigoto**（表示名「偉人の言葉帳｜仕事に効く言葉」）を、AI社員が運用するための手順書です。
スケジュール実行で動くClaudeは、毎回この手順書を読んでから作業します。

## 基本情報

| 項目 | 値 |
| --- | --- |
| 管理画面（アーティファクト）slug | `f4f3fce5-b04f-46d3-b84a-4e5ba15a900d` |
| このリポジトリ | `0925od-art/meigen-office`（公開） |
| 画像の公開URLの頭 | `https://raw.githubusercontent.com/0925od-art/meigen-office/main/` |
| インスタ投稿の連携 | Windsor.ai コネクタ `instagram`、アカウントID `17841427258662963` |
| 投稿枠（日本時間） | 08:00 / 12:00 / 22:00 の1日3本 |
| 承認ルール | 代表が管理画面で「承認済み」にした投稿だけを出す。未承認は出さない |
| 時刻 | すべて日本時間（Asia/Tokyo）で考える |

## 読者とトーン

- 読者：仕事で伸び悩む社会人、部活で伸び悩む人。しんどい時に前を向ける言葉を届ける
- トーン：説教くさくしない。短く、やさしく、具体的に。「明日からこう使える」まで落とし込む
- 枠ごとの狙い
  - 08:00 朝：背中を押す、やる気が出る言葉
  - 12:00 昼：考え方・仕事術のヒントになる言葉
  - 22:00 夜：一日の終わりに肩の力が抜ける、癒やしの言葉

## 名言選びの絶対ルール（最重要）

1. **出典がはっきりしている言葉だけを使う。** 「〜の名言」として出回っているが本人の言葉か怪しいものは使わない
2. 優先する出典：原典が残っている古典・著作（『論語』『孟子』『老子』、渋沢栄一『論語と算盤』、福沢諭吉『学問のすゝめ』、宮本武蔵『五輪書』、新渡戸稲造『武士道』など）
3. 近現代の人物・スポーツ選手の言葉は、信頼できる報道・本人の著書・公式インタビューで確認できた場合だけ使い、確認したURLか書名を `source_url` / `source` に必ず残す。確認できなければ使わない
4. 近現代の言葉の引用は短く（1〜2文）。長い文章をそのまま写さない
5. `used_quotes.json` にある言葉は使わない（同じ人物は3日以上あける）
6. 迷ったら使わない。報連相の「相談」として管理画面に書く

## 投稿データの形（posts/<id>.json）

id は `YYYY-MM-DD-HH`（HH は 08 / 12 / 22）。例：`2026-11-20-08`

```json
{
  "id": "2026-11-20-08",
  "date": "2026-11-20",
  "slot": "2026-11-20 08:00",
  "person": "人物名",
  "source": "出典（書名・篇名など）",
  "source_url": "近現代の言葉なら確認したURL。古典なら空でよい",
  "theme": "誰に向けた投稿か（例：仕事がしんどい人へ）",
  "slides": [
    {"type": "cover", "kicker": "短い呼びかけ", "title": "大きな見出し\n2行まで", "sub": "〇〇の言葉"},
    {"type": "quote", "quote": "名言本文\n1行14文字以内で改行", "by": "人物名『出典』"},
    {"type": "body", "head": "どういう意味？", "lines": ["1行18文字以内", "", "空行で区切る"]},
    {"type": "body", "head": "仕事に活かすなら", "lines": ["具体的な行動に落とす", "例：〜"]},
    {"type": "end", "title": "締めの一言\n2行まで", "sub": "保存しておいてください", "handle": "@meigen_shigoto"}
  ],
  "caption": "投稿文（2000文字以内）。最後に問いかけとフォローのお願い",
  "hashtags": ["#名言", "#偉人の言葉", "... 8〜10個"]
}
```

文字数の目安：cover の title は1行7文字まで、quote は1行14文字・6行まで、body は1行18文字・8行まで。はみ出すと画像からあふれるので、作った画像は必ず目で確認する。

## 仕事A：毎朝の投稿案づくり（スケジュール実行 06時台）

1. このリポジトリを attach して clone する（add_repo で `0925od-art/meigen-office` を push 権限で追加）
2. `used_quotes.json` を読む
3. 管理画面の `posts` を `db_list` で読み、`status` が「修正依頼」のものがあれば先に直す
   - `note` の指示どおりに posts/<id>.json を直し、画像を作り直し、push し、アセットを上げ直す
   - `db_write` で images / imageUrls / caption など直した項目と `status: "承認待ち"`, `note: ""` を update（ifVersion 必須）
   - reports に「修正しました：〜」と報告
4. 今日（日本時間）の 08 / 12 / 22 の3本を作る。すでに同じ id の投稿が管理画面にあればその枠は作らない
   - 08:00 の枠が実行時刻より前に過ぎていても作ってよい（代表が承認すれば翌日以降に回す判断は代表がする）
5. 各投稿を `posts/<id>.json` に保存し、画像を作る：
   `python3 make_slides.py posts/<id>.json images/<YYYY-MM-DD>`
6. 画像を Read で開いて、文字のはみ出し・誤字がないか確認。問題があれば直して作り直す
7. `git add -A && git commit -m "<日付> 投稿案" && git push`
8. 公開URL `imageUrls` = `https://raw.githubusercontent.com/0925od-art/meigen-office/main/images/<日付>/<id>_<n>.jpg`
9. 管理画面に表示する用に、同じ画像を `upload_asset`（slug は上の表）で上げ、返ってきた url を `images` にする
10. `db_write` で `posts/<id>` を set：
    `date, slot, person, source, source_url, theme, caption, hashtags, images, imageUrls, status: "承認待ち", note: ""`
11. 社員の状態を更新：`db_list staff` で version を取り、`staff/neta` `staff/daihon` `staff/design` `staff/toukou` を update
    （`status`: 完了 / 作業中 / 待機中、`task`: 今日やったこと、`done`: 累計の仕事数を+3）
12. `reports` に4人分の報告を add（`at`: ISO時刻、`from`: 係名、`fromId`: neta / daihon / design / toukou、`text`: 1〜3文）
    最後の投稿・報告係の報告は「代表、本日の3本の確認をお願いします」で締める
13. `used_quotes.json` に今日の3本（日付・人物・名言の冒頭・出典）を追記して commit / push

## 仕事B：投稿（スケジュール実行 08:01 / 12:01 / 22:01）

1. 今の日本時間から枠を決める：7〜10時なら 08、11〜14時なら 12、21〜23時なら 22。`slot = "YYYY-MM-DD HH:00"`
2. `db_list` で `posts` を読み、`slot` が一致する投稿を探す
3. 見つかった投稿の `status` で分ける
   - **承認済み** → 投稿する（4へ）
   - **承認待ち / 修正依頼** → 投稿しない。reports に投稿・報告係から「〇時の投稿は未承認のため見送りました」と報告して終わり
   - **投稿済み** → 何もしない
   - 見つからない → reports に「〇時の投稿案がありませんでした」と報告して終わり
4. Windsor.ai の `execute_action`：connector `instagram`、account `17841427258662963`、action `create_carousel_post`、
   params `image_urls` = 投稿の `imageUrls`（2〜10枚）、`caption` = `caption + "\n\n" + hashtags をスペースでつないだもの`（2200文字以内）
   - `imageUrls` が無い投稿は投稿せず、エラーとして報告する
5. 成功したら `db_write` で `status: "投稿済み"`, `postedAt`（ISO時刻）, 返ってきたメディアIDがあれば `mediaId` を update。
   reports に投稿・報告係から「〇時に『人物名』の投稿を公開しました」と報告
6. 失敗したら1回だけやり直す。それでもだめなら `error` にエラー内容を update し、reports に報告。勝手に別の投稿を出さない
7. 投稿は1回の実行で1本だけ。同じ投稿を二度出さない（実行前に status が投稿済みでないか必ず確認）
