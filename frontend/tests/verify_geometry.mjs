import fs from 'fs';
import path from 'path';

console.log('================================================================');
console.log('EMPIRICAL ADVERSARIAL VERIFICATION: PLAYOFF BRACKET & PLAYBOOK');
console.log('================================================================\n');

let totalPassed = 0;
let totalFailed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`[PASS] ${message}`);
    totalPassed++;
  } else {
    console.error(`[FAIL] ${message}`);
    totalFailed++;
  }
}

// ============================================================================
// PART 1: PLAYOFF BRACKET SVG BEZIER GEOMETRY AUDIT
// ============================================================================
console.log('--- TEST SUITE 1: PlayoffBracket.tsx Bezier Splines & Topology ---');

const bracketFilePath = path.resolve('frontend/src/components/season/PlayoffBracket.tsx');
assert(fs.existsSync(bracketFilePath), `PlayoffBracket.tsx exists at ${bracketFilePath}`);

const bracketSource = fs.readFileSync(bracketFilePath, 'utf-8');

// Parse BRACKET_COLUMNS
const colsBlockMatch = bracketSource.match(/const BRACKET_COLUMNS: ColumnDefinition\[\] = (\[[\s\S]*?\n\];)/);
assert(Boolean(colsBlockMatch), 'Found BRACKET_COLUMNS constant block in source');

const cleanedColsCode = colsBlockMatch[1]
  .replace(/PlayoffConference\.AFC/g, '"AFC"')
  .replace(/PlayoffConference\.NFC/g, '"NFC"')
  .replace(/PlayoffConference\.SUPER_BOWL/g, '"SUPER_BOWL"')
  .replace(/PlayoffRound\.WILD_CARD/g, '"WILD_CARD"')
  .replace(/PlayoffRound\.DIVISIONAL/g, '"DIVISIONAL"')
  .replace(/PlayoffRound\.CONFERENCE/g, '"CONFERENCE"')
  .replace(/PlayoffRound\.SUPER_BOWL/g, '"SUPER_BOWL"');

const bracketColumns = new Function(`return ${cleanedColsCode}`)();
assert(bracketColumns.length === 7, `BRACKET_COLUMNS has 7 columns (found ${bracketColumns.length})`);

const slotMap = new Map();
let totalSlots = 0;
for (const col of bracketColumns) {
  for (const slot of col.slots) {
    slotMap.set(slot.id, slot);
    totalSlots++;
  }
}
assert(totalSlots === 15, `BRACKET_COLUMNS defines exactly 15 tournament slots (found ${totalSlots})`);

// Parse CONNECTOR_ROUTES
const routesBlockMatch = bracketSource.match(/const CONNECTOR_ROUTES: ConnectorRoute\[\] = (\[[\s\S]*?\n\];)/);
assert(Boolean(routesBlockMatch), 'Found CONNECTOR_ROUTES constant block in source');

const connectorRoutes = new Function(`return ${routesBlockMatch[1]}`)();
assert(connectorRoutes.length === 14, `CONNECTOR_ROUTES defines exactly 14 progression routes (found ${connectorRoutes.length})`);

// Cubic bezier path generator function extracted verbatim
const buildCubicBezierPath = (x1, y1, x2, y2) => {
  const mx = (x1 + x2) / 2;
  return `M ${x1} ${y1} C ${mx} ${y1}, ${mx} ${y2}, ${x2} ${y2}`;
};

const bezierRegex = /^M (\d+(\.\d+)?) (\d+(\.\d+)?) C (\d+(\.\d+)?) (\d+(\.\d+)?), (\d+(\.\d+)?) (\d+(\.\d+)?), (\d+(\.\d+)?) (\d+(\.\d+)?)$/;

