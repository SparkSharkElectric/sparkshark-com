# WordPress Redirect Audit Checklist (Read-Only)

**Status:** Local-only. Not committed to git. Inherits `migration-evidence-pack/.gitignore: *`.
**Created:** 2026-05-10
**Anchored to main commit:** `ab80db2`
**Scope:** Audit only. **No edits.** No plugin activation/deactivation. No setting saves. No DNS changes. No Vercel changes. No WordPress or WP Engine state changes.

---

## Why this audit exists

Before the WordPress → Vercel DNS cutover, every redirect that is **currently helping the legacy WP site** must be identified so the necessary subset can be recreated as 301s in `vercel.json` (or intentionally dropped). Redirects on a WP site can live in **at least eight different surfaces**, and "the WP Engine User Portal Redirect Rules tab is empty" does **not** mean the site has no redirects. This checklist walks the surfaces in observation order.

---

## 1. WP Admin → Plugins → Installed Plugins

**Navigate to:** WP Admin → Plugins → Installed Plugins.

**For each row, record:** plugin name, version, status (Active / Inactive), and "Update available" flag.

**Plugins to flag with extra attention** (high-likelihood redirect sources):

- **Redirection** (`john-godley/redirection`) — full-featured redirect manager. Stores rules in DB tables.
- **Yoast SEO** — free build has no redirect manager. **Yoast SEO Premium** (paid) adds Redirects → SEO → Redirects.
- **Rank Math SEO** — free build includes Redirections module. **Rank Math Pro** extends it.
- **SEOPress** — free build has no redirect manager. **SEOPress Pro** (paid) adds Redirections.
- **WPCode** (formerly Insert Headers and Footers Code by WPCode) — code-snippet manager. Snippets can contain raw `wp_redirect` / `wp_safe_redirect` / `header('Location: …')` PHP calls.
- **Safe Redirect Manager** — Custom post-type-based redirect manager (post type `srm_redirect`).
- **301 Redirects** — multiple plugins exist by this name; "301 Redirects" by WebFactory Ltd is the most common.
- **Simple 301 Redirects** — older simple plugin; pairs source → destination.
- **All in One SEO** (AIOSEO) — Pro tier includes redirect manager.

**Also flag** any plugin whose name contains: `redirect`, `301`, `htaccess`, `seo`, `rewrite`, `snippet`, `code`, `cache`, `link manager`. Cache plugins (W3 Total Cache, WP Rocket, LiteSpeed) typically don't store redirects but can intercept request flow.

**Screenshot requirement:** Plugins list with `All` filter active so inactive plugins are visible. Save to:

```
migration-evidence-pack/08-legacy-flanco-entity-audit/wordpress-redirect-plugins/01-wp-admin-plugins-list-all-2026-05-10.png
```

Optional second screenshot with `Active` filter to make the active set easy to read:

```
migration-evidence-pack/08-legacy-flanco-entity-audit/wordpress-redirect-plugins/02-wp-admin-plugins-list-active-2026-05-10.png
```

---

## 2. WP Admin — Likely redirect-rule locations to check

Walk each location **in order**. Capture a screenshot of each, even if the location is empty (an empty list is also evidence).

### 2.1 Tools → Redirection
- Plugin: **Redirection**.
- Tabs to check: Redirects, Groups, Site, Logs, 404s, Options.
- Look for a "Export" option (CSV / JSON / Apache / Nginx) and run an export per format if available.
- Save list screenshot and any exports to `wordpress-redirect-plugins/` with date-stamped names, e.g. `redirection-redirects-list-2026-05-10.png`, `redirection-export.csv`.

### 2.2 Yoast SEO → Redirects
- Requires **Yoast SEO Premium**.
- Tabs: Redirects (regular), Regex Redirects.
- Look for Import/Export → Export. Capture the redirect list screenshot and export.
- Save as `yoast-redirects-list-2026-05-10.png`, `yoast-redirects-export.csv` (or whatever the export format produces).

### 2.3 Rank Math → Redirections
- Free build includes this module if enabled.
- Capture the list, including: source URL, redirect type (301/302/307/410/451), match type (exact, contains, starts with, ends with, regex), enabled/disabled status, hits.
- Look for Import/Export and run an export.
- Save as `rank-math-redirections-2026-05-10.png`, `rank-math-export.csv`.

### 2.4 SEOPress → Redirections
- Requires **SEOPress Pro**.
- Capture the list and export if available.
- Save as `seopress-redirections-2026-05-10.png`, `seopress-export.csv`.

