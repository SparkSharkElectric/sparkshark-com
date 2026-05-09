#!/usr/bin/env python3
"""qa.py — post-build quality gate for sparkshark.com.

Runs after `python3 build.py`. Walks the URL manifest from sitemap.xml,
applies a rule registry against the built HTML, and writes qa-report.md.

Usage:
    python3 qa.py                 # full sweep — every sitemap entry + extras
    python3 qa.py /reviews/       # specific page(s); intersected with manifest
    python3 qa.py --ci            # machine-readable stdout for CI logs
    python3 qa.py --strict        # promote warnings to failures

Exit codes:
    0  every page passed
    1  one or more pages failed (or warnings in --strict mode)
    2  setup error (sitemap missing, IO error, no targets matched)

Brand-data dependencies — keep in sync with build.py BRAND dict:
    name           Spark Shark Electric (3 words; never SparkShark)
    phone_display  (405) 436-4776
    city           Moore
    zip            73160
    license        #163603
"""
from __future__ import annotations

import argparse
import datetime
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITEMAP = ROOT / "sitemap.xml"
REPORT = ROOT / "qa-report.md"
SITE_HOST = "https://www.sparkshark.com"

# Bonus paths not in sitemap but worth screening (404 page is high-leak-risk).
EXTRA_PATHS = ["/404.html"]

# Pages where the marketing-asset rule (mascot, logo) applies.
MARKETING_PAGES = {
    "/",
    "/about-us/",
    "/locations-we-serve/",
    "/reviews/",
    "/contact-us/",
    "/services/",
}

# ── Rule data ────────────────────────────────────────────────────────────────

SCAFFOLDING_PATTERNS: list[tuple[str, str]] = [
    (r"\([^)]*\b(?:centered|large|small|medium|bold|wide|narrow)\b[^)]*\)",
     "scaffolding leak: parenthetical layout cue rendered as copy"),
    (r"=== ?SECTION:", "scaffolding leak: literal `=== SECTION:` marker"),
    (r"(?m)^SECTION:", "scaffolding leak: line-anchored `SECTION:` marker"),
    (r"\bMETA DESCRIPTION\b", "scaffolding leak: `META DESCRIPTION` label rendered"),
    (r"\bHERO SUBTITLE\b", "scaffolding leak: `HERO SUBTITLE` label rendered"),
    (r"<h[1-6][^>]*>\s*(?:TITLE|H1|H2)\s*</h[1-6]>",
     "scaffolding leak: heading text is a label"),
]

PLACEHOLDER_PATTERNS: list[tuple[str, str]] = [
    (r"\[VERIFY:[^\]]*\]",
     "unfilled placeholder: `[VERIFY: ...]` tag in rendered HTML"),
    (r"(?i)lorem ipsum", "unfilled placeholder: lorem ipsum"),
    (r"<li>\s*(?:Stars|Number|Subtext|Rating|Quote)\s*:\s*</li>",
     "orphan label bullet: empty `<li>Label:</li>`"),
    (r"<li>\s*<strong>\s*(?:Stars|Number|Subtext|Rating|Quote)\s*:\s*</strong>\s*</li>",
     "orphan label bullet: `<li><strong>Label:</strong></li>` no content"),
    (r"<strong>\s*(?:Stars|Number|Subtext|Rating|Quote)\s*:\s*</strong>\s*</p>",
     "orphan label: `<strong>Label:</strong></p>` with no content"),
]

STALE_STRINGS = [
    "Flanco Electric",
    "(405) 796-8111",
    "(405) 389-8896",
    "1817 Linwood",
    "1033 NW 9th",
    "621 Sally",
    "BSF Investment",
    "Plumberx Plumbing",
    "Plumbing Machanic",
]

BRAND_MISSPELLINGS = ["SparkShark", "Sparkshark"]

DISCOURAGED_WORDS: list[tuple[str, str]] = [
    (r"\bbonded\b", "discouraged word: `bonded`"),
    (r"\bowner-operator\b", "discouraged phrase: `owner-operator`"),
    (r"(?<!home)\bowner\b(?!ship)",
     "discouraged word: `owner` (homeowner / ownership are allowed)"),
]

NAP_REQUIREMENTS = [
    ("(405) 436-4776", "NAP missing: phone `(405) 436-4776`"),
    ("Moore", "NAP missing: city `Moore`"),
    ("73160", "NAP missing: ZIP `73160`"),
    ("163603", "NAP missing: license `#163603`"),
]

LICENSE_TOKEN = "163603"


