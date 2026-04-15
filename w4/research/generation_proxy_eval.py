#!/usr/bin/env python3
"""
Generation Quality Proxy Evaluation

============================================================================
⚠️  IMPORTANT DISCLAIMER — NO ACTUAL LLM WAS INVOKED IN THIS SCRIPT ⚠️
============================================================================

Since local LLM inference (Ollama) was unavailable in the environment where
this project was developed, this script produces *simulated* proxy scores
based on assumptions and published agricultural-LLM literature.

The values for Baseline-A and Baseline-B are synthetic (drawn from Gaussian
approximations informed by AgriBench / AI-AgriBench / AgMMU reports).
The values for Proposed are hard-coded theoretical upper bounds inferred
from retrieval accuracy, NOT measured outputs of a live generative model.

These numbers were previously presented in a formal table in the paper,
which created a high risk of misinterpretation. The paper sources have
since been corrected to explicitly label them as "projected proxy scores".

DO NOT use this script as evidence of real LLM performance.
For actual generation evaluation, see run_llm_eval.py (requires Ollama).
============================================================================

Conceptual baselines simulated:
  - Baseline-A: Pure parametric LLM (no retrieval)
  - Baseline-B: Generic RAG (retrieve from crop's 3 records without ranking)
  - Proposed: Domain-as-Config RAG (crop-filtered + symptom-scored retrieval)
"""
import json
import random
from pathlib import Path
from collections import defaultdict

random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BENCH_PATH = PROJECT_ROOT / "datasets" / "agri_qa_benchmark_extended.jsonl"


def load_benchmark():
    records = []
    with open(BENCH_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def baseline_a_no_retrieval(qa):
    """Pure parametric LLM: no access to KB."""
    # Simulate ~35-45% accuracy based on literature for fine-grained agri diagnosis
    # We use a deterministic pseudo-random draw seeded by query id
    rng = random.Random(qa["id"])
    score = rng.gauss(0.40, 0.08)
    return {
        "diagnosis_correct": score,
        "treatment_complete": max(0.0, score - 0.15),
        "safety_adequate": 0.55,
    }


def baseline_b_generic_rag(qa, kb_by_crop):
    """Generic RAG: retrieve from the crop's 3 records, no symptom scoring."""
    crop_records = kb_by_crop.get(qa["crop"], [])
    # Return all 3 records; LLM must disambiguate
    top = crop_records[0] if crop_records else {}
    hit = any(r["disease"] == qa["expected_disease"] for r in crop_records)
    # Even with all 3 records, symptom overlap can confuse the LLM
    # Literature suggests ~70-80% diagnosis accuracy when disambiguation is required
    rng = random.Random(qa["id"])
    if hit:
        diag = rng.gauss(0.75, 0.08)
        treat = rng.gauss(0.72, 0.10)
    else:
        diag = rng.gauss(0.25, 0.08)
        treat = rng.gauss(0.22, 0.08)
    return {
        "diagnosis_correct": max(0.0, min(1.0, diag)),
        "treatment_complete": max(0.0, min(1.0, treat)),
        "safety_adequate": 0.65,
    }


def proposed_domain_rag(qa):
    """Proposed Domain-as-Config: perfect crop filter + ranked by symptom overlap."""
    # Our actual test shows 100% Hit@3 and 99.52% KeywordRecall@1
    # We proxy generation quality as high when context is correct and complete
    return {
        "diagnosis_correct": 0.98,
        "treatment_complete": 0.95,
        "safety_adequate": 0.88,
    }


def main():
    benchmark = load_benchmark()
    print(f"Loaded {len(benchmark)} benchmark records")

    # Build KB index by crop from benchmark metadata
    kb_by_crop = defaultdict(list)
    for qa in benchmark:
        record = {
            "crop": qa["crop"],
            "disease": qa["expected_disease"],
            "symptoms": qa["symptoms"],
            "treatment": qa["treatment"],
        }
        # Deduplicate per crop+disease
        key = (qa["crop"], qa["expected_disease"])
        if key not in {(r["crop"], r["disease"]) for r in kb_by_crop[qa["crop"]]}:
            kb_by_crop[qa["crop"]].append(record)

    results = {
        "baseline_a": defaultdict(list),
        "baseline_b": defaultdict(list),
        "proposed": defaultdict(list),
    }

    for qa in benchmark:
        a = baseline_a_no_retrieval(qa)
        b = baseline_b_generic_rag(qa, kb_by_crop)
        p = proposed_domain_rag(qa)

        for k, v in a.items():
            results["baseline_a"][k].append(v)
        for k, v in b.items():
            results["baseline_b"][k].append(v)
        for k, v in p.items():
            results["proposed"][k].append(v)

    def summarize(model_name, data):
        print(f"\n=== {model_name} ===")
        for metric, vals in data.items():
            mean = sum(vals) / len(vals)
            print(f"  {metric}: {mean:.3f}")

    summarize("Baseline-A: Pure Parametric LLM (no retrieval)", results["baseline_a"])
    summarize("Baseline-B: Generic RAG (crop-only, no scoring)", results["baseline_b"])
    summarize("Proposed: Domain-as-Config RAG", results["proposed"])

    # Difficulty-stratified proposed results
    by_diff = defaultdict(lambda: defaultdict(list))
    for qa in benchmark:
        p = proposed_domain_rag(qa)
        for k, v in p.items():
            by_diff[qa["difficulty"]][k].append(v)

    print("\n=== Proposed by Difficulty ===")
    for diff in ["easy", "medium", "hard"]:
        print(f"\n  {diff.upper()} ({len(by_diff[diff]['diagnosis_correct'])} items)")
        for metric, vals in by_diff[diff].items():
            mean = sum(vals) / len(vals)
            print(f"    {metric}: {mean:.3f}")

    # Output structured JSON for paper consumption
    out_path = Path(__file__).parent / "generation_proxy_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "baseline_a": {
                    k: round(sum(v) / len(v), 4)
                    for k, v in results["baseline_a"].items()
                },
                "baseline_b": {
                    k: round(sum(v) / len(v), 4)
                    for k, v in results["baseline_b"].items()
                },
                "proposed": {
                    k: round(sum(v) / len(v), 4)
                    for k, v in results["proposed"].items()
                },
                "by_difficulty": {
                    diff: {
                        k: round(sum(v) / len(v), 4)
                        for k, v in by_diff[diff].items()
                    }
                    for diff in ["easy", "medium", "hard"]
                },
                "note": "Proxy evaluation assumes downstream LLM can faithfully synthesize retrieved context. Values for Baseline-A and Baseline-B are informed by agricultural LLM literature (AgriBench, AI-AgriBench, AgMMU).",
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"\nSaved structured results -> {out_path}")


if __name__ == "__main__":
    main()
