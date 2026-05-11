#!/usr/bin/env python3
"""GSC Links audit builder — emits 3 deduped/labeled CSVs for the v5 evidence pack.

Lane discipline: reads only from raw-gsc-links-exports/ inside this folder; writes
only into the parent 07-backlinks-and-citations/ folder. No /tmp, no repo writes,
no network, no GSC API calls.
"""
import csv
import os
import re
from collections import defaultdict, OrderedDict
from urllib.parse import urlparse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(THIS_DIR)
RAW_DIR = os.path.join(OUT_DIR, "raw-gsc-links-exports")

LATEST = "https___www.sparkshark.com_-Latest links-2026-05-10.csv"
SAMPLE = "https___www.sparkshark.com_-More sample links-2026-05-10.csv"

# Internal drilldowns: raw (3) is byte-identical to (4); excluded to avoid double-counting.
INTERNAL_DRILLDOWNS = [
    "https___www.sparkshark.com_-Your pages linking to this page-2026-05-10.csv",
    "https___www.sparkshark.com_-Your pages linking to this page-2026-05-10 (1).csv",
    "https___www.sparkshark.com_-Your pages linking to this page-2026-05-10 (2).csv",
    "https___www.sparkshark.com_-Your pages linking to this page-2026-05-10 (4).csv",
    "https___www.sparkshark.com_-Your pages linking to this page-2026-05-10 (5).csv",
]
INTERNAL_EXCLUDED_DUPLICATE = "https___www.sparkshark.com_-Your pages linking to this page-2026-05-10 (3).csv"

DIRECTORY_DOMAINS = {
    "yellowpages.com", "bbb.org", "callupcontact.com", "chamberofcommerce.com",
    "dexknows.com", "mapquest.com", "networx.com", "provenexpert.com",
    "smartelectricalservices.net", "superpages.com", "uscity.net",
    "best-electrician-moore.com",
}
SOCIAL_CONTENT_DOMAINS = {
    "twitter.com", "x.com", "pinterest.com", "reddit.com", "medium.com",
}


def reg_domain(url: str) -> str:
    h = (urlparse(url).hostname or "").lower()
    if h.startswith("www."):
        h = h[4:]
    return h


def read_csv_rows(path: str):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


# ---------------- EXTERNAL ----------------
latest_rows = read_csv_rows(os.path.join(RAW_DIR, LATEST))
sample_rows = read_csv_rows(os.path.join(RAW_DIR, SAMPLE))

ext = OrderedDict()
for r in latest_rows:
    url = r["Linking page"].strip()
    ext.setdefault(url, {"sources": set(), "last_crawled": ""})
    ext[url]["sources"].add("Latest links")
    ext[url]["last_crawled"] = r.get("Last crawled", "").strip()
for r in sample_rows:
    url = r["Linking page"].strip()
    ext.setdefault(url, {"sources": set(), "last_crawled": ""})
    ext[url]["sources"].add("More sample links")

