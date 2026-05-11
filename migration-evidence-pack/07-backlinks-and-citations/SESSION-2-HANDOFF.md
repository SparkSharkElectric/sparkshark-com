# Backlink Capture — Session 2 Handoff

**Goal:** continue building the most comprehensive backlink list for `sparkshark.com` possible. Mission is unchanged from session 1: don't miss a single link.

**Last session date:** 2026-05-11
**Committed to repo:** 2026-05-11 evening in `sparkshark-com/migration-evidence-pack/07-backlinks-and-citations/`
**Live working CSV:** `migration-evidence-pack/07-backlinks-and-citations/master-backlinks-working.csv`
**Session 1 totals:** 27 unique domains / ~40 URLs

### Read order before acting
1. This handoff
2. `BACKLINK_RISK_FINDINGS.md` (May 10 GSC audit, classification)
3. `master-backlinks-working.csv` (current state)
4. Cross-doc: `../../docs/migration/SOURCE-OF-TRUTH.md` §11 (analytics ownership gap)
5. Cross-doc: `../../docs/migration/cutover-runbook.md` Risk 6 (GTM reclaim during cutover)

---

## 1) What's done (do not redo)

| # | Source | Status | Result |
|---|---|---|---|
| 1 | Google Search Console | ✅ Done | 28 URLs / 17 domains from May 10 audit, in `gsc-external-links-all-deduped.csv` |
| 2 | Bing Webmaster Tools API | ✅ Done | Verified `https://sparkshark.com/`; `GetUrlLinks` returns 0 results; Bing's index has effectively zero backlinks for the site. Re-check in 24-72 hr in case it populates. |
| 3 | WebSearch open-web pass | ✅ Done | +10 confirmed Brock-owned/-referencing backlinks (Yelp, FB, IG, TikTok, Thumbtack, theorg, agreatertown, featured.com Brock profile, glassdoor OKC, LinkedIn Brock). 7+ collision filter rows (Spark Sharks in Ontario, Wisconsin, Elk Grove CA, Sacramento CA) |
| 4 | GoDaddy DNS for Ahrefs TXT | ✅ Done | Added `ahrefs-site-verification_eb9deeaf...` TXT at @, propagated to public resolvers |
| 5 | Free aggregators | ✅ Done — dry | OpenLinkProfiler 404 on both URL patterns (dead); Ubersuggest / SmallSEOTools gated |

## 2) What's pending

| # | Source | Status | Action |
|---|---|---|---|
| **6** | **Ahrefs Webmaster Tools scrape (free tier)** | 🟢 **TOP PRIORITY THIS SESSION** | Ahrefs CSV export is paid ($129 Lite minimum). AWT free tier shows data in UI only. Plan: drive Brock's logged-in browser via **Chrome MCP** (tools `mcp__claude-in-chrome__*`) to scrape Site Explorer → Backlinks + Referring Domains views. Save scraped rows as CSVs alongside `master-backlinks-working.csv`. |
| 7 | WP Engine access logs | ⏳ Blocked | SSH key in 1P works but user-portal shell doesn't expose logs. After Brock rotates WPE API token, use WPE Public API `GET /v1/installs/{id}/logs` to download last 90 days. Or Brock manually downloads from my.wpengine.com → install → Access Logs. |
| 8 | GA4 referrals | ⏳ Blocked on property mismatch | Live site fires `G-QK02QH3SWY` via `GTM-W7V4RS7C` which Brock does NOT own. Brock owns GTM `GTM-TBCXCXGS` (orphaned) and 3 GA4 properties — 480290314 Flanco Electric (**Brock CONFIRMED owns this account 2026-05-11 evening**), 481482348 Spark Shark, 488680346 Spark Shark. None contains the live measurement ID. **Action for session 2:** Brock to grant service account `sparkshark-seo-reader@fluid-emissary-493106-s2.iam.gserviceaccount.com` as Viewer on (a) Flanco Electric property 480290314 — for legacy pre-rebrand referral history, and (b) Spark Shark property 488680346 — retry with Admin role this time (first attempt failed). Then pull source/medium=referral data from both. |
| 9 | Common Crawl + AWS Athena | ⏳ Brock said "later" | $5-15 query for full open-web inbound-link sweep. Decision deferred. |
| 10 | Wayback CDX enrichment | ⏳ | Run last, after master list is built — confirm historical existence of each known referring URL. |

## 3) Critical context (read before acting)

