---
meta:
  artifact_id: RES-PLN-G4-REVIEW-002
  file: RES-PLN-G4-REVIEW-002.md
  author: gpt-5.2
  source_type: ai
  source: Codex
  prompt_id: PRM-PLN-TRANS-002
  timestamp: "2026-03-08T20:56:00+09:00"
  model: gpt-5.2
  content_hash: a7b4c003e8e9eb235f54877778049b7c3edd5afcaf11ae491dae3165cce24c7f
---

## 1. YAML→MD ギャップ（Faithfulness起点）

### PLN-PLN-ALLURE-001

- [MD追記] (sim=0.016) - text: 自動ゲート結果はG1〜G5およびPromptfooの結果を一覧で表示し、各ゲートの判定とスコアとエビデンス参照を確認できるようにする。
- [MD追記] (sim=0.017) - text: G2の証跡リンクは必要な場合に付けられるようにする。
- [MD追記] (sim=0.017) - text: 各ゲートの内訳とスコア分布はゲート別および評価軸別に確認できるようにする。
- [MD追記] (sim=0.033) - text: G2は人のチェックリスト結果を別枠で表示し、チェック項目ごとのスコアを集計して反映する。
- [MD追記] (sim=0.033) - text: G2のAbortは理由を必須とし、Doneは理由不要とする。
- [MD追記] (sim=0.033) - text: Abort分析はカテゴリ分布と理由品質を集計し、判断回避の常態化を検知する。
- [MD追記] (sim=0.033) - text: Traceability Matrixは要件から設計とテストへの紐付けを表示する。
- [MD追記] (sim=0.050) - text: スコア推移はDeep EvalとPromptfooの推移を追跡し、モデル変動や改修前後の品質変化を可視化する。
- [MD追記] (sim=0.067) - text: 重み付き合算スコアはG1〜G5とPromptfooの各スコアをウェイト定義（9.3節）に基づいて合算した総合指標である。

### PLN-PLN-CFUI-001

- [YAML弱め] (sim=0.000) design_note: 詳細な権限境界・UI設計は基本設計フェーズで確定する
- [YAML弱め] (sim=0.000) design_note: 詳細なJSON構造・スキーマは詳細設計フェーズで確定する
- [YAML弱め] (sim=0.000) note: 基本設計フェーズで詳細を確定する
- [MD追記] (sim=0.000) - G2工程にてCheckFlowが生成する checklistresults.json が Gate Runner の入力として必須
- [MD追記] (sim=0.000) - 出力JSONをRunnerが消費・検証するため、データフォーマットの早期確定が両プロジェクトに影響
- [MD追記] (sim=0.000) - JSON定義仕様の早期確定（企画完了後、要件定義フェーズ冒頭で実施）
- [MD追記] (sim=0.000) - checklistresults.json スキーマの確定は要件定義フェーズで最優先
- [MD追記] (sim=0.000) ui_goal: NotebookLMのような動的展開型マインドマップUIを活用した品質ゲート基盤
- [MD追記] (sim=0.000) concept_name: テンプレート駆動型アプリケーション
- [MD追記] (sim=0.000) adoption: PWA（Progressive Web App）
- [MD追記] (sim=0.000) - responsibilities: チェックリストの実行・状態更新・JSONエクスポート
- [MD追記] (sim=0.000) method: 認証なし（任意）

### PLN-PLN-CHECKLIST-001

- [MD追記] (sim=0.019) - name: 要件妥当性チェックリスト
- [MD追記] (sim=0.020) - トレーサビリティ
- [MD追記] (sim=0.020) - 詳細はPLNパックのチェックリストに反映
- [MD追記] (sim=0.039) - 重み付け、判定ロジック
- [MD追記] (sim=0.039) - planning_v1 の工程パック構成例にも含まれる
- [MD追記] (sim=0.058) - name: 企画MD↔企画YAML整合性（PLNパックに搭載）
- [MD追記] (sim=0.059) - 運用考慮（ログ・権限）
- [MD追記] (sim=0.078) - 企画文書をYAML化し、構造・ID・metaを検証するゲートを置く

### PLN-PLN-CI_INTEGRATION-001

