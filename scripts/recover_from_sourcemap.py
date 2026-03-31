#!/usr/bin/env python3
import json
from pathlib import Path

MAP_PATH = Path("cli.js.map")
OUT_DIR = Path("recovered-src")

# Whether to restore only application source files
ONLY_SRC = True


def normalize_source_path(source: str) -> str:
    while source.startswith("../"):
        source = source[3:]
    return source.lstrip("/\\")


def is_safe_relative_path(path: str) -> bool:
    p = Path(path)
    return not any(part == ".." for part in p.parts)


def main() -> None:
    if not MAP_PATH.exists():
        raise FileNotFoundError(f"Source map not found: {MAP_PATH}")

    with MAP_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    sources = data.get("sources", [])
    sources_content = data.get("sourcesContent", [])

    if len(sources) != len(sources_content):
        raise ValueError(
            f"Length mismatch: sources={len(sources)} vs sourcesContent={len(sources_content)}"
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0

    for src, content in zip(sources, sources_content):
        if content is None:
            skipped += 1
            continue

        if ONLY_SRC and not src.startswith("../src/"):
            skipped += 1
            continue

        rel = normalize_source_path(src)
        if not is_safe_relative_path(rel):
            skipped += 1
            continue

        target = OUT_DIR / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written += 1

    print(f"Done. written={written}, skipped={skipped}, out_dir={OUT_DIR}")


if __name__ == "__main__":
    main()
