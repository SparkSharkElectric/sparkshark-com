# Coalition Technologies — Pre-Cutover Findings

> **STATUS: Historical.** Cutover completed 2026-05-14. This pre-cutover SEO research remains useful as reference; the "pre-cutover" framing is now historical.

**Source:** Gmail dig of `brock@sparkshark.com`, 2026-05-11.
**Engagement basis:** Basecamp project "BSF Investment Group, LLC DBA Spark Shark // Joint // SEO & Local PPC" (Basecamp ID 3140673, bucket 40751486). All Basecamp to-do content below is preserved from email snippets and verbatim-quoted plaintext; full to-do bodies live behind Basecamp URLs we can no longer access post-cancellation.
**Read-only audit. No site changes proposed here.**

## 1. Engagement timeline & scope

- **Pre-history (≤ Mar 2025):** Prior engagement under brand "Flanco Electric." Brand swap to "Spark Shark Electric" handed off via Drive ZIP on 2025-03-21 / 2025-03-25 (Caroline Giercyk, Doug Drenkow). Strategy doc on file from that era: **`Flanco Electric-Marketing-Strategy-01152025 (2).pdf`** (attached to the "Coalition Data/Stuff" Dec 2025 thread).
- **Pause:** Services paused after May 15, 2025 invoice for non-payment (Doug Drenkow, 2025-06-24 / 2025-08-15). No work performed June–mid-September 2025.
- **Restart (Sept 15, 2025):** Brock re-engaged. Sept 19 "Updated KPIs and Campaign Next Steps" call set the new program scope: SEO + Local PPC, $3,800/mo invoice (CT-018980 Nov, CT-018981 Dec confirmed in Gmail). Stated KPI baseline: **35 quality leads/month, $1,200 avg lead value, $30-40k/month revenue from website + ads**; results-timeline expectation set to **"more substantial traction beginning around months 9–12"** (Maggie Chambers, 2025-09-23 thread). Basecamp project carried over the old "Flanco Electric" name until October — first message that uses "Spark Shark" in the Basecamp DBA label appears around 2025-10-28.
- **Active build:** Oct 13 – Dec 16, 2025 (~9 weeks). Bi-weekly alignment calls (Caroline & Jaco; Maggie / Joel Gerstman on escalations). PDFs in our possession: `Alignment Call Notes - 10-31-2025.pdf`, `Alignment Call Notes - 11-18-2025 (2).pdf`, `Alignment Call Notes - Spark Shark.pdf` (12/01/2025), and the October 2025 Campaign Report PDF + Client Dashboard.
- **Cancellation:** Brock/Seth verbally cancelled on Dec 16, 2025. Coalition's same-day written response (Jaco Cilliers, "Following Up on Campaign Results and Cancellation Notice") notes: "The agreement requires 30 days written notice prior to the billing period for which the cancellation goes into effect… services would complete as of January 15, 2026." Final follow-up Zoom held Dec 22, 2025. Basecamp digests continued to fire through 2026-02-02 with 3 open to-dos still assigned to Brock/Seth (no Coalition-side activity after Jan 6).
- **Scope per the Sept 19 thread:** "Confirming access → Updated Technical Analysis → Building Your Strategy" (3-month plan, front-loaded). The "Updated Technical Analysis" appears to have been delivered as the **Initial SEO Report** referenced by Jaco in the cancellation email (we do **not** have a copy in Gmail — Basecamp-only deliverable, now likely behind cancelled access).

## 2. Link-building deliverables (legit backlinks built)

This is the area with the **least extractable evidence**. The Basecamp project had a dedicated **"Link Building"** column, and a Nov 1 daily digest confirms "1 to-do was created on: Link Building" with another checked off Nov 3. The only Link-Building to-do whose subject we can see in Gmail is **[For Review] Operating Hours** (Jaco, 2025-11-01) — read as a citation/listing operating-hours-confirmation step, not an actual link.

No emails name a built referring domain, no anchor-text list, no "live link" notification ever crossed Gmail. The Nov 18 call notes mention **"Provide author bio and headshot for link-building (photo appointment scheduled)"** as a Brock to-do — implying Coalition's link build was author-bio / guest-byline based, but **we have zero evidence any guest posts went live**. The Oct 2025 Campaign Report PDF (attached to the Nov 14 report email) is the most likely place a backlink count would appear; **read that PDF first** before assuming Coalition built nothing.

**Migration implication:** Conservatively assume **0–5 placed backlinks**. None of the listed redirects in `vercel.json` should break a Coalition-built link unless we discover one pointing at a deep URL during the 11-section attachment audit. **No disavow file, no toxic-link audit, no link cleanup** was ever mentioned in Gmail — so we do not need to carry one over.

## 3. On-page / copy work shipped to the legacy WP site

