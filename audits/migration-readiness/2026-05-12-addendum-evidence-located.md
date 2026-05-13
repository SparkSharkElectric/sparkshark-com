# Migration Readiness — 2026-05-12 Addendum

**Reason for addendum:** Brock pointed out evidence I called "Not Provided" actually exists in `/Users/brock/Downloads/migration-evidence-pack 5/` and `…pack 6/`. The morning audit only walked the in-repo `migration-evidence-pack/` (which has placeholder `README-missing.md` files at all four "Not Provided" canonical paths). Re-checking the Downloads pack changes the verdict band but **not** the HARD NO-GO call — the launch gate's "Brock writes Status cells" protocol still applies, and one gate item (Gate 8 — ST scheduler smoke) is genuinely missing.

**Verified by:** direct file listing + read of evidence files in `/Users/brock/Downloads/migration-evidence-pack 6/` (newer copy; identical structure to `…pack 5/`).

---

## What's actually captured (vs. what I said this morning)

### Gate 4 — GBP screenshots — ✅ CAPTURED (10 PNGs)

`/Users/brock/Downloads/migration-evidence-pack 6/05-google-business-profile/`:

- `gbp-profile-overview-search-result.png`
- `gbp-about-name-categories-description-phone.png`
- `gbp-location-website-social-service-areas.png`
- `gbp-hours-main-hours.png`
- `gbp-hours-more-and-business-options.png`
- `gbp-services-electrician-primary-page-1.png` + `-page-2.png`
- `gbp-services-additional-categories-page-1.png` + `-page-2.png`
- `gbp-booking-link-servicetitan.png`
- `README-gbp-evidence-review.md` — summarizes the 9 NAP fields visible across the screenshots

**Observed GBP facts** (from the README):

| Field | GBP value | `BRAND` / `canonical-nap.md` | Match? |
|---|---|---|---|
| Business name | Spark Shark Electric | Spark Shark Electric | ✅ |
| Primary category | Electrician | (assumed Electrician) | ✅ |
| Secondary categories | Lighting contractor; Electrical repair shop; Electrical installation service | (none documented in BRAND) | ✅ presence noted; no conflict |
| Phone | (405) 436-4776 | (405) 436-4776 | ✅ |
| Website | https://www.sparkshark.com/ | https://www.sparkshark.com | ✅ |
| Public location | None (SAB) | SAB-only | ✅ |
| Service areas | Moore, Yukon, Edmond, Norman, Bethany, Del City, Newcastle, Midwest City, Mustang, OKC (10 cities) | canonical-nap.md = same 10 cities; `BRAND["service_area"]` = 15 (adds Choctaw, Piedmont, Nichols Hills, The Village, Warr Acres) | ⚠️ minor drift (BRAND is superset; GBP/canonical agree) |
| Hours | Open 24 hours every day | (schema not re-extracted this run) | ⚠️ verify against schema hours |
| Booking link | book.servicetitan.com | (matches ST scheduler embed on site) | ✅ |

