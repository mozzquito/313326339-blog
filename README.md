# 313326339.xyz — Tech Digest Blog

Blog สรุป tech events และ tools สำหรับ community ไทย

## Stack

- **Astro** — static site generator
- **Cloudflare Pages** — hosting ฟรี
- **Claude API** — AI สรุปเนื้อหา

---

## Setup ครั้งแรก

```bash
npm install
npm run dev
# เปิด http://localhost:4321
```

---

## วิธีเพิ่ม post ใหม่

### Option A: ใช้ script (แนะนำ)

```bash
# ติดตั้ง dependency
pip install anthropic requests beautifulsoup4

# set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# สรุปจาก URL
python scripts/summarize.py \
  --url "https://aws.amazon.com/events/summits/bangkok/" \
  --title "AWS Summit Bangkok 2026" \
  --type event \
  --tags "aws,cloud,bangkok"

# สรุปจากข้อความ (copy มาจาก Facebook)
python scripts/summarize.py \
  --text "paste text here..." \
  --title "Cursor AI — features ใหม่" \
  --type tool \
  --tags "ai,coding,cursor"
```

### Option B: เขียนเอง

สร้างไฟล์ `src/pages/posts/YYYY-MM-DD-slug.md`:

```markdown
---
layout: ../../layouts/PostLayout.astro
title: "ชื่อ post"
date: "2026-01-01"
type: event          # หรือ tool
description: "สรุปสั้นๆ"
tags: [aws, cloud]
---

เนื้อหา...
```

---

## Deploy บน Cloudflare Pages

1. Push โค้ดขึ้น GitHub
2. เข้า [Cloudflare Dashboard](https://dash.cloudflare.com) → Pages → Create project
3. Connect GitHub repo นี้
4. ตั้งค่า:
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
5. กด Deploy
6. ไปที่ Pages → Custom domains → เพิ่ม `313326339.xyz`
7. Cloudflare จะ auto-configure DNS ให้

ครั้งต่อไปแค่ `git push` เว็บ update อัตโนมัติ ✅

---

## โครงสร้างโปรเจค

```
src/
  layouts/
    BaseLayout.astro    ← layout หลัก (header, footer)
    PostLayout.astro    ← layout สำหรับแต่ละ post
  pages/
    index.astro         ← หน้าแรก (list posts)
    posts/
      *.md              ← blog posts ทั้งหมด
scripts/
  summarize.py          ← AI summarizer
```
# 313326339-blog