### 2.5 Code Snippets → All Snippets (WPCode)
- Plugin: **WPCode** (or legacy "Insert Headers and Footers").
- Capture the full snippets list with: title, type (PHP / JS / HTML / CSS / Universal / Text), location (Auto Insert vs Shortcode), priority, status.
- For **every active PHP snippet**, open the snippet and screenshot the code. Redirect logic typically appears as `wp_redirect`, `wp_safe_redirect`, `header('Location:`, `header("Location:`, `$_SERVER['REQUEST_URI']` matching, `is_404()` early hooks, or `template_redirect` action handlers.
- Save list screenshot to `wpcode-snippets-list-2026-05-10.png`. Save each redirect-bearing snippet body as `wpcode-snippet-<title-slug>-2026-05-10.png`.

### 2.6 Settings → 301 Redirects (or similar)
- Plugin: **301 Redirects** (WebFactory Ltd) or similar.
- Capture redirect list (source → destination, status code).
- Save as `301-redirects-list-2026-05-10.png`, `301-redirects-export.csv` if available.

### 2.7 Tools → Safe Redirect Manager
- Plugin: **Safe Redirect Manager**.
- Capture redirect list. SRM stores redirects as posts of custom type `srm_redirect`.
- Save as `safe-redirect-manager-list-2026-05-10.png`. There is no built-in export; one option is to use WP-CLI later (see §4.6).

### 2.8 All in One SEO → Redirects
- Requires **AIOSEO Pro**.
- Capture list and export if available.
- Save as `aioseo-redirects-2026-05-10.png`, `aioseo-export.csv`.

### 2.9 Settings → Permalinks
- Not a redirect manager per se, but the permalink structure (`/%postname%/`, `/%year%/%monthnum%/%postname%/`, custom) drives the **default** WordPress canonical redirects (the rewrite engine 301s from non-canonical to canonical form). Date-archive structure here is what generates URLs like `/2023/12/...` that show up in the GSC data.
- Capture the Permalinks screen.
- Save as `wp-permalinks-2026-05-10.png`.

---

## 3. Pattern search — what to look for in every list

Across **every** redirect surface above, scan for source / destination patterns that match the legacy footprint. Highlight matches in the screenshots or note them in a per-list `.md` next to the screenshot.

**Brand / legal-entity patterns:**

- `flanco`
- `flancoelectric`
- `Flanco Electric`
- `sparkshark`
- `spark-shark`
- `bsf`
- `bsfinvestment`

**Legacy URL patterns:**

- `/2023/`, `/2023/12/`, `/2024/`, `/2024/01/` (WP date archives)
- `/category/`, `/category/<anything>/`
- `/tag/`, `/tag/<anything>/`
- `/author/`, `/author/<anything>/`
- `/wp-content/`, `/wp-content/uploads/`, `/wp-content/themes/`, `/wp-content/plugins/`
- `/wp-admin/`, `/wp-login.php`
- `/feed`, `/feed/`, `/rss`, `/comments/feed/`
- `/sitemap_index.xml`, `/sitemap.xml.gz`
- `/repair/`
- `/finacing/` (note the legacy misspelling — and also check `/financing/`)
- `/projects/`
- `/lander` (and `/lander/`, `/lander-<variant>`)
- `/?p=<number>` (default WP non-pretty permalinks)
- `/?page_id=<number>`
- `/services/<old-slug>/`
- `/our-residential-electrical-services/`
- `/price/`

**Destination patterns that warrant scrutiny:**

- Any destination that goes off-domain (e.g. `book.servicetitan.com`, `flancoelectric.com`, a Wix page, a Squarespace page).
- Any destination containing `?utm_*` (preserved UTM tagging — relevant for §3.5 of `13-deep-research/00_DEEP_RESEARCH_INPUT_BRIEF.md`).
- Any destination that returns 404 today (broken rules — capture them for the disposition decision: rewrite, drop, or fix).

---

## 4. WP-CLI / SSH inspection (if available later)

These commands are **read-only**. No writes, no deletes, no plugin activation, no setting changes. Save the output to date-stamped files in `wordpress-redirect-plugins/`.

If WP-CLI is not available on WP Engine SSH, the equivalent WP Admin / phpMyAdmin steps are noted.

### 4.1 Active plugins

```bash
wp plugin list --status=active --format=table
wp plugin list --format=csv > wp-plugins-2026-05-10.csv
```

### 4.2 List database tables

```bash
wp db tables --format=csv > wp-db-tables-2026-05-10.csv
```

Spot-check for tables matching: `redirection`, `redirect`, `yoast`, `rank_math`, `seopress`, `srm`, `aioseo`, `wpcode`.

### 4.3 wp_options keys containing redirect-related names

