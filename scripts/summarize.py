#!/usr/bin/env python3
"""
summarize.py — สรุป event/tool แล้วสร้างไฟล์ Markdown สำหรับ blog

Usage:
  python scripts/summarize.py --url "https://..." --type event --title "AWS Summit 2026" --tags "aws,cloud"
  python scripts/summarize.py --text "paste text here" --type tool --title "Cursor AI"

Requirements:
  pip install anthropic requests beautifulsoup4
"""

import anthropic
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_FETCH = True
except ImportError:
    HAS_FETCH = False


def fetch_url(url: str) -> str:
    """ดึง text จาก URL"""
    if not HAS_FETCH:
        print("⚠️  ติดตั้ง requests และ beautifulsoup4 ก่อน: pip install requests beautifulsoup4")
        sys.exit(1)
    r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)[:8000]


def summarize(content: str, title: str, content_type: str, client: anthropic.Anthropic) -> str:
    """เรียก Claude API เพื่อสรุป"""
    type_label = "event" if content_type == "event" else "tool/article"
    prompt = f"""คุณเป็น tech writer ภาษาไทย สรุป {type_label} นี้ให้เป็น blog post ภาษาไทยที่อ่านง่าย

ชื่อ: {title}

เนื้อหา:
{content}

---

สรุปเป็น Markdown (ไม่ต้องใส่ front matter) โดยมีหัวข้อ:
## Overview
## Highlight {"Sessions" if content_type == "event" else "Features"}
## สิ่งที่ takeaway กลับมาได้เลย
## สรุป (1-2 ประโยคสั้นๆ เป็น blockquote)

ใช้ภาษาไทยที่เป็นกันเอง อ่านง่าย ไม่ formal เกินไป"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:60]


def build_markdown(title: str, summary: str, content_type: str, tags: list[str], date: str) -> str:
    tags_str = str(tags).replace("'", '"')
    return f"""---
layout: ../../layouts/PostLayout.astro
title: "{title}"
date: "{date}"
type: {content_type}
description: ""
tags: {tags_str}
---

{summary}

---

*เขียนโดย Phongcheat — ถ้าชอบแชร์ต่อได้เลยครับ*
"""


def main():
    parser = argparse.ArgumentParser(description="สรุป event/tool เป็น blog post")
    parser.add_argument("--url", help="URL ที่จะดึงข้อมูล")
    parser.add_argument("--text", help="ข้อความที่จะสรุป")
    parser.add_argument("--title", required=True, help="ชื่อ post")
    parser.add_argument("--type", choices=["event", "tool"], default="event", help="ประเภท")
    parser.add_argument("--tags", default="", help="tags คั่นด้วย comma เช่น aws,cloud")
    parser.add_argument("--api-key", help="Anthropic API key (หรือใช้ env ANTHROPIC_API_KEY)")
    args = parser.parse_args()

    if not args.url and not args.text:
        print("❌ ต้องระบุ --url หรือ --text")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=args.api_key) if args.api_key else anthropic.Anthropic()

    print(f"🔍 กำลังประมวลผล: {args.title}")
    content = fetch_url(args.url) if args.url else args.text
    print("🤖 กำลังสรุปด้วย Claude...")
    summary = summarize(content, args.title, args.type, client)

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(args.title)
    filename = f"{date}-{slug}.md"

    output_dir = Path(__file__).parent.parent / "src" / "pages" / "posts"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename

    output_path.write_text(build_markdown(args.title, summary, args.type, tags, date), encoding="utf-8")
    print(f"✅ สร้างไฟล์แล้ว: src/pages/posts/{filename}")
    print(f"   → เปิด http://localhost:4321/posts/{date}-{slug}")


if __name__ == "__main__":
    main()
