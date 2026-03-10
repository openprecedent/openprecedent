#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="check-branch-freshness")
    parser.add_argument("--base-ref", default="upstream/main")
    parser.add_argument("--allow-missing-base-ref", action="store_true")
    return parser


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], check=False, capture_output=True, text=True)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    verify = _git("rev-parse", "--verify", args.base_ref)
    if verify.returncode != 0:
        if args.allow_missing_base_ref:
            print(f"Skipping branch freshness check: base ref {args.base_ref} is unavailable")
            return 0
        print(f"Branch freshness check failed: base ref {args.base_ref} is unavailable")
        return 1

    contains = _git("merge-base", "--is-ancestor", args.base_ref, "HEAD")
    if contains.returncode == 0:
        print(f"Branch freshness check passed: HEAD contains {args.base_ref}")
        return 0

    print(
        f"Branch freshness check failed: current branch does not contain the latest {args.base_ref}. "
        "Rebase onto the latest upstream/main before pushing."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
