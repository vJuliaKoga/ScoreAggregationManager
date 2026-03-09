---
meta:
  artifact_id: PRM-PLN-TRANS-002
  file: PRM-PLN-TRANS-002.md
  author: "@juria.koga"
  source_type: human
  source: manual
  timestamp: "2026-03-01T15:24:00+09:00"
  content_hash: 137f2fb8cf5f836829fabd906b67ded679d17b5a6485d1e5627a3993eaf69e22
---

あなたは AIDD-QualityGates の分析担当です。コードやファイルの編集はしません。
DeepEval結果（0308_2051.json）を読み取り、「YAMLにあってMDにないもの」「MDにあってYAMLにないもの」を一覧化してください。
出力はMarkdownのみ。

# 入力

- DeepEval結果JSON: 0308_2051.json

# 出力

- output\G4\reports\pln_eval\RES-PLN-G4-REVIEW-002.md

# 出力形式（厳守）

## 1. YAML→MD ギャップ（Faithfulness起点）

- ファイルごとに見出しを作る（例：### PLN-PLN-PACK-001）
- その下に、top_missing_lines を箇条書きでそのまま列挙
- 各項目にラベルを付ける：
  - [MD追記] 参照MDが薄いだけで、SSOTに書くべき主張
  - [YAML弱め] 未確定/言い切り過多/設計で決めるべき主張
  - [メタ除外] 変換理由/章ラベル/運用メタ（rationale/primary_section/ssot_note相当）

## 2. MD→YAML ギャップ（Coverage起点）

- details.coverage.files[].items[] を見て、covered=false の item をファイルごとに列挙
- 可能なら best_sim と best_match（空なら空）も併記
- 各項目にラベルを付ける：
  - [YAML追記] YAML側に同語彙の短文を最小追記すべき
  - [言い回し統一] YAMLに近い語彙があるので表現寄せで解消できる
  - [不要] 企画SSOTとして不要（または重複）

## 3. 優先度Top10

- 1と2を統合して、修正インパクトが高い順にTop10を出す（理由も1行）

# 注意

- 0308_2051.json の情報だけで判断し、推測で新しい内容を作らない。
- 変更は提案のみ。diffは出さない。