# Per-URL migration notes (manual labels — reviewed against source CSVs).
NOTES = {
    "https://www.networx.com/c.flanco-electric": "FLANCO-ERA citation. Active third-party page using legacy brand. Request takedown or rebrand to Spark Shark; conflicts with public NAP.",
    "https://www.bbb.org/us/ok/moore/profile/electrical-contractors/spark-shark-electric-0995-90130075": "BBB profile (Moore). Verify NAP, claim, confirm hours/phone before DNS cutover.",
    "https://www.bbb.org/us/ok/oklahoma-city/profile/electrical-contractors/spark-shark-electric-0995-90130075/addressId/134759": "BBB profile (OKC alt address). Reconcile with Moore profile to avoid duplicate-listing confusion.",
    "https://www.mapquest.com/us/oklahoma/spark-shark-electric-778761940": "MapQuest profile. NAP-critical; claim/verify before cutover.",
    "https://www.chamberofcommerce.com/business-directory/oklahoma/moore/electrician/2034210950-spark-shark-electric": "ChamberOfCommerce.com directory listing. Verify NAP.",
    "https://www.callupcontact.com/b/businessprofile/Spark_Shark_Electric/9878135": "CallUpContact business profile. Verify NAP, claim if possible.",
    "https://www.provenexpert.com/en-us/spark-shark-electric/": "ProvenExpert reviews profile. Verify ownership and review content.",
    "https://smartelectricalservices.net/business/spark-shark-electric-ok-91055/": "Third-party directory listing for Spark Shark. Verify accuracy.",
    "http://uscity.net/listing/spark_shark_electric-12248252": "USCity.net directory listing. HTTP (not HTTPS). Verify NAP.",
    "https://best-electrician-moore.com/": "Third-party local listicle homepage. Verify Spark Shark inclusion still accurate.",
    "https://best-electrician-moore.com/spark-shark-electric": "Third-party brand-specific writeup. Verify content accuracy and NAP.",
    "https://www.dexknows.com/chickasha-ok/electrical-power-systems-maintenance": "Generic category page (Chickasha electrical maintenance) — no direct Spark Shark profile detected. Monitor.",
    "https://www.superpages.com/macomb-ok/generators": "Generic category page (Macomb generators) — no direct Spark Shark profile detected. Monitor.",
    "https://twitter.com/The_Spark_Shark": "Spark Shark X/Twitter profile (twitter.com host).",
    "https://x.com/The_Spark_Shark": "Spark Shark X profile (x.com host). Same account as twitter.com link.",
    "https://www.pinterest.com/sparksharkelectric/": "Spark Shark Pinterest profile. Verify branding and bio links.",
    "https://www.reddit.com/r/AskElectricians/comments/1on2zvl/hey_folks_question_on_if_i_need_to_replace_my/": "Reddit thread. Likely user-mention only; monitor.",
    "https://medium.com/family-kids/holiday-hosting-electrical-tips-for-a-safe-worry-free-gathering-7de0e0d42eed": "Medium article. Verify whether Spark Shark mention is brand-controlled.",
    "https://www.yellowpages.com/oklahoma-city-ok/hunzicker-lighting": "YellowPages competitor/category page (Hunzicker Lighting). Co-citation noise; not a direct Spark Shark backlink. Monitor only.",
    "https://www.yellowpages.com/oklahoma-city-ok/messer-electric": "YellowPages competitor listing (Messer Electric). Co-citation noise. Monitor only.",
    "https://www.yellowpages.com/moore-ok/lighting-fixtures": "YellowPages category page (Moore lighting fixtures). Co-citation noise. Monitor only.",
    "https://www.yellowpages.com/oklahoma-city-ok/generators": "YellowPages category page (OKC generators). Co-citation noise. Monitor only.",
    "https://www.yellowpages.com/oklahoma-city-ok/dr-sparks-dds": "YellowPages dentist listing (Dr. Sparks DDS). Lexical 'spark' overlap, NOT Spark Shark. False-positive citation. Monitor only.",
    "https://www.yellowpages.com/midwest-city-ok/lighting-consultants-designers": "YellowPages category page. Co-citation noise. Monitor only.",
    "https://www.yellowpages.com/oklahoma-city-ok/power-generator-kohler": "YellowPages category page. Co-citation noise. Monitor only.",
    "https://www.yellowpages.com/oklahoma-city-ok/electrical-power-systems-maintenance": "YellowPages category page. Co-citation noise. Monitor only.",
    "https://www.yellowpages.com/norman-ok/generators": "YellowPages category page (Norman generators). Co-citation noise. Monitor only.",
    "https://www.yellowpages.com/chickasha-ok/generators": "YellowPages category page (Chickasha generators). Co-citation noise. Monitor only.",
}


def write_external():
    out = os.path.join(OUT_DIR, "gsc-external-links-all-deduped.csv")
    fieldnames = [
        "linking_url", "linking_domain", "last_crawled", "source_export_files",
        "contains_flanco", "contains_spark", "contains_bsf",
        "appears_directory_or_citation", "appears_social_or_content", "notes",
    ]
    rows = []
    for url, meta in sorted(ext.items()):
        dom = reg_domain(url)
        url_l = url.lower()
        rows.append({
            "linking_url": url,
            "linking_domain": dom,
            "last_crawled": meta["last_crawled"],
            "source_export_files": ", ".join(sorted(meta["sources"])),
            "contains_flanco": "true" if "flanco" in url_l else "false",
            "contains_spark": "true" if "spark" in url_l else "false",
            "contains_bsf": "true" if "bsf" in url_l else "false",
            "appears_directory_or_citation": "true" if dom in DIRECTORY_DOMAINS else "false",
            "appears_social_or_content": "true" if dom in SOCIAL_CONTENT_DOMAINS else "false",
            "notes": NOTES.get(url, ""),
        })
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return len(rows)


# ---------------- INTERNAL ----------------
WP_PATH_PATTERNS = ["/category/", "/tag/", "/author/", "/wp-content/", "/wp-admin/", "/?p=", "/feed/"]


def write_internal():
    pages = defaultdict(lambda: {"sources": set()})
    for fname in INTERNAL_DRILLDOWNS:
        for r in read_csv_rows(os.path.join(RAW_DIR, fname)):
            url = r["Linking page"].strip()
            if url:
                pages[url]["sources"].add(fname)
    out = os.path.join(OUT_DIR, "gsc-internal-links-all-deduped.csv")
    fieldnames = [
        "internal_linking_page", "source_export_files", "count_across_exports",
        "contains_flanco", "contains_2023_or_2024_blog_path",
        "contains_old_archive_or_wp_path", "notes",
    ]
    rows = []
    for url, meta in sorted(pages.items()):
        url_l = url.lower()
        is_blog = bool(re.search(r"/(2023|2024)/\d{2}/", url_l))
        is_wp_archive = any(p in url_l for p in WP_PATH_PATTERNS)
        notes_parts = []
        if "flanco" in url_l:
            notes_parts.append("FLANCO-ERA URL — must redirect to Spark Shark equivalent before DNS cutover.")
        if is_blog:
            notes_parts.append("Legacy 2023/2024 blog post path. Confirm in Vercel redirect map.")
        if "/price/" in url_l:
            notes_parts.append("Page only appears in 2 of 5 internal drilldowns — possibly removed/unlinked.")
        rows.append({
            "internal_linking_page": url,
            "source_export_files": ", ".join(sorted(meta["sources"])),
            "count_across_exports": len(meta["sources"]),
            "contains_flanco": "true" if "flanco" in url_l else "false",
            "contains_2023_or_2024_blog_path": "true" if is_blog else "false",
            "contains_old_archive_or_wp_path": "true" if is_wp_archive else "false",
            "notes": " ".join(notes_parts),
        })
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return len(rows)


