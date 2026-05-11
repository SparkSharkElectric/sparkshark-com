# Source-of-Truth Cleanup & Handoff Manifest

**Authored:** 2026-05-11 (post-inventory pass)
**Authored by:** prior Claude session, inventory-only mode (no file changes made)
**Purpose:** Hand off to a fresh session everything needed to write ONE canonical source-of-truth doc and execute cleanup of the ~50 scattered migration artifacts.

---

## TL;DR — current state of the migration

- **Verdict:** HARD NO-GO. Score 40/100 (auto-fail cap).
- **Two independent triggers:** (a) launch gate has 4 of 9 rows open, (b) `sparkshark.com` apex is attached to the **wrong Vercel project** (`spark-fsm`, not `sparkshark-com`); `www.sparkshark.com` has no project assignment at all.
- **Site itself is in good shape** — pages, redirects, schema, contact form, ST scheduler embed all verified.
- **What's missing is paperwork + the domain attachment.** Operational, not architectural.
- **Authoritative artifact today:** `audits/migration-readiness/2026-05-11-plain-english.md`. Everything else either feeds it or is downstream of it.

---

## How files are organized (the inventory)

### sparkshark-com (the marketing site repo) — 3 active migration files, 2 reference

| Path | Size | Date | Role |
|---|---|---|---|
| `audits/migrate-day-decision/2026-05-11-seed-prompt-vs-current-truth-diff.md` | 11.6 KB | 13:33 today | **Diff-only** doc — what the seed prompt said vs reality. Caveat below. |
| `audits/migration-readiness/2026-05-11.md` | 23.0 KB | 11:29 today | Full migration-auditor run, scored 40/100. Per-category breakdown. |
| `audits/migration-readiness/2026-05-11-plain-english.md` | 5.6 KB | 11:29 today | **The cleanest existing SoT** — exec-readable, action-loaded. |
| `docs/migration/launch-gate.md` | 12.2 KB | 11:03 today | Canonical 9-row gate. **5 Approved (1, 2, 3, 5, 6), 4 Not Provided (4, 7, 8, 9).** |
| `docs/migration/vercel-preview-validation.md` | 11.2 KB | May 10 | Preview-validation evidence only. |
| `vercel.json` | 4.8 KB | 07:36 today | Production config: 27 redirects, security headers, `BASE=""` build cmd. |
| `CLAUDE.md` | 20.4 KB | 07:36 today | Repo context. **Has stale "0/9 approved" line — actual is 5/9.** |

### spark-fsm/audits — 35+ HTMLs, only 1 currently relevant

The vast majority (`2026-05-07-*`, `2026-05-08-*`, `2026-05-09-*`, all `sparkshark-uiux-*`, all `sparkshark-cutover-hardening-*` versions, all `sparkshark-session-handoff-*` versions) are older UI/UX, homepage-fix, and rebuild work — superseded by what's now in sparkshark-com. Only one HTML is currently load-bearing:

| Path | Size | Date | Role |
|---|---|---|---|
| `audits/migration-risk-defense-runbook-2026-05-11.html` | 24.5 KB | 13:07 today | **6-risk mapping + pre-flip Brock/Claude queues + DNS-day-of sequence + 72-hour post-flip monitor + rollback playbook.** This IS the missing cutover-runbook content. |

### ~/.claude/plans — 1 relevant file

| Path | Size | Date | Role |
|---|---|---|---|
| `parallel-gliding-pancake.md` | 30.1 KB | May 10 | v4 Vercel migration delta plan (the doc that produced launch-gate.md). |

### ~/.claude/projects/-Users-brock/memory — 9 migration-adjacent

Existing and relevant:
- `feedback_vercel_pre_cutover_gate.md` — verify-domain-attachment-three-ways rule
- `project_sparkshark_repo_visibility.md` — repo currently public, flip to private post-launch
- `project_sparkshark_rebrand_in_place.md` — sparkshark.com = rebranded Flanco WP install
- `reference_sparkshark_wordpress.md` — WP/WPE creds + API
- `reference_godaddy.md` — DNS at GoDaddy
- `project_tech_ops_domain_split.md` — bare domain vs ssecrm.tech split
- `project_sparkshark_ai_vision.md` — vision
- `project_sparkshark_video_system.md` — video (not migration-core)
- `reference_sparkshark_api_keys.md` — keys

**Correction — diff doc citations DO exist, in session-scoped memory:**