- [MD追記] (sim=0.000) action: ワークフローツール最終工程で CI成果物（zip等）をアップロード
- [MD追記] (sim=0.000) - CI成果物をアップロードして最終サマリを1枚に集約
- [MD追記] (sim=0.000) - 自動ゲート結果＋人の判断ログ（理由・証跡リンク）＋サマリを統合して保管
- [MD追記] (sim=0.018) action: 同工程でチェックリスト入力を確定（Coach相当）
- [MD追記] (sim=0.018) - 合計点（自動＋チェックリスト）
- [MD追記] (sim=0.019) - 0.70未満は必ずWarningを出す
- [MD追記] (sim=0.037) - name: ワークフローツール（最終工程）
- [MD追記] (sim=0.037) - name: 証跡ハブ（Allure）
- [MD追記] (sim=0.056) - チェックリスト（Coach相当）の入力・承認
- [MD追記] (sim=0.057) - pass|warn|fail
- [MD追記] (sim=0.075) - 各ゲート・各評価軸のスコアを機械可読な成果物として出力（再現可能・比較可能）
- [MD追記] (sim=0.111) - ブロック（Fail）条件は重大ゲート（例：スキーマ逸脱、必須情報欠落等）に限定し、段階的に導入

### PLN-PLN-DATASPEC-001

- [MD追記] (sim=0.024) - contents: レポートに統合するための出力
- [MD追記] (sim=0.071) - contents: 各ゲートのレポートJSON＋サマリ（exitcode含む）
- [MD追記] (sim=0.073) - status(Done|Abort)

### PLN-PLN-DEFINITION-001

- [MD追記] (sim=0.016) - ② 指示が守られていることを確認する
- [MD追記] (sim=0.016) - ① AIに正しく指示を与える
- [MD追記] (sim=0.016) - 曖昧語排除チェック
- [MD追記] (sim=0.016) - 構造一貫性テスト
- [MD追記] (sim=0.032) - definition: 正しく指示
- [MD追記] (sim=0.032) - definition: 遵守確認
- [MD追記] (sim=0.032) - definition: 品質可視化
- [MD追記] (sim=0.032) - JSON Schema検証
- [MD追記] (sim=0.032) - Deep Eval評価
- [MD追記] (sim=0.032) - Allure Reportでゲート結果をモニタ

### PLN-PLN-DISTRIBUTION-001

- [MD追記] (sim=0.021) - distribution: チェックリストツールとして配布
- [MD追記] (sim=0.043) - component: Gate Runner
- [MD追記] (sim=0.087) - 品質保証ゲート（G2）として出力結果を活用。人間による評価を重み付けスコアリング。

### PLN-PLN-IDISSUANCE-001

- [MD追記] (sim=0.027) - stdoutへ発行ID出力（他ツール連携を想定）
- [MD追記] (sim=0.041) - レジストリの next_nnn 更新
- [YAML弱め] (sim=0.067) - 現状は single-user 前提（ロックなし）で運用開始

### PLN-PLN-PACK-001

- [MD追記] (sim=0.000) - 企画を機械可読にする
- [MD追記] (sim=0.000) - 企画段階のQA観点を入れる
- [MD追記] (sim=0.015) - BASおよびDETパックは設計工程の品質観点を拡張する。
- [MD追記] (sim=0.015) - PLNパックは企画を機械可読化し企画段階のQA観点を標準で適用する。
- [MD追記] (sim=0.015) - 各工程パックはチェックリストとスキーマとプロンプトとテンプレートをセットで提供する。
- [MD追記] (sim=0.015) - BASとDETパックは構造整合観点を拡張し後工程の設計崩壊を予防する。
- [MD追記] (sim=0.029) - REQパックは要件妥当性チェックをhumanレビューとDeep Evalの両方で実施する。
- [MD追記] (sim=0.043) - 要件妥当性チェック（human+Deep Eval）
- [MD追記] (sim=0.044) - pack: REQ（要件）
- [MD追記] (sim=0.044) - pack: PLN（企画）
- [MD追記] (sim=0.059) - PLNパック（企画）は企画を機械可読にし、企画段階のQA観点を標準装備する。