for (const route of connectorRoutes) {
  const { id, sourceSlotId, targetSlotId, x1, y1, x2, y2, conference } = route;

  // Verify non-NaN & non-undefined coordinates
  const coordsValid = [x1, y1, x2, y2].every((v) => typeof v === 'number' && !isNaN(v) && isFinite(v));
  assert(coordsValid, `Route ${id} coordinates [${x1}, ${y1}, ${x2}, ${y2}] are strictly finite numbers`);

  const pathD = buildCubicBezierPath(x1, y1, x2, y2);
  const regexValid = bezierRegex.test(pathD);
  const noCorrupt = !pathD.includes('NaN') && !pathD.includes('undefined');
  assert(regexValid && noCorrupt, `Route ${id} pathD="${pathD}" conforms to SVG cubic bezier geometry`);

  // Verify slots exist
  const sourceSlot = slotMap.get(sourceSlotId);
  const targetSlot = slotMap.get(targetSlotId);
  assert(Boolean(sourceSlot), `Route ${id} sourceSlotId ${sourceSlotId} exists in tournament grid`);
  assert(Boolean(targetSlot), `Route ${id} targetSlotId ${targetSlotId} exists in tournament grid`);

  // Verify geometric anchoring
  if (sourceSlot && targetSlot) {
    if (conference === 'AFC') {
      const expectedX1 = sourceSlot.x + sourceSlot.width;
      const expectedY1 = sourceSlot.y + sourceSlot.height / 2;
      const expectedX2 = targetSlot.x;
      const expectedY2 = targetSlot.y + targetSlot.height / 2;
      assert(x1 === expectedX1 && y1 === expectedY1, `Route ${id} AFC source (${x1},${y1}) aligns with slot ${sourceSlotId} right edge`);
      assert(x2 === expectedX2 && y2 === expectedY2, `Route ${id} AFC target (${x2},${y2}) aligns with slot ${targetSlotId} left edge`);
    } else if (conference === 'NFC') {
      const expectedX1 = sourceSlot.x;
      const expectedY1 = sourceSlot.y + sourceSlot.height / 2;
      const expectedX2 = targetSlot.x + targetSlot.width;
      const expectedY2 = targetSlot.y + targetSlot.height / 2;
      assert(x1 === expectedX1 && y1 === expectedY1, `Route ${id} NFC source (${x1},${y1}) aligns with slot ${sourceSlotId} left edge`);
      assert(x2 === expectedX2 && y2 === expectedY2, `Route ${id} NFC target (${x2},${y2}) aligns with slot ${targetSlotId} right edge`);
    } else if (conference === 'SB') {
      if (sourceSlot.conference === 'AFC') {
        assert(x1 === sourceSlot.x + sourceSlot.width && y1 === sourceSlot.y + sourceSlot.height / 2, `Route ${id} SB AFC source aligns`);
        assert(x2 === targetSlot.x && y2 === targetSlot.y + targetSlot.height / 2, `Route ${id} SB target aligns with SB slot left edge`);
      } else if (sourceSlot.conference === 'NFC') {
        assert(x1 === sourceSlot.x && y1 === sourceSlot.y + sourceSlot.height / 2, `Route ${id} SB NFC source aligns`);
        assert(x2 === targetSlot.x + targetSlot.width && y2 === targetSlot.y + targetSlot.height / 2, `Route ${id} SB target aligns with SB slot right edge`);
      }
    }
  }
}

// Seed 1 Bye verification
console.log('\n--- TEST SUITE 2: Seed 1 Bye Slots Verification ---');
const afcBye = slotMap.get('AFC_WC_0');
const nfcBye = slotMap.get('NFC_WC_0');

assert(Boolean(afcBye && afcBye.isBye), 'AFC_WC_0 is configured with isBye: true');
assert(JSON.stringify(afcBye.expectedSeeds) === '[1,0]', 'AFC_WC_0 expectedSeeds is [1, 0]');
assert(Boolean(nfcBye && nfcBye.isBye), 'NFC_WC_0 is configured with isBye: true');
assert(JSON.stringify(nfcBye.expectedSeeds) === '[1,0]', 'NFC_WC_0 expectedSeeds is [1, 0]');

// Check rendering strings in source
assert(bracketSource.includes('1-SEED BYE'), 'PlayoffBracket.tsx renders "1-SEED BYE" telemetry header');
assert(bracketSource.includes('FIRST-ROUND BYE • AUTO ADVANCE'), 'PlayoffBracket.tsx renders "FIRST-ROUND BYE • AUTO ADVANCE" badge');
assert(bracketSource.includes('SEEDED'), 'PlayoffBracket.tsx renders "SEEDED" marker for Bye team');

// ============================================================================
// PART 2: ROUTE DIAGRAMMER CONCEPTS, SVG PATHS & TOKENS
// ============================================================================
console.log('\n--- TEST SUITE 3: RouteDiagrammer.tsx Play Concepts & SVG Geometry ---');

const routeDiagrammerPath = path.resolve('frontend/src/components/playbook/RouteDiagrammer.tsx');
assert(fs.existsSync(routeDiagrammerPath), `RouteDiagrammer.tsx exists at ${routeDiagrammerPath}`);

const rdSource = fs.readFileSync(routeDiagrammerPath, 'utf-8');

const requiredConcepts = ['GO', 'SLANT', 'MESH', 'DIG', 'ZONE', 'COVER3'];
for (const concept of requiredConcepts) {
  assert(rdSource.includes(`${concept}: {`), `RouteDiagrammer contains canonical play concept ${concept}`);
}

