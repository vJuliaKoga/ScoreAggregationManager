---
meta:
  artifact_id: PLN-PLN-DATASPEC-001
  file: PLN-PLN-DATASPEC-001.md
  author: gpt-5.2
  source_type: ai
  source: codex
  prompt_id: PRM-PLN-MD-001
  timestamp: '2026-03-03T21:06:59+09:00'
  model: gpt-5.2
  content_hash: f2de9d11734e69933277f31fe8f7c512c6665c9e3a28b019ec4ac04c57f66d99
---




## 15. 具体的なデータ仕様（最低限）

### 15.1 checklistresults.json（Coach出力）

保持フィールド：

- checkedby
- timestamp
- status(Done|Abort)
- reason
- evidencerefs
- statusはDoneまたはAbortで記録する。
- checklistresults.jsonはcheckedbyとtimestampとreasonとevidencerefsを保持してG2検証に渡す。
- checklistresults.jsonのstatus(Done|Abort)はG2判定の必須入力である。

G2がこれらのフィールドを検証する。

### 15.2 Gate出力（Runner）

- output/ の内容：各ゲートのレポートJSON＋サマリ（exitcode含む）
- allure-results/ の内容：レポートに統合するための出力（Allure用）
- Runnerのoutputには各ゲートのレポートJSONとexitcodeを含むサマリを出力する。
- allure-resultsにはレポート統合用の出力を格納しAllureで可視化できるようにする。
- outputには各ゲートのレポートJSONとサマリ（exitcode含む）を出力する。
- allure-resultsはレポートに統合するための出力として保存する。

