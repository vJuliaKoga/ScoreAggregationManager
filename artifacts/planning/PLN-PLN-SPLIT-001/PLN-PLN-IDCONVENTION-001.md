---
meta:
  artifact_id: PLN-PLN-IDCONVENTION-001
  file: PLN-PLN-IDCONVENTION-001.md
  author: gpt-5.2
  source_type: ai
  source: codex
  prompt_id: PRM-PLN-MD-001
  timestamp: '2026-03-03T21:07:01+09:00'
  model: gpt-5.2
  content_hash: a60e48669721d4fdf1f0e97283324a6d0ab65233ab94e68b8b1ec21486de5639
---




## 12. ID規約（本企画に明記して採用）

### 12.1 ルール（共通）

IDの基本形は `{PREFIX}-{PHASE}-{PURPOSE}-{NNN}` という構造である。

- NNN部分は3桁の連番で構成する。
- PREFIX：成果物種別（PLN/REQ/BAS/DET/CHK/PRM/RES/ABT/DEC…）
- PHASE：工程（PLN/REQ/BAS/DET/OPS…）
- PURPOSE：用途（GOAL/PROB/SCOPE/CONS/FNC/NFR/DES/EVAL/AMB/YAML…）

### 12.2 推奨パターン（本企画書）

本企画書の主張・方針・スコープなども PLN-PLN-{PURPOSE}-NNN としてIDを付与する。

- 例：PLN-PLN-FLW-001 は企画ゴール
- IDフォーマットはPREFIXとPHASEとPURPOSEとNNNの4要素をハイフン連結した形を標準とする。
- NNNは常に3桁の連番で管理し桁数を固定する。
- 企画ゴールの例としてPLN-PLN-FLW-001を採用し用途語の意味を識別できるようにする。