Coalition delivered **at least 5 numbered copy batches** to the WordPress install (sparkshark.com on WP Engine). We have Gmail evidence of Batches #4 and #5 explicitly; Batches #1–#3 were never named in Gmail subject lines — they happened earlier (pre-restart and/or in Basecamp-only).

- **Copy Batch #4** — assigned 2025-11-13 (Jaco), reviewed/edited Nov 22 ("our designer is ready to…"), approved 2025-11-27. Internal comment 2025-11-27 from Jaco: "Yes, that can just be removed on Wordpress, it's no problem" — confirms direct WP edits, not staging.
- **Copy Batch #5** — assigned 2025-12-20 (Jaco), approved by Seth on 2025-12-26 (Basecamp "Seth F. completed a to-do! Copy ✓ [For Review] Copy Batch #5"). Joel Gerstman commented Dec 24.
- **Specific shipped pages:**
  - `https://www.sparkshark.com/contact-us/` — **new embedded contact form went live 2025-11-20** (Jaco, "🏆 New Contact Form Live on Contact Us Page"). Brock tested it: "I sent a test through and it worked." Submissions flow → unknown handler (most likely WP/SEOPress contact form; verify in WP admin before flipping DNS).
  - **Privacy Policy** and **Terms & Conditions** — Coalition switched from Termly's hosted policy embed to the **HTML embed format** on 2025-10-24 (Maggie Chambers thread), so the policies now live on-domain at sparkshark.com under WP. This was done to satisfy **ServiceTitan brand registration** (Privacy Policy needed STOP/CANCEL/UNSUBSCRIBE language; T&Cs needed message types, frequency, HELP keyword). Contact Us page also got a disclosure snippet.
  - **Main navigation** — sticky menu + "Contact" CTA button shipped 2025-10-28 (Jaco, "🏆 Main navigation updates are live").
  - **Announcement Bar** — shipped 2026-01-06 by Jaco AFTER cancellation notice but inside the wind-down billing window: "the Announcement Bar Optimization is live on your website. We normally see quick results with these in LLMS, so we will keep an eye out…" (Note: "LLMS" = LLM search visibility — Coalition was already optimizing for AI-search retrieval.)
  - Site-wide hours, footer NAP, etc. — implied by the "Operating Hours" review to-do under Link Building, but no diff posted to Gmail.

**Migration implication:** The **static repo must contain final-state copies of every page Coalition edited** — at minimum: Contact Us (with form), Privacy Policy (HTML-embedded), Terms & Conditions, Home/main nav, and the announcement bar text. Spot-check each against the live WP version before DNS cutover — the static export may pre-date Coalition's edits.

## 4. Technical SEO changes (redirects, robots, sitemap, schema)

- **SEOPress Pro plugin update** — Coalition asked Brock for the SEOPress Pro license key on 2025-11-27 (Jaco, private to-do). Brock supplied it on 2025-12-02 ("Here is is. Let me know if you need login or anything else"). They updated the plugin; this means **SEOPress was Coalition's on-page SEO / sitemap / schema engine on the WP install**. On the static migration, SEOPress meta titles/descriptions/schema are not portable — they live in WP DB. If any per-page meta/schema was tuned by Coalition between Nov 27 and Dec 16, it exists only in WP and **must be exported manually** before cutover or those edits die with WP.
- **No redirect rules, no robots.txt edit, no sitemap.xml change, no canonical-tag change, no JSON-LD additions** were ever named in Gmail. Coalition's stated approach was front-load highest-impact items — those would have shown up in alignment-call notes; the call PDFs are the place to verify.
- **No disavow file** ever mentioned.

**Migration implication for `vercel.json`:** The 27 redirects in the static repo were NOT authored by Coalition. Risk that we break a Coalition-built deep link is low. Higher risk: SEOPress was generating XML sitemaps at `/sitemap.xml`; the static site must serve an equivalent sitemap or GSC will report 0 indexable pages within days.

## 5. Tracking + analytics + third-party widgets installed

