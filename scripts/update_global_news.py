#!/usr/bin/env python3
"""Fetch publisher headlines through Google News RSS; fail closed, no fabricated news."""
import datetime as dt
import email.utils
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

URL = "https://news.google.com/rss/search?q=when%3A1d+world+breaking+news&hl=en-US&gl=US&ceid=US:en"
req = urllib.request.Request(URL, headers={"User-Agent": "REVENGERS-Global/1.0"})
with urllib.request.urlopen(req, timeout=25) as response:
    xml = response.read(2_000_000)
root = ET.fromstring(xml)
items = []
seen = set()
now = dt.datetime.now(dt.timezone.utc)
for item in root.findall("./channel/item"):
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    source = (item.findtext("source") or "Publisher").strip()
    raw_date = item.findtext("pubDate") or ""
    try:
        published = email.utils.parsedate_to_datetime(raw_date).astimezone(dt.timezone.utc)
    except (ValueError, TypeError):
        continue
    if not title or not link.startswith("https://") or title in seen or not (now - dt.timedelta(hours=30) <= published <= now + dt.timedelta(minutes=5)):
        continue
    seen.add(title)
    items.append({"title": title[:220], "url": link, "source": source[:80], "published_at": published.isoformat()})
    if len(items) == 35:
        break
if len(items) < 3:
    raise SystemExit("Insufficient current news; refusing to publish misleading headlines")
output = {"updated_at": now.isoformat(), "source": "Google News RSS", "articles": items}
Path("global-news.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
print(f"Updated {len(items)} headlines")
