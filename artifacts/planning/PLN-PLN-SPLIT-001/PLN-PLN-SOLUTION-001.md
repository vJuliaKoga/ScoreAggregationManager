---
meta:
  artifact_id: PLN-PLN-SOLUTION-001
  file: PLN-PLN-SOLUTION-001.md
  author: gpt-5.2
  source_type: ai
  source: codex
  prompt_id: PRM-PLN-MD-001
  timestamp: "2026-03-03T21:07:03+09:00"
  model: gpt-5.2
  content_hash: b02d65677419135f212f5fce1cd46d452ab73fc2feda080f5d7c305a94fe42cf
---

## 6. ソリューション概要（2層構造）

### 6.1 CheckFlow（視座共有＋人の最終判断）

CheckFlowは視座共有と人の最終判断を目的としたUIツールである。

「押せば展開されるQAワークフロー」UI。工程タブ → タスク展開 → 観点/テンプレ/例/参照 → Done/Abort。

- 工程タブ：[企画][要件][基本設計][詳細設計][実装][テスト]（段階導入では表示制御）
- タスクはTodoから展開してDoneまたはAbortを選択し次項目を解放する。
- Abortとする場合は理由を必須とし、Doneは理由不要とする。
- 出力は checklistresults.json（チェック者・時刻・理由・エビデンス参照）

Coachの目的：

- 初学者が「何を見ればいいか」を迷わない（観点をチュートリアル化）
- 最終判断を人が負うことを、Done/Abortの操作とログで強制する
- 監査・説明に耐える判断ログを残す
- 段階導入では表示制御を行う
- CheckFlowは視座共有だけでなく人の最終判断をDoneとAbortのログとして残す運用を強制する。
- 初学者でも観点を追えるようにチュートリアル化した工程タブを提供する。
- 段階導入時は表示制御を行い対象工程のみを有効化する。
- CheckFlowは視座共有＋人の最終判断を担いDoneとAbortの判断ログを監査と説明に耐える形で残す。
- 工程タブは企画からテストまでを段階導入では表示制御し初学者の判断導線を維持する。

### 6.2 Gate Runner（自動検証：Docker/CLI）

Coachの出力や、企画/要件/設計のYAML等を入力に、品質ゲートを実行し output/ と allure-results/ を生成する。

- 配布はDocker/CLI（CIでもローカルでも同じ結果）
- 出力はAllureに集約し、品質の可視化ハブにする（自動ゲート結果＋人の判断ログ＋ダッシュボード添付）
- Gate Runnerの出力はAllureへ集約し自動ゲート結果と判断ログを一体で監査できるようにする。
- 出力はAllureに集約し自動ゲート結果と人の判断ログとダッシュボード添付を一体管理する。
