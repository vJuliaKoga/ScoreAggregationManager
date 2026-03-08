#!/usr/bin/env python3
"""
meta:
    artifact_id: TST-G4-EVAL-007
    file: g4_deepeval.py
    author: '@juria.koga'
    source_type: human
    source: manual
    timestamp: '2026-03-03T18:35:00+09:00'
    content_hash: d42c5504d6a020a5436c114fd2347d42a161e2a68b72ed9fed9d07d8ca46dc10
---
Faithfulness + Coverage(derived_from 1:1) + Completeness + Global Consistency
=============================================================================================

更新理由:
- Faithfulness（ファイル単位）: 参照にない創作（ハルシネーション）を検出
    - タイムアウト対策: 参照全文ではなく、関連参照チャンク上位Kを retrieval_context に投入
    - Faithfulness入力は「FaithView」として、meta/日時/ハッシュ/パス等のノイズや null/空を除外
    - 変換理由/章ラベル（rationale/primary_section 等）は原文一致しない前提でFaithViewから除外
- Coverage（derived_from 1:1 / ルールベース）: 参照(split MD)の主要論点が、対応YAMLに落ちているか
- Completeness（derived_from 1:1 / ルールベース）: nullのまま放置されている“埋まっているべき可能性”を検知（追加APIなし）
- Global Consistency（横断/ルールベース）: 分割YAML間や参照との矛盾を検出

環境変数（主なもの）:
    AIDD_STAGE                 : 対象工程 (例: PLN, REQ)
    AIDD_YAML_DIR              : 評価対象YAMLディレクトリ
    AIDD_OUT_ROOT              : 出力ルートディレクトリ
    AIDD_EVAL_MODEL            : 使用モデル (例: gpt-5.2)

    # 参照入力
    AIDD_REF_PATHS             : 参照ファイル/ディレクトリ（md/yaml/dir/glob混在OK）
    AIDD_REF_MODE              : AUTO|MD|YAML

    # Faithfulness
    AIDD_FAITHFULNESS_USE_DERIVED_FROM_CONTEXT : 1で有効（既定 1）
    AIDD_FAITHFULNESS_TOPK_REF_CHUNKS          : 参照チャンク数（既定 4）
    AIDD_FAITHFULNESS_REF_CHUNK_MAX_CHARS      : 参照チャンク1個の最大文字数（既定 900）
    AIDD_FAITHFULNESS_ACTUAL_MAX_CHARS         : actual_output 最大（既定 1800）
    AIDD_FAITHFULNESS_CONTEXT_MAX_CHARS        : retrieval_context 最大（既定 2200）
    AIDD_FAITHFULNESS_TRUTHS_LIMIT             : truths抽出上限（既定 10）
    AIDD_FAITHFULNESS_RETRY_ON_TIMEOUT         : 1で有効（既定 1）
    AIDD_FAITHFULNESS_ACTUAL_MAX_CHARS_RETRY   : リトライ actual 最大（既定 1200）
    AIDD_FAITHFULNESS_CONTEXT_MAX_CHARS_RETRY  : リトライ ctx 最大（既定 1600）
    AIDD_FAITHFULNESS_TRUTHS_LIMIT_RETRY       : リトライ truths 上限（既定 6）

    # Faithfulness reason のモード
    AIDD_FAITHFULNESS_REASON_MODE              : local|llm（既定 local）

    # FaithView 生成設定
    AIDD_FAITHFULNESS_STRIP_TOP_KEYS           : top-levelでFaithViewから外すキー（既定 "meta"）
    AIDD_FAITHFULNESS_STRIP_ANYLEVEL_KEYS      : 任意階層でFaithViewから外すキー（既定 "rationale,primary_section,ssot_note"）
    AIDD_FAITHFULNESS_PRUNE_NULLS              : 1でnull/空/空配列/空dictを再帰的に除外（既定 1）
    AIDD_FAITHFULNESS_PRUNE_MAX_DEPTH          : 再帰の最大深さ（既定 12）
    AIDD_FAITHFULNESS_NOISY_ASCII_SCALAR_MAXLEN: ASCII単語だけの短ラベルをノイズ扱いする最大長（既定 24）

    # local reason
    AIDD_FAITHFULNESS_LOCAL_REASON_TOPN        : 抽出行数（既定 12）
    AIDD_FAITHFULNESS_LOCAL_REASON_SIM_TH      : “根拠薄い”判定の類似度閾値（既定 0.12）
    AIDD_FAITHFULNESS_LOCAL_REASON_MIN_LEN     : 短すぎる行を無視（既定 10）

    # Completeness
    AIDD_COMPLETENESS_ENABLE                   : 1で有効（既定 1）
    AIDD_COMPLETENESS_TOPN                     : 出力する疑義件数（既定 12）
    AIDD_COMPLETENESS_EVIDENCE_TH              : 参照に根拠がありそう判定の閾値（既定 0.12）
    AIDD_COMPLETENESS_WARN_COUNT               : 疑義件数がこの値以上でWARN（既定 1）
    AIDD_COMPLETENESS_FAIL_COUNT               : 疑義件数がこの値以上でFAIL（既定 3）

    # Coverage
    AIDD_COVERAGE_ENABLE        : 1で有効（既定 1）
    AIDD_COVERAGE_MAX_ITEMS     : 参照から抽出する論点数の上限（既定 80）
    AIDD_COVERAGE_MIN_ITEM_LEN  : 論点として採用する最小文字数（既定 6）
    AIDD_COVERAGE_SIM_THRESHOLD : 簡易類似度閾値（既定 0.25）
    AIDD_COVERAGE_SKIP_HEADINGS : 見出し(#...)を論点抽出に含めるか（1で含めない、既定 1）

    # Consistency
    AIDD_CONSISTENCY_ENABLE     : 1で有効（既定 1）
    AIDD_CONSISTENCY_MAX_FACTS_PER_FILE : 1ファイルから抽出するscalar fact上限（既定 1200）
    AIDD_CONSISTENCY_IGNORE_KEYS: 無視キー（カンマ区切り）
"""

import os
import sys
import glob
import json
import uuid
import re
import time
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Tuple, Set, Optional

import yaml

DEEPEVAL_AVAILABLE = True
try:
    from deepeval.metrics import FaithfulnessMetric
    from deepeval.test_case import LLMTestCase
except Exception:
    DEEPEVAL_AVAILABLE = False


# ──────────────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────────────

STAGE = os.environ.get("AIDD_STAGE", "PLN")
YAML_DIR = os.environ.get("AIDD_YAML_DIR", "artifacts/planning/yaml/v3")
OUT_ROOT = os.environ.get("AIDD_OUT_ROOT", "output/G4/transform")
EVAL_MODEL = os.environ.get("AIDD_EVAL_MODEL", "gpt-5.2")

REF_MODE = os.environ.get("AIDD_REF_MODE", "AUTO").upper().strip()

REF_PATHS_RAW = os.environ.get("AIDD_REF_PATHS", "").strip()
FILE_PATH = os.environ.get("AIDD_FILE_PATH", "").strip()
if not FILE_PATH:
    FILE_PATH = os.environ.get("AIDD_MD_PATH", "artifacts/planning/PLN-PLN-FLW-002.md").strip()

if REF_PATHS_RAW:
    REF_INPUTS = [p.strip() for p in REF_PATHS_RAW.split(",") if p.strip()]
else:
    REF_INPUTS = [FILE_PATH] if FILE_PATH else []

_skip_raw = os.environ.get("AIDD_FAITHFULNESS_SKIP", "")
FAITHFULNESS_SKIP_ALL = _skip_raw.strip() == "*"
FAITHFULNESS_SKIP_FILES = {s.strip() for s in _skip_raw.split(",") if s.strip() and s.strip() != "*"}

SKIP_DERIVED_SCOPE = os.environ.get("AIDD_FAITHFULNESS_SKIP_DERIVED_FROM_SCOPE", "1").lower() in ("1", "true", "yes")
USE_DERIVED_FROM_CONTEXT = os.environ.get("AIDD_FAITHFULNESS_USE_DERIVED_FROM_CONTEXT", "1").lower() in ("1", "true", "yes")

TOPK_REF_CHUNKS = int(os.environ.get("AIDD_FAITHFULNESS_TOPK_REF_CHUNKS", "4") or "4")
REF_CHUNK_MAX_CHARS = int(os.environ.get("AIDD_FAITHFULNESS_REF_CHUNK_MAX_CHARS", "900") or "900")

FAITH_ACTUAL_MAX = int(os.environ.get("AIDD_FAITHFULNESS_ACTUAL_MAX_CHARS", "1800") or "1800")
FAITH_CTX_MAX = int(os.environ.get("AIDD_FAITHFULNESS_CONTEXT_MAX_CHARS", "2200") or "2200")
FAITH_TRUTHS_LIM = int(os.environ.get("AIDD_FAITHFULNESS_TRUTHS_LIMIT", "10") or "10")

