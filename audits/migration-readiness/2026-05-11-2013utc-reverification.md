# Migration Readiness Audit — Re-verification

**Run date:** 2026-05-11 (20:13 UTC) — ~4h after the 16:24 UTC canonical run
**Auditor:** Claude (this Cowork session)
**Mode:** Re-verification triangulation per `seo-geo-verification.md` (independent vantage on the canonical audit)
**Canonical run this supersedes / triangulates:** `2026-05-11.md` + `2026-05-11-plain-english.md` (16:24 UTC)
**`main` HEAD:** `6a3df34` `docs(migration): source-of-truth + cutover runbook + audit history + tree cleanup (#10)`
**Live alias verified:** `https://sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app`

> **Headline:** verdict unchanged. **HARD NO-GO · 40 / 100 (capped).** Both auto-fail triggers still fire. No Brock-side blocker has been closed since 16:24 UTC. Two independent audit vantages now agree on the same verdict — confidence is higher, not lower.

---

## What the second vantage re-confirmed

Independent curl sweep at 20:13 UTC from this session, using `Mozilla/5.0` UA, cold-cache fresh processes per VER-01 / VER-02:

| Check | Method | Result | Matches 16:24 audit? |
|---|---|---|---|
| Homepage `/` returns 200 | `curl -sI` | `HTTP/2 200` | Yes |
| `robots.txt` allows all + sitemap → www.sparkshark.com | `curl -s` | Confirmed | Yes |
| `sitemap.xml` parses, all `<loc>` use canonical hostname | `curl -s` + grep | Confirmed | Yes |
| 17 of 27 redirects sampled — all return 301 → 200 after `-L` | curl × 17 | 17 / 17 PASS | Yes |
| 4-node `@graph` on `/` = WebSite + Organization + LocalBusiness/Electrician + FAQPage | full JSON-LD parse (`json.loads`, not regex) | 1 block, 4 nodes intact | Yes |
| Service page (`/electrical-panels/`) adds BreadcrumbList + Service | full parse | Confirmed (also has a standalone FAQPage block — duplicate of the in-graph FAQPage; minor, not a blocker) | Yes |
| `tel:+14054364776` on every sampled page | grep `tel:` separately from displayed text | 7-page sample, every match correct | Yes |
| GTM `GTM-TBCXCXGS` loads × 2 per page (head + body) | grep | All 7 pages | Yes |
| ServiceTitan scheduler embed | grep `data-api-key` + `data-schedulerid` | `mwr2241pezdya33y00nyx0ok` + `sched_b2upae383kzlb9qjuhmqnyvt` on `/` and `/contact-us/` | Yes |
| `aggregateRating` in JSON-LD | full parse | `4.8` on every page sampled | Yes |
| **llms.txt vs llms-full.txt rating drift** | grep both | **llms.txt says `4.9`, llms-full.txt + BRAND + JSON-LD say `4.8`** — RANK-08 still FAIL | Yes (known) |
| `BRAND` dict values in `build.py` | grep | name, phone, license, rating, review_count all canonical | Yes |
| `/Users/` path leak across `api/ scripts/ docs/ vercel.json` | grep | 9 hits, all in `docs/migration/*.md` — SEC-04 FAIL (operational pointers, not credentials) | Yes |
| Flanco / SparkShark misspellings in shipping HTML | grep (excl. archived audits + home-staging snapshot) | Clean | Yes |
| Launch-gate Status cells | `git log -p docs/migration/launch-gate.md` author check | All commits authored by `brock@sparkshark.com` — LG-02 PASS | Yes |
| Gate-4 GBP evidence on disk but Status still `Not Provided` | `ls /migration-evidence-pack/05-google-business-profile/` | 10 PNGs present (name/categories, hours, services, location, booking link, profile overview) — Brock has not promoted Status | Yes |
| Gate-7 `tracking-ids.md` exists at canonical path | `ls /migration-evidence-pack/06-current-tracking/tracking-ids.md` | Present, but the file body itself says "should not be treated as fully approved until exact GA4 ID + GTM decision + Ads conversion confirmed" — Brock has not promoted Status | Yes |
| Gate-9 `canonical-nap.md` exists at canonical path | `ls /migration-evidence-pack/11-verified-business-facts/canonical-nap.md` | Present, decision is SAB-only, NAP frozen — Brock has not promoted Status | Yes |
| Gate-8 ServiceTitan smoke booking | `ls /migration-evidence-pack/06-current-tracking/servicetitan-scheduler-test-proof/` | Only `DEFERRED_TO_NEW_SESSION.md` + `README-missing.md` — genuinely Not Provided | Yes |
| Cutover smoke script `scripts/cutover-smoke.sh` | `find` across sparkshark-com | **Does not exist** — CUT-02 FAIL | Yes |
| Typed-out DNS rollback values | grep `12-launch-and-rollback/` | Only screenshots — ROLL-03 FAIL | Yes |

