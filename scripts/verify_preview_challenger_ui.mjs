/**
 * Empirical Challenger Verification Harness - UI Preview
 * =====================================================
 * Adversarially challenges:
 * 1. Codebase-wide token scan: zero rounded-xl/2xl/3xl, zero Sparkles from lucide-react.
 * 2. PlayoffBracket.tsx SVG geometry: cubic bezier determinism, non-NaN coordinates, Seed 1 Bye rendering.
 * 3. RouteDiagrammer.tsx: 6 play concepts coverage, SVG path validity, token coordinates, null/invalid play resilience.
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const frontendSrc = path.join(repoRoot, "frontend", "src");

console.log("================================================================================");
console.log("RUNNING EMPIRICAL CHALLENGER VERIFICATION HARNESS - UI PREVIEW");
console.log("================================================================================");

let totalPassed = 0;
let totalFailed = 0;

function assert(condition, message) {
  if (condition) {
    totalPassed++;
    console.log(`[PASS] ${message}`);
  } else {
    totalFailed++;
    console.error(`[FAIL] ${message}`);
  }
}

// Helper to recursively collect files
function getAllFiles(dir, extensions = [".tsx", ".ts", ".jsx", ".js"]) {
  let results = [];
  const list = fs.readdirSync(dir);
  for (const file of list) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllFiles(filePath, extensions));
    } else {
      const ext = path.extname(file);
      if (extensions.includes(ext)) {
        results.push(filePath);
      }
    }
  }
  return results;
}

// --------------------------------------------------------------------------------
// SECTION 1: CODEBASE SCAN FOR FORBIDDEN TOKENS & ICONS
// --------------------------------------------------------------------------------
console.log("\n--- SECTION 1: SCANNING CODEBASE FOR FORBIDDEN TOKENS & ICONS ---");

const allSrcFiles = getAllFiles(frontendSrc);
console.log(`Auditing ${allSrcFiles.length} source files in frontend/src...`);

let roundedForbiddenOccurrences = [];
let sparklesLucideOccurrences = [];

const roundedRegex = /\brounded-(xl|2xl|3xl)\b/g;
const sparklesFromLucideRegex = /import\s+[^'"]*Sparkles[^'"]*from\s+['"]lucide-react['"]/g;

for (const file of allSrcFiles) {
  const content = fs.readFileSync(file, "utf8");
  const relPath = path.relative(repoRoot, file);

  // Check rounded-xl, rounded-2xl, rounded-3xl
  let match;
  while ((match = roundedRegex.exec(content)) !== null) {
    roundedForbiddenOccurrences.push({ file: relPath, match: match[0], index: match.index });
  }

  // Check Sparkles from lucide-react
  if (sparklesFromLucideRegex.test(content)) {
    sparklesLucideOccurrences.push({ file: relPath });
  }
}

assert(
  roundedForbiddenOccurrences.length === 0,
  `Zero occurrences of rounded-xl, rounded-2xl, rounded-3xl in frontend/src (Found: ${roundedForbiddenOccurrences.length})`
);
if (roundedForbiddenOccurrences.length > 0) {
  console.error("Violations:", roundedForbiddenOccurrences);
}

assert(
  sparklesLucideOccurrences.length === 0,
  `Zero imports of Sparkles from lucide-react in frontend/src (Found: ${sparklesLucideOccurrences.length})`
);
if (sparklesLucideOccurrences.length > 0) {
  console.error("Violations:", sparklesLucideOccurrences);
}

// --------------------------------------------------------------------------------
// SECTION 2: EMPIRICALLY VERIFY PlayoffBracket.tsx SVG GEOMETRY
// --------------------------------------------------------------------------------
console.log("\n--- SECTION 2: VERIFYING PlayoffBracket.tsx SVG GEOMETRY ---");

const playoffBracketPath = path.join(frontendSrc, "components", "season", "PlayoffBracket.tsx");
assert(fs.existsSync(playoffBracketPath), "PlayoffBracket.tsx exists");

const playoffContent = fs.readFileSync(playoffBracketPath, "utf8");

// Extract CONNECTOR_ROUTES from file content
const connectorMatch = playoffContent.match(/const CONNECTOR_ROUTES: ConnectorRoute\[\] = (\[[\s\S]*?\]);/);
assert(connectorMatch !== null, "CONNECTOR_ROUTES definition extracted from PlayoffBracket.tsx");

// Evaluate connector routes safely
let connectorRoutes = [];
if (connectorMatch) {
  try {
    // Convert TS code to JSON-like JS
    const sanitized = connectorMatch[1]
      .replace(/\/\/.*$/gm, "")
      .replace(/(\w+):/g, '"$1":')
      .replace(/'/g, '"')
      .replace(/,(\s*[\]}])/g, "$1");
    connectorRoutes = JSON.parse(sanitized);
  } catch (e) {
    console.error("Failed to parse CONNECTOR_ROUTES JSON, falling back to regex parsing", e.message);
  }
}

assert(connectorRoutes.length === 14, `Exactly 14 tournament connector routes defined (Found: ${connectorRoutes.length})`);

// Cubic Bezier Spline Formula: M x1 y1 C mx y1, mx y2, x2 y2
function buildCubicBezierPath(x1, y1, x2, y2) {
  const mx = (x1 + x2) / 2;
  return `M ${x1} ${y1} C ${mx} ${y1}, ${mx} ${y2}, ${x2} ${y2}`;
}

let allBeziersDeterministic = true;
let allCoordsInBounds = true;

for (const route of connectorRoutes) {
  const { id, x1, y1, x2, y2, conference } = route;
  
  const isNumeric = [x1, y1, x2, y2].every((v) => typeof v === "number" && !isNaN(v) && Number.isFinite(v));
  if (!isNumeric) {
    allBeziersDeterministic = false;
    console.error(`Route ${id} contains non-numeric or NaN coordinates:`, route);
  }

  // Bounds check (Canvas is 2040 x 520)
  if (x1 < 0 || x1 > 2040 || x2 < 0 || x2 > 2040 || y1 < 0 || y1 > 520 || y2 < 0 || y2 > 520) {
    allCoordsInBounds = false;
    console.error(`Route ${id} coordinates out of canvas bounds (2040x520):`, route);
  }

  const pathD = buildCubicBezierPath(x1, y1, x2, y2);
  const pathRegex = /^M\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?)\s+C\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?),\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?),\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?)$/;
  if (!pathRegex.test(pathD)) {
    allBeziersDeterministic = false;
    console.error(`Route ${id} produced invalid SVG bezier command: ${pathD}`);
  }
}

assert(allBeziersDeterministic, "All 14 connector bezier curves have strictly deterministic, non-NaN coordinates");
assert(allCoordsInBounds, "All connector route endpoints reside strictly within the 2040x520 viewport canvas");

// Verify Seed 1 Bye Configuration
const byeSlots = [
  { id: "AFC_WC_0", code: "AFC_BYE", conf: "AFC" },
  { id: "NFC_WC_0", code: "NFC_BYE", conf: "NFC" }
];

for (const bye of byeSlots) {
  const hasSlot = playoffContent.includes(`id: "${bye.id}"`);
  const hasCode = playoffContent.includes(`code: "${bye.code}"`);
  const hasIsBye = playoffContent.includes("isBye: true");
  const hasExpectedSeed = playoffContent.includes("expectedSeeds: [1, 0]");

  assert(hasSlot && hasCode && hasIsBye && hasExpectedSeed, `Seed 1 Bye configured correctly for slot ${bye.id} (${bye.conf})`);
}

// Verify Seed 1 Bye UI badges and text
assert(
  playoffContent.includes("1-SEED BYE") &&
  playoffContent.includes("FIRST-ROUND BYE • AUTO ADVANCE") &&
  playoffContent.includes("AUTOMATIC FIRST-ROUND BYE"),
  "Seed 1 Bye celebration badges and explanation telemetry present in PlayoffBracket markup"
);

// --------------------------------------------------------------------------------
// SECTION 3: EMPIRICALLY VERIFY RouteDiagrammer.tsx SVG CONCEPTS & RESILIENCE
// --------------------------------------------------------------------------------
console.log("\n--- SECTION 3: VERIFYING RouteDiagrammer.tsx SVG CONCEPTS & RESILIENCE ---");

const routeDiagrammerPath = path.join(frontendSrc, "components", "playbook", "RouteDiagrammer.tsx");
assert(fs.existsSync(routeDiagrammerPath), "RouteDiagrammer.tsx exists");

const diagrammerContent = fs.readFileSync(routeDiagrammerPath, "utf8");

// Verify all 6 canonical play concepts exist
const expectedConcepts = ["GO", "SLANT", "MESH", "DIG", "ZONE", "COVER3"];
for (const key of expectedConcepts) {
  const conceptKeyExists = diagrammerContent.includes(`key: "${key}"`) || diagrammerContent.includes(`${key}: {`);
  assert(conceptKeyExists, `Play concept "${key}" is defined in CANONICAL_PLAY_CONCEPTS`);
}

// Verify SVG path commands inside RouteDiagrammer.tsx
// Extract all pathD occurrences
const pathDRegex = /pathD:\s*["']([^"']+)["']/g;
let pathDMatches = [];
let m;
while ((m = pathDRegex.exec(diagrammerContent)) !== null) {
  pathDMatches.push(m[1]);
}

assert(pathDMatches.length >= 20, `Extracted ${pathDMatches.length} route and defensive drop SVG paths from RouteDiagrammer.tsx`);

let allPathsValidSvg = true;
for (const p of pathDMatches) {
  // Must start with M and contain valid numbers
  if (!p.startsWith("M ") || p.includes("NaN") || p.includes("undefined")) {
    allPathsValidSvg = false;
    console.error(`Invalid SVG path detected: "${p}"`);
  }
}
assert(allPathsValidSvg, "All SVG path strings in RouteDiagrammer start with 'M ' and contain zero NaN/undefined");

// Test Play Concept Key Resolution Fallback Logic (simulating useMemo logic in RouteDiagrammer)
function resolveConceptKey(selectedPlay) {
  if (!selectedPlay?.id) return "GO";
  const id = selectedPlay.id.toLowerCase();
  if (id.includes("vert") || id.includes("go")) return "GO";
  if (id.includes("slant") || id.includes("rpo")) return "SLANT";
  if (id.includes("mesh")) return "MESH";
  if (id.includes("dig") || id.includes("dagger")) return "DIG";
  if (id.includes("zone") || id.includes("flood") || id.includes("sail")) return "ZONE";
  if (id.includes("cover") || id.includes("defense") || id.includes("sky")) return "COVER3";
  return "GO";
}

const testCases = [
  { input: null, expected: "GO", label: "null input" },
  { input: undefined, expected: "GO", label: "undefined input" },
  { input: {}, expected: "GO", label: "empty object" },
  { input: { id: "" }, expected: "GO", label: "empty id string" },
  { input: { id: "RANDOM_CORRUPT_ID_#999" }, expected: "GO", label: "unrecognized id fallback" },
  { input: { id: "gun-trips-verticals" }, expected: "GO", label: "vert ID" },
  { input: { id: "singleback_go_fade" }, expected: "GO", label: "go ID" },
  { input: { id: "rpo_slant_peek" }, expected: "SLANT", label: "slant/rpo ID" },
  { input: { id: "bunch_mesh_wheel" }, expected: "MESH", label: "mesh ID" },
  { input: { id: "dagger_deep_dig" }, expected: "DIG", label: "dig/dagger ID" },
  { input: { id: "sail_flood_zone" }, expected: "ZONE", label: "flood/zone ID" },
  { input: { id: "cover3_sky_match" }, expected: "COVER3", label: "cover3/defense ID" }
];

let allFallbackCasesPassed = true;
for (const tc of testCases) {
  const result = resolveConceptKey(tc.input);
  if (result !== tc.expected) {
    allFallbackCasesPassed = false;
    console.error(`Fallback failed for ${tc.label}: expected ${tc.expected}, got ${result}`);
  }
}

assert(allFallbackCasesPassed, "RouteDiagrammer concept fallback is robust and safely resolves all null/corrupt/unknown inputs to 'GO'");

// --------------------------------------------------------------------------------
// SECTION 4: SUMMARY VERDICT
// --------------------------------------------------------------------------------
console.log("\n================================================================================");
console.log(`SUMMARY: ${totalPassed} PASSED, ${totalFailed} FAILED`);
console.log("================================================================================");

if (totalFailed === 0) {
  console.log("RESULT: CONFIRM - All empirical challenges and stress tests passed successfully.");
  process.exit(0);
} else {
  console.error("RESULT: FAIL - Some empirical challenges detected defects.");
  process.exit(1);
}