All three live at:
```
/Users/brock/Library/Application Support/Claude/local-agent-mode-sessions/5c7680ce-9a80-46c8-a052-5c0fa27e570e/e93bec34-2ac9-47fe-a03f-fa9befd18a2e/spaces/058edfe0-0759-497c-b3bd-f801ad0a55c5/memory/
```

- `project_cutover_next_actions_2026_05_10_pt2.md` — yesterday's hardening session. Code work done in sandbox: GTM (`GTM-TBCXCXGS`) + empty `GSC_VERIFICATION_VALUE` constants added to `build.py`; contact form rewired to `/api/contact-form` (new Vercel Edge Function with honeypot + rate limit + Resend); PR-3 redirects trimmed 15→13. 6 Brock-side actions were listed; status of each as of TODAY's audit:
  - PR-1 (bethany) via `gh pr create` — **status unclear; new session must verify with `gh pr list`**.
  - Vercel env vars (RESEND_API_KEY, CONTACT_FORM_FROM, CONTACT_FORM_TO) — **DONE** (today's audit confirms all set 4h ago).
  - Resend DKIM/SPF at GoDaddy — **DONE** (LEAD-01 PASS: live email delivered to theteam@sparkshark.com today at 16:23 UTC).
  - `pr3-vercel-redirects-deploy.sh` — **DONE** (27 redirects live in `vercel.json`).
  - Gates #5/#6 screenshot renames — **DONE** (both gates Approved today).
  - Gate #8 ST scheduler smoke booking — **STILL PENDING**. **Critical: use the `sparkshark-com` main alias `sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app`, NOT `spark-fsm.vercel.app`** (the latter is the FSM dispatcher project and returns 307 at `/`).
  - GSC verification — **DEFERRED** (constant ships empty; silent emitter verified).

- `project_cutover_reality_check_2026_05_10.md` — yesterday's independent triage. Headline: NOT safe to cut DNS yesterday. HARDEN findings still relevant to verify:
  - `llms.txt` claims `4.9 across 117+` while `BRAND` + `llms-full.txt` say `4.8` — **STILL FAILING** per today's audit (RANK-08 FAIL).
  - `/moore/` had unapproved "Founder and CEO" body text — **NEW SESSION MUST VERIFY** whether this was approved or removed. Note: "Founder and CEO" IS Brock's correct title per global CLAUDE.md, but the memory flag was that the *body-text use* wasn't pre-approved.
  - `/electrical-panels/` had duplicate FAQPage JSON-LD — **NEW SESSION MUST VERIFY** whether this was deduped. Today's audit covers schema generally but didn't single this URL out.

- `project_privacy_policy_405_796_8111.md` — confirms `(405) 796-8111` on `/privacy-policy/` must be **preserved verbatim** with a `KEEP` HTML comment above it. TCPA requires opt-in number = opt-out number, so the legacy Flanco subscriber list still needs the old number reachable here. All other pages: `405-796-8111` remains forbidden. New session must verify the KEEP comment is in place in current `/privacy-policy/index.html`.

These memories are session-scoped (not canonical). The diff doc was correct to cite them; my earlier grep was incomplete because canonical memory lives at `~/.claude/projects/-Users-brock/memory/` and these are at a different root.

### /Users/brock/Downloads/migration-evidence-pack 6/ — already has its own SoT

154 files across 7 categorized folders. Three top-level summary docs already exist:
- `00_CURRENT_EVIDENCE_STATUS.md` (10.3 KB)
- `00_EVIDENCE_REVIEW_AND_CLEANUP_REPORT.md` (11.2 KB)
- `00_FILE_MANIFEST.md` (9.2 KB)

The pack is self-described. **No cleanup needed inside the pack.** The launch-gate cites it by path.

---

## KEEP — feed these into the new source-of-truth (read in this order)

1. **`audits/migration-readiness/2026-05-11-plain-english.md`** — start here. It's already the clearest summary; the SoT should be a slightly-expanded version of this.
2. **`docs/migration/launch-gate.md`** — gate row-by-row.
3. **`audits/migration-readiness/2026-05-11.md`** — full score breakdown; pull the per-category tables for the SoT.
4. **`audits/migrate-day-decision/2026-05-11-seed-prompt-vs-current-truth-diff.md`** — read for the seed-prompt diffs (helpful context for why a fresh "official" SoT is needed), but **do not trust its citations to non-existent memory files**.
5. **`/Users/brock/Projects/spark-fsm/audits/migration-risk-defense-runbook-2026-05-11.html`** — load-bearing. Contains:
   - Pre-flip Brock-owned queue (5 steps to close the gate)
   - Pre-flip Claude-owned queue (6 verification steps)
   - DNS-flip day-of sequence (5 steps)
   - Post-flip 72-hour monitor table (7 windows)
   - Rollback playbook (5 scenarios)
6. **`vercel.json`** — quote the redirect count + headers in the SoT for ground truth.
7. **`CLAUDE.md`** — for repo-context-as-of-today (and to update the stale "0/9" line).
8. **`/Users/brock/.claude/plans/parallel-gliding-pancake.md`** — read only if the SoT needs background on *why* certain choices were made (Vercel header policy, BASE flip, etc.).
9. **`/Users/brock/Downloads/migration-evidence-pack 6/00_EVIDENCE_REVIEW_AND_CLEANUP_REPORT.md`** — read only if the SoT needs evidence-pack provenance.

---

## ARCHIVE — preserve but move out of active scope

These are historical or superseded. Move them so they stop competing for attention. Recommended destination: `spark-fsm/audits/_archive/2026-05-pre-cutover/` (new folder).

**Superseded "current" docs in `/Users/brock/Projects/spark-fsm/audits/`:**

```
migration-auditor-skill-proposal-2026-05-11.html        # proposal — skill is now installed at ~/.claude/skills/migration-auditor/
sparkshark-cutover-2026-05-11-autonomous-closeout.html  # superseded by today's readiness audit
sparkshark-cutover-2026-05-11-handoff.html              # superseded
sparkshark-cutover-next-actions-2026-05-10-pt2.html     # superseded
sparkshark-cutover-reality-check-2026-05-10.html        # superseded
sparkshark-pack-vs-live-diff-2026-05-10.html            # superseded
sparkshark-vercel-migration-status-2026-05-10.html      # superseded
sparkshark-session-handoff-2026-05-10.html              # v1 — keep v4 if any
sparkshark-session-handoff-2026-05-10-v2.html           # superseded
sparkshark-session-handoff-2026-05-10-v3.html           # superseded
sparkshark-session-handoff-2026-05-10-v4.html           # latest of this series
sparkshark-cutover-hardening-sprint-2026-05-10.html     # v1
sparkshark-cutover-hardening-sprint-2026-05-10-v3.html
sparkshark-cutover-hardening-sprint-2026-05-10-v4.html
sparkshark-cutover-hardening-sprint-2026-05-10-v5.html  # latest
security-sweep-2026-05-11-pre-cutover-handoff.html      # useful security context
```

**Older work (no longer migration-relevant) in `/Users/brock/Projects/spark-fsm/audits/`:**

```
2026-05-07-homepage-broken/      (entire folder — old homepage rescue)
2026-05-07-wp-fixes/             (entire folder — old WP fixes)
2026-05-09-homepage-iterations/  (entire folder — old homepage iterations)
2026-05-10-gsc-pull/             (folder — GSC data; useful but historical)
ui-snapshots/                    (folder — old UI screenshots)
screenshots/                     (folder — generic screenshots)
2026-05-08-block-1-final.html
2026-05-08-block-1-status.html
2026-05-08-homepage-execution-master-handoff.html
2026-05-08-sparkshark-homepage-audit.html
sparkshark-rebuild-handoff-2026-05-08.html
sparkshark-rebuild-handoff-2026-05-08-v2.html
sparkshark-rebuild-research-2026-05-08.html
sparkshark-conversion-recs-2026-05-09.html
sparkshark-uiux-handoff-2026-05-08.html
sparkshark-uiux-handoff-2026-05-09.html
sparkshark-uiux-p0-patch-2026-05-09.html
sparkshark-uiux-p1a-delta-2026-05-09.html
```

**Reference research in `/Users/brock/Projects/sparkshark-com/`:**

These belong somewhere, but not at repo root competing with the live build artifacts. Recommended destination: `sparkshark-com/docs/research/`.

```
spark_shark_final_merged_seo_geo_research_document.md  (62 KB)
Perplexity Validation Report for Spark Shark SEO GEO Brief.md  (51 KB)
```

---

## DELETE — scratch with no value

Only `.DS_Store` files (macOS file-system noise). Found in:
- `/Users/brock/Projects/sparkshark-com/audits/.DS_Store`
- `/Users/brock/Projects/sparkshark-com/docs/.DS_Store`
- `/Users/brock/Projects/spark-fsm/audits/.DS_Store`
- `/Users/brock/Projects/spark-fsm/audits/screenshots/.DS_Store`
- `/Users/brock/Downloads/migration-evidence-pack 6/.DS_Store`

(Optional. They re-appear whenever Finder browses a directory. Adding `.DS_Store` to a global `~/.gitignore_global` is a better long-term fix.)

---

## What's MISSING — gaps the new SoT must address or call out

1. **`sparkshark-com/docs/migration/cutover-runbook.md` does not exist.** The readiness audit treats this as a hard fail. **The content for it exists** — it's inside the HTML runbook at `/Users/brock/Projects/spark-fsm/audits/migration-risk-defense-runbook-2026-05-11.html`. Next session should convert the HTML to markdown and commit it to the canonical path. That single action closes one of the four hard fails.
2. **Smoke script doesn't exist.** Per the audit. New session should write it (curl-loop over the 27 redirects + 21 indexed URLs on the preview alias).
3. **Typed-out DNS rollback values don't exist.** Only the 3 GoDaddy paginated screenshots from Gate #5. The HTML runbook (DNS-flip step 4) gives the apex IPs (`141.193.213.10` + `141.193.213.11`) but the full A/CNAME/MX/TXT/DKIM/DMARC values still need to be transcribed into a paste-ready block under `migration-evidence-pack 6/12-launch-and-rollback/`.
4. **Rollback trigger criteria not fully documented.** The HTML runbook has a partial table; should be reconciled with audit §8 ROLL-03/ROLL-04 findings.
5. **gitleaks not installed locally.** SEC-01 sweep can't run today. `brew install gitleaks` (decision: do it now or skip until cutover-day morning).
6. **CLAUDE.md is stale on gate count.** Says "0/9 Approved" — actually 5/9. Should be `5/9 Approved (Gates 1, 2, 3, 5, 6); 4 Not Provided (4 GBP, 7 Tracking IDs, 8 ST Scheduler test, 9 Canonical NAP)`.
7. **Domain attachment hasn't been re-checked since 16:24 UTC today.** Brock may have already moved `sparkshark-com` between teams or attached domains. Re-verify before writing the SoT score.
8. **Pre-cutover short-window GSC baseline** (last 28 days) hasn't been captured. The HTML runbook flags this as Claude-owned step 1 in the pre-flip queue.
9. **PR-1 bethany status unknown.** Memory `project_cutover_next_actions_2026_05_10_pt2.md` lists it as still-pending Brock action. New session must run `gh pr list --state all --search bethany --repo SparkSharkElectric/sparkshark-com` to confirm whether it merged.
10. **`/privacy-policy/` KEEP-comment verification.** Memory says `(405) 796-8111` on `/privacy-policy/` must be preserved verbatim with a `<!-- KEEP -->` HTML comment above it (TCPA compliance — opt-in = opt-out number for legacy Flanco subscriber list). New session must grep the live page to confirm the comment + number are both still in place.
11. **`/electrical-panels/` duplicate FAQPage JSON-LD.** Flagged yesterday in memory `project_cutover_reality_check_2026_05_10.md`. Today's audit didn't single this URL out, so status is unclear. New session must curl + grep `application/ld+json` blocks on the live preview to confirm exactly one FAQPage node.
12. **`/moore/` "Founder and CEO" body-text approval.** Flagged yesterday as unapproved body text. The title itself is correct (per global CLAUDE.md), but its appearance in body copy on the city page wasn't pre-approved. New session must verify whether it was removed, approved, or remains pending.
13. **Gate #8 ST scheduler smoke booking — alias precision matters.** Use `sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app`, NOT `spark-fsm.vercel.app`. The latter is the FSM dispatcher and returns 307 at `/`. Bookings against the wrong alias will look successful but won't reach the marketing-site code path.

---

## Step 2 — exact prompt to paste into the new session

Open a fresh Claude Code session in `/Users/brock/Projects/sparkshark-com` and paste:

> I need ONE source-of-truth doc for the sparkshark.com WordPress → Vercel migration. Don't re-run any audit. Read these 12 files in this order, then write the SoT to `docs/migration/SOURCE-OF-TRUTH.md`:
>
> 1. `audits/migration-readiness/2026-05-11-plain-english.md`
> 2. `docs/migration/launch-gate.md`
> 3. `audits/migration-readiness/2026-05-11.md` (first 200 lines for score detail)
> 4. `audits/migrate-day-decision/2026-05-11-seed-prompt-vs-current-truth-diff.md` (its memory citations are real — they live in session-scoped storage, see files 10-12 below)
> 5. `/Users/brock/Projects/spark-fsm/audits/migration-risk-defense-runbook-2026-05-11.html`
> 6. `vercel.json`
> 7. `CLAUDE.md`
> 8. `/Users/brock/.claude/plans/parallel-gliding-pancake.md` (first 60 lines only)
> 9. `/Users/brock/Downloads/migration-evidence-pack 6/00_EVIDENCE_REVIEW_AND_CLEANUP_REPORT.md`
> 10. `~/.claude/projects/-Users-brock/memory/project_cutover_next_actions_2026_05_10_pt2.md`
> 11. `~/.claude/projects/-Users-brock/memory/project_cutover_reality_check_2026_05_10.md`
> 12. `~/.claude/projects/-Users-brock/memory/project_privacy_policy_405_796_8111.md`
>
> (Files 10-12 are auto-loaded via `MEMORY.md` at session start — you'll already have them in context. Read explicitly only if MEMORY.md was truncated.)
>
> The SoT should have these sections (in this order):
> 1. **Verdict + score** (one line each).
> 2. **Top 3 blockers** with status and owner.
> 3. **What's verified ready** (bulleted).
> 4. **Brock-owned action queue** (5 items from the HTML runbook, with time estimates).
> 5. **Claude-owned action queue** (6 items from the HTML runbook).
> 6. **DNS-flip day-of sequence** (5 steps, from the HTML runbook).
> 7. **Post-flip 72-hour monitor** (table from the HTML runbook).
> 8. **Rollback playbook** (table from the HTML runbook).
> 9. **Where authoritative evidence lives** (paths only, no transcription).
> 10. **What this doc supersedes** (list every file in the ARCHIVE section of `audits/migrate-day-decision/2026-05-11-cleanup-handoff-manifest.md`).
>
> Then do these two follow-up writes:
> 1. Convert the HTML runbook to markdown and save as `docs/migration/cutover-runbook.md`. This closes one of the four hard fails in the readiness audit.
> 2. Update `CLAUDE.md` lines that say "0/9 items Approved" to "5/9 items Approved (Gates 1, 2, 3, 5, 6); 4 Not Provided (Gates 4, 7, 8, 9)". Add one line under "Current Priority" pointing to `docs/migration/SOURCE-OF-TRUTH.md`.
>
> Cleanup is **separately approved by Brock** — don't move archive files in this session. Just write the three docs above. The handoff manifest at `audits/migrate-day-decision/2026-05-11-cleanup-handoff-manifest.md` has the full ARCHIVE list for when Brock greenlights the moves.
>
> Do not invent verdicts. If a source file disagrees with another, prefer the readiness audit; flag the disagreement in a "Known discrepancies" footnote.

---

## My (this session's) decision on the HTML runbook

Brock asked me to decide what to do with `/Users/brock/Projects/spark-fsm/audits/migration-risk-defense-runbook-2026-05-11.html`.

**Decision: PROMOTE to `sparkshark-com/docs/migration/cutover-runbook.md`** (as markdown, via the next session per the prompt above). It contains the exact content the readiness audit says is missing — risk-by-risk mapping, pre-flip Brock + Claude queues, DNS-flip step sequence, post-flip 72-hour monitor, and rollback playbook. Once promoted:
- It satisfies "missing cutover-runbook" hard fail.
- The original HTML moves to `spark-fsm/audits/_archive/2026-05-pre-cutover/` along with the rest.

**Why HTML → markdown, not just move the HTML:** the launch-gate is markdown, the audits are markdown, the SoT will be markdown. Mixing one HTML into `docs/migration/` breaks git-diff readability and grep-ability.

---

## Sanity check before the new session starts

Before pasting the Step 2 prompt:

1. **Has Brock moved the sparkshark.com domain to the right Vercel project yet?** If yes, the SoT score will change. Run `vercel domains ls` first to confirm current state.
2. **Has Brock promoted any launch-gate row to Approved since 11:03 today?** If yes, gate count moves.
3. **Is the preview alias still live?** Quick curl: `curl -sI -o /dev/null -w "%{http_code}\n" https://sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app/` should return 200.

If any of those changed, mention it at the top of the new-session prompt so the SoT reflects today's reality, not 11:03's.

---

## What this manifest does NOT do

- It does NOT delete or move any file.
- It does NOT update `CLAUDE.md`'s stale "0/9" line.
- It does NOT write `cutover-runbook.md`.
- It does NOT re-run the migration auditor.

Those are all Step 2 work. This manifest is read-only inventory + decisions.

---

*End of manifest. Hand this file to the next session along with the Step 2 prompt above.*