**Layer-disagreement check (per `seo-geo-verification.md`):** none. Every check that disagrees between layers got the lower-confidence verdict in the 16:24 run; this run found no new disagreements.

---

## What's changed since 16:24 UTC

- `docs/migration/SOURCE-OF-TRUTH.md`, `cutover-runbook.md`, and the 33-HTML `audits/_archive/` reorganization landed in PR #10 (commit `6a3df34`). These are documentation moves, not blocker closes.
- No new Status-cell promotions on `docs/migration/launch-gate.md` (the four `Not Provided` rows are unchanged).
- No new artifacts in `migration-evidence-pack/06-current-tracking/servicetitan-scheduler-test-proof/`.
- No new file at `scripts/cutover-smoke.sh`.
- No new typed-out DNS rollback values in `migration-evidence-pack/12-launch-and-rollback/`.
- Vercel domain attachment unchanged on the basis of repo evidence (the canonical run cited `vercel domains ls` evidence; this run has no Vercel CLI/token access from the sandbox, so the DOM-01/02 verdict is propagated from the 16:24 audit at PASS-through confidence, not re-verified independently).

**Net:** zero Brock-side blockers closed in the last 4 hours; the verdict is mechanically stable.

---

## What I would not stake on without a fresh Brock action

1. **DOM-01 / DOM-02.** I have no Vercel CLI/REST token available in this sandbox, so I cannot independently re-run `vercel domains ls` or hit `GET /v9/projects/sparkshark-com/domains`. The FAIL verdict is inherited from the 16:24 audit. If Brock has reassigned the domain between 16:24 and 20:13 UTC in the Vercel UI, this audit would not catch it. **Suggested next action:** Brock pastes the current output of `vercel domains ls` (or a screenshot of the Vercel Domains tab on both projects) for a one-line confirmation.
2. **SEC-01 (gitleaks).** No `.gitleaks.toml` exists in `sparkshark-com` (it lives in `spark-fsm`). The check is UNVERIFIED, not PASS. A one-line CI workflow that runs gitleaks on `sparkshark-com` would close this for every future audit.
3. **GBP screenshot field-by-field NAP cross-check.** I have not opened the 10 PNGs and read them. The 16:24 audit's GBP UNVERIFIED defaults stand. Suggested next action: Brock confirms each of the 9 NAP fields visually, or grants OCR access on the PNGs.

---

## Single next action

Same as the 16:24 audit: **fix the Vercel domain attachment first** (≈ 10 min in Vercel UI). Without that, none of the four Brock-side gate items matter — DNS would route the marketing domain to the dispatcher project regardless. Once that's reassigned, the gate-4/7/9 Status-cell promotions take ~25 min, and Gate-8 ST smoke booking takes ~10 min. Total Brock time to move from HARD NO-GO to GO WITH CAUTION: roughly 60–75 minutes plus the four Claude-owned single-file PRs (`scripts/cutover-smoke.sh`, typed-out DNS rollback values, rollback trigger criteria, GSC pre-cutover baseline). None of those PRs touch protected surfaces, so the PR-authority procedure applies but the risk is low.

---

## Provenance

This run was triggered by Brock invoking `/migration-auditor:migration-auditor` at 20:11 UTC after refreshing both repos (`git fetch --all`). The audit used: anonymous `curl` with `Mozilla/5.0` UA, fresh Python processes for each JSON-LD parse, no shared cookies, no `WebFetch` (per `feedback_web_fetch_unreliable_for_seo_verification.md`). Outputs are written to disk in the sparkshark-com working tree but **not committed**. Per skill contract, any PR requires the 7-step PR-authority procedure and explicit Brock `go`.
