# Online Presence Inventory — Pre-Cutover Sweep

> **STATUS: Historical.** Cutover completed 2026-05-14. This inventory of external Spark Shark / Flanco surfaces remains useful as reference; verify current state before acting on anything still flagged for update.

**Compiled:** 2026-05-11 (read-only, Gmail + Drive only — no live-site crawl)
**Scope:** Every external surface where `sparkshark.com`, "Spark Shark Electric", "Flanco Electric", or `flancoelectricok.com` has a representation that could break, drift, or need updating when DNS flips from WP Engine to Vercel.
**Source-of-truth file:** `/Users/brock/Projects/sparkshark-com/docs/migration/SOURCE-OF-TRUTH.md` (not modified).
**Canonical NAP (from project memory):** Spark Shark Electric · Moore/OKC metro (SAB) · `(405) 436-4776` · `https://sparkshark.com/`. The 405-796-8111 number is the Flanco-legacy line, now a TCPA SMS opt-out reference allowed *only* on `/privacy-policy/`.

---

## 1. Google Business Profile (GBP)

- **Profile:** "Spark Shark Electric", `business.google.com/n/5367853091978436554` (FID `7408919064427464879`); 19 viewers/month per Apr 2026 performance report. ~8 named reviewers in last 30 days.
- **Managers:** Brock + `Spark Agent` service-account Manager added 2026-04-26.
- **Vendor management:** Strategy Zoo (Tobes + Morgan) posts GBP content on a $1,550/mo SEO retainer; auto-payments failed Apr 23-25, 2026 — relationship may be in flux.
- **Action:** Confirm GBP website URL still resolves post-flip; Gate #4 in `launch-gate.md` (GBP screenshots) still **Not Provided**.

## 2. Directory Listings & Citations

- **Yelp:** Live, claimed page; rep Jonathon Koeppel (`jkoeppel@yelp.com`) pushing "$3,240 bonus" promo May 5 + May 11. URL not captured.
- **Bing Places:** **Live as "Spark Shark Electric" since 2026-02-27** (`bp-norep@microsoft.com`). Rebrand from Flanco appears complete here.
- **Apple Maps / Business Connect:** Case **18466826**; 2026-02-13 rejection at "1033 …" address; 2026-02-16 still "unable to verify". **Apple Maps listing is NOT live.**
- **Foursquare:** Signup-code email Feb 9, 2026 — account *started*, never confirmed live.
- **Nextdoor:** Active SS Business Page in Moore; Cheyenne Pine ("Regency Park" handle) replies to recommendation asks with `SparkShark.com 405-436-4776` — correct NAP.
- **Thumbtack:** Active paid-lead source — ST dispatch 4/30 tagged `Type: Thumbtack lead cost $60.55`. URL not captured.
- **Angi:** 2025-03-21 invoice from `brian.mifflin@angi.com` — old Flanco-era relationship; current status unconfirmed.
- **BBB / Networx / HomeAdvisor / Houzz / YellowPages / Manta / Yext / Whitespark:** **No inbound emails.** Either no live profile or it's at an address brock@ doesn't own.

**Action:** Master directory spreadsheet + rotate NAP from Flanco→Spark Shark wherever a Flanco profile still lives.

## 3. Social Profiles

- **Facebook:** `facebook.com/flancoelectric` — username `flancoelectric`. **Still on legacy handle** (per `rachelhall001@gmail.com` OffPage spreadsheet, Dec 2023). Stale Drive-shared login `flancoelectricok@gmail.com / flancoelectric123` — rotate.
- **LinkedIn (Brock personal):** Active; weekly performance digest May 11.
- **LinkedIn company page / Instagram / TikTok / X / Pinterest / YouTube:** No mailbox evidence of any SS-brand admin accounts.

**Action:** Decide FB rename vs create new; reserve IG/TikTok handles; stand up LinkedIn company page.

## 4. Review Platforms (beyond GBP)

- **GBP:** ~8 named reviews/30d — strong velocity.
- **Yelp:** Reviews exist (rep references "great page"); count not captured.
- **BBB / Networx:** No emails.
- **Thumbtack:** Actively delivering paid leads — reviews/rating presumably exist.
- **Third-party review widgets on WP:** None evidenced in mailbox (live-site crawl out of scope).

**Action:** Pre-flip, screenshot Yelp + Thumbtack review counts/ratings for drift detection.

## 5. GSC, GA, GTM, Tracking IDs