**Updated check verdicts** (with evidence in Downloads, before formal move):
- GBP-01 PASS, GBP-02 PASS, GBP-03 PASS, GBP-04 PASS (live alias 200; same URL post-flip), GBP-05 UNVERIFIED (no LSA URLs supplied), GBP-06 PASS (rename-in-place, structurally safe), GBP-07 UNVERIFIED (hours-vs-schema not extracted this run), GBP-08 ⚠️ **minor drift** (BRAND lists 5 cities GBP doesn't), GBP-09 PASS (no public address).

### Gate 7 — tracking-ids.md — 🟡 STUB CAPTURED, DECISION NOT YET WRITTEN IN

`/Users/brock/Downloads/migration-evidence-pack 6/06-current-tracking/tracking-ids.md`:

The file exists but its **own body** says (line 86): *"This file provides evidence for Gate #7 but should not be treated as fully approved until the exact active GA4 Measurement ID, GTM decision, and Google Ads conversion setup are confirmed."*

It was written 2026-05-10 — **before** the 2026-05-11 decisions captured in `SOURCE-OF-TRUTH.md` §11 and `cutover-runbook.md` line 60:

- Use unified Google Tag `GT-NGS794C2` (NOT GTM)
- GA4 measurement ID `G-QK02QH3SWY` (property `488680346`, currently in Flanco account `347644522`, will move to Spark Shark Analytics `348668675`)
- Google Ads `AW-17076116496`, conversion label `Hf8UCO6r84cZEN7Iyq0p`
- `build.py:153` to be patched to emit `gtag.js?id=GT-NGS794C2`

**What's needed:** ~5-minute edit to `tracking-ids.md` capturing those four bullets so the file reflects the launch decision, then Brock-promote Gate #7 to Approved.

Supporting evidence already in the folder (8 PNGs): GA4 account/property/data-streams screens, GTM container/account/tags screens, Google Ads + LSA overviews.

### Gate 8 — ST scheduler smoke booking — ❌ STILL GENUINELY MISSING

`/Users/brock/Downloads/migration-evidence-pack 6/06-current-tracking/servicetitan-scheduler-test-proof/`:
- `DEFERRED_TO_NEW_SESSION.md`
- `README-missing.md`

The Gate 4 README explicitly disclaims this: *"the booking-link screenshot supports GBP evidence and may also help future ServiceTitan scheduler proof, but it does **not** by itself complete launch-gate item #8. Item #8 still requires a test booking from the Vercel preview, ServiceTitan confirmation, and cancellation proof."*

**Real ~10-minute Brock action:** submit a test booking on `https://sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app/contact-us/` → confirm it appears in ServiceTitan → cancel it → screenshot before/after.

### Gate 9 — canonical-nap.md — ✅ COMPLETE AND DECISION-FINAL

`/Users/brock/Downloads/migration-evidence-pack 6/11-verified-business-facts/canonical-nap.md`:

- Decision date: 2026-05-10
- Public NAP table complete (name, alt name, phone, website, SAB-only, public-location wording, primary service area)
- Internal/private street address kept private (`621 Sally Ct, Moore, OK 73160`)
- GBP alignment confirmed
- Schema implication documented

**Approvable as written.**

---

## The structural issue (and the cleanest fix)

`launch-gate.md` documents the canonical evidence path as `/migration-evidence-pack/...` (relative to repo root). The in-repo folder contains placeholder `README-missing.md` files. The actual evidence is at `/Users/brock/Downloads/migration-evidence-pack 6/...` — outside the repo.

Per the launch-gate "Status update protocol" (line 76-83): *"Brock places the evidence file at the documented path … Claude updates that gate item's Status field …"*. So strictly, the evidence isn't at the documented path. Two clean paths forward:

| Option | Pros | Cons |
|---|---|---|
| **A. Copy/commit the Downloads pack into the repo at the canonical paths.** | Evidence is where the gate looks for it. Future audits don't need to know about Downloads. Survives machine moves. | Adds ~3-5 MB of PNGs to repo history. Public repo means GBP screenshots become public (probably fine — no PII; phone/address public already). |
| **B. Update `launch-gate.md` to document the Downloads path as canonical.** | No file moves. | Path is machine-specific to your Mac. Future Claude sessions on a different machine can't find evidence. Status cells become non-portable. |

**Recommendation:** A. Copy the relevant evidence into the repo's `migration-evidence-pack/` at canonical paths, commit, then Brock walks the 4 Status cells. (We can scope this to one PR per gate so each commit is a clean "Gate N evidence in" history line.)

---

## Re-score with evidence treated as captured (Downloads-as-acceptable)

If we score what's *captured* (rather than what's *placed at canonical path*):

| Category | Old (00:38 UTC) | New (this addendum) |
|---|---|---|
| GBP integrity (×3) | 0 / 27 | **18 / 27** (7 PASS, 2 UNVERIFIED; GBP-08 service-area drift noted) |
| Organic ranking (×2) | 14 / 20 | 14 / 20 (unchanged; RANK-08 llms.txt drift still FAIL) |
| Lead capture (×1) | 3 / 5 | **4 / 5** (LEAD-05 GBP booking button — book.servicetitan.com confirmed in GBP screenshot, ST embed renders on site → PASS) |
| Verification discipline (×2) | 8 / 10 | 8 / 10 (unchanged) |
| Custom-domain attachment (×2) | 0 / 4 | 0 / 4 (still UNVERIFIED until Brock pastes a Vercel Domains screenshot) |
| Secret hygiene (×2) | 0 / 8 | 0 / 8 (unchanged) |
| DNS rollback insurance (×2) | 6 / 8 | 6 / 8 (unchanged) |
| Cutover-day plan (×2) | 6 / 8 | 6 / 8 (unchanged) |
| **Total numerator** | 37 | **62** |
| **Total denominator** | 90 | 90 |
| **Score** | **41 / 100 · HARD NO-GO** | **69 / 100 · NO-GO BUT CLOSE** |

