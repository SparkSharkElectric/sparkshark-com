# Migration Readiness — 2026-05-11 — Plain English

> Refreshed at 16:24 UTC. Supersedes the 16:09 UTC version. Material change: Vercel custom-domain attachment is now a confirmed FAIL, not unverified.

## One paragraph

If you flipped DNS today, sparkshark.com would still load Vercel — but it would load the **wrong** Vercel project. The sparkshark.com domain is attached to the team that owns spark-fsm (your dispatcher), not the team that owns the marketing site. Layered on top of that, four of your nine launch-gate rows are still marked "Not Provided," the cutover runbook + smoke script + typed-out DNS rollback values don't exist yet, and `llms.txt` is the lone surface still claiming a 4.9 rating instead of 4.8. The new site itself is in great shape — pages load, redirects work, the contact form delivers, schema is intact, the phone link is consistent everywhere. What's broken is the **bridge** between DNS and the project, plus the cutover-day paperwork.

## Score

**40 out of 100. HARD NO-GO.** Two independent triggers — the launch gate has open rows, AND the Vercel domain attachment is on the wrong team. Either one alone would force HARD NO-GO; you have both.

40 is a capped score, not a measurement. The math without the cap is 42. Most points are missing because of operational paperwork (runbook, smoke script, typed-DNS), not site defects. None of the open blockers are "the site is broken."

## Top 3 things blocking cutover

1. **The Vercel domain is on the wrong team. *(New since this morning.)*** Your `sparkshark.com` domain lives in the same Vercel team as `spark-fsm` (the FSM dispatcher), and it's assigned to that project. The marketing site `sparkshark-com` is a different project in a different team — and it has zero domains attached. If DNS flipped today, customers typing sparkshark.com would land on the dispatcher, not the marketing site. Fix is a 10-minute Vercel UI move once you decide which way to consolidate.

2. **Four launch-gate rows are still "Not Provided" — only you can move them.** Three of the four (Gate 4 GBP, Gate 7 Tracking IDs, Gate 9 Canonical NAP) just need you to read the evidence already in the pack and write "Approved" in the Status cell. The fourth (Gate 8 ServiceTitan booking) needs a real new action from you: submit a test booking on the live Vercel alias `/contact-us/`, confirm it shows up in ServiceTitan, cancel it, save the screenshots. Total time on your side: roughly 90 minutes.

3. **No cutover runbook, no smoke script, no rollback triggers, no typed-out DNS values.** Four operational artifacts that should exist before flip day. The screenshots of the old DNS records exist; the values are not typed into a paste-ready block. Under rollback pressure, reading numbers off a phone screenshot is slow and error-prone. I can draft all four — about 90 minutes of my time across five single-file PRs.

## Top 3 things confirmed ready

1. **The site itself is solid.** All redirects work, all 21 indexed URLs resolve to a real page, the 4-node schema graph is intact, the phone link is consistent across every page sampled, and the contact form delivers to your Resend inbox (verified live at 16:23 UTC today). WordPress Web Rules / Rewrite Rules / Access Rules are all empty — `vercel.json` is the only redirect layer to worry about.

2. **Production secrets are in place.** RESEND_API_KEY, CONTACT_FORM_TO, CONTACT_FORM_FROM are all set on the sparkshark-com Vercel project, in production scope, set 4 hours ago. No personal-machine paths or Flanco strings bleeding through.

3. **Cutover insurance is half-captured.** WP Engine has a fresh backup labeled "Migration Backup 05-10-2026." Three DNS pagination screenshots exist. The DNS layer is recoverable from screenshots even before the typed-out values get added.

## Single next action

**Open Vercel in your browser and decide which team owns the marketing site.** Right now sparkshark.com is in `spark-shark-electric` (your spark-fsm team) and the marketing project `sparkshark-com` is in `spark-shark-electric-2b2f3a3a` (a separate team with only `sscrm.tech` attached). Pick one of:

  - **Option A:** move project `sparkshark-com` into team `spark-shark-electric`. Then attach `www.sparkshark.com` (primary) + `sparkshark.com` (apex, auto-301 to www) to the sparkshark-com project there.
  - **Option B:** move both `sparkshark.com` and `www.sparkshark.com` into team `spark-shark-electric-2b2f3a3a`. Then attach them to the sparkshark-com project there. Note: any spark-fsm subdomains (ops/agent/field/portal) would also need to come along — this option is messier.

Option A is the lighter move. Either way, it's about 10 minutes inside the Vercel dashboard, plus DNS doesn't actually need to flip until you've also closed the four open gate rows. Once you've made the move, ping me and I'll re-run `/migration-audit`. With this one fix, the score moves out of the auto-fail cap; with the gate-row promotions, it likely lands in the 70s.

## What this says about the migration overall

This is a low-drama HARD NO-GO with one new wrinkle. The wrinkle (domain attachment on the wrong team) is precisely the kind of thing the auditor was designed to catch — a "the site looks fine, but the crossover is wrong" failure mode that would have been invisible until DNS flipped. Caught today instead of cutover day = the audit paid for itself in one run.

## Where the long version lives

`audits/migration-readiness/2026-05-11.md` (in the sparkshark-com repo). Same audit, just with every check broken out, every curl command cited, and every fix sequenced.
