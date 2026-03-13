from __future__ import annotations

import os
import subprocess
from pathlib import Path


def resolve_openprecedent_bin(root_dir: Path, explicit: str | None = None) -> str:
    if explicit:
        return explicit

    env_value = os.environ.get("OPENPRECEDENT_BIN")
    if env_value:
        return env_value

    release_candidate = root_dir / "target" / "release" / "openprecedent"
    if release_candidate.exists():
        return str(release_candidate)

    debug_candidate = root_dir / "target" / "debug" / "openprecedent"
    if debug_candidate.exists():
        return str(debug_candidate)

    subprocess.run(
        ["cargo", "build", "-q", "-p", "openprecedent-cli", "--manifest-path", str(root_dir / "Cargo.toml")],
        check=True,
        capture_output=True,
        text=True,
    )
    return str(debug_candidate)