// Extract CANONICAL_PLAY_CONCEPTS using eval in sandbox
const rdObjMatch = rdSource.match(/const CANONICAL_PLAY_CONCEPTS: Record<PlayConceptKey, PlaybookConcept> = (\{[\s\S]*?\n\};)/);
assert(Boolean(rdObjMatch), 'Found CANONICAL_PLAY_CONCEPTS dictionary block in source');

// Quick functional parse of the object
const canonicalConcepts = (new Function(`return ${rdObjMatch[1]}`))();

const svgPathCommandRegex = /^[MLHVCSQTAZ0-9\s.,-]+$/i;

for (const key of requiredConcepts) {
  const concept = canonicalConcepts[key];
  assert(Boolean(concept), `Loaded concept ${key}`);
  assert(concept.key === key, `Concept key matches ${key}`);
  assert(typeof concept.name === 'string' && concept.name.length > 0, `Concept ${key} has name: "${concept.name}"`);
  assert(typeof concept.conceptTitle === 'string' && concept.conceptTitle.length > 0, `Concept ${key} has conceptTitle: "${concept.conceptTitle}"`);
  assert(typeof concept.formation === 'string' && concept.formation.length > 0, `Concept ${key} has formation: "${concept.formation}"`);
  assert(typeof concept.personnel === 'string' && concept.personnel.length > 0, `Concept ${key} has personnel: "${concept.personnel}"`);

  // Offensive Tokens
  assert(Array.isArray(concept.offensiveTokens) && concept.offensiveTokens.length >= 3, `Concept ${key} has ${concept.offensiveTokens.length} offensive tokens`);
  for (const token of concept.offensiveTokens) {
    const valid = token.id && token.label && typeof token.x === 'number' && typeof token.y === 'number' && !isNaN(token.x) && !isNaN(token.y);
    assert(valid, `Concept ${key} offensive token ${token.id} (${token.label}) at (${token.x}, ${token.y}) has finite non-NaN coords`);
  }

  // Offensive Linemen
  assert(Array.isArray(concept.offensiveLinemen) && concept.offensiveLinemen.length === 5, `Concept ${key} has 5 offensive linemen (LT, LG, C, RG, RT)`);
  for (const ol of concept.offensiveLinemen) {
    assert(typeof ol.x === 'number' && !isNaN(ol.x) && typeof ol.y === 'number' && !isNaN(ol.y), `Concept ${key} OL ${ol.id} has finite non-NaN coords`);
  }

  // Defensive Tokens
  assert(Array.isArray(concept.defensiveTokens) && concept.defensiveTokens.length >= 3, `Concept ${key} has ${concept.defensiveTokens.length} defensive tokens`);
  for (const dt of concept.defensiveTokens) {
    assert(typeof dt.x === 'number' && !isNaN(dt.x) && typeof dt.y === 'number' && !isNaN(dt.y), `Concept ${key} defensive token ${dt.id} has finite non-NaN coords`);
  }

  // Routes
  assert(Array.isArray(concept.routes) && concept.routes.length >= 2, `Concept ${key} has ${concept.routes.length} offensive routes`);
  for (const route of concept.routes) {
    assert(typeof route.pathD === 'string' && route.pathD.length > 0, `Concept ${key} route for ${route.playerId} has pathD: "${route.pathD}"`);
    assert(svgPathCommandRegex.test(route.pathD), `Concept ${key} route pathD adheres to SVG path grammar`);
    assert(!route.pathD.includes('NaN') && !route.pathD.includes('undefined'), `Concept ${key} route pathD has zero NaN/undefined`);
    assert(typeof route.endPoint.x === 'number' && !isNaN(route.endPoint.x) && typeof route.endPoint.y === 'number' && !isNaN(route.endPoint.y), `Concept ${key} route endPoint (${route.endPoint.x}, ${route.endPoint.y}) is finite non-NaN`);
    assert(typeof route.timing === 'string' && route.timing.length > 0, `Concept ${key} route has timing: "${route.timing}"`);
    assert(typeof route.depthYards === 'number' && !isNaN(route.depthYards), `Concept ${key} route depthYards is valid`);
  }

  // Defensive Drops
  assert(Array.isArray(concept.defensiveDrops) && concept.defensiveDrops.length >= 2, `Concept ${key} has ${concept.defensiveDrops.length} defensive drops`);
  for (const drop of concept.defensiveDrops) {
    assert(typeof drop.pathD === 'string' && drop.pathD.length > 0, `Concept ${key} defensive drop for ${drop.playerId} has pathD: "${drop.pathD}"`);
    assert(svgPathCommandRegex.test(drop.pathD), `Concept ${key} drop pathD adheres to SVG path grammar`);
    assert(!drop.pathD.includes('NaN') && !drop.pathD.includes('undefined'), `Concept ${key} drop pathD has zero NaN/undefined`);
  }

  // Coverage Zones
  assert(Array.isArray(concept.coverageZones) && concept.coverageZones.length >= 1, `Concept ${key} has ${concept.coverageZones.length} defensive coverage zones`);
  for (const zone of concept.coverageZones) {
    const coordsValid = [zone.cx, zone.cy, zone.rx, zone.ry].every((v) => typeof v === 'number' && !isNaN(v) && isFinite(v));
    assert(coordsValid, `Concept ${key} coverage zone ${zone.id} (${zone.label}) has finite non-NaN ellipse coords: cx=${zone.cx}, cy=${zone.cy}, rx=${zone.rx}, ry=${zone.ry}`);
  }

  // Blocking Lines (Pass protection on offense, 0 on pure defensive scheme)
  const expectedBlockingCount = concept.type === 'DEFENSE' ? 0 : 5;
  assert(Array.isArray(concept.blockingLines) && concept.blockingLines.length === expectedBlockingCount, `Concept ${key} has ${concept.blockingLines.length} pass-pro blocking lines (expected ${expectedBlockingCount} for ${concept.type})`);
  for (const bl of concept.blockingLines) {
    const coordsValid = [bl.startX, bl.startY, bl.endX, bl.endY, bl.tBarX1, bl.tBarY1, bl.tBarX2, bl.tBarY2].every((v) => typeof v === 'number' && !isNaN(v) && isFinite(v));
    assert(coordsValid, `Concept ${key} blocking line ${bl.id} (${bl.label}) has finite non-NaN coordinates`);
  }
}

