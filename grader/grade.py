"""Sandboxed auto-grader for PySecLabs capstones.

Runs a student's Python script inside a throwaway Docker network that can only see the
lab VM, then scores stdout against a YAML rubric.

Usage:
    python grader/grade.py student/port_scanner.py --rubric rubrics/port_scanner.yaml
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("pip install -r grader/requirements.txt  (needs pyyaml)")

LAB_NETWORK = "pyseclabs_lab"
IMAGE = "python:3.12-slim"


def run_in_sandbox(script: Path, timeout: int) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "submission.py"
        target.write_bytes(script.read_bytes())
        return subprocess.run(
            [
                "docker", "run", "--rm", "--network", LAB_NETWORK,
                "--read-only", "--cap-drop", "ALL",
                "--security-opt", "no-new-privileges",
                "-v", f"{tmp}:/work:ro", "-w", "/work",
                IMAGE, "python", "submission.py",
            ],
            capture_output=True, text=True, timeout=timeout,
        )


def score(rubric: dict, stdout: str, returncode: int) -> tuple[int, list[str]]:
    notes: list[str] = []
    points = 0
    for check in rubric["checks"]:
        kind, value, weight = check["type"], check["value"], check.get("points", 1)
        ok = {
            "contains": lambda: value in stdout,
            "line_count_at_least": lambda: len(stdout.splitlines()) >= value,
            "exit_zero": lambda: returncode == 0,
        }[kind]()
        if ok:
            points += weight
        else:
            notes.append(f"missing: {check['type']} {value!r} (-{weight})")
    return points, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("--rubric", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    rubric = yaml.safe_load(args.rubric.read_text())
    result = run_in_sandbox(args.script, args.timeout)
    points, notes = score(rubric, result.stdout, result.returncode)
    total = sum(c.get("points", 1) for c in rubric["checks"])
    print(json.dumps({
        "score": f"{points}/{total}",
        "percent": round(100 * points / total, 1),
        "notes": notes,
        "stdout_head": result.stdout[:400],
        "stderr_head": result.stderr[:400],
    }, indent=2))
    return 0 if points == total else 1


if __name__ == "__main__":
    sys.exit(main())
