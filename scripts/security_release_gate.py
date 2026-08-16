from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

SRC = ROOT / "src"


@dataclass(frozen=True)
class GateResult:
    name: str
    passed: bool
    detail: str


def tracked_files() -> list[str]:
    completed = subprocess.run(
        [
            "git",
            "ls-files",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    return [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip()
    ]


def source_text() -> str:
    pieces: list[str] = []

    for path in SRC.rglob("*.py"):
        pieces.append(
            path.read_text(
                encoding="utf-8"
            )
        )

    return "\n".join(
        pieces
    )


def check_no_private_keys_tracked() -> GateResult:
    files = tracked_files()

    bad = [
        file
        for file in files
        if file.endswith(".p8")
    ]

    return GateResult(
        name="No Apple private keys tracked",
        passed=not bad,
        detail=(
            "PASS"
            if not bad
            else f"Tracked: {bad}"
        ),
    )


def check_no_runtime_database_tracked() -> GateResult:
    files = tracked_files()

    bad = [
        file
        for file in files
        if (
            file.endswith(".db")
            or file.endswith(".db-wal")
            or file.endswith(".db-shm")
        )
    ]

    return GateResult(
        name="No runtime databases tracked",
        passed=not bad,
        detail=(
            "PASS"
            if not bad
            else f"Tracked: {bad}"
        ),
    )


def check_no_obvious_execution_primitives() -> GateResult:
    text = source_text()

    patterns = {
        "eval(": r"\beval\s*\(",
        "exec(": r"\bexec\s*\(",
        "os.system(": r"\bos\.system\s*\(",
        "subprocess.run(": r"\bsubprocess\.run\s*\(",
        "subprocess.Popen(": r"\bsubprocess\.Popen\s*\(",
    }

    hits: list[str] = []

    for label, pattern in patterns.items():
        if re.search(
            pattern,
            text,
        ):
            hits.append(
                label
            )

    return GateResult(
        name="No unknown-code execution path",
        passed=not hits,
        detail=(
            "PASS"
            if not hits
            else (
                "Review required: "
                + ", ".join(hits)
            )
        ),
    )


def check_pairing_tokens_not_plaintext_in_schema() -> GateResult:
    candidates = list(
        SRC.rglob(
            "*.py"
        )
    )

    schema_text = "\n".join(
        path.read_text(
            encoding="utf-8"
        )
        for path in candidates
        if "registry" in path.name
    )

    has_hash = (
        "token_hash"
        in schema_text
    )

    return GateResult(
        name="Pairing token hashing present",
        passed=has_hash,
        detail=(
            "PASS"
            if has_hash
            else "token_hash not found"
        ),
    )


def check_learning_profile_separation() -> GateResult:
    learning_dir = (
        SRC
        / "code2plain"
        / "learning"
    )

    text = "\n".join(
        path.read_text(
            encoding="utf-8"
        )
        for path in learning_dir.rglob(
            "*.py"
        )
    )

    forbidden = [
        "phone_number",
        "apns_token",
        "ntfy_topic",
        "source_code",
    ]

    hits = [
        value
        for value in forbidden
        if value in text
    ]

    return GateResult(
        name="Learning profile privacy separation",
        passed=not hits,
        detail=(
            "PASS"
            if not hits
            else (
                "Unexpected fields: "
                + ", ".join(hits)
            )
        ),
    )


def main() -> None:
    checks = [
        check_no_private_keys_tracked(),
        check_no_runtime_database_tracked(),
        check_no_obvious_execution_primitives(),
        check_pairing_tokens_not_plaintext_in_schema(),
        check_learning_profile_separation(),
    ]

    print()
    print(
        "========================================"
    )
    print(
        " CODE2PLAIN SECURITY RELEASE GATE"
    )
    print(
        "========================================"
    )
    print()

    for check in checks:
        marker = (
            "PASS"
            if check.passed
            else "FAIL"
        )

        print(
            f"[{marker}] {check.name}"
        )

        print(
            f"       {check.detail}"
        )

    failed = [
        check
        for check in checks
        if not check.passed
    ]

    print()

    if failed:
        print(
            "PERSONAL BETA RELEASE GATE: FAIL"
        )

        raise SystemExit(
            1
        )

    print(
        "PERSONAL BETA RELEASE GATE: PASS"
    )

    print()
    print(
        "Public/commercial production "
        "security is NOT implied."
    )


if __name__ == "__main__":
    main()
