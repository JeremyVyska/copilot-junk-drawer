#!/usr/bin/env node
/**
 * extract-week.js
 * Copies the Clockify SQLite DB (locked while app runs), queries AutoTrackerItems
 * for the past 7 days, buckets entries into 30-minute slots, and writes a JSON
 * report to ./weekly-exports/YYYY-MM-DD_week.json
 *
 * Usage:
 *   node extract-week.js              # past 7 days
 *   node extract-week.js --days 14    # past 14 days
 *   node extract-week.js --from 2026-02-10 --to 2026-02-16
 */

const Database = require('better-sqlite3');
const fs = require('fs');
const path = require('path');

// ── Config ────────────────────────────────────────────────────────────────────
// Default: Windows location. Update for macOS/Linux if needed:
//   macOS: ~/Library/Application Support/Clockify/ClockifyDB_v2.db
//   Linux: ~/.config/Clockify/ClockifyDB_v2.db
const DB_SRC  = path.join(process.env.LOCALAPPDATA || process.env.HOME, 'Clockify', 'ClockifyDB_v2.db');
const DB_COPY = path.join(__dirname, 'ClockifyDB_copy.db');
const OUT_DIR = path.join(__dirname, 'weekly-exports');

// ── Arg parsing ───────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
let fromDate, toDate;

const daysIdx = args.indexOf('--days');
const fromIdx = args.indexOf('--from');
const toIdx   = args.indexOf('--to');

if (fromIdx !== -1 && toIdx !== -1) {
  fromDate = args[fromIdx + 1];
  toDate   = args[toIdx   + 1];
} else {
  const days = daysIdx !== -1 ? parseInt(args[daysIdx + 1]) : 7;
  const now  = new Date();
  toDate     = now.toISOString().slice(0, 10);
  const from = new Date(now);
  from.setDate(from.getDate() - days);
  fromDate = from.toISOString().slice(0, 10);
}

console.log(`Extracting AutoTrack data from ${fromDate} to ${toDate}`);

// ── Copy DB ───────────────────────────────────────────────────────────────────
console.log(`Copying ${DB_SRC} ...`);
if (!fs.existsSync(DB_SRC)) {
  console.error(`ERROR: Database not found at ${DB_SRC}`);
  console.error('Please verify Clockify is installed and AutoTracker is enabled.');
  process.exit(1);
}
fs.copyFileSync(DB_SRC, DB_COPY);

// ── Query ─────────────────────────────────────────────────────────────────────
const db   = new Database(DB_COPY, { readonly: true });
const rows = db.prepare(`
  SELECT
    id, Name, AppTitle, Description, Url,
    Start, End, TotalTime, IdleSeconds,
    Browser, IsEntryCreated, UrlAccessDenied
  FROM AutoTrackerItems
  WHERE Start >= '${fromDate}'
    AND Start <  '${toDate} 23:59:59'
    AND (IdleSeconds IS NULL OR IdleSeconds < 120)   -- skip fully-idle windows
  ORDER BY Start
`).all();
db.close();

console.log(`Found ${rows.length} entries`);

// ── Bucket into 30-min slots ──────────────────────────────────────────────────
function slotKey(isoStr) {
  // isoStr like "2026-02-16 09:14:22.123"
  const d = new Date(isoStr.replace(' ', 'T'));
  const mm = d.getMinutes() < 30 ? '00' : '30';
  const hh = String(d.getHours()).padStart(2, '0');
  const date = isoStr.slice(0, 10);
  return `${date} ${hh}:${mm}`;
}

function parseDuration(totalTime) {
  // "00:03:38" -> seconds
  if (!totalTime) return 0;
  const [h, m, s] = totalTime.split(':').map(Number);
  return h * 3600 + m * 60 + s;
}

function formatDuration(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  if (h > 0) return `${h}h ${m}m`;
  if (m > 0) return `${m}m ${s}s`;
  return `${s}s`;
}

const slots = {}; // slotKey -> { slot, entries[], totalActiveSeconds }

for (const row of rows) {
  const key = slotKey(row.Start);
  if (!slots[key]) {
    slots[key] = { slot: key, totalActiveSeconds: 0, entries: [] };
  }
  const durationSec = parseDuration(row.TotalTime);
  slots[key].totalActiveSeconds += durationSec;
  slots[key].entries.push({
    app:          row.Name,
    title:        row.AppTitle,
    description:  row.Description,
    url:          row.Url !== '-' ? row.Url : null,
    start:        row.Start,
    end:          row.End,
    duration:     row.TotalTime,
    durationSec,
    idleSec:      row.IdleSeconds ?? 0,
    browser:      row.Browser > 0,
    entryCreated: row.IsEntryCreated === 1,
  });
}

// Build sorted output
const slotList = Object.values(slots).sort((a, b) => a.slot.localeCompare(b.slot));
slotList.forEach(s => {
  s.totalActive = formatDuration(s.totalActiveSeconds);
  // Sort entries within slot by duration desc so most prominent appear first
  s.entries.sort((a, b) => b.durationSec - a.durationSec);
});

// Group by day
const byDay = {};
for (const slot of slotList) {
  const day = slot.slot.slice(0, 10);
  if (!byDay[day]) byDay[day] = [];
  byDay[day].push(slot);
}

const output = {
  generated:  new Date().toISOString(),
  from:       fromDate,
  to:         toDate,
  totalSlots: slotList.length,
  totalEntries: rows.length,
  days: Object.entries(byDay).map(([date, slots]) => ({
    date,
    slots,
  })),
};

// ── Write output ──────────────────────────────────────────────────────────────
fs.mkdirSync(OUT_DIR, { recursive: true });

// Full week file
const outFile = path.join(OUT_DIR, `${toDate}_week.json`);
fs.writeFileSync(outFile, JSON.stringify(output, null, 2));
console.log(`Written to ${outFile}`);

// Per-day files for parallel day agents
for (const day of output.days) {
  const dayFile = path.join(OUT_DIR, `${day.date}_daydata.json`);
  fs.writeFileSync(dayFile, JSON.stringify(day, null, 2));
  console.log(`  Day file: ${dayFile}`);
}

console.log(`Days covered: ${Object.keys(byDay).join(', ')}`);

// Clean up temporary DB copy
fs.unlinkSync(DB_COPY);
console.log('Cleanup complete.');
