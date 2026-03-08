---
meta:
  artifact_id: PLN-PLN-CHECKLIST-001
  file: PLN-PLN-CHECKLIST-001.md
  author: gpt-5.2
  source_type: ai
  source: codex
  prompt_id: PRM-PLN-MD-001
  timestamp: "2026-03-03T21:06:59+09:00"
  model: gpt-5.2
  content_hash: aa6a48b2d0510a8c3430f9709d398f7dee90a5bd8fcbd469ab8501a05549ed3f
---

## 10. チェックリスト資産（標準搭載）

### 10.1 要件妥当性チェックリスト（CHK-REQ-REVIEW-001）

チェックリスト名：要件妥当性チェックリスト

本ツールの中核となる「要件レビュー」チェックリスト。AIDDで落ちがちな観点をまとめて提供する。

- human_review
- 重み付け、判定ロジック
- 検証可能性
- AI可読性
- トレーサビリティ
- スキーマ準拠
- 運用考慮（ログ・権限）

### 10.2 企画MD↔企画YAML整合性（PLNパックに搭載）

チェックリスト名：企画MD↔企画YAML整合性

企画を"機械可読化"する入口として以下を行う：

- 企画文書をYAML化し、構造・ID・metaを検証するゲートを置く
- 詳細はPLNパックのチェックリストに反映
- planning_v1 の工程パック構成例にも含まれる