# ---------------- DOMAIN SUMMARY ----------------
DOMAIN_LABELS = {
    "yellowpages.com":              ("citation/directory", "P3 ignore/monitor",       "Co-citation noise; competitor/category listings, no direct Spark Shark profile detected. Monitor only."),
    "bbb.org":                      ("business/profile",   "P1 review before DNS",    "Two BBB profiles (Moore + OKC). Claim/verify NAP, reconcile duplicate addressId before DNS cutover."),
    "best-electrician-moore.com":   ("content/blog/forum", "P2 post-launch cleanup",  "Third-party local listicle with Spark Shark writeup. Verify accuracy after launch."),
    "callupcontact.com":            ("citation/directory", "P2 post-launch cleanup",  "Spark Shark business profile. Verify NAP, claim if possible."),
    "chamberofcommerce.com":        ("business/profile",   "P1 review before DNS",    "Spark Shark directory listing. Verify NAP before DNS cutover."),
    "dexknows.com":                 ("citation/directory", "P3 ignore/monitor",       "Generic category page only; no direct Spark Shark profile detected. Monitor."),
    "mapquest.com":                 ("business/profile",   "P1 review before DNS",    "Spark Shark map listing. NAP-critical; claim/verify before cutover."),
    "medium.com":                   ("content/blog/forum", "P3 ignore/monitor",       "Single article reference. Monitor; no action unless brand-owned."),
    "networx.com":                  ("citation/directory", "P0 redirect/citation risk","FLANCO-ERA citation (/c.flanco-electric). Request takedown or rebrand to Spark Shark; conflicts with public NAP."),
    "pinterest.com":                ("social/profile",     "P2 post-launch cleanup",  "Spark Shark Pinterest profile. Verify ownership and bio links."),
    "provenexpert.com":             ("business/profile",   "P2 post-launch cleanup",  "Spark Shark reviews profile. Claim/verify."),
    "reddit.com":                   ("content/blog/forum", "P3 ignore/monitor",       "User thread. Monitor only."),
    "smartelectricalservices.net":  ("citation/directory", "P2 post-launch cleanup",  "Third-party Spark Shark directory listing. Verify accuracy."),
    "superpages.com":               ("citation/directory", "P3 ignore/monitor",       "Generic category page only; no direct Spark Shark profile. Monitor."),
    "twitter.com":                  ("social/profile",     "P2 post-launch cleanup",  "Spark Shark X profile (twitter.com host). Verify links and bio."),
    "uscity.net":                   ("citation/directory", "P2 post-launch cleanup",  "Spark Shark directory listing (HTTP). Verify NAP; request HTTPS upgrade if possible."),
    "x.com":                        ("social/profile",     "P2 post-launch cleanup",  "Spark Shark X profile (x.com host). Same account as twitter.com link."),
}


def write_domain_summary():
    by_dom = defaultdict(list)
    for url, meta in ext.items():
        by_dom[reg_domain(url)].append((url, meta))
    out = os.path.join(OUT_DIR, "gsc-link-summary-by-domain.csv")
    fieldnames = [
        "linking_domain", "unique_linking_urls", "latest_last_crawled",
        "contains_flanco_reference", "likely_type", "migration_priority",
        "recommended_action",
    ]
    rows = []
    for dom in sorted(by_dom.keys()):
        urls = by_dom[dom]
        latest = max((u[1]["last_crawled"] for u in urls if u[1]["last_crawled"]), default="")
        has_flanco = any("flanco" in u[0].lower() for u in urls)
        likely_type, priority, action = DOMAIN_LABELS.get(dom, ("unknown", "P3 ignore/monitor", "No label assigned. Review manually."))
        rows.append({
            "linking_domain": dom,
            "unique_linking_urls": len(urls),
            "latest_last_crawled": latest,
            "contains_flanco_reference": "true" if has_flanco else "false",
            "likely_type": likely_type,
            "migration_priority": priority,
            "recommended_action": action,
        })
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    n_ext = write_external()
    n_int = write_internal()
    n_dom = write_domain_summary()
    print(f"external_rows={n_ext}")
    print(f"internal_rows={n_int}")
    print(f"domain_rows={n_dom}")
    print(f"excluded_duplicate_drilldown={INTERNAL_EXCLUDED_DUPLICATE}")