# ── Data types ───────────────────────────────────────────────────────────────

@dataclass
class PageResult:
    url: str
    file: Path
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def verdict(self) -> str:
        return "FAIL" if self.issues else "PASS"


# ── Manifest ────────────────────────────────────────────────────────────────

def load_manifest() -> list[str]:
    """Return the ordered list of URL paths to check."""
    if not SITEMAP.exists():
        sys.stderr.write(
            f"qa.py: {SITEMAP.name} not found in {ROOT}. "
            "Run `python3 build.py` first.\n"
        )
        sys.exit(2)
    try:
        tree = ET.parse(SITEMAP)
    except ET.ParseError as exc:
        sys.stderr.write(f"qa.py: failed to parse {SITEMAP.name}: {exc}\n")
        sys.exit(2)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    paths: list[str] = []
    for loc in tree.getroot().findall("sm:url/sm:loc", ns):
        url = (loc.text or "").strip()
        if url.startswith(SITE_HOST):
            url = url[len(SITE_HOST):]
        paths.append(url or "/")
    paths.extend(EXTRA_PATHS)
    seen, unique = set(), []
    for p in paths:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def url_to_file(url: str) -> Path:
    """Map a URL path to the on-disk built file."""
    if url.endswith(".html"):
        return ROOT / url.lstrip("/")
    return ROOT / url.lstrip("/") / "index.html"


# ── Footer detection ────────────────────────────────────────────────────────

def footer_regions(html: str) -> list[tuple[int, int]]:
    """Return (start, end) byte offsets for each <footer>...</footer> span."""
    regions: list[tuple[int, int]] = []
    for opener in re.finditer(r"<footer\b[^>]*>", html, re.IGNORECASE):
        rest = html[opener.end():]
        closer = re.search(r"</footer\s*>", rest, re.IGNORECASE)
        if closer:
            regions.append((opener.start(), opener.end() + closer.end()))
    return regions


def in_footer(idx: int, regions: list[tuple[int, int]]) -> bool:
    return any(start <= idx < end for start, end in regions)


# ── Rules ────────────────────────────────────────────────────────────────────

def _trim(snippet: str, n: int = 80) -> str:
    s = snippet.strip()
    return s if len(s) <= n else s[: n - 3] + "..."


def _scan(patterns: list[tuple[str, str]], html: str) -> list[str]:
    out: list[str] = []
    for pattern, msg in patterns:
        for m in re.finditer(pattern, html):
            out.append(f"{msg} — `{_trim(m.group(0))}`")
    return out


def check_scaffolding(html: str) -> list[str]:
    return _scan(SCAFFOLDING_PATTERNS, html)


def check_placeholders(html: str) -> list[str]:
    return _scan(PLACEHOLDER_PATTERNS, html)


def check_stale_strings(html: str) -> list[str]:
    return [f"stale string found: `{s}`" for s in STALE_STRINGS if s in html]


def check_brand_spelling(html: str) -> list[str]:
    return [
        f"brand misspelling: `{bad}` (must be `Spark Shark Electric`)"
        for bad in BRAND_MISSPELLINGS
        if bad in html
    ]


def _strip_tags(html: str) -> str:
    """Drop tags so word-boundary searches don't match attribute values."""
    return re.sub(r"<[^>]+>", " ", html)


def check_discouraged_words(html: str) -> list[str]:
    text = _strip_tags(html)
    return [msg for pattern, msg in DISCOURAGED_WORDS if re.search(pattern, text)]


def check_nap(html: str) -> list[str]:
    return [msg for needle, msg in NAP_REQUIREMENTS if needle not in html]


def check_license_placement(html: str) -> list[str]:
    matches = list(re.finditer(LICENSE_TOKEN, html))
    if not matches:
        return []  # NAP rule covers absence
    regions = footer_regions(html)
    if not regions:
        return [f"license `#{LICENSE_TOKEN}` present but no <footer> on page"]
    out_count = sum(1 for m in matches if not in_footer(m.start(), regions))
    if out_count:
        return [
            f"license `#{LICENSE_TOKEN}` found outside <footer> "
            f"({out_count} of {len(matches)} occurrence(s))"
        ]
    return []


def check_marketing_assets(url: str, html: str) -> list[str]:
    if url not in MARKETING_PAGES:
        return []
    issues: list[str] = []
    if not re.search(r"<img[^>]*(?:src|alt)=[^>]*mascot", html, re.IGNORECASE):
        issues.append("required asset missing: mascot `<img>` not found")
    if not re.search(r"<img[^>]*(?:src|alt)=[^>]*logo", html, re.IGNORECASE):
        issues.append("required asset missing: logo `<img>` not found")
    return issues