- **GSC:** Both `sparkshark.com` (Domain) + `https://www.sparkshark.com/` (URL) verified since 2025-05-25.
- **New GSC owner 2026-05-05:** `sparkshark-seo-reader@fluid-emissary-493106-s2.iam.gserviceaccount.com` (Spark Agent), message-type `WNC-627102`.
- **Open GSC alert:** 2026-05-08 "**Unparsable structured data issues**" — 1 issue.
- **GTM container:** ~~`GTM-TBCXCXGS`~~ **SUPERSEDED 2026-05-11.** Per the tracking-IDs decision now captured in `SOURCE-OF-TRUTH.md` §2 + `cutover-runbook.md`: GTM is being **skipped entirely** in favor of the **unified Google Tag `GT-NGS794C2`** (Site Kit-managed). Live-tag inspection of www.sparkshark.com on 2026-05-11 found three tag IDs on the WP install — `GTM-W7V4RS7C` (Coalition-era GTM container, abandoned), `AW-17076116496` (Google Ads conversion account with label `Hf8UCO6r84cZEN7Iyq0p`), and `GT-NGS794C2` (kept). Follow-up code work: swap `build.py:153` from a GTM loader to `gtag.js?id=GT-NGS794C2` before preview reverification.
- **GA4 / Google Ads / Bing Webmaster / Microsoft Clarity:** Google Ads = `AW-17076116496` with conversion label `Hf8UCO6r84cZEN7Iyq0p`. GA4 measurement ID = the stream behind `GT-NGS794C2` (read from `migration-evidence-pack/05-ga4-data-streams.png`, the `https://sparkshark.com` stream — not the case-variant). Bing / Clarity: no measurement IDs surfaced in mailbox.
- **ServiceTitan DNI:** Live on legacy WP — `dni('init','2399891870')` from `static.servicetitan.com/marketing-ads/dni.js`. **Must be re-implemented on Vercel** or call-tracking dies at flip.

## 6. Backlinks & Inbound Mentions

- **Strategy Zoo retainer:** $1,550/mo with Tobes/Morgan; 3× payment failures Apr 23-25 — relationship may be ending. Producing "moore electrical contractors", "electrical-panels" pages; duplicate-content issue flagged 2026-04-16.
- **Coalition Technologies:** Owns WP embeds (DNI + ST Web Scheduler widget `087bee26-1d9f-41cf-9ed7-d03fdea9822f`). Needs decommission notice.
- **BigThinkers Media (`bigthinkersmedia@gmail.com`):** Two Drive sheets Jan 2024 ("Backlinks Report", "Mario Backlinks") — 100+ rows of `*.tinyblogging.com`, `*.csublogs.com`, `*.suomiblog.com` **PBN spam-tier** links pointing at `flancoelectricok.com`. Toxic profile.
- **rachelhall001@gmail.com:** "OffPage Optimization - Flancoelectricok.com (18-Dec-2023)" sheet — same PBN spam pattern; ranks tracked, mostly "Not in 100".
- **Disavow file:** No evidence one was filed.

**Action:** File `disavow.txt` for BigThinkers + rachelhall001 PBN domains in GSC before flip.

## 7. Phone / Call Tracking

- **Canonical line:** `(405) 436-4776`.
- **Legacy / TCPA line:** `(405) 796-8111` — Flanco-era; allowed verbatim only on `/privacy-policy/`.
- **ServiceTitan DNI:** Live on WP (init 2399891870). **Will not auto-port to Vercel** — re-add or call-attribution dies at flip.
- **CallRail / WhatConverts / Callbox:** No evidence. SS relies on ST DNI alone.

## 8. Email / Domain / DNS

- **Registrar:** GoDaddy, customer # 641218365; NS `ns77/78.domaincontrol.com`.
- **Host:** WP Engine install `flancoelectric` (URL `www.sparkshark.com`). Recent backups 2026-05-02, 5-06, 5-07 ("Claude Backup"), 5-08, 5-10 ("Migration Backup 05-10-2026"); multiple restores 5-06 + 5-08.
- **WPE SSH keys added 2026-05-07/08:** `brock@sparkshark.com-wpengine`, `viktor-agent@sparkshark` — rotate post-launch.
- **DMARC:** Active aggregate reporting (Google + Outlook + Yahoo/AOL) — SPF/DKIM/DMARC configured.
- **GoDaddy access:** Jordan Brannon access level updated 2026-05-02; API-key events 5-02, 5-08; product removed 2026-05-11 (content unclear).
- **Legacy `flancoelectricok.com`:** No mailbox evidence of live MX. `flancoelectricok@gmail.com` is a public Gmail. CertainPath billing still tags Brock as "Flanco Electric (aka Spark Shark) CP000283" — billing identity not renamed.