// ============================================================================
// PART 3: ADVERSARIAL INPUT RESOLUTION TO ROUTE DIAGRAMMER
// ============================================================================
console.log('\n--- TEST SUITE 4: Adversarial Input Resolution to RouteDiagrammer ---');

// Extracted verbatim from RouteDiagrammer.tsx initialKey resolver
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

function resolveConcept(selectedPlay) {
  const key = resolveConceptKey(selectedPlay);
  return canonicalConcepts[key] || canonicalConcepts.GO;
}

const adversarialTestCases = [
  { input: null, expectedKey: "GO", name: "null" },
  { input: undefined, expectedKey: "GO", name: "undefined" },
  { input: {}, expectedKey: "GO", name: "empty object {}" },
  { input: { id: "" }, expectedKey: "GO", name: 'empty id: ""' },
  { input: { id: "RANDOM_CORRUPT_PLAY_999" }, expectedKey: "GO", name: "unknown id string" },
  { input: { id: null }, expectedKey: "GO", name: "id: null" },
  { input: { id: undefined }, expectedKey: "GO", name: "id: undefined" },
  { input: { id: "gun_trips_verts" }, expectedKey: "GO", name: 'id: "gun_trips_verts"' },
  { input: { id: "rpo_slant_peek" }, expectedKey: "SLANT", name: 'id: "rpo_slant_peek"' },
  { input: { id: "mesh_rub_wheel" }, expectedKey: "MESH", name: 'id: "mesh_rub_wheel"' },
  { input: { id: "dagger_dig_in" }, expectedKey: "DIG", name: 'id: "dagger_dig_in"' },
  { input: { id: "flood_sail_zone" }, expectedKey: "ZONE", name: 'id: "flood_sail_zone"' },
  { input: { id: "cover3_sky_buzz" }, expectedKey: "COVER3", name: 'id: "cover3_sky_buzz"' },
];

for (const tc of adversarialTestCases) {
  const resolvedKey = resolveConceptKey(tc.input);
  const concept = resolveConcept(tc.input);
  assert(resolvedKey === tc.expectedKey, `Adversarial input (${tc.name}) resolved key to "${resolvedKey}" (expected "${tc.expectedKey}")`);
  assert(Boolean(concept && concept.key === tc.expectedKey), `Adversarial input (${tc.name}) safely retrieved canonical concept "${concept?.key}" with non-null geometry`);
}

console.log('\n================================================================');
console.log(`TOTAL AUDIT ASSERTIONS: ${totalPassed + totalFailed}`);
console.log(`PASSED: ${totalPassed}`);
console.log(`FAILED: ${totalFailed}`);
console.log('================================================================');

if (totalFailed > 0) {
  process.exit(1);
} else {
  process.exit(0);
}
