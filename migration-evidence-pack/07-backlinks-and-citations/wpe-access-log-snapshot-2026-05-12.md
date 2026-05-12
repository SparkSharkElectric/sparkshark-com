# WP Engine access-log pull — 2026-05-12

**Outcome: source exhausted. Zero new referring domains, zero new editorial backlinks.** This closes out the last unrun backlink source; `master-backlinks-final.csv` is now the final list.

## What WP Engine actually exposes (mechanism confirmed)

The Session-2/3 plan assumed one of three retrieval paths. All three were checked on 2026-05-12 with the **rotated** `wp_engine` creds:

| Path | Result |
|---|---|
| **WPE Public API** (`api.wpengineapi.com/v1`) | **No logs endpoint exists.** Swagger enumerated — `/installs/{id}` has `backups`, `domains`, `ssl_certificates`, `cache`, `usage`, etc., but nothing for access/error logs. Used the API only to confirm the install: `flancoelectric` (id `03ba3838-…`, `primary_domain=www.sparkshark.com`, prod). |
| **SSH to the install** (1Password `WP Engine SSH Key — flancoelectric`) | Connected fine (lands in `/home/wpe-user`, docroot symlinked at `~/sites/flancoelectric → /nas/content/live/flancoelectric`). **No web access logs on the filesystem** — no `~/logs/`, no `/var/log/nginx`, no `/var/log/apache2`. WP Engine's SSH Gateway does not surface raw web-server logs. |
| **User Portal** (`my.wpengine.com → install → Logs → Access`) | This is the only place access logs live. The portal shows **"the last 1,500 entries"** — and the underlying JSON feed (`/installs/flancoelectric/site_logs_feed_data?environment=nginx`) returns exactly 1,500 rows. On this site that's **≈13 hours** of traffic (2026-05-11 14:36 → 2026-05-12 03:15 UTC), because the request stream is dominated by bot/scanner noise (`/wp-json/...`, `/?author=1`, `/xmlrpc.php`, `/archives/2008/.../credit-repair...`, ACME-challenge probes, etc.). |

**There is no "last 90 days" of access logs at WP Engine** — not via API, not via SSH, not via the portal. WPE retains only a rolling ~1,500-request window unless you stand up log forwarding/streaming going forward (out of scope for migration evidence). The 1,500-row snapshot captured 2026-05-12 03:15 UTC is therefore the entire WPE contribution to this workstream.

## What was in the snapshot

The portal feed *does* include a `referer` field (the table view doesn't, but the JSON does). Of 1,500 nginx rows + 1,500 php rows pulled and de-duplicated:

- **27 unique referer strings total**, of which **24 are self-referrals** (`www.sparkshark.com/*`, `sparkshark.com/*`, including a `?fbclid=…` homepage hit and legacy `sparkshark.com/{new,old,wp,blog,backup,wordpress}/` probe paths from bots).
- **3 external referring hosts**, all already represented in the master and none of them editorial backlinks:
  - `https://www.google.com/` (×3) + `https://www.google.com/search?q=wordpress` (×1) — organic SERP / bot-scanner referrals, **not a backlink**.
  - `https://l.facebook.com/` (×1) — Facebook's outbound-link wrapper. Together with the `?fbclid=…` homepage self-referrals, this corroborates the existing `facebook.com` row (Brock-owned FB business page) — a real live inbound click.
  - `https://t.co/` (×1) — X/Twitter's link shortener (path stripped). Corroborates the existing `twitter.com` / `x.com` rows (Brock-owned `@The_Spark_Shark`) — a real live inbound click.

## Merge applied

No new rows. `+wpe-logs` appended to `source_set` (and `last_seen_source` bumped to `2026-05-12`) on three existing rows: `facebook.com` (the P1 Brock-owned page), `twitter.com`, `x.com` — flagged in `notes` as redirect-wrapper / fbclid corroboration, not a newly-discovered editorial link. No new spam domains → `disavow-sparkshark.com.txt` unchanged. Brand-collision and spam filters had nothing to act on (no external referer matched the Ontario/Wisconsin/California "Spark Shark" patterns or the `.shop/.top/.click/seoexpress*/rankvance*` PBN patterns).

## Artifacts

- `wpe-access-log-referers-2026-05-12.json` — slimmed dump: per-environment entry counts, date ranges, the full unique-referer set, and the external (non-self) referers. (Raw 3,000-row pull was not retained — it's bot noise; this captures everything backlink-relevant.)

## Caveat for future re-runs

If you want WPE referrer data with real coverage, the only way is to configure **log forwarding / log streaming** on the install (to S3 / a SIEM) *before* the traffic happens — you can't retroactively get more than the live ~1,500-request window. Given GSC's link graph + the full Ahrefs pull are already captured and added essentially nothing real, this is not worth doing for the migration. Treat the WPE source as **closed**.
