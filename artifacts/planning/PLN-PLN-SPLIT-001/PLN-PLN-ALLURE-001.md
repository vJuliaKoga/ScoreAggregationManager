---
meta:
  artifact_id: PLN-PLN-ALLURE-001
  file: PLN-PLN-ALLURE-001.md
  author: gpt-5.2
  source_type: ai
  source: codex
  prompt_id: PRM-PLN-MD-001
  timestamp: "2026-03-03T21:06:58+09:00"
  model: gpt-5.2
  content_hash: 570b99e56a356dd4b1cbd8e435393138e6a6c709a4f67e4f836661a2603c30df
---

## 14. Allureによる可視化（品質のハブ）

Allure Reportは以下を一元表示する。

- 自動ゲート結果はG1〜G5およびPromptfooの結果を一覧で表示する。
- 自動ゲート結果では各ゲートの判定とスコアとエビデンス参照を表示する。
- G2は人のチェックリスト結果を別枠で表示し、チェック項目ごとのスコアを集計して反映する。
- G2のAbortは理由を必須とし、Doneは理由不要とする。
- G2の証跡リンクは必要な場合に付けられるようにする。
- 重み付き合算スコアはG1〜G5とPromptfooの各スコアをウェイト定義（9.3節）に基づいて合算した総合指標である。
- 各ゲートの内訳とスコア分布はゲート別および評価軸別に確認できるようにする。
- スコア推移はDeep EvalとPromptfooの推移を追跡し、モデル変動や改修前後の品質変化を可視化する。
- Abort分析はカテゴリ分布を集計し、判断回避の常態化を検知する。
- Traceability Matrixは要件から設計とテストへの紐付けを表示する。
- G2は人のチェックリスト結果でDoneまたはAbortの判断を表示し、Abort時の理由を必須で記録する。
- Abort分析はカテゴリ分布と理由品質を集計し、判断回避の常態化を検知する。
- 重み付き合算スコアはウェイト定義（9.3節）に基づいて算出する総合指標である。