RETRY_ON_TIMEOUT = os.environ.get("AIDD_FAITHFULNESS_RETRY_ON_TIMEOUT", "1").lower() in ("1", "true", "yes")
RETRY_ACTUAL_MAX = int(os.environ.get("AIDD_FAITHFULNESS_ACTUAL_MAX_CHARS_RETRY", "1200") or "1200")
RETRY_CTX_MAX = int(os.environ.get("AIDD_FAITHFULNESS_CONTEXT_MAX_CHARS_RETRY", "1600") or "1600")
RETRY_TRUTHS_LIM = int(os.environ.get("AIDD_FAITHFULNESS_TRUTHS_LIMIT_RETRY", "6") or "6")

WARN_THRESHOLD = 0.70

# reason mode
REASON_MODE_RAW = os.environ.get("AIDD_FAITHFULNESS_REASON_MODE", "local").strip().lower()
FAITH_REASON_MODE = REASON_MODE_RAW if REASON_MODE_RAW in ("local", "llm") else "local"

# FaithView normalization
_STRIP_TOP_KEYS_RAW = os.environ.get("AIDD_FAITHFULNESS_STRIP_TOP_KEYS", "meta").strip()
FAITH_STRIP_TOP_KEYS = [k.strip() for k in _STRIP_TOP_KEYS_RAW.split(",") if k.strip()]

# 任意階層で除外したいキー（変換理由/章ラベルなど）
_STRIP_ANY_KEYS_RAW = os.environ.get("AIDD_FAITHFULNESS_STRIP_ANYLEVEL_KEYS", "rationale,primary_section,ssot_note").strip()
FAITH_STRIP_ANYLEVEL_KEYS = {k.strip() for k in _STRIP_ANY_KEYS_RAW.split(",") if k.strip()}

FAITH_PRUNE_NULLS = os.environ.get("AIDD_FAITHFULNESS_PRUNE_NULLS", "1").lower() in ("1", "true", "yes")
FAITH_PRUNE_MAX_DEPTH = int(os.environ.get("AIDD_FAITHFULNESS_PRUNE_MAX_DEPTH", "12") or "12")

NOISY_ASCII_SCALAR_MAXLEN = int(os.environ.get("AIDD_FAITHFULNESS_NOISY_ASCII_SCALAR_MAXLEN", "24") or "24")

# local reason config
LOCAL_REASON_TOPN = int(os.environ.get("AIDD_FAITHFULNESS_LOCAL_REASON_TOPN", "12") or "12")
LOCAL_REASON_SIM_TH = float(os.environ.get("AIDD_FAITHFULNESS_LOCAL_REASON_SIM_TH", "0.12") or "0.12")
LOCAL_REASON_MIN_LEN = int(os.environ.get("AIDD_FAITHFULNESS_LOCAL_REASON_MIN_LEN", "10") or "10")

# Completeness
COMPLETENESS_ENABLE = os.environ.get("AIDD_COMPLETENESS_ENABLE", "1").lower() in ("1", "true", "yes")
COMP_TOPN = int(os.environ.get("AIDD_COMPLETENESS_TOPN", "12") or "12")
COMP_EVIDENCE_TH = float(os.environ.get("AIDD_COMPLETENESS_EVIDENCE_TH", "0.12") or "0.12")
COMP_WARN_COUNT = int(os.environ.get("AIDD_COMPLETENESS_WARN_COUNT", "1") or "1")
COMP_FAIL_COUNT = int(os.environ.get("AIDD_COMPLETENESS_FAIL_COUNT", "3") or "3")

# Coverage
COVERAGE_ENABLE = os.environ.get("AIDD_COVERAGE_ENABLE", "1").lower() in ("1", "true", "yes")
COV_MAX_ITEMS = int(os.environ.get("AIDD_COVERAGE_MAX_ITEMS", "80") or "80")
COV_MIN_ITEM_LEN = int(os.environ.get("AIDD_COVERAGE_MIN_ITEM_LEN", "6") or "6")
COV_SIM_THRESHOLD = float(os.environ.get("AIDD_COVERAGE_SIM_THRESHOLD", "0.25") or "0.25")
COV_SKIP_HEADINGS = os.environ.get("AIDD_COVERAGE_SKIP_HEADINGS", "1").lower() in ("1", "true", "yes")

# Consistency
CONSISTENCY_ENABLE = os.environ.get("AIDD_CONSISTENCY_ENABLE", "1").lower() in ("1", "true", "yes")
CONS_MAX_FACTS_PER_FILE = int(os.environ.get("AIDD_CONSISTENCY_MAX_FACTS_PER_FILE", "1200") or "1200")

CONS_IGNORE_KEYS_RAW = os.environ.get(
    "AIDD_CONSISTENCY_IGNORE_KEYS",
    "meta.,timestamp,updated_at,created_at,hash,checksum,rationale,ssot_note,primary_section,traceability.,referenced_internal_ids"
).strip()
CONS_IGNORE_KEYS = [k.strip().lower() for k in CONS_IGNORE_KEYS_RAW.split(",") if k.strip()]

DURATION_WARN_MS = int(os.environ.get("AIDD_DURATION_WARN_MS", "300000") or "300000")  # 5min default


# ──────────────────────────────────────────────────────────────────────────────
# IO / parsing
# ──────────────────────────────────────────────────────────────────────────────

