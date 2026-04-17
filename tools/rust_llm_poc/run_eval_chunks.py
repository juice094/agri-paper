#!/usr/bin/env python3
"""Run agri-paper eval in small chunks to avoid background-task heartbeat timeout.

Each chunk runs 5 samples (~12-15 min on RTX 4060 7B Q4).
The script prints a heartbeat every 30s while waiting for eval.exe.
"""
import json
import subprocess
import sys
import time
from pathlib import Path
from threading import Thread

EVAL_EXE = Path(r"C:\Users\22414\Desktop\agri-paper\tools\rust_llm_poc\target\release\eval.exe")
OUT_DIR = Path(r"C:\Users\22414\Desktop\agri-paper\w4\research")
CHUNK_SIZE = 5
TOTAL_SAMPLES = 80
ENV = {"CUDNN_LIB": r"C:\Users\22414\cudnn_stub"}

# Force unbuffered stdout so background task heartbeat sees our prints
import sys, os
os.environ["PYTHONUNBUFFERED"] = "1"
sys.stdout.reconfigure(line_buffering=True)

def run_chunk(offset: int, limit: int) -> Path:
    cmd = [str(EVAL_EXE), "--offset", str(offset), "--limit", str(limit)]
    print(f"\n[Chunk] Starting offset={offset} limit={limit}")
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env={**dict(subprocess.os.environ), **ENV},
    )

    alive = True
    def heartbeat():
        while alive:
            time.sleep(30)
            if alive:
                print(f"  ... heartbeat: chunk offset={offset} still running ...")

    hb = Thread(target=heartbeat)
    hb.start()

    for line in proc.stdout:
        print(line, end="")

    alive = False
    hb.join()
    proc.wait()

    if proc.returncode != 0:
        print(f"[Chunk] WARNING: exit code {proc.returncode}", file=sys.stderr)
    else:
        print(f"[Chunk] Completed offset={offset} limit={limit}")

    # Discover output file created by this chunk
    candidates = sorted(OUT_DIR.glob(f"llm_eval_raw_*_{offset}_{offset + limit}.jsonl"), key=lambda p: p.stat().st_mtime)
    if candidates:
        return candidates[-1]
    return None

def merge_and_summarize():
    raw_files = sorted(OUT_DIR.glob("llm_eval_raw_*_*.jsonl"))
    if not raw_files:
        print("No raw files found.")
        return

    all_records = []
    for f in raw_files:
        with open(f) as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                try:
                    all_records.append(json.loads(line))
                except json.JSONDecodeError:
                    break

    merged_path = OUT_DIR / "llm_eval_raw_merged.jsonl"
    with open(merged_path, "w") as fp:
        for r in all_records:
            fp.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nMerged {len(all_records)} records into {merged_path}")

    # Summary
    scores_by_condition = {}
    for r in all_records:
        cond = r["condition"]
        scores_by_condition.setdefault(cond, []).append(r["cpj_score"])

    summary = {}
    for cond, scores in scores_by_condition.items():
        n = len(scores)
        summary[cond] = {
            "count": n,
            "avg_plant": round(sum(s["plant_accuracy"] for s in scores) / n, 3),
            "avg_disease": round(sum(s["disease_accuracy"] for s in scores) / n, 3),
            "avg_symptom": round(sum(s["symptom_accuracy"] for s in scores) / n, 3),
            "avg_format": round(sum(s["format_adherence"] for s in scores) / n, 3),
            "avg_completeness": round(sum(s["completeness"] for s in scores) / n, 3),
            "avg_total": round(sum(s["total"] for s in scores) / n, 3),
        }

    summary_path = OUT_DIR / "llm_eval_summary_merged.json"
    with open(summary_path, "w") as fp:
        json.dump(summary, fp, indent=2, ensure_ascii=False)
    print(f"Summary saved to {summary_path}")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

def main():
    # Determine resume point by inspecting existing raw files
    existing = sorted(OUT_DIR.glob("llm_eval_raw_*_*.jsonl"))
    completed_offsets = set()
    for f in existing:
        parts = f.stem.split("_")
        if len(parts) >= 4 and parts[-2].isdigit() and parts[-1].isdigit():
            o = int(parts[-2])
            e = int(parts[-1])
            # validate file has roughly (e-o)*3 lines
            with open(f) as fp:
                valid = 0
                for line in fp:
                    line=line.strip()
                    if not line: continue
                    try:
                        json.loads(line)
                        valid += 1
                    except:
                        break
            if valid >= (e - o) * 3 - 2:  # allow 1 incomplete sample
                for i in range(o, e):
                    completed_offsets.add(i)

    offsets_to_run = [i for i in range(0, TOTAL_SAMPLES) if i not in completed_offsets]
    print(f"Resuming: {len(completed_offsets)} samples already done, {len(offsets_to_run)} remaining.")

    for i in range(0, len(offsets_to_run), CHUNK_SIZE):
        chunk_offsets = offsets_to_run[i:i + CHUNK_SIZE]
        offset = chunk_offsets[0]
        limit = chunk_offsets[-1] - offset + 1
        run_chunk(offset, limit)

    merge_and_summarize()

if __name__ == "__main__":
    main()