### PLN-PLN-PHILOSOPHY-001

- [MD追記] (sim=0.070) - 『考えなくていいQA』ではなく『考える順番を固定するQA』
- [MD追記] (sim=0.093) - AIに判断を委譲しない（判断は人、検証は自動、証跡はシステム）

### PLN-PLN-QADESIGN-001

- [MD追記] (sim=0.000) - 要件側の derivedfrom へ接続する方針
- [MD追記] (sim=0.000) - 『企画→要件へトレース可能』を自動検証できるようにする
- [MD追記] (sim=0.000) - 検証可能性の観点から、成功条件やKPIが測定可能でテスト可能な言葉で表現されているかを確認する。
- [MD追記] (sim=0.000) - スコープの観点から、スコープ内・外およびAbort条件が事前に定義されているかを確認する。
- [MD追記] (sim=0.000) - 企画IDは要件側のderivedfromへ接続し企画から要件までのトレースを自動検証できる状態を維持する。
- [MD追記] (sim=0.000) - 企画IDは要件側のderivedfromへ接続する方針を維持し企画→要件へトレース可能な状態を自動検証する。
- [MD追記] (sim=0.000) - QA観点は検証可能性とスコープを中心に運用保守・証跡・権限の考慮を確認する。
- [MD追記] (sim=0.000) - 構造の逸脱を最大リスクとして設計する。
- [MD追記] (sim=0.000) - viewpoint: 検証可能性
- [MD追記] (sim=0.000) - viewpoint: スコープ
- [MD追記] (sim=0.000) principle: 構造の逸脱を最大リスクとして設計
- [MD追記] (sim=0.000) - content: 曖昧語チェック + 内容lint

### PLN-PLN-RISK-001

- [MD追記] (sim=0.000) - CheckFlow先行で教育
- [MD追記] (sim=0.020) - ゲートでブロック
- [MD追記] (sim=0.020) - 理由品質の最低基準を設ける
- [MD追記] (sim=0.020) - Warning運用
- [MD追記] (sim=0.020) - Runner任意
- [MD追記] (sim=0.040) - risk: AIモデル変動
- [MD追記] (sim=0.040) - risk: 導入ハードル
- [MD追記] (sim=0.060) - risk: 形骸化／適当Done

### PLN-PLN-SCOREPOLICY-001

- [MD追記] (sim=0.000) - condition: CI失敗
- [MD追記] (sim=0.000) - condition: トレーサビリティ欠落
- [MD追記] (sim=0.000) - condition: 構造重大違反
- [MD追記] (sim=0.000) - condition: 曖昧語の過剰検出
- [MD追記] (sim=0.000) guidance: 軽微な構造違反や数件の曖昧語は減点対応とし、スピードを優先
- [MD追記] (sim=0.000) guidance: 厳格な統制を適用。微細な逸脱も修正対象
- [MD追記] (sim=0.000) - Allure上でWarningとして表示
- [MD追記] (sim=0.000) - '0.70は pass_threshold: 0.7 を社内標準の警告ラインとして採用'
- [MD追記] (sim=0.013) - Warningに『理由要約／改善ガイド／再実行条件』をセットで出す
- [MD追記] (sim=0.013) criterion: ID参照の不整合、または孤立した定義の存在
- [MD追記] (sim=0.013) criterion: DeepEvalスコアが0.6未満
- [MD追記] (sim=0.013) - level: LOW Risk

### PLN-PLN-SOLUTION-001

- [MD追記] (sim=0.013) - 監査・説明に耐える「判断ログ」を残す
- [MD追記] (sim=0.013) - タスクはTodoから展開してDoneまたはAbortを選択し次項目を解放する。
- [MD追記] (sim=0.013) - CheckFlowは視座共有だけでなく人の最終判断をDoneとAbortのログとして残す運用を強制する。
- [MD追記] (sim=0.013) - 初学者でも観点を追えるようにチュートリアル化した工程タブを提供する。
- [MD追記] (sim=0.013) - 段階導入時は表示制御を行い対象工程のみを有効化する。
- [MD追記] (sim=0.013) - 工程タブは企画からテストまでを段階導入では表示制御し初学者の判断導線を維持する。
- [MD追記] (sim=0.013) - 出力はAllureに集約し自動ゲート結果と人の判断ログとダッシュボード添付を一体管理する。
- [MD追記] (sim=0.013) - 段階導入では表示制御
- [MD追記] (sim=0.013) - 段階導入では表示制御を行う。
- [MD追記] (sim=0.026) description: 視座共有＋人の最終判断
- [MD追記] (sim=0.027) - Abortとする場合は理由を必須とし、Doneは理由不要とする。
- [MD追記] (sim=0.027) - Gate Runnerの出力はAllureへ集約し自動ゲート結果と判断ログを一体で監査できるようにする。

