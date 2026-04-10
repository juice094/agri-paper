#!/usr/bin/env python3
"""Merge original 15 + extended 15 seed records and generate a 210-record QA benchmark."""
import json
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ORIGINAL_PATH = PROJECT_ROOT / "w3" / "engineer" / "agri_knowledge_base" / "agricultural_diseases.jsonl"
EXTENDED_PATH = PROJECT_ROOT / "w4" / "research" / "extended_diseases.jsonl"
OUTPUT_PATH = PROJECT_ROOT / "datasets" / "agri_qa_benchmark_extended.jsonl"


def load_jsonl(path: Path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def make_templates(record, idx):
    c, d, s, t = record["crop"], record["disease"], record["symptoms"], record["treatment"]
    templates = [
        {
            "query": f"My {c} shows {s.split(',')[0].lower()}. What disease could this be?",
            "type": "diagnosis_from_first_symptom",
            "difficulty": "easy",
        },
        {
            "query": f"I observed {s.lower()} on my {c}. How should I manage it?",
            "type": "diagnosis_and_management",
            "difficulty": "medium",
        },
        {
            "query": f"What are the typical symptoms of {d} in {c}?",
            "type": "symptom_recognition",
            "difficulty": "easy",
        },
        {
            "query": f"Which treatment options are recommended for {d} affecting {c}?",
            "type": "treatment_recall",
            "difficulty": "easy",
        },
        {
            "query": f"A farmer reports {s.split(',')[1].strip().lower()} and {s.split(',')[2].strip().lower()} in a {c} field. Diagnose the disease and suggest control measures.",
            "type": "multi_symptom_diagnosis",
            "difficulty": "medium",
        },
        {
            "query": f"How can I prevent or treat {d} in {c} cultivation?",
            "type": "prevention_and_treatment",
            "difficulty": "medium",
        },
        {
            "query": f"In the field, {c.lower()} plants exhibit {s.lower()}. Provide a diagnosis and actionable recommendations.",
            "type": "field_observation",
            "difficulty": "hard",
        },
    ]
    results = []
    for i, tmpl in enumerate(templates):
        qid = f"agri_qa_{idx:03d}_{i}"
        keywords = [kw.strip().lower() for kw in t.split(";")[:2]]
        results.append({
            "id": qid,
            "crop": c,
            "query": tmpl["query"],
            "expected_disease": d,
            "expected_keywords": keywords,
            "symptoms": s,
            "treatment": t,
            "type": tmpl["type"],
            "difficulty": tmpl["difficulty"],
        })
    return results


def main():
    random.seed(42)
    original = load_jsonl(ORIGINAL_PATH)
    extended = load_jsonl(EXTENDED_PATH)
    seeds = original + extended

    records = []
    for idx, r in enumerate(seeds):
        records.extend(make_templates(r, idx))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Generated {len(records)} QA records -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
