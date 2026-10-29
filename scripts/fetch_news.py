"""Récupère les flux RSS listés dans feeds.json et écrit news.json.

Lancé automatiquement par GitHub Actions (voir .github/workflows/news.yml).
Aucune donnée personnelle n'est utilisée ici : le tri "pour toi" se fait sur le téléphone.
"""
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_AGE_DAYS = 10
MAX_ITEMS = 120
UA = "Mozilla/5.0 (compatible; BudgetPWA-news/1.0)"


def clean(text, limit=None):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    if limit and len(text) > limit:
        text = text[: limit].rsplit(" ", 1)[0] + "…"
    return text


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def local(tag):
    return tag.rsplit("}", 1)[-1]


def child_text(el, *names):
    for c in el:
        if local(c.tag) in names and (c.text or "").strip():
            return c.text
    return ""


def parse_feed(data, source):
    root = ET.fromstring(data)
    items = []
    for el in root.iter():
        kind = local(el.tag)
        if kind not in ("item", "entry"):
            continue
        title = clean(child_text(el, "title"))
        link = ""
        for c in el:
            if local(c.tag) == "link":
                link = (c.get("href") or c.text or "").strip()
                if link:
                    break
        summary = clean(child_text(el, "description", "summary", "content"), 220)
        date = parse_date(child_text(el, "pubDate", "published", "updated", "date"))
        if title and link.startswith(("http://", "https://")):
            items.append({"title": title, "link": link, "summary": summary, "source": source,
                          "date": date.isoformat() if date else None})
    return items


def main():
    feeds = json.loads((ROOT / "feeds.json").read_text(encoding="utf-8"))
    all_items, ok = [], 0
    for f in feeds:
        try:
            req = urllib.request.Request(f["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                items = parse_feed(r.read(), f["name"])
            print(f"OK   {f['name']}: {len(items)} articles")
            all_items += items
            ok += 1
        except Exception as e:  # un flux en panne ne doit pas bloquer les autres
            print(f"FAIL {f['name']}: {e}", file=sys.stderr)

    out = ROOT / "news.json"
    if ok == 0:
        print("Aucun flux n'a répondu : news.json n'est pas modifié.", file=sys.stderr)
        return

    limit = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    seen, kept = set(), []
    for it in sorted(all_items, key=lambda x: x["date"] or "", reverse=True):
        if it["link"] in seen:
            continue
        if it["date"] and datetime.fromisoformat(it["date"]) < limit:
            continue
        seen.add(it["link"])
        kept.append(it)
    data = {"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "items": kept[:MAX_ITEMS]}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"news.json : {len(data['items'])} articles")


if __name__ == "__main__":
    main()