### PLN-PLN-TRACEABILITY-001

- [MD追記] (sim=0.000) - Allure出力
- [MD追記] (sim=0.030) value_statement: ConTrackが既にあっても『品質ゲートとしての検査・可視化・ブロック』の価値が本企画側に残る
- [MD追記] (sim=0.032) - layer: Core（本ツール）
- [YAML弱め] (sim=0.032) - layer: Adapter（将来）
- [MD追記] (sim=0.063) - ConTrack API連携（存在確認、リンク生成、関係解決）

## 2. MD→YAML ギャップ（Coverage起点）

### PLN-PLN-ALLURE-001

- [言い回し統一] item: 自動ゲート結果はG1〜G5およびPromptfooの結果を一覧で表示する。 | best_sim: 0.2000 | best_match: - text: 自動ゲート結果はG1〜G5およびPromptfooの結果を一覧で表示し、各ゲートの判定とスコアとエビデンス参照を確認できるようにする。
- [YAML追記] item: 自動ゲート結果では各ゲートの判定とスコアとエビデンス参照を表示する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: G2は人のチェックリスト結果でDoneまたはAbortの判断を表示し、Abort時の理由を必須で記録する。 | best_sim: 0.0000 | best_match:
- [言い回し統一] item: 重み付き合算スコアはウェイト定義（9.3節）に基づいて算出する総合指標である。 | best_sim: 0.1429 | best_match: - text: 重み付き合算スコアはG1〜G5とPromptfooの各スコアをウェイト定義（9.3節）に基づいて合算した総合指標である。

### PLN-PLN-BACKGROUND-001

- [YAML追記] item: 品質の不可視性はQA実施の有無だけでは中身が見えず判断根拠を追跡できない状態である。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 仕様の曖昧性と仕様と実装の乖離は手戻り増加を招く主要課題である。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: QA観点の属人化と判断根拠の不在は責任の不明確化を招く要因である。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 導入方針は企画段階から工程パックで運用しCheckFlowでチュートリアル化する。 | best_sim: 0.0000 | best_match:

### PLN-PLN-CFUI-001

- [YAML追記] item: CheckFlowはNotebookLMのような動的展開型マインドマップUIを活用した品質ゲート基盤である。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: テンプレート駆動型アプリケーションをコンセプトとし、単一エンジンから複数フェーズに対応する。 | best_sim: 0.0000 | best_match:
- [言い回し統一] item: Phase 1では認証なし（任意）とし、確認者名を自己申告で入力する方式とする。 | best_sim: 0.2000 | best_match: - phase: Phase 1
- [言い回し統一] item: Userの主な責務はチェックリストの実行・状態更新・JSONエクスポートである。 | best_sim: 0.1667 | best_match: responsibilities: チェックリストの実行・状態更新・JSONエクスポート
- [YAML追記] item: 詳細な権限境界およびUI設計は基本設計フェーズで確定する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 詳細なJSON構造およびスキーマは詳細設計フェーズで確定する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: G2工程でCheckFlowが生成するchecklistresults.jsonはGate Runnerの入力として必須である。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: CheckFlowの出力JSONをRunnerが消費・検証する構造のため、データフォーマットの早期確定が両プロジェクトに影響する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: JSON定義仕様は企画完了後、要件定義フェーズ冒頭で早期に確定する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: CheckFlowのコンセプトはテンプレート駆動型アプリケーションであり単一エンジンで複数フェーズを生成する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 技術基盤はPWAを採用しブラウザ配布と将来の商用展開を両立する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: G2工程で生成するchecklistresults.jsonはGate Runner入力として必須とする。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: JSON定義仕様は要件定義フェーズ冒頭で確定しchecklistresults.jsonスキーマを最優先で合意する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 詳細な権限境界とUI設計は基本設計フェーズで確定し詳細なJSON構造は詳細設計フェーズで確定する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: テンプレート駆動型アプリケーションとしてPWAを採用しUserはチェックリスト実行と状態更新とJSONエクスポートを担当する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: G2工程で生成するchecklistresults.jsonはGate Runner入力として必須であり要件定義フェーズ冒頭でスキーマを最優先確定する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: CheckFlowの出力JSONをGate Runnerが消費・検証する構造であるため、データフォーマットの早期確定が両プロジェクトに影響する | best_sim: 0.0000 | best_match:

