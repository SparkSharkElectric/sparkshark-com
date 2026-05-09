#!/usr/bin/env node
// Fetch the 5 most-recent Google Business Profile reviews for Spark Shark Electric
// via the Google Places API (New) and write the normalized result to
// data/gbp-reviews.json. build.py reads that JSON to render the carousel.
//
// API key resolution order:
//   1. GOOGLE_PLACES_API_KEY env var
//   2. 1Password CLI: `op read 'op://SparkShark/GOOGLE_PLACES_API_KEYS/api_key'`
//
// Usage:
//   node _tools/fetch-gbp-reviews.mjs
//
// Requirements: Node 18+ (uses built-in fetch + top-level await).

import { writeFileSync, mkdirSync } from "node:fs";
import { execSync } from "node:child_process";

const QUERY = "Spark Shark Electric Moore OK";
const OUT_PATH = "data/gbp-reviews.json";

let apiKey = process.env.GOOGLE_PLACES_API_KEY;
if (!apiKey) {
  try {
    apiKey = execSync(
      "op read 'op://SparkShark/GOOGLE_PLACES_API_KEYS/api_key'",
      { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }
    ).trim();
  } catch (e) {
    console.error("ERROR: GOOGLE_PLACES_API_KEY not set and op CLI fallback failed.");
    console.error("Run: op signin   then retry.");
    process.exit(1);
  }
}

// Step 1 — find place by text search
const searchRes = await fetch("https://places.googleapis.com/v1/places:searchText", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": apiKey,
    "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress",
  },
  body: JSON.stringify({ textQuery: QUERY }),
});

if (!searchRes.ok) {
  console.error(`Search failed: ${searchRes.status}`);
  console.error(await searchRes.text());
  process.exit(1);
}

const searchData = await searchRes.json();
const place = searchData.places?.[0];
if (!place?.id) {
  console.error(`No place matched query: ${QUERY}`);
  console.error(JSON.stringify(searchData, null, 2));
  process.exit(1);
}

console.log(`Found: ${place.displayName?.text} — ${place.formattedAddress}`);
console.log(`Place ID: ${place.id}`);

// Step 2 — get details with reviews
const detailRes = await fetch(`https://places.googleapis.com/v1/places/${place.id}`, {
  headers: {
    "X-Goog-Api-Key": apiKey,
    "X-Goog-FieldMask":
      "id,displayName,rating,userRatingCount,reviews.rating,reviews.text,reviews.originalText,reviews.relativePublishTimeDescription,reviews.publishTime,reviews.authorAttribution",
  },
});

if (!detailRes.ok) {
  console.error(`Details failed: ${detailRes.status}`);
  console.error(await detailRes.text());
  process.exit(1);
}

const detail = await detailRes.json();

// Normalize reviews into a stable shape for build.py
const reviews = (detail.reviews || []).map((r) => ({
  author: r.authorAttribution?.displayName || "Anonymous",
  rating: r.rating ?? null,
  text: r.text?.text || r.originalText?.text || "",
  publishTime: r.publishTime || null,
  relativeTime: r.relativePublishTimeDescription || "",
}));

const out = {
  fetchedAt: new Date().toISOString(),
  placeId: place.id,
  rating: detail.rating ?? null,
  reviewCount: detail.userRatingCount ?? null,
  reviews,
};

mkdirSync("data", { recursive: true });
writeFileSync(OUT_PATH, JSON.stringify(out, null, 2) + "\n");

console.log(
  `Wrote ${reviews.length} reviews to ${OUT_PATH} ` +
    `(rating=${out.rating}, total=${out.reviewCount})`
);
