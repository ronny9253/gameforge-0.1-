#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path

REQUIRED = [
    "task_id","title","objective","scope","requirements","constraints",
    "dependencies","allowed_paths","forbidden_paths","acceptance_criteria",
    "tests","expected_outputs"
]

def fail(msg):
    print(f"[FAIL] {msg}")
    return 1

def main():
    if len(sys.argv) != 2:
        print("Usage: task_validate.py <task.json>")
        return 2
    p = Path(sys.argv[1])
    if not p.is_file():
        return fail(f"task not found: {p}")
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return fail(f"invalid JSON: {e}")
    missing = [k for k in REQUIRED if k not in d]
    if missing:
        return fail("missing fields: " + ", ".join(missing))
    if not re.fullmatch(r"TASK-\d{3}", d["task_id"]):
        return fail("task_id must match TASK-001 format")
    for k in REQUIRED:
        if k == "dependencies":
            if not isinstance(d[k], list):
                return fail("field must be a list: dependencies")
            continue
        if k != "task_id" and (not isinstance(d[k], (list, str)) or len(d[k]) == 0):
            return fail(f"field must be non-empty: {k}")
    allowed = set(d["allowed_paths"])
    forbidden = set(d["forbidden_paths"])
    overlap = allowed & forbidden
    if overlap:
        return fail("path appears in both allowed and forbidden: " + ", ".join(sorted(overlap)))
    print("GAMEFORGE TASK VALIDATION v0.1")
    print("=" * 34)
    print(f"[PASS] {d['task_id']} — {d['title']}")
    print("[PASS] Required contract fields")
    print("[PASS] Task ID format")
    print("[PASS] Non-empty task sections")
    print("[PASS] Allowed/forbidden paths do not overlap")
    print("-" * 34)
    print("RESULT: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
