---
meta:
  artifact_id: PLN-PLN-RISK-001
  file: PLN-PLN-RISK-001.md
  author: gpt-5.2
  source_type: ai
  source: codex
  prompt_id: PRM-PLN-MD-001
  timestamp: '2026-03-03T21:07:02+09:00'
  model: gpt-5.2
  content_hash: 2d7e70e19ba82ff72d59c789ab7561faf4dc1afb59cedb21e1dfbddf63bcac10
---




## 19. リスクと対策（最初から明記）

- risk: 形骸化／適当Done
  - ゲートでブロック
  - 理由品質の最低基準を設ける
- risk: AIモデル変動
  - モデル固定
  - スコア推移監視
  - Warning運用
- risk: 導入ハードル
  - Coach先行で教育
  - Runner任意
  - CIへ段階移行
- 形骸化／適当Doneのリスクにはゲートでブロックする運用と理由品質の最低基準で対処する。
- AIモデル変動のリスクにはモデル固定とスコア推移監視を組み合わせWarning運用で早期検知する。
- 導入ハードルのリスクにはCoach先行で教育しRunnerは任意導入からCIへ段階移行する。
- Abort判断の理由品質が基準未満の場合は再評価を求める。
- Warning運用は判断回避の常態化を抑止する。

