# Migration Readiness — Plain English — 2026-05-12

> Brock asked: "Do we really need to finish anything, or are we assuming it's not ready?" — verify the fear instead of guessing.
>
> **Answer: a little of both.** The website itself is technically ready. The *paperwork* around it isn't, and one specific code change must ship before we flip — otherwise we'll lose analytics visibility right at the moment we need it most.

---

## Today's score

**41 / 100 · HARD NO-GO** — *not* because the site would hurt rankings, but because the launch gate has Brock's handwriting missing on 4 of 9 rows. Score lifts to ~80 / 100 (GO WITH CAUTION) after ~45 minutes of your time and ~80 minutes of mine.

---

## What you should NOT be scared of (verified, not guessed)

1. **Losing rankings.** Same domain. All 21 indexed pages either kept or 301'd to a relevant page. Schema preserved. NAP frozen. Google sees the same business; only the host changes.
2. **Google "un-verifying" you.** Your GSC verification is the DNS TXT record at the apex (`1DyR8lUg…`). When DNS flips, only A records change. TXT records stay put at GoDaddy. Google keeps feeding you data the whole way through.
3. **Losing GBP reviews.** The cutover plan is "rename in place" at GBP, not "create new listing". Reviews are tied to listing identity — they stay.
4. **The new site looking broken.** Homepage 200s. Redirects work end-to-end. Contact form works (we POSTed it again at 01:38 UTC tonight and got `{"ok":true}` back). ServiceTitan scheduler renders. Phone-number link is correct on every page. Sitemap correct hostname. robots.txt allows crawlers.
5. **GoDaddy losing the domain.** Registration stays where it is. Only A records change.

---

## What you SHOULD be scared of (also verified)

### #1 — Analytics goes dark at flip moment, and we can't tell if the flip hurt us

The live WP site tracks visitors with Google Tag `GT-NGS794C2`. The new Vercel site emits a *different* tracking container (`GTM-TBCXCXGS`). If we flip DNS today, **GA4 + Google Ads conversion tracking discontinues the second the flip happens.** The site still works. The ads still fire. But we can't see whether traffic dropped, leads dropped, or everything is fine — because the measurement stream breaks.

**Fix:** one ~30-minute code change to swap the tracking container in `build.py`. Must ship before flip.

### #2 — If something looks weird at flip, the rollback is slower than it should be

Today you have screenshots of the old DNS values but not typed-out copies. Under pressure, reading hex off a phone screenshot is slow and error-prone. We also don't have a one-button smoke script — every check is eyeballed page by page.

**Fix:** two short PRs from me (~45 min combined): typed-out DNS values + the smoke script.

### #3 — Brock-only paperwork on the launch gate

Four rows of `docs/migration/launch-gate.md` say `Not Provided`. Only you can promote them to `Approved`. The underlying evidence is mostly in hand; this is your signature, not new work:

- **Gate 4: GBP screenshots** — capture 9 fields on your phone (name, phone, website URL, primary + secondary categories, services, hours, address/SAB toggle, description). ~10 min.
- **Gate 7: tracking-ids.md** — decision recorded; just author the file with `GT-NGS794C2` + the GA4 + Ads IDs already known. ~5 min.
- **Gate 8: ST scheduler smoke booking** — submit a test booking on the live alias, confirm it lands in ServiceTitan, cancel it, screenshot. ~10 min.
- **Gate 9: canonical-nap.md** — fill the template. NAP is frozen, so this is just transcribing what's already true. ~10 min.

---

## Top 3 things confirmed ready

1. **The site itself.** Schema renders, all 27 redirects resolve 301→200, indexed URLs covered, contact form delivers, scheduler renders, NAP consistent, sitemap correct, robots.txt allows crawlers.
2. **The rollback insurance.** WP Engine "Migration Backup 05-10-2026" exists. Pre-flip DNS captured in 3 screenshots. Legacy WP install stays live and restorable for as long as you want.
3. **The cutover runbook.** `docs/migration/cutover-runbook.md` exists with a 7-window post-flip monitor (0-60min through Day-30) and rollback playbook. We have a plan for the day-of.

---

## Single next action — the order that costs you the least time for the most risk-reduction

1. **YOU (5 min):** GA4 → Admin → move property `488680346` from Flanco Electric account → Spark Shark Analytics account.
2. **ME (30 min, one PR):** swap `build.py:153` from `GTM-TBCXCXGS` to `gtag.js?id=GT-NGS794C2`. Verify on preview alias. Wait for your `go`.
3. **YOU (45 min total, your phone):** capture GBP screenshots → fill `canonical-nap.md` → author `tracking-ids.md` → run ST scheduler smoke booking → promote Gates 4, 7, 8, 9 to `Approved`.
4. **ME (~45 min, two PRs):** ship `scripts/cutover-smoke.sh` + `rollback-values.md`. Fix the `llms.txt` rating drift while I'm in there.
5. **YOU (2 min):** screenshot Vercel Domains tab showing both domains `Verified` — closes the last UNVERIFIED.
6. **YOU:** re-run `/migration-audit`. Score should land in the 80s = **GO WITH CAUTION**. Then you make the call to flip DNS.

**Total time, both of us: ~2 hours of focused work. Total exposure if we flip today instead: ~$500-2,000 in lost attribution + ad-spend inefficiency for 1-2 weeks.**

---

## The honest framing

The fear that "the migration will hurt us" is mostly **not justified** by the technical evidence. Same domain, schema preserved, URLs covered, GSC verification carries through, GBP rename-in-place — all the structural defenses are already in place.

The fear that **"if something goes wrong on flip day, we won't catch it fast enough"** is partly justified — the analytics swap and the smoke-script gap mean we'd go blind at the worst possible moment. That's the part worth fixing before flip.

So: **not fear, no. But not "just flip it today" either.** A focused 2-hour push gets the score into GO WITH CAUTION territory and the analytics continuity locked in. After that, flip-day is paperwork.

---

**Full technical detail:** `audits/migration-readiness/2026-05-12.md`
**Sync to iPhone:** this file is in iCloud under `Spark Shark/spark-fsm/audits/migration-readiness/2026-05-12-plain-english.md`.
