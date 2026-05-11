# Cutover-Day Evidence Checklist (Local)

**Maps to launch-gate items #5 and #6** in `docs/migration/launch-gate.md`.

This file is local-only. **Do not commit.** Evidence captured here is the rollback insurance for DNS cutover day.

---

## Required pre-cutover evidence (gate-blocking)

### [ ] Current DNS records screenshot — gate item #5

- **Save at:** `migration-evidence-pack/12-launch-and-rollback/current-dns-before-cutover.png`
- **Captures:** GoDaddy DNS records for `sparkshark.com` and `www.sparkshark.com` BEFORE any change is made — A, CNAME, TXT, MX, and any other relevant records visible.
- **Why it blocks launch:** DNS rollback is impossible without a recorded baseline. If the Vercel cutover fails and we need to revert, we need to know exactly what the old values were.
- **Done criteria (verbatim):** "Screenshot/export from GoDaddy/DNS provider showing current A, CNAME, TXT, MX, and any relevant records before Vercel cutover."

### [ ] WP Engine backup confirmation — gate item #6

- **Save at:** `migration-evidence-pack/12-launch-and-rollback/wp-engine-backup-confirmation.png`
- **Captures:** WP Engine portal screenshot showing a fresh backup was created on cutover day, with date / time visible. Old WordPress site remains live (WP Engine still hosting) so it can be restored if Vercel cutover fails.
- **Why it blocks launch:** If Vercel cutover fails, we need the legacy site preserved and restorable.
- **Done criteria (verbatim):** "Screenshot showing a fresh WP Engine backup has been created, date/time visible, and old site remains available for rollback."

---

## Recommended Vercel-side evidence (not gate-blocking, but captured for the record)

### [ ] Vercel build log for the production deploy

- **Save at:** `migration-evidence-pack/12-launch-and-rollback/vercel-build-log.txt` (or `.png` of the Vercel UI)
- **Captures:** full output of `BASE="" python3 build.py` running under Vercel's `buildCommand` with no errors, sitemap URL count correct (40), deploy ID and commit hash recorded.

### [ ] Vercel project settings screenshot

- **Save at:** `migration-evidence-pack/12-launch-and-rollback/vercel-project-settings.png`
- **Captures:** domains attached (`www.sparkshark.com` primary, `sparkshark.com` apex), framework preset, build / output settings, environment variables (none expected for v1), Git integration state.

### [ ] Vercel preview validation re-run output

- **Save at:** `migration-evidence-pack/12-launch-and-rollback/preview-validation.txt`
- **Captures:** re-run of the validation commands from `docs/migration/vercel-preview-validation.md` against the production deploy alias once the domain is attached and DNS has propagated.

---

## Rollback plan (REQUIRED before cutover)

- [ ] DNS provider login confirmed (GoDaddy)
- [ ] Old DNS values transcribed below for one-line restore
- [ ] Decision-maker on rollback identified: Brock
- [ ] Rollback trigger criteria documented (which symptoms = rollback?)
- [ ] Communication plan if rollback fires (who, how, when)

### Old DNS values (transcribe before changing anything)

```
sparkshark.com:
  A      <value>
  TXT    <value>
  MX     <value>
  ...

www.sparkshark.com:
  A      <value>
  CNAME  <value>
  TXT    <value>
  ...
```

### Rollback trigger criteria — examples to harden before cutover

- Homepage 5xx for >5 min
- Phone link broken (`tel:` href changed)
- ServiceTitan scheduler embed fails to load on homepage and contact page
- robots.txt or sitemap.xml returns wrong host
- Schema validation fails on top organic landing pages

---

## Cutover authorization

DNS cutover is **blocked** until **all 9 launch-gate items** in `docs/migration/launch-gate.md` are **Approved** OR **Not Applicable** with written reason. **Only Brock** may mark items Approved or Not Applicable.

This checklist itself does **NOT** authorize cutover. It captures the cutover-day rollback evidence required for gate items #5 and #6, plus optional Vercel-side evidence for the post-cutover record.

---

## Reference

- Launch gate: `docs/migration/launch-gate.md`
- Preview validation: `docs/migration/vercel-preview-validation.md`
- Vercel deploy contract: `vercel.json`