### PLN-PLN-CHECKLIST-001

- [YAML追記] item: 要件妥当性チェックリストは重み付けと判定ロジックを含めて評価結果を算出する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: トレーサビリティ観点では要件IDの紐付けと参照整合を確認する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 運用考慮観点ではログ保全と権限管理が宣言されていることを確認する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 要件妥当性チェックリストの評価は重み付けと判定ロジックに基づいて決定する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 企画MDと企画YAMLの整合性チェックは構造とIDとmetaの整合を検証対象とする。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: この整合性チェック項目はPLNパックの標準チェックリストへ反映して運用する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: planningv1の工程パック構成例にも同チェックを組み込んで再利用する。 | best_sim: 0.0000 | best_match:

### PLN-PLN-CI_INTEGRATION-001

- [YAML追記] item: CI成果物をアップロードして最終サマリを1枚に集約する | best_sim: 0.0000 | best_match:
- [YAML追記] item: 自動ゲート結果と人の判断ログと最終サマリを統合して保管する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 人の判断ログではAbortの理由を必須とし、Doneは理由不要とする。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 証跡リンクは必要な場合に付けられるようにする。 | best_sim: 0.0000 | best_match:
- [言い回し統一] item: 集約コマンド（軽量）で以下を生成し、Allureに統合 | best_sim: 0.2222 | best_match: action: 集約（軽量）で合計点/分布/判定を生成し、Allureに統合
- [YAML追記] item: ワークフローツール最終工程ではCI成果物のzip等アップロードを必須にする。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 同工程でCoach相当のチェックリスト入力を確定し合計点を算出する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 判定結果はpassとwarnとfailの三値で出力しAllureへ統合する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 各ゲートと各評価軸のスコアは機械可読な成果物として継続比較できる形式で保存する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 自動ゲート結果と人の判断ログと最終サマリを単一の証跡として保管する。 | best_sim: 0.0000 | best_match:
- [言い回し統一] item: ワークフローツール最終工程ではチェックリスト（Coach相当）の入力と承認を行いCI成果物をアップロードする。 | best_sim: 0.2000 | best_match: action: 同工程でチェックリスト入力を確定（Coach相当）
- [言い回し統一] item: 自動評価成果物（CI）：各ゲートJSONに以下を含める | best_sim: 0.1429 | best_match: - name: CI（Gate Runner / Docker）
- [言い回し統一] item: チェックリスト成果物（Workflow/Coach）：checklistresults.json 相当 | best_sim: 0.1429 | best_match: workflow: null
- [言い回し統一] item: itemid / risklevel / selection / score / reason / evidencerefs | best_sim: 0.1667 | best_match: - selection

### PLN-PLN-DATASPEC-001

- [YAML追記] item: statusはDoneまたはAbortで記録する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: checklistresults.jsonはcheckedbyとtimestampとreasonとevidencerefsを保持してG2検証に渡す。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: Runnerのoutputには各ゲートのレポートJSONとexitcodeを含むサマリを出力する。 | best_sim: 0.0000 | best_match:
- [言い回し統一] item: outputには各ゲートのレポートJSONとサマリ（exitcode含む）を出力する。 | best_sim: 0.1667 | best_match: contents: 各ゲートのレポートJSON＋サマリ（exitcode含む）