```bash
wp option list --search='*redirect*' --format=csv > wp-options-redirect-2026-05-10.csv
wp option list --search='*wpcode*'   --format=csv > wp-options-wpcode-2026-05-10.csv
wp option list --search='*seopress*' --format=csv > wp-options-seopress-2026-05-10.csv
wp option list --search='*rank_math*' --format=csv > wp-options-rank-math-2026-05-10.csv
wp option list --search='*wpseo*'    --format=csv > wp-options-yoast-2026-05-10.csv
wp option list --search='*301*'      --format=csv > wp-options-301-2026-05-10.csv
wp option list --search='*srm*'      --format=csv > wp-options-srm-2026-05-10.csv
wp option list --search='*aioseo*'   --format=csv > wp-options-aioseo-2026-05-10.csv
```

`--search` accepts a SQL `LIKE` wildcard pattern — `*` becomes `%`. These calls only read; they do not mutate options. Many of these will return empty; that is also evidence — save the empty CSVs too.

### 4.4 wp_posts rows that look like redirect snippets

```bash
# Safe Redirect Manager posts
wp post list --post_type=srm_redirect --format=csv \
  --fields=ID,post_title,post_name,post_status,post_modified > wp-srm-posts-2026-05-10.csv

# WPCode snippets (post type name may be `wpcode` or `code_snippets`; try both)
wp post list --post_type=wpcode        --format=csv \
  --fields=ID,post_title,post_name,post_status,post_modified > wp-wpcode-posts-2026-05-10.csv
wp post list --post_type=code_snippets --format=csv \
  --fields=ID,post_title,post_name,post_status,post_modified > wp-code-snippets-posts-2026-05-10.csv

# Any post type whose name contains "redirect"
wp post-type list --format=csv > wp-post-types-2026-05-10.csv
```

For each candidate row, read the body (no edit):

```bash
wp post get <ID> --field=post_content > wp-post-<ID>-content-2026-05-10.txt
```

Scan the dumped content for: `wp_redirect`, `wp_safe_redirect`, `header('Location:`, `header("Location:`, `301`, `302`, `template_redirect`, `init`, `parse_request`.

### 4.5 wp_options serialized values for redirect plugins (deeper read)

For each option key returned by §4.3, dump the full value:

```bash
wp option get <option_name> > wp-option-<option_name>-2026-05-10.txt
```

Many plugin rule sets are stored as PHP-serialized arrays inside a single option key (e.g. `301_redirects`, `simple_301_redirects`, `safe_redirect_manager_options`). Reading is harmless.

### 4.6 Raw SQL via `wp db query` (read-only SELECT only)

If you want to bypass plugin-specific commands, run direct SELECT queries. **Use SELECT only — no INSERT, UPDATE, DELETE, ALTER, DROP, TRUNCATE.**

```bash
# Existence of common redirect tables
wp db query "SHOW TABLES LIKE '%redirect%';"
wp db query "SHOW TABLES LIKE '%yoast%';"
wp db query "SHOW TABLES LIKE '%rank_math%';"
wp db query "SHOW TABLES LIKE '%seopress%';"
wp db query "SHOW TABLES LIKE '%srm%';"

# Row counts where tables exist (substitute table name)
wp db query "SELECT COUNT(*) AS n FROM wp_redirection_items;"
wp db query "SELECT COUNT(*) AS n FROM wp_redirection_404;"

# Full export of redirect rows (Redirection plugin example)
wp db query "SELECT id, url, action_data, regex, group_id, status, action_type, action_code, match_url, last_count, last_access \
             FROM wp_redirection_items \
             ORDER BY id;" \
  > wp-db-redirection-items-2026-05-10.tsv
```

Save each query's output as a date-stamped file. Read-only queries do not modify the database.

### 4.7 Theme `functions.php` and `mu-plugins/`

Redirects sometimes live in the active theme's `functions.php` or in `wp-content/mu-plugins/`. WP-CLI doesn't expose these directly; SSH is needed.

```bash
# Active theme
wp theme list --status=active --format=csv

# Read functions.php of the active theme (path resolves under wp-content/themes/<slug>/)
THEME_PATH=$(wp eval 'echo get_stylesheet_directory();')
ls -la "$THEME_PATH"
[ -f "$THEME_PATH/functions.php" ] && \
  grep -nE 'wp_redirect|wp_safe_redirect|header.*Location|301|302|template_redirect' "$THEME_PATH/functions.php"

# mu-plugins
WP_CONTENT=$(wp eval 'echo WP_CONTENT_DIR;')
ls -la "$WP_CONTENT/mu-plugins" 2>/dev/null
find "$WP_CONTENT/mu-plugins" -type f -name '*.php' 2>/dev/null \
  -exec grep -lE 'wp_redirect|wp_safe_redirect|header.*Location|301|302|template_redirect' {} \;
```