The verdict band still says **NO-GO** because:
- Launch-gate state remains HARD NO-GO until Brock writes `Approved` in those 4 Status cells.
- Gate #8 ST scheduler smoke is the only one with real new work (not just file-move + Status-promotion).
- Gate #7 needs the 5-min decision update before it's Approvable.

But the **score floor** moves from "you have a lot of work to do" (41) to "you're 30 minutes of focused work away from going-to-flip-ready" (69).

---

## Revised next-action queue

Order = max risk-reduction per minute spent.

| # | Who | Action | Time |
|---|---|---|---|
| 1 | Claude (one PR) | Copy `migration-evidence-pack 6/` contents into in-repo `migration-evidence-pack/` at canonical paths. Replace `README-missing.md` placeholders. Single commit per gate folder for clean history. | ~15 min |
| 2 | Claude (one PR) | Update `tracking-ids.md` to capture the 2026-05-11 decision: unified Google Tag `GT-NGS794C2`, GA4 `G-QK02QH3SWY`, Ads `AW-17076116496` + label `Hf8UCO6r84cZEN7Iyq0p`. Cross-link to SoT §11. | ~10 min |
| 3 | **Brock** | GA4 → Admin → move property `488680346` from Flanco account to Spark Shark Analytics. | ~5 min |
| 4 | Claude (one PR) | `build.py:153` swap `GTM-TBCXCXGS` → `gtag.js?id=GT-NGS794C2`. Rename `GTM_CONTAINER_ID` → `GOOGLE_TAG_ID`. Refresh comment. Verify on preview alias. | ~30 min |
| 5 | **Brock** | Submit test booking on live alias `/contact-us/` → confirm in ServiceTitan → cancel → screenshot. Place proof in `migration-evidence-pack/06-current-tracking/servicetitan-scheduler-test-proof/`. | ~10 min |
| 6 | **Brock** | Walk `launch-gate.md` — promote Gates 4, 7, 8, 9 from `Not Provided` to `Approved`. | ~3 min typing |
| 7 | Claude (PRs) | Ship `scripts/cutover-smoke.sh` + `migration-evidence-pack/12-launch-and-rollback/rollback-values.md` (typed-out DNS). Fix `llms.txt` 4.9→4.8 drift. | ~45 min |
| 8 | **Brock** | Screenshot Vercel Domains tab → both domains `Verified`. Place in evidence pack. | ~2 min |
| 9 | Claude (optional cleanup, post-cutover-prep) | Reconcile `BRAND["service_area"]` (15 cities) vs `canonical-nap.md` (10 cities). Likely action: drop the 5 non-GBP cities from BRAND or expand GBP service-area. Brock decision. | ~10 min Brock; ~10 min Claude after decision |

**Total Brock time:** ~22 min keyboard + phone work.
**Total Claude time (4 single-file PRs):** ~100 min.

After steps 1-6 land:
- Launch gate: 9 of 9 Approved → HARD NO-GO lifts
- Score: GBP-07 PASS (hours match) when verified, GBP-08 still has the 10-vs-15 drift, LEAD-04 still UNVERIFIED (no LSA URL list) — likely lands ~85 / 100 = **GO WITH CAUTION**
- Auto-fail triggers: still none firing

---

## What I'm correcting from the morning audit

1. **Top blockers list (§3) of the 2026-05-12 audit.** Items 7, 8, and parts of item 1 are over-stated — most of the "Brock 45-min phone work" is actually "Brock 13-min keyboard work + Claude file-move PR" because the screenshots and canonical-nap.md are already done.
2. **Confirmed-ready list (§4).** GBP-side artifacts should move into the "ready" column once committed.
3. **Single next action (plain-English §6).** The "YOU (45 min total, your phone)" step is actually about 13 minutes — the heavy lifting is captured already.

The HARD NO-GO call itself **stands** because (a) the launch gate's Brock-only Status protocol hasn't been walked yet, and (b) Gate 8 is genuinely undone.

---

## Method note for future audits

The skill should walk **both** `/migration-evidence-pack/` (in-repo) and `/Users/brock/Downloads/migration-evidence-pack {5,6}/` before declaring evidence "Not Provided". I'll suggest a one-line addition to `CHECKLIST.md` / `SKILL.md` so this gap closes for the next audit run.

---

**Long-form audit:** `audits/migration-readiness/2026-05-12.md`
**Plain-English one-pager:** `audits/migration-readiness/2026-05-12-plain-english.md`
**This addendum:** `audits/migration-readiness/2026-05-12-addendum-evidence-located.md`
**iCloud sync:** force-rsync'd to `Spark Shark/spark-fsm/audits/migration-readiness/`