### PLN-PLN-DEFINITION-001

- [不要] item: 構造化テンプレート | best_sim: 0.0000 | best_match:
- [言い回し統一] item: 「品質可視化」とは、Allure Reportでゲート結果をモニタリングすることを意味する。 | best_sim: 0.2000 | best_match: - definition: 品質可視化
- [YAML追記] item: QA4AIDDの第一目的はAIに正しく指示を与えることである。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: QA4AIDDの第二目的は指示遵守をJSON Schema検証とDeep Eval評価と構造一貫性テストで確認することである。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 曖昧語排除チェックは指示品質を担保する前段の必須検査として扱う。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: ① AIに正しく指示を与えることをQA4AIDDの起点とする。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: ② 指示が守られていることをJSON Schema検証とDeep Eval評価と構造一貫性テストで確認する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 品質可視化はAllure Reportでゲート結果をモニタし継続運用する。 | best_sim: 0.0000 | best_match:

### PLN-PLN-IDCONVENTION-001

- [YAML追記] item: NNN部分は3桁の連番で構成する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: IDフォーマットはPREFIXとPHASEとPURPOSEとNNNの4要素をハイフン連結した形を標準とする。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: NNNは常に3桁の連番で管理し桁数を固定する。 | best_sim: 0.0000 | best_match:

### PLN-PLN-IDISSUANCE-001

- [YAML追記] item: issueid.pyはIDレジストリから指定キーの次IDを発行しnextnnnを更新する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 発行結果はidissuedlog.yamlへ追記し同時にstdoutへ出力して他ツール連携に利用する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: issueid.pyはレジストリのnextnnn更新とstdoutへ発行ID出力を同時に実施する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 発行IDは他ツール連携を前提にidissuedlog.yamlへ追記して追跡可能にする。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 運用開始時はsingle-user前提でロックなしとし同時利用が増えた段階で集中管理へ拡張する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 運用開始時はsingle-user前提（ロックなし）で運用し同時利用増加時に拡張する。 | best_sim: 0.1111 | best_match: - 現状は single-user 前提（ロックなし）で運用開始

### PLN-PLN-PACK-001

- [YAML追記] item: BASおよびDETパックは設計工程の品質観点を拡張し設計崩壊を予防する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 各工程パックはチェックリストとスキーマとプロンプトとテンプレートを含み後工程の自動化と検証に接続する。 | best_sim: 0.0000 | best_match:

### PLN-PLN-QADESIGN-001

- [YAML追記] item: 要件側のderivedfromへ接続する方針で企画→要件トレース可能性を自動検証する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 検証可能性とスコープは成功条件とAbort条件の妥当性を確認する中核観点である。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: G2は文脈に応じた人の高度判断をCIに接続するためのチェックリスト検証を担う。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: G3は構造整合性を強制し技術的負債の増大を抑止する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: G5は要件から設計とテストの紐付けを検証し孤立した定義を検出する。 | best_sim: 0.0000 | best_match:

### PLN-PLN-RISK-001

- [不要] item: Coach先行で教育 | best_sim: 0.0000 | best_match:
- [YAML追記] item: AIモデル変動のリスクにはモデル固定とスコア推移監視を組み合わせWarning運用で早期検知する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 導入ハードルのリスクにはCoach先行で教育しRunnerは任意導入からCIへ段階移行する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: Abort判断の理由品質が基準未満の場合は再評価を求める。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: Warning運用は判断回避の常態化を抑止する。 | best_sim: 0.0000 | best_match:

### PLN-PLN-SCOREPOLICY-001

