---
meta:
  artifact_id: PRM-PLN-G4-FIX-003
  file: PRM-PLN-G4-FIX-003.md
  author: "@juria.koga"
  source_type: human
  source: manual
  timestamp: "2026-03-08T14:22:00+09:00"
  content_hash: 458ba5d946778e26d7b2d5a0cb4637aa467f32672841e9b503eea8bd990601e6
---

あなたはAIDD-QualityGatesのドキュメント整備担当です。
目的は、split MD（SSOT）を自然文で追記して、G4/PLN DeepEvalのFaithfulness FAILを減らすことです。

# 入力

- DeepEval結果JSON: 0308_1410.json（または最新）
- split MD: artifacts\planning\PLN-PLN-SPLIT-001\*.md
- YAML: artifacts\planning\yaml\*.yaml
- 1:1対応: YAMLのderived_fromがSSOT（対応MD）を指す

# 絶対禁止（形式）

- split MD をYAML構造にしない
- YAML風のキー表現は禁止（例: `name:` `purpose:` `basis:` `- key:` など “キー: 値” 形式）
- JSON形式、テーブル形式も禁止

# 追記の形式（強制）

- 追記は必ず「自然文の箇条書き」
- 1ファイルにつき3〜7個
- 各行は「〜する。」「〜である。」で終える
- 固有名詞/数値/条件語/ツール名は残す（Coverage/語彙一致のため）

# 手順

1. JSONのresultsから category="faithfulness" かつ status="fail" を抽出（scoreが低い順）。
2. 各failについて、対象YAMLを開き derived_from で対応する split MD を特定する。
3. reason(local) の [top_missing_lines] を追記候補とし、次の分類をする：
   A: SSOTとして追記すべき（企画として決めたい仕様/運用上必要/出力の意味/判断基準/スコア解釈）
   B: 追記不要（変換理由/章ラベル/運用メタ/ファイル情報/ハッシュ/タイムスタンプ等）
   C: 保留（未確定の断定、将来案）→MDへ入れず保留理由だけ残す
4. Aだけを split MD に追記する（自然文箇条書き）。

# パネル定義（MDへの書き方例：この文体で）

- 自動ゲート結果はG1〜G5およびPromptfooの結果を一覧で表示する。
- G2は人のチェックリスト結果を別枠で表示し、チェック項目ごとのスコアを集計して反映する。
- G2のAbortは理由を必須とし、Doneは理由不要とする。
- 証跡リンクは必要な場合に付けられるようにする。
- 重み付き合算スコアはウェイト定義（9.3節）に基づき各ゲート得点を合算した総合指標である。
- 各ゲートの内訳として、ゲート別のスコア分布や内訳を確認できるようにする。
- スコア推移はDeep EvalとPromptfooの推移を追跡し、改修前後やモデル変動による品質変化を可視化する。
- Abort分析はカテゴリ分布と理由品質を集計し、判断回避の常態化を検知する。
- Traceability Matrixは要件→設計→テストの紐付けを表示する。

# 出力要件

- 変更対象は split MD のみ（YAMLは変更しない）
- 変更した各MDファイルの unified diff を出す
- 各MDで「追記した要点（最大3行）」と「B/Cのスキップ理由」を併記
