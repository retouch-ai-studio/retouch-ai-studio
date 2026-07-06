#!/usr/bin/env python3
"""Fetch latest public portfolio posts from VK group.

Requires a VK service token in GitHub Secrets as VK_SERVICE_TOKEN (or VK_TOKEN).
If the token is absent, the script exits successfully and keeps existing data —
this prevents nightly workflow failures while preserving the current site.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib
import json
import os
import re
import sys
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / "vk_posts_all.json"
ASSETS = ROOT / "assets" / "images"
ASSETS.mkdir(parents=True, exist_ok=True)

GROUP_ID = -239853638
API = "https://api.vk.com/method/wall.get"
VK_VERSION = "5.199"
MOSCOW = timezone(timedelta(hours=3))

CAT_PRESETS = {
    "retouch": ("#AIРетушь", "Естественная ретушь портрета", "AI-ретушь, цветокоррекция и аккуратное улучшение портрета с сохранением естественного лица."),
    "business": ("#БизнесПортрет", "Деловой портрет по фото", "Деловой бизнес-портрет для резюме, сайта или профиля: аккуратный фон, свет и профессиональный вид."),
    "neuro": ("#НейроОбраз", "AI-образ и нейро-аватар", "AI-стилизация по фотографии: выразительный образ для аватара, соцсетей или личного бренда."),
    "restoration": ("#Реставрация", "Реставрация старого фото", "Восстановление архивного снимка: удаление дефектов, повышение чёткости и деликатная обработка."),
}


def clean_text(s: str, limit: int = 220) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s[:limit].rstrip() if s else ""


def detect_cat(text: str) -> str:
    low = text.lower()
    if any(x in low for x in ["рестав", "стар", "архив", "колор"]):
        return "restoration"
    if any(x in low for x in ["бизнес", "делов", "резюме", "hh", "linkedin"]):
        return "business"
    if any(x in low for x in ["нейро", "аватар", "cinematic", "fashion", "fantasy", "cyber"]):
        return "neuro"
    return "retouch"


def best_photo_url(post: dict[str, Any]) -> str | None:
    for att in post.get("attachments", []) or []:
        if att.get("type") != "photo":
            continue
        sizes = att.get("photo", {}).get("sizes", [])
        if not sizes:
            continue
        best = max(sizes, key=lambda x: int(x.get("width", 0)) * int(x.get("height", 0)))
        if best.get("url"):
            return best["url"]
    return None


def download_image(url: str, post_id: int) -> str | None:
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        raw = r.content
        h = hashlib.sha1(raw).hexdigest()[:16]
        ext = "jpg"
        ctype = r.headers.get("content-type", "")
        if "png" in ctype:
            ext = "png"
        elif "webp" in ctype:
            ext = "webp"
        path = ASSETS / f"vk-{abs(GROUP_ID)}-{post_id}-{h}.{ext}"
        if not path.exists():
            path.write_bytes(raw)
        return f"assets/images/{path.name}"
    except Exception as e:
        print(f"Could not download image for post {post_id}: {e}")
        return None


def load_existing() -> list[dict[str, Any]]:
    if POSTS_JSON.exists():
        try:
            return json.loads(POSTS_JSON.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_merged(new_posts: list[dict[str, Any]], old_posts: list[dict[str, Any]]) -> None:
    merged = new_posts + old_posts
    seen = set()
    unique = []
    for p in merged:
        key = p.get("id") or p.get("img") or f"{p.get('title','')}|{p.get('desc','')}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)
    POSTS_JSON.write_text(json.dumps(unique, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(unique)} posts ({len(new_posts)} fetched from VK this run)")


def main() -> int:
    token = os.getenv("VK_SERVICE_TOKEN") or os.getenv("VK_TOKEN")
    old_posts = load_existing()
    if not token:
        print("VK_SERVICE_TOKEN is not set. Keeping existing vk_posts_all.json unchanged.")
        save_merged([], old_posts)
        return 0

    params = {
        "owner_id": GROUP_ID,
        "count": 100,
        "access_token": token,
        "v": VK_VERSION,
    }
    try:
        data = requests.get(API, params=params, timeout=30).json()
    except Exception as e:
        print(f"VK request failed: {e}")
        return 0

    if "error" in data:
        print("VK API error:", data["error"])
        return 0

    items = data.get("response", {}).get("items", [])
    new_posts = []
    for item in items:
        post_id = item.get("id")
        text = item.get("text", "")
        img = best_photo_url(item)
        if not post_id or not img:
            continue
        local_img = download_image(img, post_id)
        if not local_img:
            continue
        cat = detect_cat(text)
        tag, base_title, default_desc = CAT_PRESETS[cat]
        dt = datetime.fromtimestamp(item.get("date", 0), tz=MOSCOW)
        date_label = dt.strftime("%m.%Y")
        desc = clean_text(text) or default_desc
        new_posts.append({
            "id": f"post{GROUP_ID}_{post_id}",
            "title": f"{base_title} #{post_id}",
            "date": date_label,
            "cat": cat,
            "tag": tag,
            "desc": desc,
            "img": local_img,
            "vk_url": f"https://vk.com/wall{GROUP_ID}_{post_id}",
        })

    save_merged(new_posts, old_posts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