# ── Per-page run ─────────────────────────────────────────────────────────────

def check_page(url: str) -> PageResult:
    file = url_to_file(url)
    res = PageResult(url=url, file=file)
    if not file.exists():
        res.issues.append(f"file not found: `{file.relative_to(ROOT)}`")
        return res
    try:
        html = file.read_text(encoding="utf-8")
    except OSError as exc:
        res.issues.append(f"read error: {exc}")
        return res

    res.issues.extend(check_scaffolding(html))
    res.issues.extend(check_placeholders(html))
    res.issues.extend(check_stale_strings(html))
    res.issues.extend(check_brand_spelling(html))
    res.issues.extend(check_nap(html))
    res.issues.extend(check_license_placement(html))
    res.issues.extend(check_marketing_assets(url, html))
    res.warnings.extend(check_discouraged_words(html))
    return res


# ── Reporting ───────────────────────────────────────────────────────────────

RULE_COUNT = 8


def render_report(results: list[PageResult], strict: bool) -> str:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    fails = [r for r in results if r.issues]
    passes = [r for r in results if not r.issues]
    warn_only = [r for r in results if not r.issues and r.warnings]
    overall = "FAIL" if fails or (strict and warn_only) else "PASS"

    lines: list[str] = []
    lines.append("# QA Report — sparkshark.com")
    lines.append("")
    lines.append(
        f"Run: {now} | {len(results)} pages | "
        f"Pure-Python rule engine | strict={'on' if strict else 'off'}"
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    suffix = f" — {len(fails)} pages flagged" if fails else ""
    lines.append(f"- Verdict: **{overall}**{suffix}")
    lines.append(f"- Pages PASS: {len(passes)}")
    lines.append(f"- Pages FAIL: {len(fails)}")
    lines.append(f"- Warnings only: {len(warn_only)}")
    lines.append("")

    if fails:
        lines.append("## Failures")
        lines.append("")
        for r in fails:
            lines.append(f"### {r.url}")
            lines.append("")
            for issue in r.issues:
                lines.append(f"- {issue}")
            if r.warnings:
                lines.append("- Warnings:")
                for w in r.warnings:
                    lines.append(f"  - {w}")
            lines.append("")

    if warn_only:
        lines.append("## Warnings (advisory; not blocking unless --strict)")
        lines.append("")
        for r in warn_only:
            lines.append(f"### {r.url}")
            lines.append("")
            for w in r.warnings:
                lines.append(f"- {w}")
            lines.append("")

    if passes:
        lines.append(f"## Passes ({len(passes)})")
        lines.append("")
        for r in passes:
            lines.append(f"- {r.url}")
        lines.append("")

    lines.append("## Coverage")
    lines.append("")
    lines.append(f"- Rules run: {RULE_COUNT}")
    lines.append(f"- Pages checked: {len(results)}")
    lines.append("")
    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="QA gate for sparkshark.com — pure-Python rule checker."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional URL paths to check (e.g. /reviews/). "
        "Default: every entry in sitemap.xml plus extras.",
    )
    parser.add_argument(
        "--ci", action="store_true",
        help="Machine-readable stdout, suitable for CI logs.",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Promote warnings to failures (overall verdict + exit code).",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    if args.paths:
        wanted = set(args.paths)
        unknown = wanted - set(manifest)
        for u in sorted(unknown):
            sys.stderr.write(f"qa.py: warning — `{u}` not in manifest; skipping\n")
        targets = [m for m in manifest if m in wanted]
        if not targets:
            sys.stderr.write("qa.py: no matching paths to check\n")
            return 2
    else:
        targets = manifest

    results: list[PageResult] = []
    for url in targets:
        r = check_page(url)
        results.append(r)
        if args.ci:
            sys.stdout.write(
                f"{r.verdict} {url} issues={len(r.issues)} warnings={len(r.warnings)}\n"
            )
        else:
            sys.stdout.write(f"  [{r.verdict}] {url}\n")
            for issue in r.issues:
                sys.stdout.write(f"    - {issue}\n")

    REPORT.write_text(render_report(results, args.strict), encoding="utf-8")
    sys.stdout.write(f"\nWrote {REPORT.relative_to(ROOT)}\n")

    any_fail = any(r.issues for r in results)
    any_warn = any(r.warnings for r in results)
    if any_fail or (args.strict and any_warn):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