def load_text(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()

def load_yaml_file(path: str) -> Any:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def load_yaml_dir(yaml_dir: str) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for fp in sorted(glob.glob(str(Path(yaml_dir) / "*.yaml"))):
        content = load_text(fp)
        data = yaml.safe_load(content) or {}
        result[fp] = {"content": content, "data": data}
    return result

def infer_ref_mode_by_ext(file_path: str, ref_mode: str) -> str:
    if ref_mode in ("MD", "YAML"):
        return ref_mode
    ext = Path(file_path).suffix.lower()
    if ext == ".md":
        return "MD"
    if ext in (".yaml", ".yml"):
        return "YAML"
    return "MD"

def normalize_filename(p: str) -> str:
    try:
        return Path(str(p)).name
    except Exception:
        return str(p)

def expand_ref_inputs(ref_inputs: List[str]) -> List[str]:
    out: List[str] = []
    for p in ref_inputs:
        if not p:
            continue
        pp = Path(p)
        if pp.is_dir():
            for ext in ("*.md", "*.yaml", "*.yml"):
                out.extend([str(x) for x in sorted(pp.rglob(ext))])
        elif pp.is_file():
            out.append(str(pp))
        else:
            matches = sorted(glob.glob(p, recursive=True))
            for m in matches:
                mp = Path(m)
                if mp.is_dir():
                    for ext in ("*.md", "*.yaml", "*.yml"):
                        out.extend([str(x) for x in sorted(mp.rglob(ext))])
                elif mp.is_file():
                    out.append(str(mp))
    seen: Set[str] = set()
    uniq: List[str] = []
    for x in out:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq

def truncate(s: str, max_chars: int) -> str:
    if not max_chars or max_chars <= 0:
        return s
    if len(s) <= max_chars:
        return s
    return s[:max_chars] + "\n...(truncated)"


# ──────────────────────────────────────────────────────────────────────────────
# Tokenization / similarity utils
# ──────────────────────────────────────────────────────────────────────────────

_TOKEN_SPLIT = re.compile(r"[\s、。．，,;；:：\(\)\[\]\{\}<>「」『』【】/\\|]+")
_PUNCT = re.compile(r"[^\wぁ-んァ-ン一-龥]+")

def tokenize_ja_en(s: str) -> Set[str]:
    s = s.lower()
    s = _PUNCT.sub(" ", s)
    parts = [p for p in _TOKEN_SPLIT.split(s) if p]
    return {p for p in parts if len(p) >= 2}

def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    uni = len(a | b)
    return inter / uni if uni else 0.0


# ──────────────────────────────────────────────────────────────────────────────
# FaithView normalization (do NOT affect actual YAML files)
# ──────────────────────────────────────────────────────────────────────────────

_ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_ISO_DATETIME = re.compile(r"\b\d{4}-\d{2}-\d{2}[tT ]\d{2}:\d{2}:\d{2}")
_HEX_HASH = re.compile(r"\b[a-f0-9]{32,64}\b", re.IGNORECASE)
_UUID_LIKE = re.compile(r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b", re.IGNORECASE)
_ASCII_SINGLE_TOKEN = re.compile(r"^[A-Za-z0-9_./-]+$")

def is_noisy_scalar_value(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, str):
        s = v.strip()
        if s == "":
            return True
        if _ISO_DATETIME.search(s) or _ISO_DATE.search(s):
            return True
        if _HEX_HASH.search(s) or _UUID_LIKE.search(s):
            return True
        if ".md" in s.lower() or ".yaml" in s.lower() or ".yml" in s.lower():
            return True
        if "/" in s or "\\" in s:
            return True
        if len(s) <= NOISY_ASCII_SCALAR_MAXLEN and _ASCII_SINGLE_TOKEN.match(s):
            return True
    if isinstance(v, (list, dict)) and len(v) == 0:
        return True
    return False

def prune_for_faithfulness(obj: Any, depth: int = 0) -> Any:
    """
    Faithfulnessに渡すための“FaithView”:
    - top-level strip keys（例: meta）を除外
    - any-level strip keys（例: rationale / primary_section / ssot_note）を除外
    - null/空/ノイズ値を（可能なら）除外
    - 再帰深さ制限あり
    """
    if depth > FAITH_PRUNE_MAX_DEPTH:
        return obj

    if isinstance(obj, dict):
        out: Dict[str, Any] = {}
        for k, v in obj.items():
            if depth == 0 and k in FAITH_STRIP_TOP_KEYS:
                continue
            if k in FAITH_STRIP_ANYLEVEL_KEYS:
                continue

            vv = prune_for_faithfulness(v, depth + 1)
            if FAITH_PRUNE_NULLS:
                if is_noisy_scalar_value(vv):
                    continue
                if isinstance(vv, dict) and len(vv) == 0:
                    continue
                if isinstance(vv, list) and len(vv) == 0:
                    continue
            out[k] = vv
        return out

    if isinstance(obj, list):
        out_list: List[Any] = []
        for it in obj:
            vv = prune_for_faithfulness(it, depth + 1)
            if FAITH_PRUNE_NULLS and is_noisy_scalar_value(vv):
                continue
            out_list.append(vv)
        return out_list

    return obj

def dump_yaml(obj: Any) -> str:
    return yaml.dump(obj, allow_unicode=True, sort_keys=False, default_flow_style=False)


# ──────────────────────────────────────────────────────────────────────────────
# Reference chunking (timeout mitigation)
# ──────────────────────────────────────────────────────────────────────────────

def _strip_md_formatting(s: str) -> str:
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"[*_~]", "", s)
    return s.strip()

def chunk_md(text: str, file_name: str, max_chars: int) -> List[dict]:
    lines = text.splitlines()
    chunks: List[dict] = []
    cur_title = ""
    buf: List[str] = []

    def flush():
        nonlocal buf, cur_title
        if not buf:
            return
        body = "\n".join(buf).strip()
        if body:
            body = truncate(body, max_chars)
            chunks.append({
                "ref": file_name,
                "title": cur_title or file_name,
                "text": body,
                "tokens": tokenize_ja_en(body),
            })
        buf = []

    for ln in lines:
        s = ln.rstrip()
        if re.match(r"^#{1,6}\s+", s):
            flush()
            cur_title = _strip_md_formatting(re.sub(r"^#{1,6}\s+", "", s).strip())
            continue
        if s.strip().startswith("====="):
            flush()
            continue
        buf.append(s)
        if sum(len(x) + 1 for x in buf) >= max_chars * 2:
            flush()

    flush()

    if not chunks:
        t = truncate(text.strip(), max_chars)
        chunks = [{
            "ref": file_name,
            "title": file_name,
            "text": t,
            "tokens": tokenize_ja_en(t),
        }]
    return chunks

def chunk_yaml(data: Any, file_name: str, max_chars: int) -> List[dict]:
    chunks: List[dict] = []
    if isinstance(data, dict):
        for k, v in data.items():
            sub = {k: v}
            dumped = dump_yaml(sub)
            dumped = truncate(dumped, max_chars)
            chunks.append({
                "ref": file_name,
                "title": f"{file_name}:{k}",
                "text": dumped,
                "tokens": tokenize_ja_en(dumped),
            })
    else:
        dumped = dump_yaml(data)
        dumped = truncate(dumped, max_chars)
        chunks.append({
            "ref": file_name,
            "title": file_name,
            "text": dumped,
            "tokens": tokenize_ja_en(dumped),
        })
    return chunks

def build_reference_chunks(ref_files: List[str], ref_mode: str, chunk_max_chars: int) -> Tuple[List[dict], Set[str]]:
    all_chunks: List[dict] = []
    names: Set[str] = set()
    for fp in ref_files:
        mode = infer_ref_mode_by_ext(fp, ref_mode)
        name = Path(fp).name
        names.add(name)
        if mode == "MD":
            txt = load_text(fp)
            all_chunks.extend(chunk_md(txt, name, chunk_max_chars))
        else:
            data = load_yaml_file(fp)
            all_chunks.extend(chunk_yaml(data, name, chunk_max_chars))
    return all_chunks, names

def select_topk_ref_chunks(yaml_content: str, ref_chunks: List[dict], topk: int, total_ctx_max: int) -> List[str]:
    qtok = tokenize_ja_en(yaml_content[:4000])
    scored: List[Tuple[float, dict]] = []
    for ch in ref_chunks:
        s = jaccard(qtok, ch.get("tokens") or set())
        scored.append((s, ch))
    scored.sort(key=lambda x: x[0], reverse=True)

    chosen: List[str] = []
    used = 0
    for s, ch in scored[:max(1, topk * 4)]:
        txt = ch["text"]
        header = f"===== REF_CHUNK: {ch['ref']} :: {ch['title']} (sim={s:.3f}) =====\n"
        block = header + txt.strip() + "\n"
        if not block.strip():
            continue
        if used + len(block) > total_ctx_max and chosen:
            break
        if used + len(block) > total_ctx_max and not chosen:
            block = truncate(block, total_ctx_max)
        chosen.append(block)
        used += len(block)
        if len(chosen) >= topk:
            break

    if not chosen:
        chosen = [truncate(ref_chunks[0]["text"], total_ctx_max)] if ref_chunks else [""]
    return chosen


# ──────────────────────────────────────────────────────────────────────────────
# derived_from helpers
# ──────────────────────────────────────────────────────────────────────────────

def derived_from_list(yaml_data: dict) -> List[str]:
    df = yaml_data.get("derived_from") or []
    if isinstance(df, str):
        return [df]
    if isinstance(df, list):
        return [str(x) for x in df if x is not None]
    return []

def _derived_from_name_candidates(yaml_data: dict) -> Set[str]:
    out: Set[str] = set()
    for x in derived_from_list(yaml_data):
        n = normalize_filename(x)
        if not n:
            continue
        out.add(n)
        p = Path(n)
        if p.suffix == "":
            out.add(p.name + ".md")
            out.add(p.name + ".yaml")
            out.add(p.name + ".yml")
    return out

def should_skip_by_derived_from_scope(yaml_data: dict, ref_names: Set[str]) -> Tuple[bool, str]:
    df = derived_from_list(yaml_data)
    if not df:
        return False, ""
    df_names = {normalize_filename(x) for x in df}
    if df_names.isdisjoint(ref_names):
        return True, f"[SKIP] derived_from に参照セット({sorted(ref_names)})が無いためスコープ外（derived_from={sorted(df_names)})"
    return False, ""

def is_qa_supplement(yaml_data: dict, ref_names: Set[str]) -> bool:
    for ref in derived_from_list(yaml_data):
        ref_name = normalize_filename(ref)
        if ref_name in ref_names:
            continue
        if ref_name.lower().endswith((".md", ".yaml", ".yml")):
            return True
    return False

def filter_ref_chunks_by_derived_from(
    yaml_data: dict,
    ref_chunks: List[dict],
    ref_names: Set[str],
) -> Tuple[List[dict], Set[str]]:
    df_candidates = _derived_from_name_candidates(yaml_data)
    df_hits = {n for n in df_candidates if n in ref_names}
    if not df_hits:
        return ref_chunks, set()

    filtered = [ch for ch in ref_chunks if ch.get("ref") in df_hits]
    if not filtered:
        return ref_chunks, set()

    return filtered, df_hits


# ──────────────────────────────────────────────────────────────────────────────
# Timeout detection
# ──────────────────────────────────────────────────────────────────────────────

_TIMEOUT_HINT = re.compile(
    r"(Timeout|ReadTimeout|timed out|TimeoutError|Deadline|LengthFinishReasonError|RetryError)",
    re.IGNORECASE,
)

def is_timeout_like(exc: Exception) -> bool:
    msg = str(exc) or ""
    if _TIMEOUT_HINT.search(msg):
        return True
    cause = getattr(exc, "__cause__", None)
    if cause and _TIMEOUT_HINT.search(str(cause) or ""):
        return True
    ctx = getattr(exc, "__context__", None)
    if ctx and _TIMEOUT_HINT.search(str(ctx) or ""):
        return True
    return False

def warn_if_slow(name: str, duration_ms: int):
    if duration_ms >= DURATION_WARN_MS:
        print(f"  [WARN] slow_eval: {name} duration_ms={duration_ms}", flush=True)


# ──────────────────────────────────────────────────────────────────────────────
# deepeval Faithfulness builder + reason extractor
# ──────────────────────────────────────────────────────────────────────────────

def build_faith_metric(truths_limit: int, include_reason: bool):
    base_kwargs = {
        "threshold": WARN_THRESHOLD,
        "model": EVAL_MODEL,
        "include_reason": include_reason,
        "async_mode": False,
    }
    extra_kwargs = {}
    if truths_limit and truths_limit > 0:
        extra_kwargs["truths_extraction_limit"] = truths_limit
    extra_kwargs["penalize_ambiguous_claims"] = True
    try:
        return FaithfulnessMetric(**base_kwargs, **extra_kwargs)
    except TypeError:
        return FaithfulnessMetric(**base_kwargs)

def extract_metric_reason(metric: Any) -> str:
    for attr in ("reason", "explanation", "rationale"):
        v = getattr(metric, attr, None)
        if isinstance(v, str) and v.strip():
            return v.strip()

    for attr in ("verbose_logs", "logs", "details"):
        v = getattr(metric, attr, None)
        if isinstance(v, str) and v.strip():
            return v.strip()
        if isinstance(v, list) and v:
            joined = "\n".join(str(x) for x in v if x)
            if joined.strip():
                return joined.strip()
        if isinstance(v, dict) and v:
            try:
                return json.dumps(v, ensure_ascii=False, indent=2)
            except Exception:
                return str(v)
    return ""


# ──────────────────────────────────────────────────────────────────────────────
# Local reason generation (no extra API calls)
# ──────────────────────────────────────────────────────────────────────────────

_ASSERT_WORDS = (
    "必ず", "禁止", "推奨", "要件", "shall", "must", "should", "will",
    "である", "する", "必要", "不可", "できない", "しない"
)

_CONTAINER_ONLY_LINE = re.compile(r"^\s*-?\s*[A-Za-z0-9_./-]+\s*:\s*$")

def split_yaml_lines(yaml_text: str) -> List[str]:
    lines = []
    for ln in yaml_text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        if s.startswith("====="):
            continue
        if _CONTAINER_ONLY_LINE.match(ln):
            continue
        lines.append(ln.rstrip())
    return lines

def line_priority(line: str) -> int:
    l = line.lower()
    for w in _ASSERT_WORDS:
        if w in l:
            return 2
    if re.match(r"^[\s-]*[a-zA-Z0-9_./-]+\s*:", line):
        return 1
    return 0

def build_local_reason(faith_yaml_text: str, ref_ctx_list: List[str]) -> str:
    ref_blob = "\n".join(ref_ctx_list).strip()
    ref_tok = tokenize_ja_en(ref_blob)
    lines = split_yaml_lines(faith_yaml_text)

    scored: List[Tuple[float, int, str]] = []
    for ln in lines:
        s = ln.strip()
        if len(s) < LOCAL_REASON_MIN_LEN:
            continue
        lt = tokenize_ja_en(s)
        sim = jaccard(lt, ref_tok) if ref_tok else 0.0
        pri = line_priority(s)
        scored.append((sim, -pri, s))

    scored.sort(key=lambda x: (x[0], x[1]))

    picked = []
    for sim, _npri, s in scored:
        if sim <= LOCAL_REASON_SIM_TH:
            picked.append((sim, s))
        if len(picked) >= LOCAL_REASON_TOPN:
            break

    if not picked:
        return (
            "[label] LOW_SIGNAL\n"
            "[signal] no_low_support_lines_detected\n"
            "[action]\n"
            "- 参照MDが薄い場合: split MDへ要点を逆輸入（箇条書き3〜5）\n"
            "- YAMLが言い切りすぎの場合: （案）（要検討）に落とす/断定を弱める\n"
        )

    buf = []
    buf.append("[label] SSOT_GAP_OR_OVERASSERT\n")
    buf.append(f"[signal] low_support_lines={len(picked)} (sim_th={LOCAL_REASON_SIM_TH})\n")
    buf.append("[top_missing_lines]\n")
    for sim, s in picked:
        buf.append(f"- (sim={sim:.3f}) {s}\n")
    buf.append("[action]\n")
    buf.append("- 参照MDが薄い場合: split MD(derived_from)へ上記要点を根拠として追記（箇条書き3〜5）\n")
    buf.append("- YAMLが言い切りすぎの場合: 断定語を弱める/（案）（要検討）に落とす/参照に根拠追記\n")
    buf.append("- 用語ゆれの場合: split MDとYAMLで表現を統一（別名併記も可）\n")
    return "".join(buf)


# ──────────────────────────────────────────────────────────────────────────────
# Faithfulness evaluation
# ──────────────────────────────────────────────────────────────────────────────

def auto_pass_result(fname: str, fp: str, reason: str, category: str = "faithfulness") -> dict:
    return {
        "test_name": f"{category.capitalize()} :: {fname}",
        "category": category,
        "file": fp,
        "score": 1.0,
        "passed": True,
        "status": "pass",
        "reason": reason,
        "duration_ms": 0,
        "retried": False,
    }

def eval_one_faithfulness(
    fname: str,
    yaml_content: str,
    ref_context_list: List[str],
    actual_max: int,
    ctx_max: int,
    truths_limit: int,
    include_reason: bool,
) -> Tuple[float, bool, str]:
    metric = build_faith_metric(truths_limit, include_reason=include_reason)

    joined = "\n".join(ref_context_list)
    joined = truncate(joined, ctx_max)

    tc = LLMTestCase(
        input=(
            f"このYAML（{fname}）は参照の内容を構造化したものです。"
            "構造化のためのキー名・章ラベル・分類名の追加は許容します。"
            "ただし、参照本文に存在しない『意味のある主張（要件・判断・数値・制約・因果関係など）』を追加していないかを評価してください。"
            "参照に無い主張がある場合のみ減点してください。"
        ),
        actual_output=truncate(yaml_content, actual_max),
        retrieval_context=[joined],
    )
    metric.measure(tc)
    score = float(metric.score)
    passed = bool(metric.is_successful())

    reason = ""
    if include_reason:
        reason = extract_metric_reason(metric)
    return score, passed, reason

def eval_faithfulness(
    ref_chunks: List[dict],
    ref_names: Set[str],
    yaml_files: Dict[str, Dict[str, Any]],
) -> List[dict]:
    results: List[dict] = []

    if not DEEPEVAL_AVAILABLE:
        for fp in yaml_files.keys():
            fname = Path(fp).name
            results.append({
                "test_name": f"Faithfulness :: {fname}",
                "category": "faithfulness",
                "file": fp,
                "score": 0.0,
                "passed": False,
                "status": "error",
                "reason": "deepeval is not available in this runtime (cannot import deepeval).",
                "duration_ms": 0,
                "retried": False,
                "reason_mode": "none",
            })
        return results

    for fp, info in yaml_files.items():
        fname = Path(fp).name
        yaml_data = info["data"]
        start = time.time()

        if FAITHFULNESS_SKIP_ALL:
            r = auto_pass_result(fname, fp, "[SKIP] AIDD_FAITHFULNESS_SKIP=* により全スキップ")
            r["duration_ms"] = int((time.time() - start) * 1000)
            r["reason_mode"] = "none"
            results.append(r)
            continue

        if fname in FAITHFULNESS_SKIP_FILES:
            r = auto_pass_result(fname, fp, f"[SKIP] AIDD_FAITHFULNESS_SKIP に明示指定（{fname}）")
            r["duration_ms"] = int((time.time() - start) * 1000)
            r["reason_mode"] = "none"
            results.append(r)
            continue

        if SKIP_DERIVED_SCOPE:
            skip_df, msg_df = should_skip_by_derived_from_scope(yaml_data, ref_names)
            if skip_df:
                r = auto_pass_result(fname, fp, msg_df)
                r["duration_ms"] = int((time.time() - start) * 1000)
                r["reason_mode"] = "none"
                results.append(r)
                continue

        if is_qa_supplement(yaml_data, ref_names):
            r = auto_pass_result(fname, fp, "[AUTO-PASS] 補足資料由来のファイルとしてFaithfulness自動PASS")
            r["duration_ms"] = int((time.time() - start) * 1000)
            r["reason_mode"] = "none"
            results.append(r)
            continue

        faith_view_obj = prune_for_faithfulness(yaml_data, depth=0)
        faith_yaml_text = dump_yaml(faith_view_obj).strip()
        if not faith_yaml_text:
            faith_yaml_text = info["content"]

        used_ref_chunks = ref_chunks
        df_hits: Set[str] = set()
        if USE_DERIVED_FROM_CONTEXT:
            used_ref_chunks, df_hits = filter_ref_chunks_by_derived_from(yaml_data, ref_chunks, ref_names)

        ref_ctx = select_topk_ref_chunks(
            yaml_content=faith_yaml_text,
            ref_chunks=used_ref_chunks,
            topk=TOPK_REF_CHUNKS,
            total_ctx_max=FAITH_CTX_MAX,
        )

        extra_note = f" derived_from_ctx={sorted(df_hits)}" if df_hits else ""
        print(f"  [EVAL] Faithfulness: {fname} ...{extra_note}", end=" ", flush=True)

        try:
            score, passed, _ = eval_one_faithfulness(
                fname=fname,
                yaml_content=faith_yaml_text,
                ref_context_list=ref_ctx,
                actual_max=FAITH_ACTUAL_MAX,
                ctx_max=FAITH_CTX_MAX,
                truths_limit=FAITH_TRUTHS_LIM,
                include_reason=False,
            )
            status = "pass" if passed else ("warn" if score >= 0.5 else "fail")
            print(f"score={score:.3f} → {status.upper()}")

            reason = ""
            reason_mode = "none"

            if status in ("fail", "warn"):
                local_reason = build_local_reason(faith_yaml_text, ref_ctx)

                if FAITH_REASON_MODE == "local":
                    reason = local_reason
                    reason_mode = "local"
                else:
                    try:
                        _s2, _p2, llm_reason = eval_one_faithfulness(
                            fname=fname,
                            yaml_content=truncate(faith_yaml_text, min(FAITH_ACTUAL_MAX, 900)),
                            ref_context_list=ref_ctx[:1],
                            actual_max=min(FAITH_ACTUAL_MAX, 900),
                            ctx_max=min(FAITH_CTX_MAX, 900),
                            truths_limit=min(FAITH_TRUTHS_LIM, 6),
                            include_reason=True,
                        )
                        llm_reason = (llm_reason or "").strip()
                        if llm_reason:
                            reason = llm_reason
                            reason_mode = "llm"
                        else:
                            reason = local_reason
                            reason_mode = "local_fallback"
                    except Exception as exc_reason:
                        reason = local_reason + f"\n[llm_reason_error] {exc_reason}"
                        reason_mode = "local_fallback"

            duration_ms = int((time.time() - start) * 1000)
            warn_if_slow(fname, duration_ms)

            results.append({
                "test_name": f"Faithfulness :: {fname}",
                "category": "faithfulness",
                "file": fp,
                "score": round(score, 4),
                "passed": bool(passed),
                "status": status,
                "reason": reason,
                "reason_mode": reason_mode,
                "duration_ms": duration_ms,
                "retried": False,
                "derived_from_context": sorted(df_hits) if df_hits else [],
            })

        except Exception as exc:
            if RETRY_ON_TIMEOUT and is_timeout_like(exc):
                print("TIMEOUT → RETRY", flush=True)
                try:
                    ref_ctx_retry = select_topk_ref_chunks(
                        yaml_content=faith_yaml_text,
                        ref_chunks=used_ref_chunks,
                        topk=max(1, TOPK_REF_CHUNKS // 2),
                        total_ctx_max=RETRY_CTX_MAX,
                    )
                    score, passed, _ = eval_one_faithfulness(
                        fname=fname,
                        yaml_content=faith_yaml_text,
                        ref_context_list=ref_ctx_retry,
                        actual_max=RETRY_ACTUAL_MAX,
                        ctx_max=RETRY_CTX_MAX,
                        truths_limit=RETRY_TRUTHS_LIM,
                        include_reason=False,
                    )
                    status = "pass" if passed else ("warn" if score >= 0.5 else "fail")
                    print(f"  [RETRY OK] score={score:.3f} → {status.upper()}")

                    reason = ""
                    reason_mode = "none"
                    if status in ("fail", "warn"):
                        local_reason = build_local_reason(faith_yaml_text, ref_ctx_retry)
                        reason = local_reason
                        reason_mode = "local"

                    duration_ms = int((time.time() - start) * 1000)
                    warn_if_slow(fname, duration_ms)

                    results.append({
                        "test_name": f"Faithfulness :: {fname}",
                        "category": "faithfulness",
                        "file": fp,
                        "score": round(score, 4),
                        "passed": bool(passed),
                        "status": status,
                        "reason": reason,
                        "reason_mode": reason_mode,
                        "duration_ms": duration_ms,
                        "retried": True,
                        "retry_params": {
                            "topk_ref_chunks": max(1, TOPK_REF_CHUNKS // 2),
                            "actual_max_chars": RETRY_ACTUAL_MAX,
                            "context_max_chars": RETRY_CTX_MAX,
                            "truths_limit": RETRY_TRUTHS_LIM,
                        },
                        "first_error": str(exc),
                        "derived_from_context": sorted(df_hits) if df_hits else [],
                    })
                    continue
                except Exception as exc2:
                    print(f"  [RETRY FAIL] {exc2}", flush=True)
                    duration_ms = int((time.time() - start) * 1000)
                    warn_if_slow(fname, duration_ms)
                    results.append({
                        "test_name": f"Faithfulness :: {fname}",
                        "category": "faithfulness",
                        "file": fp,
                        "score": 0.0,
                        "passed": False,
                        "status": "error",
                        "reason": f"Timeout-like error then retry failed. first={exc} / retry={exc2}",
                        "reason_mode": "none",
                        "duration_ms": duration_ms,
                        "retried": True,
                        "first_error": str(exc),
                        "retry_error": str(exc2),
                        "derived_from_context": sorted(df_hits) if df_hits else [],
                    })
                    continue

            print(f"ERROR: {exc}", flush=True)
            duration_ms = int((time.time() - start) * 1000)
            warn_if_slow(fname, duration_ms)
            results.append({
                "test_name": f"Faithfulness :: {fname}",
                "category": "faithfulness",
                "file": fp,
                "score": 0.0,
                "passed": False,
                "status": "error",
                "reason": str(exc),
                "reason_mode": "none",
                "duration_ms": duration_ms,
                "retried": False,
                "derived_from_context": sorted(df_hits) if df_hits else [],
            })

    return results


# ──────────────────────────────────────────────────────────────────────────────
# Coverage (derived_from 1:1 / rule-based)
# ──────────────────────────────────────────────────────────────────────────────

def extract_reference_items_for_coverage(ref_texts: List[str], max_items: int, min_len: int, skip_headings: bool) -> List[str]:
    items: List[str] = []
    for txt in ref_texts:
        for line in txt.splitlines():
            raw = line.strip()
            if not raw:
                continue
            if raw.startswith("====="):
                continue

            is_heading = bool(re.match(r"^#{1,6}\s+", raw))
            is_bullet = bool(re.match(r"^([-*+]|(\d+\.))\s+", raw))

            if skip_headings and is_heading:
                continue

            if not (is_heading or is_bullet):
                continue

            s = raw
            s = re.sub(r"^#{1,6}\s+", "", s)
            s = re.sub(r"^([-*+]|(\d+\.))\s+", "", s)
            s = _strip_md_formatting(s)

            if s.lower() in ("todo", "tbd", "pending"):
                continue
            if len(s) < min_len:
                continue

            items.append(s)
            if len(items) >= max_items:
                break
        if len(items) >= max_items:
            break

    seen: Set[str] = set()
    uniq: List[str] = []
    for x in items:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq

def compute_global_coverage(ref_items: List[str], yaml_files: Dict[str, Dict[str, Any]], sim_th: float) -> Tuple[float, List[dict]]:
    corpus_lines: List[str] = []
    for info in yaml_files.values():
        for ln in info["content"].splitlines():
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            corpus_lines.append(ln)

    line_tokens: List[Set[str]] = [tokenize_ja_en(l) for l in corpus_lines]

    details: List[dict] = []
    covered = 0

    for item in ref_items:
        it_tok = tokenize_ja_en(item)
        best = 0.0
        best_line = ""
        for ln, tok in zip(corpus_lines, line_tokens):
            if not tok:
                continue
            s = jaccard(it_tok, tok)
            if s > best:
                best = s
                best_line = ln
            if best >= 0.85:
                break

        is_cov = best >= sim_th
        if is_cov:
            covered += 1

        details.append({
            "item": item,
            "covered": is_cov,
            "best_sim": round(best, 4),
            "best_match": best_line[:240] + ("..." if len(best_line) > 240 else ""),
        })

    score = (covered / len(ref_items)) if ref_items else 1.0
    return score, details


# ──────────────────────────────────────────────────────────────────────────────
# Completeness (derived_from 1:1 / rule-based)
# ──────────────────────────────────────────────────────────────────────────────

def collect_null_paths(data: Any, prefix: str = "", out: Optional[List[Tuple[str, Any]]] = None, limit: int = 2000) -> List[Tuple[str, Any]]:
    if out is None:
        out = []
    if len(out) >= limit:
        return out

    if isinstance(data, dict):
        for k, v in data.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            collect_null_paths(v, p, out, limit)
            if len(out) >= limit:
                break
    elif isinstance(data, list):
        for i, v in enumerate(data):
            p = f"{prefix}[{i}]"
            collect_null_paths(v, p, out, limit)
            if len(out) >= limit:
                break
    else:
        if data is None:
            out.append((prefix, None))
        elif isinstance(data, str) and data.strip() == "":
            out.append((prefix, data))
    return out

def path_tokens(path: str) -> Set[str]:
    s = re.sub(r"[\[\]\d]+", " ", path)
    s = s.replace(".", " ")
    return tokenize_ja_en(s)

def completeness_check_one(yaml_data: dict, ref_text: str) -> Tuple[str, int, int, List[dict]]:
    nulls = collect_null_paths(yaml_data)
    null_total = len(nulls)

    ref_tok = tokenize_ja_en(ref_text or "")
    suspicious_items: List[Tuple[float, str]] = []

    for p, _v in nulls:
        if not p:
            continue
        pt = path_tokens(p)
        sim = jaccard(pt, ref_tok) if (pt and ref_tok) else 0.0
        if sim >= COMP_EVIDENCE_TH:
            suspicious_items.append((sim, p))

    suspicious_items.sort(key=lambda x: x[0], reverse=True)
    suspicious = len(suspicious_items)

    if suspicious >= COMP_FAIL_COUNT:
        status = "fail"
    elif suspicious >= COMP_WARN_COUNT:
        status = "warn"
    else:
        status = "pass"

    details = []
    for sim, p in suspicious_items[:COMP_TOPN]:
        details.append({
            "path": p,
            "evidence_sim": round(sim, 4),
            "suggestion": "参照に該当要素がある可能性。nullのままでよいか確認し、必要なら値を埋める/（TBD）等の表現を明示。",
        })

    return status, null_total, suspicious, details


# ──────────────────────────────────────────────────────────────────────────────
# Global Consistency (rule-based)
# ──────────────────────────────────────────────────────────────────────────────

def should_ignore_key(path_key: str) -> bool:
    lk = path_key.lower()
    for ig in CONS_IGNORE_KEYS:
        if ig and ig in lk:
            return True
    return False

def is_scalar(x: Any) -> bool:
    return isinstance(x, (str, int, float, bool)) or x is None

def scalar_norm(x: Any) -> str:
    if x is None:
        return "null"
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, (int, float)):
        if isinstance(x, float) and x.is_integer():
            x = int(x)
        return str(x)
    s = str(x).strip()
    s = re.sub(r"\s+", " ", s)
    return s

def collect_scalar_facts(data: Any, prefix: str = "", out: Optional[List[Tuple[str, str]]] = None, limit: int = 1200) -> List[Tuple[str, str]]:
    if out is None:
        out = []
    if len(out) >= limit:
        return out

    if isinstance(data, dict):
        for k, v in data.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            if should_ignore_key(p):
                continue
            collect_scalar_facts(v, p, out, limit)
            if len(out) >= limit:
                break
    elif isinstance(data, list):
        for i, v in enumerate(data):
            p = f"{prefix}[{i}]"
            collect_scalar_facts(v, p, out, limit)
            if len(out) >= limit:
                break
    else:
        if is_scalar(data) and prefix:
            out.append((prefix, scalar_norm(data)))

    return out

_NUM_FACT = re.compile(
    r"(?P<label>(threshold|thresh|warn|warning|pass|fail|fatal|score|avg|average|minimum|max|maximum))[^0-9]{0,20}(?P<num>\d+(\.\d+)?)",
    re.IGNORECASE,
)

def extract_numeric_constraints(ref_texts: List[str]) -> Dict[str, Set[str]]:
    out: Dict[str, Set[str]] = {}
    blob = "\n".join(ref_texts)
    for m in _NUM_FACT.finditer(blob):
        label = (m.group("label") or "").lower()
        num = m.group("num")
        if label and num:
            out.setdefault(label, set()).add(num)
    return out

def scan_numeric_in_yaml(yaml_files: Dict[str, Dict[str, Any]]) -> Dict[str, Set[str]]:
    out: Dict[str, Set[str]] = {}
    for info in yaml_files.values():
        txt = info["content"]
        for m in _NUM_FACT.finditer(txt):
            label = (m.group("label") or "").lower()
            num = m.group("num")
            if label and num:
                out.setdefault(label, set()).add(num)
    return out

def compute_global_consistency(
    yaml_files: Dict[str, Dict[str, Any]],
    ref_texts: List[str],
) -> Tuple[float, List[dict]]:
    path_map: Dict[str, Dict[str, List[str]]] = {}

    for fp, info in yaml_files.items():
        facts = collect_scalar_facts(info["data"], limit=CONS_MAX_FACTS_PER_FILE)
        for path, val in facts:
            if not path:
                continue
            if should_ignore_key(path):
                continue
            pv = path_map.setdefault(path, {})
            pv.setdefault(val, []).append(Path(fp).name)

    contradictions: List[dict] = []
    checked_paths = 0

    for path, vmap in path_map.items():
        vals = list(vmap.keys())
        checked_paths += 1
        if len(vals) <= 1:
            continue
        contradictions.append({
            "type": "path_value_conflict",
            "path": path,
            "values": [{"value": v, "files": sorted(fs)} for v, fs in vmap.items()],
        })

    ref_nums = extract_numeric_constraints(ref_texts)
    yaml_nums = scan_numeric_in_yaml(yaml_files)
    for label, expected in ref_nums.items():
        observed = yaml_nums.get(label, set())
        if not observed:
            continue
        if not observed.issubset(expected) or not expected.issubset(observed):
            contradictions.append({
                "type": "numeric_mismatch",
                "label": label,
                "expected": sorted(expected),
                "observed": sorted(observed),
            })

    path_conflicts = sum(1 for c in contradictions if c["type"] == "path_value_conflict")
    numeric_conflicts = sum(1 for c in contradictions if c["type"] == "numeric_mismatch")

    if checked_paths <= 0:
        base = 1.0
    else:
        base = 1.0 - (path_conflicts / checked_paths)

    score = max(0.0, min(1.0, base - (0.05 * numeric_conflicts)))
    return score, contradictions


# ──────────────────────────────────────────────────────────────────────────────
# Output / Allure
# ──────────────────────────────────────────────────────────────────────────────

def summary(results: List[dict]) -> dict:
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    scores = [float(r.get("score", 0.0)) for r in results if "score" in r]
    avg = (sum(scores) / len(scores)) if scores else 0.0
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "avg_score": round(avg, 4),
        "warning": avg < WARN_THRESHOLD,
    }

def make_out_paths(out_root: str) -> Tuple[Path, Path]:
    yaml_subdir = YAML_DIR.replace("\\", "_").replace("/", "_").strip("_")
    ts_fname = datetime.now().strftime("%m%d_%H%M") + ".json"
    base_dir = Path(out_root) / yaml_subdir
    return base_dir / ts_fname, base_dir / "allure-results"

def write_results(all_results: List[dict], out_root: str, meta: dict) -> dict:
    json_path, allure_dir = make_out_paths(out_root)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    allure_dir.mkdir(parents=True, exist_ok=True)

    overall_pass = all(r.get("passed", False) for r in all_results)

    faith_results = [r for r in all_results if r["category"] == "faithfulness"]
    cov_results = [r for r in all_results if r["category"] == "coverage"]
    comp_results = [r for r in all_results if r["category"] == "completeness"]
    cons_results = [r for r in all_results if r["category"] == "consistency"]

    output = {
        "gate_id": "G4",
        "stage": STAGE,
        "model": EVAL_MODEL,
        "timestamp": datetime.now().isoformat(),
        "inputs": meta.get("inputs", {}),
        "summary": {
            "total": len(all_results),
            "passed": sum(1 for r in all_results if r.get("passed")),
            "failed": sum(1 for r in all_results if not r.get("passed")),
            "overall_status": "pass" if overall_pass else "fail",
            "faithfulness": summary(faith_results),
            "coverage": summary(cov_results),
            "completeness": summary(comp_results),
            "consistency": summary(cons_results),
        },
        "results": all_results,
        "details": meta.get("details", {}),
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    ts_ms = int(time.time() * 1000)
    for r in all_results:
        if r.get("status") == "error":
            allure_status = "broken"
        else:
            allure_status = "passed" if r.get("passed") else "failed"

        ar = {
            "uuid": str(uuid.uuid4()),
            "name": r["test_name"],
            "status": allure_status,
            "stage": "finished",
            "start": ts_ms,
            "stop": ts_ms + int(r.get("duration_ms", 0)),
            "labels": [
                {"name": "suite", "value": f"G4 {STAGE} Transform"},
                {"name": "feature", "value": r["category"].capitalize()},
                {"name": "severity", "value": r.get("severity", "normal")},
                {"name": "tag", "value": "G4"},
            ],
            "parameters": [
                {"name": "score", "value": str(r.get("score", ""))},
                {"name": "model", "value": EVAL_MODEL},
                {"name": "status", "value": r.get("status", "")},
            ],
            "description": r.get("reason", ""),
            "steps": [],
        }
        allure_path = allure_dir / f"{ar['uuid']}-result.json"
        with open(allure_path, "w", encoding="utf-8") as f:
            json.dump(ar, f, ensure_ascii=False, indent=2)

    output["_meta"] = {"json_path": str(json_path), "allure_dir": str(allure_dir)}
    return output


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    ref_files = expand_ref_inputs(REF_INPUTS)

    if not ref_files and not FAITHFULNESS_SKIP_ALL and (COVERAGE_ENABLE or CONSISTENCY_ENABLE or COMPLETENESS_ENABLE):
        print("[G4] ERROR: 参照ファイルが見つかりません。AIDD_REF_PATHS または AIDD_FILE_PATH を設定してください。")
        sys.exit(2)

    ref_chunks: List[dict] = []
    ref_names: Set[str] = set()
    ref_text_map_for_rule: Dict[str, str] = {}

    if ref_files:
        ref_chunks, ref_names = build_reference_chunks(ref_files, REF_MODE, REF_CHUNK_MAX_CHARS)
        for fp in ref_files:
            name = Path(fp).name
            mode = infer_ref_mode_by_ext(fp, REF_MODE)
            if mode == "MD":
                ref_text_map_for_rule[name] = load_text(fp)
            else:
                data = load_yaml_file(fp)
                ref_text_map_for_rule[name] = dump_yaml(data)

    yaml_files = load_yaml_dir(YAML_DIR)

    print(f"\n{'=' * 72}")
    print(f"[G4] Transform Quality Check")
    print(f"[G4] Stage : {STAGE}")
    print(f"[G4] Model : {EVAL_MODEL}")
    print(f"[G4] YAMLs : {YAML_DIR}  ({len(yaml_files)} files)")
    print(f"[G4] REF  : {', '.join(ref_files) if ref_files else '(none)'}")
    print(f"[G4] deepeval available: {DEEPEVAL_AVAILABLE}")
    print(f"[G4] Faithfulness topK ref chunks: {TOPK_REF_CHUNKS} (chunk_max_chars={REF_CHUNK_MAX_CHARS}, ctx_max={FAITH_CTX_MAX})")
    print(f"[G4] Faithfulness derived_from context filter: {'ON' if USE_DERIVED_FROM_CONTEXT else 'OFF'}")
    print(f"[G4] Faithfulness reason mode: {FAITH_REASON_MODE}")
    print(f"[G4] Faithfulness strip top keys: {FAITH_STRIP_TOP_KEYS}")
    print(f"[G4] Faithfulness strip any-level keys: {sorted(list(FAITH_STRIP_ANYLEVEL_KEYS))}")
    print(f"[G4] Faithfulness prune_nulls={'ON' if FAITH_PRUNE_NULLS else 'OFF'} prune_max_depth={FAITH_PRUNE_MAX_DEPTH}")
    print(f"[G4] Faithfulness noisy ASCII scalar maxlen: {NOISY_ASCII_SCALAR_MAXLEN}")
    print(f"[G4] Coverage    : {'ON' if COVERAGE_ENABLE else 'OFF'} (derived_from per-file)")
    print(f"[G4] Completeness: {'ON' if COMPLETENESS_ENABLE else 'OFF'} (derived_from per-file)")
    print(f"[G4] Consistency : {'ON' if CONSISTENCY_ENABLE else 'OFF'}")
    print(f"{'=' * 72}\n")

    all_results: List[dict] = []
    details_meta: dict = {}

    # 1) Faithfulness
    print("[G4] ── Faithfulness（ファイル単位）──")
    faith_results = eval_faithfulness(ref_chunks, ref_names, yaml_files)
    all_results.extend(faith_results)

    # 2) Coverage (derived_from 1:1 / per-file)
    if COVERAGE_ENABLE:
        print("\n[G4] ── Coverage（derived_from 単位）──")
        start = time.time()

        if not ref_text_map_for_rule:
            all_results.append({
                "test_name": "Coverage :: GLOBAL",
                "category": "coverage",
                "file": YAML_DIR,
                "score": 0.0,
                "passed": False,
                "status": "error",
                "reason": "No reference content available for coverage (ref_text_map_for_rule is empty).",
                "duration_ms": int((time.time() - start) * 1000),
            })
        else:
            per_file_scores: List[float] = []
            per_file_details: List[dict] = []

            for yfp, info in yaml_files.items():
                yname = Path(yfp).name
                ydata = info["data"]
                ycontent = info["content"]

                df_candidates = _derived_from_name_candidates(ydata)
                df_hits = [n for n in sorted(df_candidates) if n in ref_text_map_for_rule]

                if not df_hits:
                    all_results.append({
                        "test_name": f"Coverage :: {yname}",
                        "category": "coverage",
                        "file": yfp,
                        "score": 0.0,
                        "passed": False,
                        "status": "error",
                        "reason": f"derived_from が無い/参照に解決できません (derived_from={derived_from_list(ydata)})",
                        "duration_ms": 0,
                    })
                    per_file_details.append({
                        "file": yname,
                        "derived_from": derived_from_list(ydata),
                        "resolved_refs": [],
                        "score": 0.0,
                        "status": "error",
                        "items": [],
                    })
                    continue

                ref_blob = "\n\n".join(f"===== REF_FILE: {rn} =====\n{ref_text_map_for_rule[rn]}" for rn in df_hits)

                ref_items = extract_reference_items_for_coverage(
                    [ref_blob],
                    COV_MAX_ITEMS,
                    COV_MIN_ITEM_LEN,
                    skip_headings=COV_SKIP_HEADINGS,
                )

                tmp_yaml_files = {yfp: {"content": ycontent, "data": ydata}}
                cov_score, cov_details = compute_global_coverage(ref_items, tmp_yaml_files, COV_SIM_THRESHOLD)

                per_file_scores.append(float(cov_score))
                passed = cov_score >= WARN_THRESHOLD
                status = "pass" if passed else ("warn" if cov_score >= 0.5 else "fail")

                all_results.append({
                    "test_name": f"Coverage :: {yname}",
                    "category": "coverage",
                    "file": yfp,
                    "score": round(float(cov_score), 4),
                    "passed": bool(passed),
                    "status": status,
                    "reason": f"derived_from={df_hits} covered_items={sum(1 for d in cov_details if d['covered'])}/{len(cov_details)} (sim_th={COV_SIM_THRESHOLD})",
                    "duration_ms": 0,
                    "derived_from_context": df_hits,
                })

                per_file_details.append({
                    "file": yname,
                    "derived_from": derived_from_list(ydata),
                    "resolved_refs": df_hits,
                    "score": round(float(cov_score), 4),
                    "status": status,
                    "ref_items_count": len(ref_items),
                    "covered_count": sum(1 for d in cov_details if d["covered"]),
                    "items": cov_details[:min(len(cov_details), 60)],
                })

            global_score = (sum(per_file_scores) / len(per_file_scores)) if per_file_scores else 0.0
            global_passed = global_score >= WARN_THRESHOLD
            global_status = "pass" if global_passed else ("warn" if global_score >= 0.5 else "fail")

            all_results.append({
                "test_name": "Coverage :: GLOBAL",
                "category": "coverage",
                "file": YAML_DIR,
                "score": round(float(global_score), 4),
                "passed": bool(global_passed),
                "status": global_status,
                "reason": f"avg_of_files={len(per_file_scores)} (sim_th={COV_SIM_THRESHOLD})",
                "duration_ms": int((time.time() - start) * 1000),
            })

            details_meta["coverage"] = {
                "mode": "derived_from_per_file",
                "sim_threshold": COV_SIM_THRESHOLD,
                "skip_headings": COV_SKIP_HEADINGS,
                "max_items_per_file": COV_MAX_ITEMS,
                "min_item_len": COV_MIN_ITEM_LEN,
                "files": per_file_details[:min(len(per_file_details), 200)],
            }

            print(f"  [COVERAGE] global(avg) score={global_score:.3f}  files={len(per_file_scores)}/{len(yaml_files)}  status={global_status.upper()}")

    # 3) Completeness (derived_from 1:1 / per-file)
    if COMPLETENESS_ENABLE:
        print("\n[G4] ── Completeness（derived_from 単位）──")
        start = time.time()

        if not ref_text_map_for_rule:
            all_results.append({
                "test_name": "Completeness :: GLOBAL",
                "category": "completeness",
                "file": YAML_DIR,
                "score": 0.0,
                "passed": False,
                "status": "error",
                "reason": "No reference content available for completeness (ref_text_map_for_rule is empty).",
                "duration_ms": int((time.time() - start) * 1000),
            })
        else:
            per_file_scores: List[float] = []
            per_file_details: List[dict] = []

            for yfp, info in yaml_files.items():
                yname = Path(yfp).name
                ydata = info["data"]

                df_candidates = _derived_from_name_candidates(ydata)
                df_hits = [n for n in sorted(df_candidates) if n in ref_text_map_for_rule]

                if not df_hits:
                    all_results.append({
                        "test_name": f"Completeness :: {yname}",
                        "category": "completeness",
                        "file": yfp,
                        "score": 0.0,
                        "passed": False,
                        "status": "error",
                        "reason": f"derived_from が無い/参照に解決できません (derived_from={derived_from_list(ydata)})",
                        "duration_ms": 0,
                    })
                    per_file_details.append({
                        "file": yname,
                        "derived_from": derived_from_list(ydata),
                        "resolved_refs": [],
                        "status": "error",
                        "null_total": 0,
                        "suspicious": 0,
                        "items": [],
                    })
                    continue

                ref_blob = "\n\n".join(ref_text_map_for_rule[rn] for rn in df_hits)
                status, null_total, suspicious, details = completeness_check_one(ydata, ref_blob)

                if status == "pass":
                    score = 1.0
                    passed = True
                elif status == "warn":
                    score = 0.7
                    passed = False
                else:
                    score = 0.0
                    passed = False

                all_results.append({
                    "test_name": f"Completeness :: {yname}",
                    "category": "completeness",
                    "file": yfp,
                    "score": round(float(score), 4),
                    "passed": bool(passed),
                    "status": status,
                    "reason": f"null_total={null_total} suspicious_nulls={suspicious} (evidence_th={COMP_EVIDENCE_TH})",
                    "duration_ms": 0,
                    "derived_from_context": df_hits,
                })

                per_file_scores.append(float(score))
                per_file_details.append({
                    "file": yname,
                    "derived_from": derived_from_list(ydata),
                    "resolved_refs": df_hits,
                    "status": status,
                    "null_total": null_total,
                    "suspicious": suspicious,
                    "items": details,
                })

            global_score = (sum(per_file_scores) / len(per_file_scores)) if per_file_scores else 0.0
            global_passed = global_score >= WARN_THRESHOLD
            global_status = "pass" if global_passed else ("warn" if global_score >= 0.5 else "fail")

            all_results.append({
                "test_name": "Completeness :: GLOBAL",
                "category": "completeness",
                "file": YAML_DIR,
                "score": round(float(global_score), 4),
                "passed": bool(global_passed),
                "status": global_status,
                "reason": f"avg_of_files={len(per_file_scores)}",
                "duration_ms": int((time.time() - start) * 1000),
            })

            details_meta["completeness"] = {
                "mode": "derived_from_per_file",
                "evidence_threshold": COMP_EVIDENCE_TH,
                "warn_count": COMP_WARN_COUNT,
                "fail_count": COMP_FAIL_COUNT,
                "files": per_file_details[:min(len(per_file_details), 200)],
            }

            print(f"  [COMPLETENESS] global(avg) score={global_score:.3f}  files={len(per_file_scores)}/{len(yaml_files)}  status={global_status.upper()}")

    # 4) Global Consistency
    if CONSISTENCY_ENABLE:
        print("\n[G4] ── Global Consistency（横断）──")
        start = time.time()
        if not yaml_files:
            all_results.append({
                "test_name": "Consistency :: GLOBAL",
                "category": "consistency",
                "file": YAML_DIR,
                "score": 1.0,
                "passed": True,
                "status": "pass",
                "reason": "No YAML files to check.",
                "duration_ms": int((time.time() - start) * 1000),
            })
        else:
            cons_score, cons_details = compute_global_consistency(yaml_files, list(ref_text_map_for_rule.values()))
            passed = cons_score >= WARN_THRESHOLD
            status = "pass" if passed else ("warn" if cons_score >= 0.5 else "fail")

            all_results.append({
                "test_name": "Consistency :: GLOBAL",
                "category": "consistency",
                "file": YAML_DIR,
                "score": round(float(cons_score), 4),
                "passed": bool(passed),
                "status": status,
                "reason": f"contradictions={len(cons_details)}",
                "duration_ms": int((time.time() - start) * 1000),
            })

            details_meta["consistency"] = {
                "contradictions_count": len(cons_details),
                "ignore_keys": CONS_IGNORE_KEYS,
                "contradictions": cons_details[:min(len(cons_details), 200)],
            }
            print(f"  [CONSISTENCY] score={cons_score:.3f}  contradictions={len(cons_details)}  status={status.upper()}")

    meta = {
        "inputs": {
            "yaml_dir": YAML_DIR,
            "ref_inputs": REF_INPUTS,
            "ref_files": ref_files,
            "ref_mode": REF_MODE,
            "faithfulness_skip_all": FAITHFULNESS_SKIP_ALL,
            "faithfulness_skip_files": sorted(list(FAITHFULNESS_SKIP_FILES)),
            "skip_derived_from_scope": SKIP_DERIVED_SCOPE,
            "faithfulness_use_derived_from_context": USE_DERIVED_FROM_CONTEXT,
            "faithfulness_topk_ref_chunks": TOPK_REF_CHUNKS,
            "faithfulness_ref_chunk_max_chars": REF_CHUNK_MAX_CHARS,
            "faithfulness_actual_max_chars": FAITH_ACTUAL_MAX,
            "faithfulness_context_max_chars": FAITH_CTX_MAX,
            "faithfulness_truths_limit": FAITH_TRUTHS_LIM,
            "faithfulness_reason_mode": FAITH_REASON_MODE,
            "faithfulness_strip_top_keys": FAITH_STRIP_TOP_KEYS,
            "faithfulness_strip_anylevel_keys": sorted(list(FAITH_STRIP_ANYLEVEL_KEYS)),
            "faithfulness_prune_nulls": FAITH_PRUNE_NULLS,
            "faithfulness_prune_max_depth": FAITH_PRUNE_MAX_DEPTH,
            "faithfulness_noisy_ascii_scalar_maxlen": NOISY_ASCII_SCALAR_MAXLEN,
            "local_reason_topn": LOCAL_REASON_TOPN,
            "local_reason_sim_th": LOCAL_REASON_SIM_TH,
            "local_reason_min_len": LOCAL_REASON_MIN_LEN,
            "coverage_enable": COVERAGE_ENABLE,
            "completeness_enable": COMPLETENESS_ENABLE,
            "consistency_enable": CONSISTENCY_ENABLE,
        },
        "details": details_meta,
    }

    output = write_results(all_results, OUT_ROOT, meta)

    s = output["summary"]
    print(f"\n{'=' * 72}")
    print("[G4] SUMMARY")
    print(f"     Overall      : {s['overall_status'].upper()}  (total={s['total']}, passed={s['passed']}, failed={s['failed']})")
    fs = s["faithfulness"]
    print(f"     Faithfulness : avg={fs['avg_score']:.3f}  passed={fs['passed']}/{fs['total']}{' ⚠ WARNING' if fs['warning'] else ''}")
    cs = s["coverage"]
    print(f"     Coverage     : avg={cs['avg_score']:.3f}  passed={cs['passed']}/{cs['total']}{' ⚠ WARNING' if cs['warning'] else ''}")
    cps = s["completeness"]
    print(f"     Completeness : avg={cps['avg_score']:.3f}  passed={cps['passed']}/{cps['total']}{' ⚠ WARNING' if cps['warning'] else ''}")
    ks = s["consistency"]
    print(f"     Consistency  : avg={ks['avg_score']:.3f}  passed={ks['passed']}/{ks['total']}{' ⚠ WARNING' if ks['warning'] else ''}")
    print(f"\n[G4] Output : {output['_meta']['json_path']}")
    print(f"[G4] Allure : {output['_meta']['allure_dir']}")
    print(f"{'=' * 72}\n")

    sys.exit(0 if s["overall_status"] == "pass" else 1)


if __name__ == "__main__":
    main()
