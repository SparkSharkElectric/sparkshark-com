# Backlink Capture — Session 4 → (done) Handoff

**Written:** 2026-05-12. **Status: workstream COMPLETE — backlink list stamped FINAL.** This is the last handoff; there is no Session 5 for this workstream. Remaining items are Brock-actions / post-launch and tracked in §3 + `BACKLINK-SUMMARY.md` §4.

**Read order if you're picking this up cold:**
1. This file.
2. `BACKLINK-SUMMARY.md` — the live (now final) state of everything.
3. `master-backlinks-final.csv` — 145 rows / 129 unique referring domains, canonical.
4. `wpe-access-log-snapshot-2026-05-12.md` — what WPE access logs do and don't give you (read this before anyone tries to "re-pull WPE logs" thinking they'll get more).
5. Cross-doc: `../../docs/migration/SOURCE-OF-TRUTH.md` (still the canonical migration doc).

---

## 1) What Session 4 did

| # | Task | Result |
|---|---|---|
| 1 | **WP Engine access-log pull** (the last unrun source) | Done. Mechanism confirmed: **(a)** WPE Public API has no logs endpoint (swagger enumerated — only used it to confirm the install: `flancoelectric`, prod, `www.sparkshark.com`); **(b)** WPE SSH Gateway exposes no web access logs (`~/logs/`, `/var/log/nginx`, `/var/log/apache2` absent — connected fine with the 1Password SSH key, just nothing there); **(c)** the User Portal feed `site_logs_feed_data?environment=nginx` is the only source and returns just the **last ~1,500 requests** (≈13 h on this bot-heavy site). **There is no 90-day access-log archive at WPE.** Snapshot pulled 2026-05-12 03:15 UTC. |
| 2 | **Extract + filter + merge** | 27 unique referers in the snapshot; 24 self-referrals; **3 external hosts** — `google.com` ×4 (SERP/bot, not a backlink), `l.facebook.com` ×1 (corroborates the existing `facebook.com` row, consistent with `fbclid` self-referrals), `t.co` ×1 (corroborates `twitter.com`/`x.com`). **Zero new referring domains; zero new editorial backlinks.** Brand-collision + PBN filters had nothing to act on. Merge: no new rows; `+wpe-logs` appended to `source_set` (+`last_seen_source=2026-05-12`) on the `facebook.com` P1 row, `twitter.com`, `x.com`, flagged in `notes` as redirect-wrapper / fbclid corroboration. `disavow-sparkshark.com.txt` unchanged (no new spam). Artifacts written: `wpe-access-log-snapshot-2026-05-12.md`, `wpe-access-log-referers-2026-05-12.json`. |
| 3 | **Stamp final** | WPE done (exhausted), Athena deliberately deferred per Brock, Bing index empty → renamed `master-backlinks-cumulative.csv` → `master-backlinks-final.csv` (via `git mv`, then the 3-row merge applied on top). Updated `BACKLINK-SUMMARY.md` (title/status, §1 heading, sources list, §5.C, §6 artifact map, §7) and the `disavow-sparkshark.com.txt` header comment. `docs/migration/SOURCE-OF-TRUTH.md` does not reference the old filename — nothing to change there. |
| — | **Flagged a secret leak** | While exploring the WPE install over SSH, `cat`'d `/nas/content/live/flancoelectric/_wpeprivate/config.json`, which contains a platform-managed PHP-session-DB password (`WPENGINE_SESSION_DB_PASSWORD`, for a 127.0.0.1-only MySQL) and the legacy `wpengine_apikey` (for `api.wpengine.com/1.2`). Both are now in the Claude transcript. Added to the security-follow-ups bucket (see §3). Low-to-moderate risk (session DB not internet-reachable; WPE regenerates `config.json`), but Brock should decide whether to rotate the legacy API key. |

**No commit/push was made.** Evidence-pack changes don't alter built HTML, but the repo rule stands — Brock approves before push (a push = a Vercel deploy; DNS is not flipped, so nothing goes live regardless).