### Brand-name collisions (filter aggressively)
At least 4 other "Spark Shark" businesses exist. Filter every WebSearch / scrape result:
- Spark Shark Electric / @sparksharkelectric — **Barrie, Ontario, Canada** (NOT Brock's)
- Spark Shark LLC — Pewaukee, WI (NOT Brock's)
- The Spark Shark — Elk Grove, CA (NOT Brock's)
- The Spark Shark — Sacramento, CA (NOT Brock's)

**Brock's confirmed social handles** (do NOT confuse):
- Facebook: `facebook.com/sparksharkelectric` (page name "SparkShark", OKC 405-436-4776, theteam@sparkshark.com)
- Instagram: `instagram.com/thesparkshark` (NOT @sparksharkelectric — that's Ontario)
- Twitter/X: `twitter.com/The_Spark_Shark` / `x.com/The_Spark_Shark`
- TikTok: `tiktok.com/@sparkshark.com`
- Pinterest: `pinterest.com/sparksharkelectric`
- LinkedIn (Brock personal): `linkedin.com/in/brock-flanary/`

**Filter rule:** any backlink whose domain shows non-OK / non-OKC geography in its content/bio is NOT Brock's. Confirm via NAP (Name + 621 Sally Ct Moore OK 73160 or 405-436-4776).

### Existing GSC export (use as Source #1 baseline)
- `gsc-external-links-all-deduped.csv` — 28 URLs / 17 domains, classified P0-P3
- `gsc-link-summary-by-domain.csv` — domain-level rollup
- `BACKLINK_RISK_FINDINGS.md` — full risk classification by tier

### Site state context (current 2026-05-11)
- Cutover from WP Engine (WordPress) to Vercel is in progress; `_vercel` TXTs present for both apex + www
- DNS at GoDaddy (ns77/78.domaincontrol.com); DNS API write access works (1P "GoDaddy API")
- Live site currently still resolving to WP Engine IPs (141.193.213.10/11)
- GSC has BOTH `sc-domain:sparkshark.com` and `https://www.sparkshark.com/` verified at siteOwner

## 4) Credentials inventory (1Password vault: SparkShark)

⚠️ **CRITICAL — Redaction rule:** When inspecting 1P items, redact by **field type** (CONCEALED, SSHKEY), NOT by label keyword match. Block-list filtering on "pass"/"key"/"secret" failed in session 1 and leaked Brock's WP Engine Customer Portal password + API token into transcript. Both are pending rotation. See `~/.claude/projects/-Users-brock/memory/feedback_redaction_filter_strict.md`.

| Item title | ID | What you need |
|---|---|---|
| `GSC Service Account — sparkshark-seo-reader` | `cj4b5rwfzosxnfdfysoem77tfy` | em-dash in title breaks `op read`; use `op item get` then parse `fluid-emissary-493106-s2-b709fb730209.json` field |
| `GoDaddy API` | `wjfxw3a5tu7mr5gfsa67reo2z4` | Key + Secret; works on `api.godaddy.com/v1/domains/sparkshark.com/records*` |
| `Bing Webmaster API` | `flce3j5fqd5hkeatd65jbatbhq` | `api_key` field; works on `ssl.bing.com/webmaster/api.svc/json/*` |
| `WP Engine SSH Key — flancoelectric (Spark Shark)` | `7baqqyeiyungknahpf44ah455m` | SSH key + host + user (concealed); install name "flancoelectric" |
| `wp_engine` | — | Customer Portal login + API token — **BOTH LEAKED 2026-05-11, ROTATE BEFORE USING** |
| `Vercel - brock-3920 Personal Team Token` | `my3gl766tqytkvvw67m35qb67i` | (Not used in this project but available) |

## 5) Working API/data references

### Google Search Console (Webmasters API v3)
- Scope: `https://www.googleapis.com/auth/webmasters.readonly`
- Service account has siteOwner on both `sc-domain:sparkshark.com` and `https://www.sparkshark.com/`
- ⚠️ **GSC API does NOT expose the Links report.** Backlinks are UI-only export. Already done in May 10 audit.

### Bing Webmaster API
- Base: `https://ssl.bing.com/webmaster/api.svc/json/`
- Verified site URL is `https://sparkshark.com/` (apex with trailing slash — match exactly)
- **Correct backlink endpoint is `GetUrlLinks`** (NOT `GetInboundLinks` which 404s). Per-URL paginated.
- Response has UTF-8 BOM — strip `b'\xef\xbb\xbf'` prefix before `json.loads`
- All endpoints return 0 inbound links as of 2026-05-11 17:00 — Bing index is empty for sparkshark.com

### GA4 Data API
- Scope: `https://www.googleapis.com/auth/analytics.readonly`
- Same service account works once Brock adds it as Viewer
- Currently only property 481482348 is granted; data there is empty (20 users in 90d, all "Unassigned" or CPC-tagged)
- Live measurement ID `G-QK02QH3SWY` is owned by a third party we don't have access to

### GoDaddy API
- Auth header: `Authorization: sso-key {Key}:{Secret}`
- Read all TXT: `GET /v1/domains/sparkshark.com/records/TXT`
- Add TXT (preserves existing): `PATCH /v1/domains/sparkshark.com/records` with body `[{"type":"TXT","name":"@","data":"...","ttl":600}]`

## 6) Coding patterns that work (reuse these)

### Mint Google service-account access token (JWT)
```bash
op item get "GSC Service Account — sparkshark-seo-reader" --vault SparkShark --format json --reveal > /tmp/.sa.json
chmod 600 /tmp/.sa.json
JWT=$(python3 -c "
import json, time, base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
d=json.load(open('/tmp/.sa.json'))
fields={f.get('label'):f.get('value','') for f in d.get('fields',[])}
sa=json.loads(fields['fluid-emissary-493106-s2-b709fb730209.json'])
now=int(time.time())
h={'alg':'RS256','typ':'JWT','kid':sa['private_key_id']}
c={'iss':sa['client_email'],'scope':'<SCOPE>','aud':'https://oauth2.googleapis.com/token','exp':now+3600,'iat':now}
b=lambda o: base64.urlsafe_b64encode(json.dumps(o,separators=(',',':')).encode()).rstrip(b'=').decode()
si=f'{b(h)}.{b(c)}'.encode()
k=serialization.load_pem_private_key(sa['private_key'].encode(),password=None)
sig=k.sign(si,padding.PKCS1v15(),hashes.SHA256())
print(si.decode()+'.'+base64.urlsafe_b64encode(sig).rstrip(b'=').decode())
")
TOK=$(curl -sS -X POST https://oauth2.googleapis.com/token -d "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=${JWT}" | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")
rm -f /tmp/.sa.json
```

### Safe 1Password inspection (type-based redaction)
```python
SAFE_TYPES = {'STRING','MENU','DATE'}
for f in d.get('fields',[]):
    val = '[redacted, len='+str(len(f.get('value','')))+']' if f.get('type') not in SAFE_TYPES else f.get('value','')
    print(f"  label={f.get('label')!r}  type={f.get('type')}  val={val[:60]}")
```

### Use Python 3.14 + curl (urllib SSL fails on macOS — use curl for HTTPS)

## 7) Deliverables for this session

1. **Ahrefs Webmaster Tools scrape via Chrome MCP** — primary goal
2. Merge new rows into `master-backlinks-working.csv` with `source_set` column tagged "awt"
3. Final dedup pass: normalize URLs (strip utm_*/fbclid/gclid, collapse www, http→https, trailing slash), tag every row with set of sources that surfaced it
4. Wayback CDX enrichment pass on the union list — add first-seen / last-seen dates
5. Produce final `master-backlinks-final.csv` + a one-page summary doc with top recommendations

## 8) Notes on Chrome MCP for AWT scrape

- Tools are `mcp__claude-in-chrome__*`; if deferred, load via ToolSearch `query: "claude-in-chrome", max_results: 30`
- Brock should already be logged into ahrefs.com in his browser
- Navigate to ahrefs.com/webmaster-tools → site → Backlinks report
- Free AWT shows the Backlinks profile in Site Explorer-style UI; harvest rows by scrolling and parsing DOM
- If pagination is limited, also scrape Referring Domains report (typically a different cap)
- Expect 50-1000+ rows depending on site; deeper than GSC's 28

## 9) Session-end checklist

- [ ] All Ahrefs rows merged into master CSV with source tag
- [ ] Final dedup pipeline run
- [ ] Wayback enrichment complete
- [ ] `master-backlinks-final.csv` written
- [ ] One-page summary: top 5 link equity assets, top 3 risks (Flanco-era citations), P0/P1/P2/P3 action list
- [ ] Status of GA4 property hunt + WP Engine token rotation (still pending or resolved?)
- [ ] If GA4 access granted to Flanco property 480290314, pull legacy referral history and merge as `source_set=ga4-flanco-legacy`

## 10) Brock-confirmed ownership facts (do not re-litigate)

- **Flanco Electric GA4 account 347644522** — Brock OWNS (confirmed 2026-05-11 evening). Can grant SA access in next session.
- **Spark Shark Analytics account 348668675** — Brock owns. Properties 481482348 (SA already added) and 488680346 (first add attempt failed — retry with Admin role).
- **GTM account 6296666179 "Spark Shark"** — Brock owns container `GTM-TBCXCXGS` for sparkshark.com (NOT deployed on live site).
- **GTM-W7V4RS7C** — currently in the live www.sparkshark.com homepage `<noscript>` iframe. Brock does NOT own. The cutover-runbook characterizes this as "Coalition-era abandoned" — but the container ID is still in the live HTML at audit time, so it is at minimum "loaded but unowned" and possibly still firing tags. Coalition is presumably the prior marketing agency.
- **GA4 G-QK02QH3SWY** — measurement ID extracted from the live `GTM-W7V4RS7C` container's `gtm.js` config. Owner unknown; not in any of Brock's 3 visible GA4 properties. Data flowing here for years is locked behind a third party.
- **Cutover implication:** `docs/migration/cutover-runbook.md` Risk 6 already plans the `build.py:153` swap (GTM → `gtag.js?id=GT-NGS794C2`) as a pre-flip task. That swap is also the moment we lose `GTM-W7V4RS7C` from the live site — a feature, not a bug. After cutover, the unowned tag manager is gone. Add a follow-up to wire Brock-owned `GTM-TBCXCXGS` separately if a future tag-manager surface is desired.
