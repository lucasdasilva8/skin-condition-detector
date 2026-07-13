#!/usr/bin/env python3
"""Fetch skin-care articles from trusted RSS feeds and update frontend/blog/posts.json.

Run manually:  python scripts/update_blog.py
Automated:     GitHub Action every 2 weeks (.github/workflows/update-blog.yml)
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "frontend" / "blog" / "posts.json"
MAX_POSTS = 24

SKIN_KEYWORDS = re.compile(
    r"\b(skin|dermatolog|melanoma|sunscreen|sunburn|eczema|psoriasis|acne|"
    r"rash|mole|uv|ultraviolet|keratosis|carcinoma|lesion|vitiligo|rosacea|"
    r"dermatitis|wart|tinea|fungal|itch|pigment)\b",
    re.I,
)

RSS_FEEDS = [
    {
        "url": "https://www.skincancer.org/feed/",
        "source": "Skin Cancer Foundation",
        "domain": "skincancer.org",
        "default_category": "advice",
    },
    {
        "url": "https://medlineplus.gov/groupfeeds/new.xml",
        "source": "MedlinePlus (NIH)",
        "domain": "medlineplus.gov",
        "default_category": "study",
    },
]

HARVARD_BLOG = {
    "url": "https://www.health.harvard.edu/blog",
    "source": "Harvard Health Publishing",
    "domain": "health.harvard.edu",
    "default_category": "advice",
}

CATEGORY_HINTS = [
    (re.compile(r"\b(study|research|trial|findings|journal|published)\b", re.I), "study"),
    (re.compile(r"\b(should|recommend|tips|how to|guide|prevention|protect)\b", re.I), "advice"),
]


def strip_html(text: str) -> str:
    text = unescape(re.sub(r"<[^>]+>", " ", text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s*The post .* appeared first on .*", "", text, flags=re.I)
    return text.strip()


def classify(title: str, summary: str, default: str) -> str:
    blob = f"{title} {summary}"
    for pattern, category in CATEGORY_HINTS:
        if pattern.search(blob):
            return category
    return default


def parse_date(item) -> str:
    for tag in ("pubDate", "published", "updated", "dc:date"):
        el = item.find(tag)
        if el is None and tag == "dc:date":
            el = item.find("{http://purl.org/dc/elements/1.1/}date")
        if el is not None and el.text:
            try:
                return parsedate_to_datetime(el.text.strip()).date().isoformat()
            except (TypeError, ValueError, OverflowError):
                pass
            text = el.text.strip()[:10]
            if re.match(r"\d{4}-\d{2}-\d{2}", text):
                return text
    return datetime.now(timezone.utc).date().isoformat()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:80] or "post"


def fetch_url(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "SkinScan-BlogUpdater/1.0"})
    with urlopen(req, timeout=30) as resp:
        return resp.read()


def fetch_harvard_blog() -> list[dict]:
    """Harvard Health no longer publishes RSS; scrape the blog index instead."""
    posts = []
    try:
        html = fetch_url(HARVARD_BLOG["url"]).decode("utf-8", errors="replace")
    except Exception as exc:
        print(f"Skip {HARVARD_BLOG['url']}: {exc}")
        return posts

    links = []
    for match in re.finditer(
        r'href="(https://www\.health\.harvard\.edu/blog/[^"#?]+)"', html
    ):
        url = match.group(1).rstrip("/")
        if url not in links:
            links.append(url)

    for url in links[:15]:
        slug = url.rsplit("/", 1)[-1]

        try:
            article_html = fetch_url(url).decode("utf-8", errors="replace")
        except Exception:
            continue

        title_match = re.search(
            r'<script type="application/ld\+json">(.*?)</script>',
            article_html,
            re.S,
        )
        title = ""
        published = datetime.now(timezone.utc).date().isoformat()
        if title_match:
            try:
                data = json.loads(title_match.group(1))
                nodes = data.get("@graph", [data]) if isinstance(data, dict) else []
                for node in nodes:
                    if isinstance(node, dict) and node.get("@type") == "Article":
                        title = node.get("headline", "")
                        if node.get("datePublished"):
                            published = node["datePublished"][:10]
                        break
            except json.JSONDecodeError:
                pass

        if not title:
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", article_html, re.S)
            title = strip_html(h1.group(1)) if h1 else slug.replace("-", " ").title()

        meta = re.search(
            r'<meta (?:name="description"|property="og:description") content="([^"]+)"',
            article_html,
        )
        summary = strip_html(meta.group(1)) if meta else title
        if len(summary) > 280:
            summary = summary[:277].rstrip() + "…"

        if not SKIN_KEYWORDS.search(f"{title} {summary}"):
            continue

        posts.append(
            {
                "id": slugify(title),
                "title": title,
                "summary": summary,
                "url": url,
                "source": HARVARD_BLOG["source"],
                "domain": HARVARD_BLOG["domain"],
                "category": classify(title, summary, HARVARD_BLOG["default_category"]),
                "published": published,
            }
        )

    return posts


def fetch_rss(feed: dict) -> list[dict]:
    posts = []
    try:
        root = ET.fromstring(fetch_url(feed["url"]))
    except Exception as exc:
        print(f"Skip {feed['url']}: {exc}")
        return posts

    items = root.findall(".//item")
    if not items:
        items = root.findall(".//{http://www.w3.org/2005/Atom}entry")

    for item in items:
        title_el = item.find("title")
        if title_el is None:
            title_el = item.find("{http://www.w3.org/2005/Atom}title")
        link_el = item.find("link")
        if link_el is None:
            link_el = item.find("{http://www.w3.org/2005/Atom}link")
        if title_el is None:
            continue

        title = strip_html(title_el.text or "")
        url = ""
        if link_el is not None:
            url = (link_el.text or link_el.get("href") or "").strip()
        if not title or not url:
            continue

        desc_el = item.find("description")
        if desc_el is None:
            desc_el = item.find("{http://purl.org/rss/1.0/modules/content/}encoded")
        if desc_el is None:
            desc_el = item.find("{http://www.w3.org/2005/Atom}summary")
        summary = strip_html(desc_el.text if desc_el is not None else title)
        if len(summary) > 280:
            summary = summary[:277].rstrip() + "…"

        blob = f"{title} {summary}"
        if not SKIN_KEYWORDS.search(blob):
            continue

        posts.append(
            {
                "id": slugify(title),
                "title": title,
                "summary": summary,
                "url": url,
                "source": feed["source"],
                "domain": feed["domain"],
                "category": classify(title, summary, feed["default_category"]),
                "published": parse_date(item),
            }
        )
    return posts


def dedupe_posts(posts: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for post in sorted(posts, key=lambda p: p["published"], reverse=True):
        key = post["url"].lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(post)
    return unique[:MAX_POSTS]


def load_existing() -> list[dict]:
    if not OUTPUT.exists():
        return []
    data = json.loads(OUTPUT.read_text(encoding="utf-8"))
    return data.get("posts", [])


def main() -> None:
    fetched: list[dict] = []
    for feed in RSS_FEEDS:
        items = fetch_rss(feed)
        print(f"{feed['domain']}: {len(items)} skin-related items")
        fetched.extend(items)

    harvard = fetch_harvard_blog()
    print(f"{HARVARD_BLOG['domain']}: {len(harvard)} skin-related items")
    fetched.extend(harvard)

    merged = dedupe_posts(fetched + load_existing())
    if not merged:
        print("No posts found — keeping existing file unchanged.")
        return

    payload = {
        "last_updated": datetime.now(timezone.utc).date().isoformat(),
        "update_note": (
            "Posts are refreshed automatically from trusted .org and .edu sources "
            "every two weeks."
        ),
        "posts": merged,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(merged)} posts to {OUTPUT}")


if __name__ == "__main__":
    main()
