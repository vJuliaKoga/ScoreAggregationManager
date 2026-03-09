---
meta:
  artifact_id: PLN-PLN-TRACEABILITY-001
  file: PLN-PLN-TRACEABILITY-001.md
  author: gpt-5.2
  source_type: ai
  source: codex
  prompt_id: PRM-PLN-MD-001
  timestamp: '2026-03-03T21:07:03+09:00'
  model: gpt-5.2
  content_hash: 0de0e2e244f38e7362d061adc738917612f0342559d3b1602753827801ad586d
---




## 11. トレーサビリティ設計（ConTrack前提でも価値が残る形）

### 11.1 2層設計

- Coreレイヤー（本ツール）はID抽出、参照整合（derivedfrom/tracestoの存在確認）、カバレッジ算出、未紐付け一覧生成、Allure出力を担う。
- Adapterレイヤー（将来）はConTrack API連携（存在確認・リンク生成・関係解決）を提供する。
- ConTrackが既に存在していても、品質ゲートとしての検査・可視化・ブロックの価値は本企画側に残る。
- CoreレイヤーはID抽出と参照整合確認とカバレッジ算出を担当し結果をAllureへ出力する。
- Adapterレイヤーは将来拡張としてConTrack API連携を受け持つ。
- ConTrack連携では存在確認とリンク生成と関係解決を段階的に実装する。
- 既存のConTrackが存在しても品質ゲートとしての検査と可視化とブロック機能は本企画側の価値として維持する。
- Core（本ツール）はID抽出と参照整合とAllure出力を担当する。
- Adapter（将来）はConTrack API連携で存在確認とリンク生成と関係解決を担当する。
- ConTrackが既に存在していても品質ゲートの検査と可視化とブロックの価値は本企画側に残る。