- [言い回し統一] item: passscore：LOW Riskは70点以上、HIGH Riskは90点以上 | best_sim: 0.1429 | best_match: - level: LOW Risk
- [YAML追記] item: 0.70未満の案件はAllure上でWarningとして表示し理由要約と改善ガイドと再実行条件を併記する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 第一段階の致命条件にはCI失敗とトレーサビリティ欠落と構造重大違反とFaithfulness壊滅と曖昧語過剰検出を含める。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: Faithfulness壊滅はDeepEvalスコアが0.6未満であることを基準に即時失格とする。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: トレーサビリティ欠落はID参照不整合または孤立定義の存在で判定する。 | best_sim: 0.0000 | best_match:
- [言い回し統一] item: LOW Riskは減点対応でスピードを優先しHIGH Riskは微細な逸脱も修正対象として厳格統制する。 | best_sim: 0.2000 | best_match: - level: LOW Risk
- [YAML追記] item: 致命条件はCI失敗とトレーサビリティ欠落と構造重大違反とFaithfulness壊滅と曖昧語過剰検出で判定する。 | best_sim: 0.0000 | best_match:
- [言い回し統一] item: 0.70未満はAllure上でWarningとして表示し理由要約／改善ガイド／再実行条件をセットで提示する。 | best_sim: 0.1429 | best_match: - Warningに『理由要約／改善ガイド／再実行条件』をセットで出す

### PLN-PLN-TRACEABILITY-001

- [YAML追記] item: CoreレイヤーはID抽出と参照整合確認とカバレッジ算出を担当し結果をAllureへ出力する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: Adapterレイヤーは将来拡張としてConTrack API連携を受け持つ。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: ConTrack連携では存在確認とリンク生成と関係解決を段階的に実装する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: 既存のConTrackが存在しても品質ゲートとしての検査と可視化とブロック機能は本企画側の価値として維持する。 | best_sim: 0.0000 | best_match:
- [YAML追記] item: ConTrackが既に存在していても品質ゲートの検査と可視化とブロックの価値は本企画側に残る。 | best_sim: 0.0000 | best_match:

## 3. 優先度Top10

1. [MD→YAML] PLN-PLN-ALLURE-001 / [YAML追記] G2は人のチェックリスト結果でDoneまたはAbortの判断を表示し、Abort時の理由を必須で記録する。
   理由: MD項目がYAMLで未カバー（best_sim=0.000）のため。
2. [MD→YAML] PLN-PLN-ALLURE-001 / [YAML追記] 自動ゲート結果では各ゲートの判定とスコアとエビデンス参照を表示する。
   理由: MD項目がYAMLで未カバー（best_sim=0.000）のため。
3. [MD→YAML] PLN-PLN-BACKGROUND-001 / [YAML追記] QA観点の属人化と判断根拠の不在は責任の不明確化を招く要因である。
   理由: MD項目がYAMLで未カバー（best_sim=0.000）のため。
4. [MD→YAML] PLN-PLN-BACKGROUND-001 / [YAML追記] 仕様の曖昧性と仕様と実装の乖離は手戻り増加を招く主要課題である。
   理由: MD項目がYAMLで未カバー（best_sim=0.000）のため。
5. [MD→YAML] PLN-PLN-BACKGROUND-001 / [YAML追記] 品質の不可視性はQA実施の有無だけでは中身が見えず判断根拠を追跡できない状態である。
   理由: MD項目がYAMLで未カバー（best_sim=0.000）のため。
6. [MD→YAML] PLN-PLN-BACKGROUND-001 / [YAML追記] 導入方針は企画段階から工程パックで運用しCheckFlowでチュートリアル化する。
   理由: MD項目がYAMLで未カバー（best_sim=0.000）のため。
7. [YAML→MD] PLN-PLN-CFUI-001 / [MD追記] (sim=0.000) - G2工程にてCheckFlowが生成する checklistresults.json が Gate Runner の入力として必須
   理由: YAML主張がMDで未反映（sim=0.000）のため。
8. [YAML→MD] PLN-PLN-CFUI-001 / [MD追記] (sim=0.000) - JSON定義仕様の早期確定（企画完了後、要件定義フェーズ冒頭で実施）
   理由: YAML主張がMDで未反映（sim=0.000）のため。
9. [YAML→MD] PLN-PLN-CFUI-001 / [MD追記] (sim=0.000) - checklistresults.json スキーマの確定は要件定義フェーズで最優先
   理由: YAML主張がMDで未反映（sim=0.000）のため。
10. [YAML→MD] PLN-PLN-CFUI-001 / [MD追記] (sim=0.000) - responsibilities: チェックリストの実行・状態更新・JSONエクスポート
    理由: YAML主張がMDで未反映（sim=0.000）のため。
