---
meta:
  artifact_id: PRM-PLN-G4-FIX-002
  file: PRM-PLN-G4-FIX-002.md
  author: "@juria.koga"
  source_type: human
  source: manual
  timestamp: "2026-03-08T13:16:00+09:00"
  content_hash: a68de1cb65eb17c4851c7366a276d448362a6c335d748564db9b6edfa4fde483
---

あなたはAIDD-QualityGatesのドキュメント整備担当です。
目的は「split MD（SSOT）を厚くしてFaithfulnessを改善すること」です。
重要：MDをYAML構造に変換したり、YAMLキー形式（name: / basis: / purpose: 等）で記述してはいけません。

# 入力

- DeepEval結果JSON: 0308_1306.json（または最新）
- split MD: artifacts\planning\PLN-PLN-SPLIT-001\*.md
- YAML: artifacts\planning\yaml\*.yaml
- 対応はYAMLの derived_from で決める（1:1）

# やること

- FaithfulnessでFAILしているYAMLについて、対応する split MD に「YAMLに含まれる“意味のある主張”」の根拠を自然文で追記する。
- 追記はMDの見出し配下に「箇条書き（自然文）」で3〜7個/ファイル。
- 追記した結果、次回のFaithfulnessで「参照に無い主張」扱いされない状態に寄せる。

# 絶対禁止（出力形式の禁止）

- YAML形式・YAML風のキー表現は禁止：
  - 例：`name:` `basis:` `purpose:` `- key:` などコロンでキーを書く形式は禁止
- YAMLの行をそのままMDへ貼り付けることも禁止する。
  - DeepEval reason の top_missing_lines はコピペせず、主張を抽象化して自然文に言い換えて追記する。
- JSON形式も禁止
- テーブルでの構造化も禁止（必要なら箇条書きで）
- “MDをYAML構造に直す” “YAML定義を書き起こす” は禁止

# 追記の書き方（強制フォーマット）

- 追記は必ずこの形で書く：
  - 見出し（既存） + その直下に箇条書き
  - 各箇条書きは「〜する。」「〜である。」など自然文で終える
  - 重要語（固有名詞/数値/条件語/ツール名）は残す
- 章ラベルや変換理由は書かない（rationale/primary_section/ssot_note相当は禁止）

# 追記内容の判断ルール

- 追記すべき（A）：
  - 企画として決めたい仕様/運用上必要なルール/出力の意味/判断基準/スコアの解釈
- 追記しない（B）：
  - 変換理由、章ラベル、ファイルパス、ハッシュ、タイムスタンプなど運用メタ
- 保留（C）：
  - 企画段階で未確定の断定（将来案、言い切り過多）→MDに入れず、保留理由をメモ

# 具体例（今回の「パネル定義」をMDに落とす場合）

以下の内容は「YAMLキー」ではなく「UI表示の項目」として、MDには自然文で書くこと。
例（このスタイルで書け。コロン禁止）：

- 自動ゲート結果はG1〜G5およびPromptfooの結果を一覧で表示する。
- G2は人のチェックリスト結果を別枠で表示し、チェック項目ごとのスコアを集計して反映する。
- G2のAbortは理由を必須とし、Doneは理由不要とする。
- 証跡リンクは必要な場合に付けられるようにする。
- 重み付き合算スコアは、ウェイト定義（9.3節）に基づいて各ゲート結果を合算した値である。
- 各ゲートの内訳として、スコア分布や内訳を確認できるようにする。
- スコア推移はDeep EvalとPromptfooの推移を追跡し、モデル変動や改修前後の品質変化を可視化する。
- Abort分析ではカテゴリ分布と理由品質を集計し、判断回避の常態化を検知する。
- Traceability Matrixでは要件→設計→テストの紐付けを確認できるようにする。

# 手順

1. JSONのresultsから category="faithfulness" かつ status="fail" のものを抽出（score低い順）。
2. 各failについて、対象YAMLを開き derived_from から対応する split MD を特定。
3. reason(local)の top_missing_lines を「MDへ追記する候補」として参照。
4. A/B/Cに分類し、AだけをMDに追記（自然文の箇条書き）。
5. B/CはMDを変更せず、短い理由をメモする。

# 出力要件

- 変更対象は split MD のみ（YAMLは変更しない）
- 変更したMDファイルの unified diff を出す
- 各MDについて、追記した要点を3行以内で要約
- B/Cのスキップ理由もファイル単位で列挙