- **ServiceTitan DNI (Dynamic Number Insertion)** — Brock sent the snippet on 2025-10-31 ("Web form for SparkShark.com" thread). Jaco confirmed Nov 4: *"this snippet is actually for Dynamic Number Insertion (DNI), which is used to track call sources by dynamically swapping the phone number on the site."* DNI snippet was installed on the WP site. Brock followed up Nov 5 with the **Web Scheduler** script (separate ServiceTitan widget) and Jaco passed it to the dev team. **Both ServiceTitan widgets are on the live WP install today.** Static-repo migration must port both `<script>` blocks verbatim (in `<body>` per Brock's email).
- **GA4 + Google Ads + ServiceTitan integration** — Caroline assigned "[Follow-Up] Service Titan - Google Ads and GA4 Integration" on 2025-12-02; Seth completed it 2025-12-26 (post-cancellation). Implies the **GA4 ↔ Google Ads conversion link via ServiceTitan** was wired during the wind-down — verify which GA4 property/measurement ID is on the WP site today and that it matches the one in `tracking-ids.md`.
- **"Update on Analytics & Tracking"** to-do (Jaco, 2025-11-22) — still **OPEN as of Feb 2, 2026** in the last Basecamp digest. The snippet body, per the assignment notification, reads "Quick update on the analytics…" — body not preserved in Gmail. This is the single most important Basecamp to-do to recover before DNS flip; it likely contains the GA4/GTM/conversion-event configuration Coalition put in place.
- **Nov 18 call notes Jaco action item:** *"Investigate and restore accurate conversion tracking related to 'Customer Reach Out' calls in CRM/Google Analytics"* — confirms there was a **broken conversion-tracking pipeline** Coalition was actively diagnosing. Status at cancellation: unknown.
- **No CallRail, no WhatConverts, no chat widget, no Hotjar, no pixel beyond GA4/Google Ads** mentioned anywhere in Gmail.

## 6. Citations, NAP, GBP, directory work

- **GBP review removal** — Maggie Chambers thread 2025-09-23: Coalition agreed to file removal requests on **the 1-star "fake" GBP reviews Brock identified**. No confirmation in Gmail that any were actually removed.
- **"Operating Hours" review** — Nov 1 Jaco to-do under "Link Building" column. Implies a directory/citation NAP update sweep was queued (most directory citation tools file hours as part of NAP). No "X citations updated" report ever sent.
- **Nov 18 call notes Jaco action item:** *"Follow up on the local SEO issue regarding the incorrect 'Sparkshark' presence and review misattribution"* — implies a **duplicate or wrong-NAP listing somewhere** (Yelp/Bing Places/Apple Maps?) was being investigated. Status at cancellation: unknown. Cross-reference with `canonical-nap.md` Gate #9.

## 7. Audit findings (fixed vs open)

Coalition never sent a written "site audit findings" doc through email. The **Initial SEO Report** referenced in the Dec 16 cancellation email is the closest equivalent — *"we discussed in our Initial SEO Report call"* — but the report itself is in Basecamp, not email. The **`Flanco Electric-Marketing-Strategy-01152025 (2).pdf`** attachment may double as the strategy doc that anchored audit findings; **read this PDF for the audit list.**

Visible-in-Gmail findings Coalition raised or fixed:

- Sticky nav + Contact CTA — fixed Oct 28.
- Embedded contact form — shipped Nov 20.
- Privacy/T&Cs ServiceTitan compliance — fixed Oct 24.
- "Customer Reach Out" conversion-tracking break — flagged Nov 18, status unknown.
- Local SEO "Sparkshark" misattribution — flagged Nov 18, status unknown.
- Image best practices for SEO — reference doc Caroline pushed Dec 8 ("[For Reference] Image Best Practices for SEO"), still open as a Brock/Seth to-do through Feb 2, 2026 — implies images on the legacy WP site likely need alt-text / compression / WebP work. The static repo's images should be audited against this before flip.
- Announcement Bar (for LLMS / AI-search visibility) — shipped Jan 6, 2026.

## 8. Identifier / credential handoffs (still-active accesses to revoke)

Confirmed Coalition received and likely still has:

- **WordPress admin access** to sparkshark.com (used for all copy batches, plugin updates, ServiceTitan script installs, contact form, announcement bar).
- **SEOPress Pro license key** — sent by Brock 2025-12-02 in Basecamp boost.
- **Termly.io login** — Nikka emailed login screenshot 2025-10-24; Maggie confirmed access. **Rotate this password immediately.**
- **ServiceTitan access** — Jaco's 2025-11-07 to-do "[Access Required] ServiceTitan." Marked complete 2025-11-13 → they had ST access for ~5 weeks. **Audit ST users → revoke any Coalition email.**
- **On-domain email access** — "Confirm Recovery Options for On Domain Email Access" (private to-do, Nov 26 → completed Nov 27). Coalition had **at least one mailbox @sparkshark.com** (most likely for SEO/sender-reputation purposes). **Audit Google Workspace users → remove.**
- **Google Ads account access** (PPC was live; CPC averaging $13, CPA $54, ~$2,150 Nov spend, $3,000 approved monthly budget) — revoke.
- **GA4 property access** — implied via the GA4 integration to-do.
- **GBP manager access** — implied via the review-removal work.
- **Search Console access** — not explicitly confirmed in Gmail but standard for SEO scope; assume yes and verify.
- **Basecamp project access** — Coalition controls; Brock/Seth lose access on their schedule.

**Action:** Sweep all eight systems above against the Coalition contact roster (Jaco Cilliers, Caroline Giercyk, Maggie Chambers, Doug Drenkow, Joel Gerstman, Joel Gerstman, Sierra Lee, Rebecca Fairbanks, anything `@coalitiontechnologies.com`). Update `tracking-ids.md` (Gate #7) with the audited list.

## 9. October 2025 Campaign Report — verbatim metrics

From the Nov 14, 2025 email body (`Spark Shark | October 2025 Campaign Report`):

> Overall Metrics:
> - Total Sessions: **596** (Increased by **▲284.52%** MoM)
> - Total New Users: **477** (Increased by **▲448.28%** MoM)

Full report lives at `https://scoretask.coalitiontechnologies.com/dashboard/FhqrbC9ImJbbPDljYDd3TswbcJXVqcI7koGeKxkm` (likely revoked post-cancellation) and as PDF attachment **`Client Dashboard Fixed Period Report.pdf`**.

From the Dec 16 cancellation email (last-30-days PPC, verbatim):

> average cost per click down to around **$13** … average CPA of **$54** … In the month of November, for example, we spent approximately **$2,150** … approved budget of **$3,000/month**.

Plus an SEMrush "overall keyword rankings" trend chart and a GSC organic clicks/impressions uptrend chart (both inline images, both need to be re-extracted from the email if we want the actual numbers).

## 10. Cancellation aftermath & deliverables still owed

- **Final billable day:** January 15, 2026, per Coalition's 30-day clause.
- **Dec 22, 2025 follow-up Zoom** — held with Joel Gerstman (Director of Marketing) added. Outcome: Brock/Seth confirmed cancellation; no save attempt accepted.
- **Open Basecamp to-dos still assigned to Brock/Seth after cancellation** (per Feb 2, 2026 Basecamp digest, the last one received):
  1. `[Action Required] Update on Analytics & Tracking` — **most important to recover before DNS flip.**
  2. `LinkedIn` — appears to be Coalition pushing Brock to post.
  3. `[For Reference] Image Best Practices for SEO` — reference doc, low urgency.
- **Nothing was contractually owed back to us** — Coalition's contract (`Coalition Contract.pdf`, in Brock's "Coalition Contract" Dec 2 thread) governs return of deliverables; that PDF needs reading before we assert anything about IP / report ownership.
- **Holiday-period escalation procedure** (Dec 23 email) — irrelevant post-Jan 15.

## 11. Attachments NOT YET extracted → queue for Drive folder `1DUKcmrQyK9RVpk3ySu-53zBsOTZaD2ae`

The SEO Attachments Drive folder is currently **empty**. Files to copy in (next session):

1. `Client Dashboard Fixed Period Report.pdf` — October 2025 campaign report. Email: `19a80e1184bcb8bf` (Nov 14, 2025, Jaco). **Highest priority — contains the only quantified Coalition output we have.**
2. `3.png` — overall-metrics chart inline-attached to same Oct report email.
3. `Coalition Contract.pdf` — Email: `19ae0ac8469440f6` (Brock → Seth, Dec 2). **Read for IP / deliverable retention clauses.**
4. `Flanco Electric-Marketing-Strategy-01152025 (2).pdf` — Email: `19b03c5306fe2be3` ("Coalition Data/Stuff," Brock → Seth, Dec 9). Likely contains the original SEO audit + keyword strategy. **Highest priority for audit findings.**
5. `Alignment Call Notes - 10-31-2025.pdf` (and duplicate `(1).pdf`) — same Dec 9 thread.
6. `Alignment Call Notes - 11-18-2025 (2).pdf` — same Dec 9 thread. Names action items: *restore Customer Reach Out conversion tracking; fix Sparkshark misattribution; provide author bio for link-building.*
7. `Alignment Call Notes - Spark Shark.pdf` — 12/01/2025 Basecamp message ID 9342547324, referenced in email `19ae0b92ae6f562a`. **Last alignment-call notes before cancellation — most likely to list any uncompleted on-page work.**
8. `Screenshot 2025-09-23 at 9.00.41 AM.png` — Maggie's "typical results timeline" chart (Email `19976fd75006554c`).
9. 3× inline `image.png` attachments from the cancellation email `19b2979d5576bf2c` — GSC organic clicks/impressions uptrend, SEMrush keyword-ranking uptrend, Jaco's email-signature image.
10. `image.png` from the Jan 6 Announcement Bar Optimization email `19b91af1c304f90f`.
11. `image.png` from Nov 20 Contact Form Live email `19aa3102623972d4` (screenshot of new form).
12. `image.png` from Oct 28 Main Navigation Live email `19a2ba5a673e697b` (screenshot of new nav).

12 attachments total. After extraction → Drive folder `1DUKcmrQyK9RVpk3ySu-53zBsOTZaD2ae` → re-read in a fresh session and merge findings back here.