Save outputs as `wp-theme-functions-redirect-grep-2026-05-10.txt` and `wp-mu-plugins-redirect-grep-2026-05-10.txt`.

### 4.8 `.htaccess` / nginx config

WP Engine runs **NGINX**, not Apache, so `.htaccess` rules are typically **not applied** even if a `.htaccess` file exists in the WP root. WP Engine routes server-level redirects through the User Portal → Redirect Rules. That surface is captured separately in `migration-evidence-pack/08-legacy-flanco-entity-audit/wp-engine-redirect-rules/`.

For completeness:

```bash
# .htaccess at WP root (informational; not active on WP Engine NGINX)
ls -la $(wp eval 'echo ABSPATH;').htaccess 2>/dev/null
[ -f $(wp eval 'echo ABSPATH;').htaccess ] && \
  /usr/bin/cat $(wp eval 'echo ABSPATH;').htaccess > wp-root-htaccess-2026-05-10.txt
```

If the file exists, save it. If WP Engine routes nginx redirects from a config file accessible via SSH, that is **WP-Engine-specific** — request the redirect-rules export from the WP Engine User Portal and save it under `wp-engine-redirect-rules/` instead.

---

## 5. Cross-reference what you find

After all evidence is collected, write a short distillation note next to the screenshots:

```
wordpress-redirect-plugins/AUDIT_FINDINGS_2026-05-10.md
```

For each redirect surface, record:

- Surface (Redirection plugin / Rank Math / WPCode / SRM / theme / mu-plugin / WP Engine / etc.)
- Rule count
- Whether the source/destination pattern matches any of the §3 patterns above
- Whether the rule is candidate for porting to `vercel.json` (and the proposed destination)
- Whether the rule is candidate for dropping (e.g. legacy WP-only rule with no remaining inbound traffic)
- Open questions

That distillation note becomes one of the Deep Research inputs (the v1.1 redirect map question in `13-deep-research/00_DEEP_RESEARCH_INPUT_BRIEF.md` §8.2).

---

## 6. Critical warning

**Do not assume no redirects exist just because WP Engine Redirect Rules is empty.** Redirects on a WP site can live in **any** of the following surfaces:

- Server-level rewrite rules (WP Engine User Portal Redirect Rules — captured separately under `wp-engine-redirect-rules/`).
- WordPress redirect plugins (§2.1, §2.6, §2.7, §2.8 above).
- SEO plugins with redirect modules (Yoast Premium, Rank Math, SEOPress Pro, AIOSEO Pro — §2.2, §2.3, §2.4, §2.8).
- WPCode snippets containing raw PHP `wp_redirect` / `wp_safe_redirect` / `header('Location:')` calls (§2.5).
- `.htaccess` or nginx config files (§4.8 — typically inert on WP Engine NGINX but worth confirming).
- Theme `functions.php` redirect handlers (§4.7).
- `mu-plugins/` redirect handlers (§4.7).
- WP Core's own rewrite rules (Settings → Permalinks structure drives non-canonical → canonical redirects automatically; §2.9).

**Each surface above can ship a 301 the browser sees, and any of them being missed during cutover means the corresponding inbound link becomes a 404 on the Vercel side.** Capture each surface, even when it appears empty.

---

## Hard rules

- This audit is **observation-only**. Do not click any "Save", "Update", "Delete", "Activate", or "Deactivate" button.
- Do not run any WP-CLI command that mutates state (`wp plugin activate`, `wp plugin deactivate`, `wp option update`, `wp option delete`, `wp post update`, `wp db import`, `wp db drop`, etc.).
- Do not run any database write SQL (no `INSERT`, `UPDATE`, `DELETE`, `ALTER`, `DROP`, `TRUNCATE`).
- Do not change DNS. Do not touch Vercel. Do not deactivate any plugin. Do not save any setting.
- DNS cutover remains **blocked** by `docs/migration/launch-gate.md`. This audit does not change any gate status.

---

## Reference

- Parent legacy-entity audit README: `migration-evidence-pack/08-legacy-flanco-entity-audit/README-legacy-entity-audit.md`
- WP Engine server-level redirect rules: `migration-evidence-pack/08-legacy-flanco-entity-audit/wp-engine-redirect-rules/`
- Backlinks / citations sibling folder: `migration-evidence-pack/07-backlinks-and-citations/`
- Vercel deploy contract: `vercel.json` (current 14 redirect entries)
- Launch gate (controlling document): `docs/migration/launch-gate.md`
- Preview validation: `docs/migration/vercel-preview-validation.md`
- Deep Research input brief: `migration-evidence-pack/13-deep-research/00_DEEP_RESEARCH_INPUT_BRIEF.md`
