---
meta:
  artifact_id: PRM-PLN-G4-FIX-004
  file: PRM-PLN-G4-FIX-004.md
  author: "@juria.koga"
  source_type: human
  source: manual
  timestamp: "2026-03-08T21:08:00+09:00"
  content_hash: 0280ff4bdeb6027a86183fe57ca7e25eeffcffd4879cf83b75dab01e5add15ad
---

あなたは AIDD-QualityGates リポジトリの修正担当です。
入力として与える「ギャップ一覧レポート」に従って、split MD または YAML を最小差分で修正してください。
出力は unified diff のみです。

# 更新履歴への記録（必須）

- 今回の修正は prompt_id: PRM-PLN-G4-FIX-004 に基づく対応として扱う
- 参照レポートは RES-PLN-G4-REVIEW-002.md とする
- 変更したファイルには、既存の更新履歴/メタ情報/注記欄がある場合のみ、
  - prompt_id: PRM-PLN-G4-FIX-004
  - reviewed_by_report: RES-PLN-G4-REVIEW-002.md
    を追記する
- 既存のスキーマやフォーマットに更新履歴欄が無い場合は、無理に新設しない
- split MD に不自然なメタ情報本文を追記しない
- YAMLの meta セクションが既にある場合のみ、その範囲で更新履歴を追記する
- 更新履歴を書けないファイルは、内容修正のみ行う

# 入力

- ギャップ一覧レポート（Markdown）
- 対象ディレクトリ
  - split MD: artifacts/planning/PLN-PLN-SPLIT-001/\*.md
  - YAML: artifacts/planning/yaml/\*.yaml

# 目的

- レポートで分類済みの差分を解消する
- 修正対象はレポートに載っている項目だけ
- DeepEval の Faithfulness / Coverage を改善する
- Completeness / Consistency を壊さない
- スキーマ検証を壊さない

# 絶対ルール

- レポートに載っていないファイルは編集しない
- ファイル名変更禁止
- derived_from 変更禁止
- split MD を YAML/JSON/テーブル構造に変換しない
- YAMLの配列型やオブジェクト型を壊さない
- null必須キーを削除しない
- コメントだけで語彙を足さない
- G2仕様は以下を守る
  - Done に理由は不要
  - Abort のみ理由が必要

# 修正ルール

## 1) [MD追記] の項目

- 対応する split MD のみ編集する
- 追記は自然文の箇条書きのみ
- 各行は「〜する。」「〜である。」で終える
- YAML風の記法は禁止
  - 例: `name:` `purpose:` `basis:` `- key:` を書かない
- 既存に同趣旨の記述がある場合は、重複追記せず表現統一に留める
- 1ファイルあたりの追記は最小限（3〜7項目目安）

## 2) [YAML追記] の項目

- 対応する YAML のみ編集する
- スキーマを壊さず、既存構造に沿って自然文を最小限で追加する
- object配列を string配列に変えない
- 既存の description / note / text / explanation / summary 相当の場所があればそこを優先して使う
- 無ければ、既存スキーマの文脈に沿う最小限の自然文フィールドに入れる
- YAML骨組みのためのダミーキー追加は禁止

## 3) [言い回し統一] の項目

- 参照MDとYAMLで重要語彙を揃える
- 意味を変えず、語彙差だけを縮める
- 数値・固有名詞・条件語は保持する

## 4) [YAML弱め] の項目

- 未確定の断定だけを弱める
- 例:
  - 「必須である」→「想定する」「方針とする」
  - 「実施する」→「実施を想定する」
- ただし意味を大きく変えない
- 確定済み仕様まで弱めない

## 5) [メタ除外] / [不要]

- 編集しない
- diffに含めない

# 作業手順

1. ギャップ一覧レポートの「優先度Top10」を上から順に処理する
2. 各項目のラベルに応じて、MD追記 / YAML追記 / 言い回し統一 / YAML弱め を実施する
3. 更新履歴欄が存在するファイルのみ、prompt_id と report名を追記する
4. 変更対象ファイルごとにまとめて diff を作る
5. 提出前にセルフチェックする

# 提出前セルフチェック

- 変更ファイルがレポート対象外に1つでも広がっていないか
- split MD に YAML風の `key: value` 行が入っていないか
- YAMLの配列/オブジェクト型を壊していないか
- Done理由不要 / Abort理由必要 の仕様に反していないか
- 同じ内容をMDとYAMLの両方に過剰重複していないか
- 更新履歴の追記先が既存フォーマットの範囲内か（新設しすぎていないか）

# 出力

- unified diff のみ
- 説明文は不要
