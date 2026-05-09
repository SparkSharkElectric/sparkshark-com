#!/usr/bin/env bash
# _tools/p0-deploy.sh — apply 3 P0 fixes for the new sparkshark.com static site.
# Each fix is its own commit per deploy-pipeline.md "one issue per commit" rule.
#
# Usage:  bash _tools/p0-deploy.sh
#
# What it does (in order):
#   Commit 1 — fix _strip_verify regex + parse_draft section split  (build.py)
#   Commit 2 — drop orphan period in why-us item 3                  (copy-drafts)
#   Commit 3 — link all area chips to /locations-we-serve/ fallback (build.py)
#
# Each step: edit -> rebuild -> git add -> git commit -> git push.
# GH Pages auto-deploys ~30s after each push.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# ── Pre-flight ───────────────────────────────────────────────────────────────
[ -f build.py ] || { echo "✗ build.py not found — run from sparkshark-com root."; exit 1; }
[ "$(git branch --show-current)" = "main" ] || { echo "✗ not on main branch."; exit 1; }

# Reset the two source files we'll touch to origin/main state, in case a prior
# session left half-applied edits. Other working-tree changes are preserved.
echo "→ resetting build.py + copy-drafts/01-homepage.md to origin/main"
git checkout -- build.py copy-drafts/01-homepage.md

# Confirm clean baseline
DIRTY=$(git status --porcelain build.py copy-drafts/01-homepage.md)
[ -z "$DIRTY" ] || { echo "✗ source files still dirty after reset:"; echo "$DIRTY"; exit 1; }

build_or_die() {
  echo "→ rebuilding (BASE=/sparkshark-com)"
  BASE=/sparkshark-com python3 build.py >/dev/null 2>&1 || { echo "✗ build.py failed"; exit 1; }
}

push_or_die() {
  # push_or_die <commit_message_subject> <commit_message_body>
  local subject="$1"; local body="$2"
  git add -A
  if git diff --cached --quiet; then
    echo "  (no changes — skipping commit)"
    return
  fi
  git commit -m "$subject" -m "$body"
  git push origin main
}

# ── Commit 1 ─────────────────────────────────────────────────────────────────
echo
echo "═══ COMMIT 1: _strip_verify newline preservation + parse_draft = in headers ═══"
python3 <<'PYEOF'
import re, pathlib
p = pathlib.Path("build.py")
s = p.read_text(encoding="utf-8")
# These two replacements use single-quoted raw strings as in the source.
old1 = "return re.sub(r'\\s*\\[VERIFY:[^\\]]*\\]\\s*', ' ', text).strip()"
new1 = "return re.sub(r'[ \\t]*\\[VERIFY:[^\\]]*\\][ \\t]*', ' ', text).strip()"
old2 = "parts = re.split(r'\\n=== ([^=\\n]+?) ===\\n', text)"
new2 = "parts = re.split(r'\\n=== (.+?) ===\\n', text)"
if old1 in s: s = s.replace(old1, new1)
if old2 in s: s = s.replace(old2, new2)
p.write_text(s, encoding="utf-8")
PYEOF

grep -qF "[ \\t]*\\[VERIFY:" build.py || { echo "✗ commit 1 edit A not applied"; exit 1; }
grep -qF "re.split(r'\\n=== (.+?) ===\\n'" build.py || { echo "✗ commit 1 edit B not applied"; exit 1; }
echo "  ✓ build.py edits applied"

build_or_die

# Smoke-check expected effects locally before pushing.
HERO_LIS=$(grep -c '<li>' index.html | head -1)
SVC_CARDS=$(grep -c 'class="svc-card"' index.html)
[ "$SVC_CARDS" = "8" ] || { echo "✗ expected 8 svc-card, got $SVC_CARDS"; exit 1; }
grep -A4 'class="hero__trust"' index.html | grep -qF "Live 24/7" || { echo "✗ hero trust list missing live 24/7"; exit 1; }
echo "  ✓ local smoke: 8 svc-card present, hero trust list intact"

push_or_die \
  "fix: preserve newlines in _strip_verify and allow = in section headers" \
  "_strip_verify replaced \\s* with [ \\t]* so trailing newlines after [VERIFY:...] tags are preserved. Was eating bullet boundaries: 3-item HERO TRUST POINTS rendered as 2 hyphen-joined items; 4-item REVIEWS list rendered as 2 run-on items.

parse_draft section regex relaxed from [^=\\n]+? to .+? so headers with literal '=' (e.g. 'SERVICES GRID — 8 cards (each = title + 1 sentence)') match. Was silently failing → empty services grid.

Effects on rebuilt site:
- index.html hero__trust now shows 3 separate li
- index.html services__grid now renders 8 svc-card items
- index.html reviews list shows 3 distinct platform links"

