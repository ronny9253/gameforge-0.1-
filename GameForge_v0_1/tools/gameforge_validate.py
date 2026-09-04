#!/usr/bin/env python3
"""GameForge v0.1 deterministic project validator.

This validator intentionally checks project contracts before trying to validate
runtime behavior. It is the first executable brick of the GameForge factory.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXPECTED_DIRS = [
    "DESIGN",
    "AI/prompts",
    "AI/workflows",
    "AI/agents",
    "AI/scripts",
    "ASSET_FACTORY/raw",
    "ASSET_FACTORY/processed",
    "ASSET_FACTORY/approved",
    "ASSET_FACTORY/rejected",
    "UnityProject/Assets/GameForge/Core",
    "UnityProject/Assets/Game/Art",
    "UnityProject/Assets/Game/Audio",
    "UnityProject/Assets/Game/Scenes",
    "UnityProject/Assets/Game/Scripts",
    "UnityProject/Assets/Game/UI",
    "QA",
    "BUILD/Android",
    "BUILD/iOS",
    "BUILD/Store",
]


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:
        return None, str(exc)


def check(condition: bool, label: str, details: str = ""):
    return condition, label, details


def validate(root: Path):
    results = []
    results.append(check((root / "DESIGN/GAMEFORGE_SPEC_v0.1.md").is_file(), "Specification"))

    gm_path = root / "DESIGN/GAME_MANIFEST.json"
    am_path = root / "DESIGN/ASSET_MANIFEST.json"
    gm, gm_err = load_json(gm_path)
    am, am_err = load_json(am_path)
    results.append(check(gm is not None, "GAME_MANIFEST JSON", gm_err or ""))
    results.append(check(am is not None, "ASSET_MANIFEST JSON", am_err or ""))

    required_gm = ["schema_version","game_id","title","version","gameforge_version","genre","orientation","target_fps","supported_platforms","core_mechanic","max_complexity","scene_entry","status"]
    if gm is not None:
        missing = [k for k in required_gm if k not in gm]
        results.append(check(not missing, "GAME_MANIFEST required fields", f"missing: {', '.join(missing)}" if missing else ""))
        if not missing:
            results.append(check(gm["max_complexity"] == 1, "Complexity envelope", f"max_complexity={gm['max_complexity']}"))
            scene = root / "UnityProject" / gm["scene_entry"]
            results.append(check(scene.is_file(), "Entry scene", str(gm["scene_entry"])))
            results.append(check(all(p in {"android","ios"} for p in gm["supported_platforms"]), "Mobile platforms"))
            results.append(check(gm["target_fps"] in {30,60}, "Target FPS", str(gm["target_fps"])))

    if am is not None:
        results.append(check(am.get("schema_version") == "0.1", "ASSET_MANIFEST schema version"))
        results.append(check(isinstance(am.get("assets"), list), "ASSET_MANIFEST assets array"))
        bad_ids = []
        missing_assets = []
        for item in am.get("assets", []) if isinstance(am.get("assets"), list) else []:
            aid = item.get("id", "")
            path = item.get("path", "")
            approved = item.get("approved")
            if not re.fullmatch(r"[a-z0-9][a-z0-9_\-]*", aid):
                bad_ids.append(aid or "<missing>")
            if path:
                # asset paths are rooted at UnityProject, e.g. Assets/Game/...
                target = root / "UnityProject" / path
                if not target.exists():
                    missing_assets.append(path)
            if approved is True and not path:
                missing_assets.append(f"{aid}: approved asset has no path")
        results.append(check(not bad_ids, "Asset IDs", f"invalid: {', '.join(bad_ids)}" if bad_ids else ""))
        results.append(check(not missing_assets, "Asset paths", f"missing: {', '.join(missing_assets)}" if missing_assets else ""))

    for rel in EXPECTED_DIRS:
        results.append(check((root / rel).is_dir(), f"Directory: {rel}"))

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a GameForge v0.1 project")
    parser.add_argument("root", nargs="?", default=".", help="GameForge project root")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"ERROR: project root not found: {root}")
        return 2

    results = validate(root)
    passed = sum(ok for ok, _, _ in results)
    total = len(results)

    print("GAMEFORGE VALIDATION v0.1")
    print("=" * 32)
    for ok, label, details in results:
        status = "PASS" if ok else "FAIL"
        suffix = f" — {details}" if details else ""
        print(f"[{status}] {label}{suffix}")
    print("-" * 32)
    print(f"RESULT: {'PASS' if passed == total else 'FAIL'} ({passed}/{total})")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
