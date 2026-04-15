#!/usr/bin/env python3
"""
Real LLM generation evaluation for agri-paper.

Requires a running Ollama instance with a pulled model (e.g. qwen2.5:7b).

Usage:
  1. Install Ollama: https://ollama.com/download/windows
  2. ollama pull qwen2.5:7b
  3. python w4/research/run_llm_eval.py
"""
import json
import random
import sys
import time
from pathlib import Path
from collections import defaultdict

import urllib.request
import urllib.error

# =============================================================================
# Configuration
# =============================================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
BENCH_PATH = PROJECT_ROOT / "datasets" / "agri_qa_benchmark_extended.jsonl"
KB_PATH = PROJECT_ROOT / "w3" / "engineer" / "agri_knowledge_base" / "agricultural_diseases_all.jsonl"
OUTPUT_DIR = Path(__file__).resolve().parent

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"
TEMPERATURE = 0.3

SAMPLE_SIZE = {"easy": 30, "medium": 30, "hard": 20}

SAFETY_BLACKLIST = [
    "gasoline", "bleach", "kerosene", "diesel", "burn the field",
    "ignore the problem", "do nothing", "toxic chemical"
]

# =============================================================================
# Helpers
# =============================================================================

def load_jsonl(path: Path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def check_ollama():
    """Check whether Ollama is reachable and the model is available."""
    try:
        req = urllib.request.Request(
            OLLAMA_URL.replace("/api/generate", "/api/tags"),
            method="GET",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m["name"] for m in data.get("models", [])]
            if MODEL not in models:
                print(f"ERROR: Ollama is running but model '{MODEL}' is not pulled.")
                print(f"Available models: {models}")
                print(f"Run: ollama pull {MODEL}")
                sys.exit(1)
            return True
    except urllib.error.URLError as e:
        print(f"ERROR: Cannot connect to Ollama at {OLLAMA_URL}")
        print(f"Detail: {e}")
        print("Please ensure Ollama is installed and running:")
        print("  1. https://ollama.com/download/windows")
        print(f"  2. ollama pull {MODEL}")
        print(f"  3. ollama run {MODEL}   # or just keep the service running")
        sys.exit(1)


def ollama_generate(prompt: str) -> str:
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": 512,
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("response", "").strip()


def build_prompt(query: str, context: str) -> str:
    return (
        "You are an agricultural extension officer. A farmer asks:\n\n"
        f'"{query}"\n\n'
        "Use the following retrieved knowledge to answer:\n\n"
        f"{context}\n\n"
        "Provide a concise diagnosis and actionable management recommendations. "
        "If the context does not contain enough information, say so."
    )


def score_answer(answer: str, expected_disease: str, expected_keywords: list):
    ans_lower = answer.lower()
    diag = 1.0 if expected_disease.lower() in ans_lower else 0.0

    keyword_hits = sum(1 for kw in expected_keywords if kw.lower() in ans_lower)
    treat = keyword_hits / max(len(expected_keywords), 1)

    safe = 1.0
    for phrase in SAFETY_BLACKLIST:
        if phrase in ans_lower:
            safe = 0.0
            break

    return {
        "diagnosis_correct": diag,
        "treatment_complete": treat,
        "safety_adequate": safe,
    }


def token_overlap_score(query: str, record: dict) -> float:
    """Lightweight token overlap for symptom ranking (matches test logic)."""
    query_tokens = set(query.lower().split())
    sym_tokens = set(record.get("symptoms", "").lower().split())
    treat_tokens = set(record.get("treatment", "").lower().split())
    if not query_tokens:
        return 0.0
    overlap = len(query_tokens & sym_tokens) + 0.5 * len(query_tokens & treat_tokens)
    return overlap


def retrieve_baseline_a(_qa, _kb):
    return "No retrieved context available."


def retrieve_baseline_b(qa, kb):
    crop = qa["crop"]
    records = [r for r in kb if r.get("crop") == crop]
    if not records:
        return "No retrieved context available."
    lines = []
    for r in records:
        lines.append(f"- {r['disease']}: {r['symptoms']} Treatment: {r['treatment']}")
    return "\n".join(lines)


def retrieve_proposed(qa, kb):
    crop = qa["crop"]
    records = [r for r in kb if r.get("crop") == crop]
    if not records:
        return "No retrieved context available."
    ranked = sorted(records, key=lambda r: token_overlap_score(qa["query"], r), reverse=True)
    top = ranked[0]
    return f"- {top['disease']}: {top['symptoms']} Treatment: {top['treatment']}"


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 60)
    print("agri-paper Real LLM Generation Evaluation")
    print("=" * 60)

    check_ollama()
    print(f"Model '{MODEL}' is available.\n")

    benchmark = load_jsonl(BENCH_PATH)
    kb = load_jsonl(KB_PATH)
    print(f"Loaded {len(benchmark)} benchmark records")
    print(f"Loaded {len(kb)} knowledge-base records\n")

    # Stratified sampling
    by_diff = defaultdict(list)
    for rec in benchmark:
        by_diff[rec["difficulty"]].append(rec)

    sampled = []
    for diff, count in SAMPLE_SIZE.items():
        pool = by_diff.get(diff, [])
        if len(pool) < count:
            print(f"WARNING: only {len(pool)} {diff} items available, using all.")
            sampled.extend(pool)
        else:
            sampled.extend(random.sample(pool, count))
    random.shuffle(sampled)
    print(f"Sampled {len(sampled)} records for evaluation\n")

    conditions = {
        "baseline_a": retrieve_baseline_a,
        "baseline_b": retrieve_baseline_b,
        "proposed": retrieve_proposed,
    }

    results = {name: [] for name in conditions}
    raw_outputs = {name: [] for name in conditions}

    total = len(sampled) * len(conditions)
    done = 0

    for qa in sampled:
        qid = qa["id"]
        for cond_name, retrieve_fn in conditions.items():
            context = retrieve_fn(qa, kb)
            prompt = build_prompt(qa["query"], context)

            try:
                answer = ollama_generate(prompt)
            except Exception as e:
                print(f"\nERROR generating for {qid} [{cond_name}]: {e}")
                answer = ""

            scores = score_answer(answer, qa["expected_disease"], qa["expected_keywords"])

            record = {
                "id": qid,
                "condition": cond_name,
                "crop": qa["crop"],
                "difficulty": qa["difficulty"],
                "expected_disease": qa["expected_disease"],
                "scores": scores,
                "prompt": prompt,
                "answer": answer,
            }
            results[cond_name].append(record)
            raw_outputs[cond_name].append({
                "id": qid,
                "query": qa["query"],
                "answer": answer,
                "scores": scores,
            })

            done += 1
            print(f"Progress: {done}/{total} ({cond_name} / {qid})", end="\r")
            time.sleep(0.5)  # Be gentle to local CPU

    print("\n")

    # Summarize
    summary = {}
    for cond_name, records in results.items():
        metrics = defaultdict(list)
        for r in records:
            for k, v in r["scores"].items():
                metrics[k].append(v)
        summary[cond_name] = {
            k: round(sum(v) / len(v), 4) if v else 0.0
            for k, v in metrics.items()
        }

    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    for cond_name, scores in summary.items():
        print(f"\n{cond_name}:")
        for metric, val in scores.items():
            print(f"  {metric}: {val:.4f}")

    # Difficulty-stratified proposed results
    proposed_by_diff = defaultdict(lambda: defaultdict(list))
    for r in results["proposed"]:
        for k, v in r["scores"].items():
            proposed_by_diff[r["difficulty"]][k].append(v)

    print("\nproposed by difficulty:")
    for diff in ["easy", "medium", "hard"]:
        print(f"\n  {diff.upper()}:")
        for metric, vals in proposed_by_diff[diff].items():
            print(f"    {metric}: {sum(vals)/len(vals):.4f}")

    # Save outputs
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_path = OUTPUT_DIR / f"llm_eval_results_{timestamp}.json"
    raw_path = OUTPUT_DIR / f"llm_eval_raw_{timestamp}.jsonl"

    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "model": MODEL,
                "temperature": TEMPERATURE,
                "sample_size": SAMPLE_SIZE,
                "summary": summary,
                "by_difficulty": {
                    diff: {k: round(sum(v)/len(v), 4) for k, v in proposed_by_diff[diff].items()}
                    for diff in ["easy", "medium", "hard"]
                },
                "disclaimer": "This evaluation uses a locally quantized LLM (Ollama). Results should be interpreted as indicative rather than definitive.",
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    with open(raw_path, "w", encoding="utf-8") as f:
        for cond_name, records in raw_outputs.items():
            for rec in records:
                f.write(json.dumps({"condition": cond_name, **rec}, ensure_ascii=False) + "\n")

    print(f"\nSaved summary -> {results_path}")
    print(f"Saved raw outputs -> {raw_path}")


if __name__ == "__main__":
    main()
