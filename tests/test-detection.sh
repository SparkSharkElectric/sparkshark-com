#!/usr/bin/env bash
# tests/test-detection.sh — hands-free regression guard for qa.py.
#
# Injects the canary bug (a literal `<h2>RATING SUMMARY (centered, large)</h2>`
# heading + orphan `Stars:` / `Number:` bullets) into reviews/index.html,
# runs `python3 qa.py /reviews/`, and expects:
#   1. qa.py exits non-zero (caught the bug).
#   2. The phrase "centered, large" appears in qa-report.md.
#
# Restores reviews/index.html and qa-report.md to their pre-test state on every
# exit path (success, failure, or interrupt) via a trap.
#
# Run from the repo root:  bash tests/test-detection.sh

set -eu

if [ ! -f reviews/index.html ]; then
  echo "test-detection.sh: reviews/index.html not found. Run 'python3 build.py' first." >&2
  exit 2
fi

PAGE_BAK=$(mktemp)
REPORT_BAK=$(mktemp)
HAD_REPORT=0

cleanup() {
  cp "$PAGE_BAK" reviews/index.html 2>/dev/null || true
  if [ "$HAD_REPORT" = "1" ]; then
    cp "$REPORT_BAK" qa-report.md 2>/dev/null || true
  fi
  rm -f "$PAGE_BAK" "$REPORT_BAK"
}
trap cleanup EXIT

cp reviews/index.html "$PAGE_BAK"
if [ -f qa-report.md ]; then
  cp qa-report.md "$REPORT_BAK"
  HAD_REPORT=1
fi

# Inject the canary bug right before </body>.
python3 - <<'PY'
from pathlib import Path
p = Path("reviews/index.html")
html = p.read_text(encoding="utf-8")
canary = (
    "\n<h2>RATING SUMMARY (centered, large)</h2>\n"
    "<ul><li>Stars:</li><li>Number:</li></ul>\n"
)
if "</body>" in html:
    html = html.replace("</body>", canary + "</body>", 1)
else:
    html = html + canary
p.write_text(html, encoding="utf-8")
PY

# Expect qa.py to FAIL on the corrupted page.
if python3 qa.py /reviews/ --ci; then
  echo "FAIL: qa.py did not detect the canary bug in reviews/index.html" >&2
  exit 1
fi

# Confirm the report names the offending phrase.
if ! grep -qi "centered, large" qa-report.md; then
  echo "FAIL: qa.py exited non-zero but 'centered, large' is not in qa-report.md" >&2
  exit 1
fi

echo "PASS (1/2): qa.py correctly detected the scaffolding canary in reviews/index.html"

# Restore before the next canary so it runs from a clean baseline.
cp "$PAGE_BAK" reviews/index.html

# ── Canary 2: orphan-fragment detection ────────────────────────────────────
# Inject an orphan-period bullet (the exact shape produced by a stripped
# [VERIFY:] tag) and confirm qa.py catches it AND names the orphan-period rule.
python3 - <<'PY'
from pathlib import Path
p = Path("reviews/index.html")
html = p.read_text(encoding="utf-8")
canary = "\n<ul><li>. Manufacturer warranties on installed parts.</li></ul>\n"
if "</body>" in html:
    html = html.replace("</body>", canary + "</body>", 1)
else:
    html = html + canary
p.write_text(html, encoding="utf-8")
PY

if python3 qa.py /reviews/ --ci; then
  echo "FAIL: qa.py did not detect the orphan-fragment canary in reviews/index.html" >&2
  exit 1
fi

if ! grep -qi "orphan-period bullet" qa-report.md; then
  echo "FAIL: qa.py exited non-zero but 'orphan-period bullet' is not in qa-report.md" >&2
  exit 1
fi

echo "PASS (2/2): qa.py correctly detected the orphan-fragment canary in reviews/index.html"
