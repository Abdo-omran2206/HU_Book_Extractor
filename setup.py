"""
HU Book — install dependencies and Playwright Chromium, or install as a package.

  python setup.py              # pip install -e . + playwright install chromium
  pip install -e .             # editable install (deps only; run Playwright step separately)
"""

from __future__ import annotations

import os
import subprocess
import sys

from setuptools import find_packages, setup

ROOT = os.path.dirname(os.path.abspath(__file__))


def read_requirements() -> list[str]:
    path = os.path.join(ROOT, "requirements.txt")
    with open(path, encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def bootstrap() -> None:
    print("Installing HU Book (editable) and Playwright Chromium…")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-e", ROOT],
        cwd=ROOT,
    )
    subprocess.check_call(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        cwd=ROOT,
    )
    print("Done. Run: python main.py")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        setup(
            name="hubook",
            version="0.1.0",
            description="HU Book — extract web-hosted EPUB-style books to a single PDF",
            packages=find_packages(include=["lib"]),
            python_requires=">=3.10",
            install_requires=read_requirements(),
        )
    else:
        bootstrap()
