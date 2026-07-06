#!/usr/bin/env python3
"""Build Photo AI landing page after VK data refresh.

The design lives in index.html. This builder only injects the fresh
vk_posts_all.json array into the `const ALL_POSTS = ...;` block, so nightly
auto-updates do not overwrite the premium layout/texts.
"""
from __future__ import annotations
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
POSTS_JSON = ROOT / "vk_posts_all.json"


def main() -> None:
    if not INDEX.exists():
        raise FileNotFoundError(INDEX)
    if not POSTS_JSON.exists():
        raise FileNotFoundError(POSTS_JSON)

    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))

    # Deduplicate by image while preserving order.
    seen = set()
    unique = []
    for post in posts:
        key = post.get("img") or f"{post.get('title','')}|{post.get('desc','')}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(post)

    POSTS_JSON.write_text(json.dumps(unique, ensure_ascii=False, indent=2), encoding="utf-8")

    html = INDEX.read_text(encoding="utf-8")
    new_block = "const ALL_POSTS = " + json.dumps(unique, ensure_ascii=False, separators=(",", ":")) + ";"
    html2, n = re.subn(r"const\s+ALL_POSTS\s*=\s*\[.*?\];", new_block, html, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("Could not find `const ALL_POSTS = [...]` in index.html")

    INDEX.write_text(html2, encoding="utf-8")
    print(f"Built index.html with {len(unique)} unique portfolio posts")


if __name__ == "__main__":
    main()