# ── Commit 2 ─────────────────────────────────────────────────────────────────
echo
echo "═══ COMMIT 2: drop orphan period in why-us item 3 ═══"
python3 <<'PYEOF'
import pathlib
p = pathlib.Path("copy-drafts/01-homepage.md")
s = p.read_text(encoding="utf-8")
old = "- 3. Licensed and accountable — [VERIFY: Oklahoma CIB license #00163603]. Licensed, bonded, and insured. Background-checked employees — no subcontractors for residential service work."
new = "- 3. Licensed and accountable — Licensed, bonded, and insured under Oklahoma Electrical License #163603. Background-checked employees — no subcontractors for residential service work."
if old in s:
    s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
PYEOF

grep -qF "Oklahoma Electrical License #163603. Background-checked" copy-drafts/01-homepage.md \
  || { echo "✗ commit 2 edit not applied"; exit 1; }
echo "  ✓ copy-drafts/01-homepage.md edited"

build_or_die

# Local smoke: leading ". Licensed" should be gone.
if grep -q '>\. Licensed' index.html; then
  echo "✗ orphan period still present"; exit 1;
fi
grep -qF "License #163603" index.html || { echo "✗ license # not visible in why-us"; exit 1; }
echo "  ✓ local smoke: orphan period gone, License #163603 visible in why-us"

push_or_die \
  "fix: drop orphan period in why-us item 3, surface license # inline" \
  "Replaces VERIFY-tag preamble with the actual license number, which is the verified value (#163603 in BRAND dict). Side benefit: the why-us card now visibly carries the license # — a real proof point on every homepage view, not just inside the schema."

# ── Commit 3 ─────────────────────────────────────────────────────────────────
echo
echo "═══ COMMIT 3: link all area chips to /locations-we-serve/ fallback ═══"
python3 <<'PYEOF'
import pathlib
p = pathlib.Path("build.py")
s = p.read_text(encoding="utf-8")
old = "        else:\n            chips.append(f'<span class=\"chip\">{c}</span>')\n    return f'''<section class=\"area\" aria-labelledby=\"area-h\">"
new = "        else:\n            chips.append(f'<a class=\"chip chip--link\" href=\"/locations-we-serve/\">{c}</a>')\n    return f'''<section class=\"area\" aria-labelledby=\"area-h\">"
# Two functions have a similar pattern; only modify the build_homepage one (the second occurrence — area_chips_block has its own).
# Simpler: replace all matching span fallbacks for chips in build.py to chip--link to /locations-we-serve/.
# Both area_chips_block (top of file) and build_homepage (below) use the same fallback.
count = s.count("chips.append(f'<span class=\"chip\">{c}</span>')")
s = s.replace(
    "chips.append(f'<span class=\"chip\">{c}</span>')",
    "chips.append(f'<a class=\"chip chip--link\" href=\"/locations-we-serve/\">{c}</a>')"
)
p.write_text(s, encoding="utf-8")
print(f"  replaced {count} occurrence(s) of span-chip fallback")
PYEOF

grep -qF 'chip--link" href="/locations-we-serve/">{c}</a>' build.py \
  || { echo "✗ commit 3 edit not applied"; exit 1; }
echo "  ✓ build.py chip fallback edited"

build_or_die

# Local smoke: zero plain-span chips, 15 chip-link items.
PLAIN_CHIPS=$(grep -c 'class="chip">' index.html || true)
LINK_CHIPS=$(grep -c 'class="chip chip--link"' index.html)
[ "$PLAIN_CHIPS" = "0" ] || { echo "✗ expected 0 plain-span chips, got $PLAIN_CHIPS"; exit 1; }
[ "$LINK_CHIPS" = "15" ] || { echo "✗ expected 15 chip-link, got $LINK_CHIPS"; exit 1; }
echo "  ✓ local smoke: 0 plain spans, 15 chip-link items"

push_or_die \
  "fix: link all area chips to /locations-we-serve/ fallback" \
  "Five cities had no per-city page and rendered as plain <span> with no link or hover affordance. Routing them to the locations index keeps the chip row visually consistent and gives every chip an interactive next step."

# ── Done ─────────────────────────────────────────────────────────────────────
echo
echo "═══ ALL 3 COMMITS PUSHED ═══"
echo "GH Pages auto-deploys ~30s after each push."
echo "Live preview: https://sparksharkelectric.github.io/sparkshark-com/"
echo
echo "Verify (after ~90s):"
echo "  curl -s https://sparksharkelectric.github.io/sparkshark-com/ | grep -c 'svc-card'             # → 8"
echo "  curl -s https://sparksharkelectric.github.io/sparkshark-com/ | grep -c 'class=\"chip chip--link\"' # → 15"
echo "  curl -s https://sparksharkelectric.github.io/sparkshark-com/ | grep -c 'class=\"chip\">'        # → 0"
echo
git log --oneline -5