**Changed/added files (uncommitted, in `migration-evidence-pack/07-backlinks-and-citations/`):**
- `master-backlinks-cumulative.csv` → renamed to `master-backlinks-final.csv` (+ 3 rows tagged `+wpe-logs`)
- `BACKLINK-SUMMARY.md` (final stamp + WPE section)
- `disavow-sparkshark.com.txt` (header comment: filename + note that WPE added no new spam)
- `wpe-access-log-snapshot-2026-05-12.md` (new)
- `wpe-access-log-referers-2026-05-12.json` (new)
- `SESSION-4-HANDOFF.md` (this file, new)

---

## 2) The list, in one line

**145 rows / 129 unique referring domains. ~41 real/actionable, ~25–35 genuinely useful editorial/citation backlinks, 83 spam/PBN/legacy-junk staged for disavow, 7 other-brand "Spark Shark" rows to ignore.** Sources: GSC + Bing(empty) + open-web search + GA4 (live 488680346 + Flanco-legacy 480290314) + Ahrefs Webmaster Tools (full, 1,080 backlinks / 90 refdomains — mostly junk) + Wayback CDX enrichment + WPE access-log snapshot (added nothing). Common Crawl/Athena deliberately deferred. **This is final.**

---

## 3) Carried-forward / post-launch items (none block "final"; all are Brock-actions or post-launch)

- **[Brock] Upload `disavow-sparkshark.com.txt`** at Search Console → Disavow links tool → property `sc-domain:sparkshark.com` (upload *replaces*, doesn't append). Post-launch. Re-pull Ahrefs AWT every ~30–60 days during the cutover window, regenerate, re-upload — the spam surge looked active as of May 2026. (Re-run procedure for the Ahrefs scrape is in `BACKLINK-SUMMARY.md` §5.A and `SESSION-3-HANDOFF.md` §4.)
- **[Brock] Verify the GA4 "candidate backlink" mentions** still needing on-page confirmation: `chatgpt.com`, `claude.ai`, `hometalk.com`, `marketspacesales.com` — open each, search the rendered DOM/source for `sparkshark.com`.
- **P0/P1 pre-flip items** (from `BACKLINK-SUMMARY.md` §4, unchanged): `networx.com/c.flanco-electric` takedown/rebrand (P0); reconcile the two BBB profiles (P1); verify NAP on Chamber/MapQuest (P1); claim Yelp + Thumbtack (P1); verify FB (`/sparksharkelectric`) + IG (`@thesparkshark`) bios (P1).
- **Security follow-up bucket** (not part of this workstream — lives with `~/.claude/projects/-Users-brock/memory/project_security_followups.md`): the existing items (re-rotate the Cloudflare token, rotate Voyage + Supabase `service_role`, delete `.zsh_history.pre-scrub` backup) **plus a new one from this session**: the WPE `_wpeprivate/config.json` PHP-session-DB password + legacy `wpengine_apikey` appeared in a Claude transcript — decide whether to rotate the legacy WPE API key (the session DB is localhost-only / platform-managed, lower priority).

---

## 4) Facts that don't change (don't re-litigate)

- **WPE access logs are NOT 90-day-retrievable.** No Public-API endpoint, no SSH-Gateway logs, portal keeps only ~1,500 requests. Anyone who wants real WPE referrer coverage must set up log forwarding/streaming *before* the traffic happens. Not worth doing for the migration. The WPE source is **closed**.
- The `wp_engine` 1Password item (vault SparkShark) was rotated 2026-05-12 (portal password + API token + API username). Use type-based redaction (CONCEALED + SSHKEY = redact; STRING/MENU/DATE = OK), never block-list filtering.
- Brand collisions, Brock's confirmed social handles, the domain's pre-Flanco poker→credit-repair history, Bing's empty index, the GSC API not exposing the Links report, the GA4 ownership facts — all as recorded in `SESSION-3-HANDOFF.md` §4. Unchanged.
- Repo policy: push = Vercel deploy; evidence-pack files don't change built HTML, but still get Brock's OK before pushing. DNS is not flipped.
