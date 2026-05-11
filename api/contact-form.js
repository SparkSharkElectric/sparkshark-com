// api/contact-form.js
//
// Vercel Edge Function that receives the /contact-us/ form, validates input,
// sends an email to theteam@sparkshark.com via Resend, and returns a JSON envelope.
//
// Wired in 2026-05-10 as part of the pre-cutover hardening sprint, replacing the
// previous Formspree placeholder action ("https://formspree.io/f/REPLACE_WITH_FORM_ID"
// which silently returned HTTP 400 — bleeding leads). This handler is the only
// runtime code in the sparkshark-com repo. The site remains a static-HTML deploy;
// this single Edge Function is the contact-form transport.
//
// ─────────────────────────────────────────────────────────────────────────────
// Required Vercel env vars (sparkshark-com project, all environments):
//
//   RESEND_API_KEY        Resend API key (starts with "re_"). Source from 1Password
//                         SparkShark vault.
//   CONTACT_FORM_FROM     Verified sender, e.g. "Spark Shark Web <web@sparkshark.com>".
//                         Domain must be verified in Resend before this works.
//   CONTACT_FORM_TO       Recipient inbox, e.g. "theteam@sparkshark.com".
//
// ─────────────────────────────────────────────────────────────────────────────
// Request: POST JSON { name, email, phone, city?, message, company? }
// `company` is an anti-spam honeypot — populated bots get a 200 with no email sent.
//
// Response (success):  { ok: true,  data: { received_at: "<ISO>" } }
// Response (failure):  { ok: false, error: "<short_code>", message: "<human>" }
//   Status: 200 success · 400 validation · 405 method · 429 rate-limit · 502 send-fail
//
// ─────────────────────────────────────────────────────────────────────────────
// Light rate-limit: in-memory per-IP bucket. Edge instances are short-lived and
// independent, so this is a spam-deterrent floor, not a guarantee.

export const config = { runtime: 'edge' };

const RATE_WINDOW_MS = 60_000;
const RATE_MAX = 3;
const rateBuckets = new Map();

function rateLimit(ip) {
  const now = Date.now();
  const bucket = rateBuckets.get(ip) || [];
  const recent = bucket.filter(t => now - t < RATE_WINDOW_MS);
  if (recent.length >= RATE_MAX) return false;
  recent.push(now);
  rateBuckets.set(ip, recent);
  return true;
}

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store',
      'x-content-type-options': 'nosniff',
    },
  });
}

function clean(s, max = 5000) {
  if (typeof s !== 'string') return '';
  return s.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '').trim().slice(0, max);
}

function emailValid(s) {
  return typeof s === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return json(405, { ok: false, error: 'method_not_allowed', message: 'POST only.' });
  }

  let body;
  const ct = req.headers.get('content-type') || '';
  try {
    if (ct.includes('application/json')) {
      body = await req.json();
    } else {
      const form = await req.formData();
      body = Object.fromEntries(form.entries());
    }
  } catch {
    return json(400, { ok: false, error: 'invalid_body', message: 'Could not parse request body.' });
  }

  // Honeypot
  if (clean(body.company)) {
    return json(200, { ok: true, data: { received_at: new Date().toISOString() } });
  }

  const name = clean(body.name, 200);
  const email = clean(body.email, 200);
  const phone = clean(body.phone, 50);
  const city = clean(body.city, 200);
  const message = clean(body.message, 5000);

  const missing = [];
  if (!name) missing.push('name');
  if (!email) missing.push('email');
  if (!phone) missing.push('phone');
  if (!message) missing.push('message');
  if (missing.length) {
    return json(400, {
      ok: false,
      error: 'missing_fields',
      message: `Missing: ${missing.join(', ')}.`,
    });
  }
  if (!emailValid(email)) {
    return json(400, { ok: false, error: 'invalid_email', message: 'Email address looks invalid.' });
  }

  const ip =
    req.headers.get('x-real-ip') ||
    (req.headers.get('x-forwarded-for') || '').split(',')[0].trim() ||
    'unknown';
  if (!rateLimit(ip)) {
    return json(429, {
      ok: false,
      error: 'rate_limited',
      message: 'Too many requests. Please call (405) 436-4776.',
    });
  }

  const apiKey = process.env.RESEND_API_KEY;
  const from = process.env.CONTACT_FORM_FROM;
  const to = process.env.CONTACT_FORM_TO;
  if (!apiKey || !from || !to) {
    return json(502, {
      ok: false,
      error: 'config_missing',
      message: 'Email transport not configured. Please call (405) 436-4776.',
    });
  }

  const subject = `Website form — ${name}${city ? ` (${city})` : ''}`;
  const textBody = [
    `New contact form submission from sparkshark.com:`,
    ``,
    `Name:    ${name}`,
    `Phone:   ${phone}`,
    `Email:   ${email}`,
    city ? `City:    ${city}` : null,
    ``,
    `Message:`,
    message,
    ``,
    `---`,
    `Submitted: ${new Date().toISOString()}`,
    `IP:        ${ip}`,
  ].filter(Boolean).join('\n');

  const htmlBody = `
<div style="font:14px/1.5 -apple-system,system-ui,Segoe UI,sans-serif;color:#0C192B;">
  <p><strong>New contact form submission from sparkshark.com</strong></p>
  <table style="border-collapse:collapse;">
    <tr><td style="padding:4px 12px 4px 0;color:#5b6470;">Name</td><td style="padding:4px 0;">${escapeHtml(name)}</td></tr>
    <tr><td style="padding:4px 12px 4px 0;color:#5b6470;">Phone</td><td style="padding:4px 0;"><a href="tel:${escapeHtml(phone.replace(/[^\d+]/g, ''))}">${escapeHtml(phone)}</a></td></tr>
    <tr><td style="padding:4px 12px 4px 0;color:#5b6470;">Email</td><td style="padding:4px 0;"><a href="mailto:${escapeHtml(email)}">${escapeHtml(email)}</a></td></tr>
    ${city ? `<tr><td style="padding:4px 12px 4px 0;color:#5b6470;">City</td><td style="padding:4px 0;">${escapeHtml(city)}</td></tr>` : ''}
  </table>
  <p style="margin-top:16px;"><strong>Message</strong></p>
  <p style="white-space:pre-wrap;background:#f5f6f8;padding:12px;border-left:3px solid #F28C28;">${escapeHtml(message)}</p>
  <p style="color:#8b949e;font-size:12px;margin-top:24px;">
    Submitted ${new Date().toISOString()} · IP ${escapeHtml(ip)}
  </p>
</div>`;

  try {
    const resendRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from,
        to: [to],
        reply_to: email,
        subject,
        text: textBody,
        html: htmlBody,
      }),
    });
    if (!resendRes.ok) {
      const detail = await resendRes.text().catch(() => '');
      return json(502, {
        ok: false,
        error: 'send_failed',
        message: 'Could not send. Please call (405) 436-4776.',
        _diagnostic: detail.slice(0, 500),
      });
    }
  } catch (err) {
    return json(502, {
      ok: false,
      error: 'send_failed',
      message: 'Could not send. Please call (405) 436-4776.',
      _diagnostic: String(err).slice(0, 500),
    });
  }

  return json(200, { ok: true, data: { received_at: new Date().toISOString() } });
}