**Action:** Confirm `flancoelectricok.com` has no MX; on renewal, point it to a 301 redirect.

## 9. Schema / Structured Data

- **Self-managed:** spark-fsm `geo_facts.json` → llms.txt + canonical schema pipeline (PR #123, ADR-013 B1). `llms.txt + schema self-check` GH Action has been **failing** on PRs #136, #137, #142 — must be green before flip.
- **GSC alert:** Unparsable structured-data issue 2026-05-08 — source is current WP build.
- **Third-party schema (Yext-style):** None evidenced. SS does not appear to be paying a directory aggregator.

## 10. Third-Party Widgets / Embeds on Current WP Site

- **ServiceTitan Web Scheduler:** Live (widget `087bee26-1d9f-41cf-9ed7-d03fdea9822f`).
- **ServiceTitan DNI:** Live (§7).
- **SEOPress PRO (WP plugin):** Confirmed 2025-12-02; version-update emails through Apr 2026. Implicit decommission on static cutover — Strategy Zoo's SEO insights may stop.
- **Chat / heatmap / form widgets (Drift / Intercom / tawk / Hotjar / Clarity / FullStory / WPForms / Formspree / Gravity):** No mailbox evidence of any.

**Action:** Live-site HTML grep before flip — mailbox does not prove absence.

## 11. Migration / Cutover / Pre-Launch Checklists

- **Authoritative repo migration docs:** `SOURCE-OF-TRUTH.md`, `launch-gate.md`, `cutover-runbook.md`, `prior-seo-evidence.md`, `vercel-preview-validation.md`.
- **Active cutover work (spark-fsm PRs 138-147):** "Path C de-index/redirect target alignment", "Path D polish-sweep audit", "RED verdict cutover sprint handoffs 2026-05-11", "archive 33 pre-cutover migration HTMLs". `secret-scan / gitleaks` + `pr-checks / guardrails` workflows **failing** on several — investigate.
- **Vercel warning:** 2026-04-29 — "1 domain needs configuration on team Spark Shark Electric" — resolve before flip.
- **Brock-authored "Domination Dashboard"** (HTML, 2026-04-28) — OKC-market live-audit, not a migration checklist.

---

## Gaps / Things Still To Verify

1. **Apple Maps:** is the rejected listing (Case 18466826) ever going to be revived? If not, decision to skip iOS coverage must be explicit.
2. **Facebook page rename:** still on `facebook.com/flancoelectric`. Plan: rename in place or create new? Affects social-proof URL on the new site.
3. **Yelp profile URL:** known to exist (rep email), but URL not captured. Need it for the new-site footer/social row.
4. **BBB:** is there a profile under Flanco Electric LLC that needs renaming/closing?
5. **LinkedIn company page:** does one exist for Spark Shark? Brock's personal LI is active; company page wasn't surfaced.
6. **Disavow file status:** not filed AFAICT — BigThinkers + rachelhall001 PBN backlinks are still pointing at flancoelectricok.com.
7. **`flancoelectricok.com` domain:** registration status, MX status, current redirect behavior unknown — could quietly leak link-equity if it expires.
8. **CertainPath billing:** still references "Flanco Electric (aka Spark Shark)" — public-facing? Need to confirm.
9. **SEOPress (WP plugin) license:** PRO license $/year, owned by brock@. Cancel post-launch.
10. **GoDaddy product cancellation 2026-05-11:** what was removed? Could be relevant.
11. **GTM `GTM-TBCXCXGS` data destination:** verified loaded on Vercel preview, but the actual GA4 measurement ID it ships to has not been captured in `tracking-ids.md` — Gate #7 still **Not Provided**.
12. **Strategy Zoo relationship status:** 3× payment failures Apr 23-25 — relationship may be ending. Affects "who publishes GBP posts" post-launch.
13. **Live-site widget audit:** mailbox does not prove there are *no* heatmap/chat/form embeds — confirm via live-site HTML diff before flip.
14. **`Spark Shark.zip` (Drive):** 48 MB zip in flancoelectric@gmail.com Drive (id `1V4CsYs2QgMGR-Co6hUFkkrKaek3wracf`) — likely brand-asset bundle; not opened (binary, behind a separate Google account).

---

**Authored:** 2026-05-11 from Brock-only inbox + Drive evidence. Not a substitute for a live-site crawl; complements it.
