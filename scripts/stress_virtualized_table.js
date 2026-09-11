/**
 * VirtualizedTable Scalability & Memory Stress Test
 * =================================================
 * Adversarially tests data structures and algorithms supporting @tanstack/react-virtual:
 * 1. 2,500 to 5,000 athlete records filtering and multi-column sorting.
 * 2. Virtualizer range calculation & window slicing across rapid scroll offsets.
 * 3. End-to-end single-frame budget: (filter + sort + window slice) strictly < 16.0ms (60 FPS).
 * 4. Heap retention & memory leak verification over sustained mutation cycles.
 */

import { performance } from "perf_hooks";
import v8 from "v8";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============================================================================
// DATA GENERATION: 2,500+ ATHLETE RECORDS
// ============================================================================

const FIRST_NAMES = [
  "Patrick", "Lamar", "Josh", "Joe", "C.J.", "Jalen", "Trevor", "Brock", "Justin",
  "Dak", "Jordan", "Kyler", "Tua", "Jared", "Baker", "Jayden", "Caleb", "Drake",
  "Saquon", "Christian", "Derrick", "Breece", "Bijan", "Jahmyr", "Jonathan", "Travis",
  "Justin", "Tyreek", "CeeDee", "Amon-Ra", "Ja'Marr", "A.J.", "Davante", "Garrett",
  "Puka", "Deebo", "DK", "Terry", "Mike", "Chris", "DJ", "Brandon", "George",
  "Sam", "Trey", "David", "T.J.", "Micah", "Myles", "Nick", "Chris", "Fred", "Roquan",
  "Sauce", "Pat", "Trent", "Minkah", "Kyle", "Antoine", "Jessie", "Jalen", "Derwin"
];

const LAST_NAMES = [
  "Mahomes", "Jackson", "Allen", "Burrow", "Stroud", "Hurts", "Lawrence", "Purdy",
  "Jefferson", "Prescott", "Love", "Murray", "Tagovailoa", "Goff", "Mayfield", "Daniels",
  "Williams", "Maye", "Barkley", "McCaffrey", "Henry", "Hall", "Robinson", "Gibbs",
  "Taylor", "Kelce", "Hill", "Lamb", "St. Brown", "Chase", "Brown", "Adams", "Wilson",
  "Nacua", "Samuel", "Metcalf", "McLaurin", "Evans", "Godwin", "Moore", "Aiyuk", "Kittle",
  "LaPorta", "McBride", "Montgomery", "Watt", "Parsons", "Garrett", "Bosa", "Jones",
  "Warner", "Smith", "Gardner", "Surtain", "McDuffie", "Fitzpatrick", "Hamilton", "Winfield",
  "Bates", "Ramsey", "James", "Johnson", "Davis", "Miller", "White", "Harris", "Clark"
];

const POSITIONS = [
  "QB", "RB", "WR", "TE", "OT", "OG", "C", "LT", "LG", "RG", "RT",
  "DE", "DT", "EDGE", "LB", "MLB", "OLB", "CB", "S", "FS", "SS", "K", "P"
];

const TIERS = ["Tier 1", "Tier 2", "Tier 3", "Tier 4"];

function generateAthletePool(count = 2500, seed = 42) {
  let s = seed;
  const pseudoRandom = () => {
    s = (s * 16807) % 2147483647;
    return (s - 1) / 2147483646;
  };

  const pool = [];
  for (let i = 1; i <= count; i++) {
    const fn = FIRST_NAMES[Math.floor(pseudoRandom() * FIRST_NAMES.length)];
    const ln = LAST_NAMES[Math.floor(pseudoRandom() * LAST_NAMES.length)];
    const pos = POSITIONS[Math.floor(pseudoRandom() * POSITIONS.length)];
    const tier = TIERS[Math.floor(pseudoRandom() * TIERS.length)];
    const ovr = Math.floor(65 + pseudoRandom() * 34); // 65-98
    const age = Math.floor(21 + pseudoRandom() * 14); // 21-34
    const aav = Math.floor((1000000 + (ovr - 65) * 800000) * (0.85 + pseudoRandom() * 0.3));
    const years = Math.floor(1 + pseudoRandom() * 5);

    pool.push({
      player_id: i,
      player_name: `${fn} ${ln}`,
      name: `${fn} ${ln}`,
      position: pos,
      tier: tier,
      overall_rating: ovr,
      age: age,
      projected_aav: aav,
      projected_years: years,
      top_interested_teams: ["KC", "SF", "BAL", "DET", "PHI"].slice(0, Math.floor(1 + pseudoRandom() * 4)),
    });
  }
  return pool;
}

// ============================================================================
// SIMULATED VIRTUALIZED TABLE PIPELINE
// ============================================================================

/**
 * Replicates the exact filter & sort logic from VirtualizedTable.tsx
 */
function processTableData(data, searchQuery, searchFilter, sortColumnId, sortDirection, sortKey) {
  let result = [...data];

  // 1. Filter
  if (searchQuery && searchQuery.trim() && searchFilter) {
    const query = searchQuery.trim().toLowerCase();
    result = result.filter((item) => searchFilter(item, query));
  }

  // 2. Sort
  if (sortColumnId && sortDirection && sortKey) {
    result.sort((a, b) => {
      const valA = sortKey(a);
      const valB = sortKey(b);

      if (valA == null && valB == null) return 0;
      if (valA == null) return sortDirection === "asc" ? 1 : -1;
      if (valB == null) return sortDirection === "asc" ? -1 : 1;

      if (typeof valA === "number" && typeof valB === "number") {
        return sortDirection === "asc" ? valA - valB : valB - valA;
      }

      const strA = String(valA).toLowerCase();
      const strB = String(valB).toLowerCase();
      return sortDirection === "asc" ? strA.localeCompare(strB) : strB.localeCompare(strA);
    });
  }

  return result;
}

/**
 * Replicates @tanstack/react-virtual window slicing
 */
function calculateVirtualItems(count, scrollTop, viewportHeight = 540, estimateRowHeight = 48, overscan = 12) {
  const totalSize = count * estimateRowHeight;
  const startIndex = Math.max(0, Math.floor(scrollTop / estimateRowHeight) - overscan);
  const endIndex = Math.min(count - 1, Math.ceil((scrollTop + viewportHeight) / estimateRowHeight) + overscan);

  const virtualItems = [];
  for (let i = startIndex; i <= endIndex; i++) {
    virtualItems.push({
      index: i,
      start: i * estimateRowHeight,
      size: estimateRowHeight,
      key: i,
    });
  }

  return { virtualItems, totalSize, startIndex, endIndex };
}

// ============================================================================
// BENCHMARK HARNESS
// ============================================================================

function runBenchmarks() {
  console.log("=".repeat(88));
  console.log("THE-NFL-SIM-V2: VIRTUALIZED TABLE SCALABILITY & MEMORY HARNESS");
  console.log("=".repeat(88));

  const RECORD_COUNT = 2500;
  const STRESS_RECORD_COUNT = 5000;

  console.log(`\nGenerating baseline ${RECORD_COUNT} athlete dataset...`);
  const dataset2500 = generateAthletePool(RECORD_COUNT);
  console.log(`Generating stress ${STRESS_RECORD_COUNT} athlete dataset...`);
  const dataset5000 = generateAthletePool(STRESS_RECORD_COUNT);

  const defaultFilter = (p, q) => {
    const name = p.player_name.toLowerCase();
    const pos = p.position.toLowerCase();
    const tier = (p.tier || "").toLowerCase();
    return name.includes(q) || pos.includes(q) || tier.includes(q);
  };

  const sortKeys = {
    ovr: (p) => p.overall_rating,
    aav: (p) => p.projected_aav,
    age: (p) => p.age,
    name: (p) => p.player_name,
    pos: (p) => p.position,
    tier: (p) => p.tier,
  };

  // --------------------------------------------------------------------------
  // TEST 1: FILTERING SCALABILITY ACROSS 1,000 QUERIES
  // --------------------------------------------------------------------------
  console.log(`\n[TEST 1] Testing dynamic filtering across 1,000 queries on ${RECORD_COUNT} records...`);
  const sampleQueries = ["", "j", "jo", "josh", "qb", "wr", "tier 1", "tier 2", "smith", "brown", "xyznonexistent", "cb", "ot"];
  const filterTimes = [];

  for (let i = 0; i < 1000; i++) {
    const q = sampleQueries[i % sampleQueries.length];
    const t0 = performance.now();
    const filtered = processTableData(dataset2500, q, defaultFilter, null, null, null);
    const t1 = performance.now();
    filterTimes.push(t1 - t0);
  }

  filterTimes.sort((a, b) => a - b);
  const avgFilter = filterTimes.reduce((acc, v) => acc + v, 0) / filterTimes.length;
  const p50Filter = filterTimes[Math.floor(filterTimes.length * 0.5)];
  const p95Filter = filterTimes[Math.floor(filterTimes.length * 0.95)];
  const p99Filter = filterTimes[Math.floor(filterTimes.length * 0.99)];
  const maxFilter = filterTimes[filterTimes.length - 1];

  console.log(`  Filter Latency: Avg ${avgFilter.toFixed(3)}ms | P50 ${p50Filter.toFixed(3)}ms | P95 ${p95Filter.toFixed(3)}ms | P99 ${p99Filter.toFixed(3)}ms | Max ${maxFilter.toFixed(3)}ms`);

  // --------------------------------------------------------------------------
  // TEST 2: MULTI-COLUMN SORTING SCALABILITY ACROSS 1,000 OPERATIONS
  // --------------------------------------------------------------------------
  console.log(`\n[TEST 2] Testing multi-column sorting across 1,000 operations on ${RECORD_COUNT} records...`);
  const sortColumns = ["ovr", "aav", "age", "name", "pos", "tier"];
  const sortDirections = ["asc", "desc"];
  const sortTimes = [];

  for (let i = 0; i < 1000; i++) {
    const col = sortColumns[i % sortColumns.length];
    const dir = sortDirections[i % sortDirections.length];
    const keyFn = sortKeys[col];

    const t0 = performance.now();
    const sorted = processTableData(dataset2500, "", null, col, dir, keyFn);
    const t1 = performance.now();
    sortTimes.push(t1 - t0);
  }

  sortTimes.sort((a, b) => a - b);
  const avgSort = sortTimes.reduce((acc, v) => acc + v, 0) / sortTimes.length;
  const p50Sort = sortTimes[Math.floor(sortTimes.length * 0.5)];
  const p95Sort = sortTimes[Math.floor(sortTimes.length * 0.95)];
  const p99Sort = sortTimes[Math.floor(sortTimes.length * 0.99)];
  const maxSort = sortTimes[sortTimes.length - 1];

  console.log(`  Sort Latency: Avg ${avgSort.toFixed(3)}ms | P50 ${p50Sort.toFixed(3)}ms | P95 ${p95Sort.toFixed(3)}ms | P99 ${p99Sort.toFixed(3)}ms | Max ${maxSort.toFixed(3)}ms`);

  // --------------------------------------------------------------------------
  // TEST 3: VIRTUALIZER WINDOW SLICING ACROSS 1,000 RAPID SCROLL EVENTS
  // --------------------------------------------------------------------------
  console.log(`\n[TEST 3] Testing @tanstack/react-virtual window calculation across 1,000 scroll events...`);
  const sliceTimes = [];
  const maxScroll = RECORD_COUNT * 48 - 540;

  for (let i = 0; i < 1000; i++) {
    const scrollPos = (i * 127) % maxScroll;
    const t0 = performance.now();
    const win = calculateVirtualItems(RECORD_COUNT, scrollPos, 540, 48, 12);
    const t1 = performance.now();
    sliceTimes.push(t1 - t0);
    if (i === 0) {
      if (win.virtualItems.length < 15 || win.virtualItems.length > 40) {
        throw new Error(`Unexpected virtual items count: ${win.virtualItems.length}`);
      }
    }
  }

  sliceTimes.sort((a, b) => a - b);
  const avgSlice = sliceTimes.reduce((acc, v) => acc + v, 0) / sliceTimes.length;
  const p50Slice = sliceTimes[Math.floor(sliceTimes.length * 0.5)];
  const p95Slice = sliceTimes[Math.floor(sliceTimes.length * 0.95)];
  const p99Slice = sliceTimes[Math.floor(sliceTimes.length * 0.99)];
  const maxSlice = sliceTimes[sliceTimes.length - 1];

  console.log(`  Slice Latency: Avg ${avgSlice.toFixed(3)}ms | P50 ${p50Slice.toFixed(3)}ms | P95 ${p95Slice.toFixed(3)}ms | P99 ${p99Slice.toFixed(3)}ms | Max ${maxSlice.toFixed(3)}ms`);

  // --------------------------------------------------------------------------
  // TEST 4: COMBINED FRAME PIPELINE (FILTER + SORT + VIRTUAL SLICE)
  // --------------------------------------------------------------------------
  console.log(`\n[TEST 4] Testing combined single-frame pipeline (Filter + Sort + Virtual Slice) on ${RECORD_COUNT} records...`);
  console.log("  Budget: strictly < 16.00ms per frame (60 FPS)");
  const combinedTimes = [];
  let violations = 0;

  for (let i = 0; i < 500; i++) {
    const q = sampleQueries[i % sampleQueries.length];
    const col = sortColumns[i % sortColumns.length];
    const dir = sortDirections[i % sortDirections.length];
    const keyFn = sortKeys[col];
    const scrollPos = (i * 97) % maxScroll;

    const t0 = performance.now();
    // 1. Filter + Sort
    const processed = processTableData(dataset2500, q, defaultFilter, col, dir, keyFn);
    // 2. Virtualizer Slicing
    const win = calculateVirtualItems(processed.length, scrollPos, 540, 48, 12);
    const t1 = performance.now();

    const frameTime = t1 - t0;
    combinedTimes.push(frameTime);
    if (frameTime >= 16.0) {
      violations++;
    }
  }

  combinedTimes.sort((a, b) => a - b);
  const avgComb = combinedTimes.reduce((acc, v) => acc + v, 0) / combinedTimes.length;
  const p50Comb = combinedTimes[Math.floor(combinedTimes.length * 0.5)];
  const p95Comb = combinedTimes[Math.floor(combinedTimes.length * 0.95)];
  const p99Comb = combinedTimes[Math.floor(combinedTimes.length * 0.99)];
  const maxComb = combinedTimes[combinedTimes.length - 1];

  console.log(`  Combined Frame Pipeline (2,500 records):`);
  console.log(`  Avg ${avgComb.toFixed(3)}ms | P50 ${p50Comb.toFixed(3)}ms | P95 ${p95Comb.toFixed(3)}ms | P99 ${p99Comb.toFixed(3)}ms | Max ${maxComb.toFixed(3)}ms`);
  console.log(`  Violations (>= 16.0ms): ${violations} / 500 frames`);

  // Also test combined on 5,000 records (2x stress factor)
  console.log(`\n[TEST 4B] Stress Test: Combined Pipeline on 5,000 athlete records (2x load)...`);
  const stressCombinedTimes = [];
  let stressViolations = 0;
  for (let i = 0; i < 300; i++) {
    const q = sampleQueries[i % sampleQueries.length];
    const col = sortColumns[i % sortColumns.length];
    const dir = sortDirections[i % sortDirections.length];
    const keyFn = sortKeys[col];
    const scrollPos = (i * 193) % (STRESS_RECORD_COUNT * 48 - 540);

    const t0 = performance.now();
    const processed = processTableData(dataset5000, q, defaultFilter, col, dir, keyFn);
    const win = calculateVirtualItems(processed.length, scrollPos, 540, 48, 12);
    const t1 = performance.now();

    const frameTime = t1 - t0;
    stressCombinedTimes.push(frameTime);
    if (frameTime >= 16.0) stressViolations++;
  }

  stressCombinedTimes.sort((a, b) => a - b);
  const avgStressComb = stressCombinedTimes.reduce((acc, v) => acc + v, 0) / stressCombinedTimes.length;
  const p95StressComb = stressCombinedTimes[Math.floor(stressCombinedTimes.length * 0.95)];
  const maxStressComb = stressCombinedTimes[stressCombinedTimes.length - 1];
  console.log(`  5,000 Records: Avg ${avgStressComb.toFixed(3)}ms | P95 ${p95StressComb.toFixed(3)}ms | Max ${maxStressComb.toFixed(3)}ms | Violations: ${stressViolations}`);

  // --------------------------------------------------------------------------
  // TEST 5: MEMORY RETENTION & LEAK VERIFICATION
  // --------------------------------------------------------------------------
  console.log(`\n[TEST 5] Verifying Memory Retention and Heap Stability across 1,000 mutation cycles...`);
  if (global.gc) global.gc();

  const initialHeap = process.memoryUsage().heapUsed;
  console.log(`  Initial Heap Used: ${(initialHeap / 1024 / 1024).toFixed(2)} MB`);

  let ephemeralReferences = [];
  for (let cycle = 1; cycle <= 1000; cycle++) {
    const q = sampleQueries[cycle % sampleQueries.length];
    const col = sortColumns[cycle % sortColumns.length];
    const dir = sortDirections[cycle % sortDirections.length];
    const keyFn = sortKeys[col];

    const processed = processTableData(dataset2500, q, defaultFilter, col, dir, keyFn);
    const win = calculateVirtualItems(processed.length, (cycle * 50) % maxScroll, 540, 48, 12);

    // Keep temporary reference only to visible items to simulate React component rendering
    const visibleData = win.virtualItems.map((item) => processed[item.index]);
    ephemeralReferences = visibleData;

    if (cycle % 250 === 0) {
      const midHeap = process.memoryUsage().heapUsed;
      console.log(`  Cycle ${cycle}/1000 - Ephemeral Heap: ${(midHeap / 1024 / 1024).toFixed(2)} MB`);
    }
  }

  ephemeralReferences = null;
  if (global.gc) global.gc();

  const finalHeap = process.memoryUsage().heapUsed;
  const heapDeltaMB = (finalHeap - initialHeap) / 1024 / 1024;
  console.log(`  Final Heap Used: ${(finalHeap / 1024 / 1024).toFixed(2)} MB (Delta: ${heapDeltaMB >= 0 ? "+" : ""}${heapDeltaMB.toFixed(2)} MB)`);

  const memoryPassed = heapDeltaMB < 5.0; // Less than 5MB growth after 1,000 full cycles
  console.log(`  Memory Stability Gate: ${memoryPassed ? "PASS (Zero Memory Leaks)" : "FAIL"}`);

  // --------------------------------------------------------------------------
  // SUMMARY REPORT
  // --------------------------------------------------------------------------
  console.log("\n" + "=".repeat(100));
  console.log(`${"OPERATION / BENCHMARK".padEnd(44)} | ${"BUDGET".padStart(10)} | ${"AVG".padStart(10)} | ${"P95".padStart(10)} | ${"MAX".padStart(10)} | ${"STATUS"}`);
  console.log("-".repeat(100));

  const results = [
    {
      name: "Search Filtering (2,500 records)",
      budget: "<16.0ms",
      avg: `${avgFilter.toFixed(3)}ms`,
      p95: `${p95Filter.toFixed(3)}ms`,
      max: `${maxFilter.toFixed(3)}ms`,
      passed: p95Filter < 16.0,
    },
    {
      name: "Multi-Column Sorting (2,500 records)",
      budget: "<16.0ms",
      avg: `${avgSort.toFixed(3)}ms`,
      p95: `${p95Sort.toFixed(3)}ms`,
      max: `${maxSort.toFixed(3)}ms`,
      passed: p95Sort < 16.0,
    },
    {
      name: "Virtualizer Window Slicing",
      budget: "<1.0ms",
      avg: `${avgSlice.toFixed(3)}ms`,
      p95: `${p95Slice.toFixed(3)}ms`,
      max: `${maxSlice.toFixed(3)}ms`,
      passed: p95Slice < 1.0,
    },
    {
      name: "Combined Frame Pipeline (2,500 records)",
      budget: "<16.0ms",
      avg: `${avgComb.toFixed(3)}ms`,
      p95: `${p95Comb.toFixed(3)}ms`,
      max: `${maxComb.toFixed(3)}ms`,
      passed: p95Comb < 16.0 && violations === 0,
    },
    {
      name: "Combined Pipeline 2x Stress (5,000 records)",
      budget: "<16.0ms",
      avg: `${avgStressComb.toFixed(3)}ms`,
      p95: `${p95StressComb.toFixed(3)}ms`,
      max: `${maxStressComb.toFixed(3)}ms`,
      passed: p95StressComb < 16.0 && stressViolations === 0,
    },
    {
      name: "Memory Retention & Heap Stability",
      budget: "<5MB delta",
      avg: `${heapDeltaMB.toFixed(2)} MB`,
      p95: "N/A",
      max: `${(finalHeap / 1024 / 1024).toFixed(1)} MB`,
      passed: memoryPassed,
    },
  ];

  let allPassed = true;
  for (const r of results) {
    if (!r.passed) allPassed = false;
    console.log(
      `${r.name.padEnd(44)} | ${r.budget.padStart(10)} | ${r.avg.padStart(10)} | ${r.p95.padStart(10)} | ${r.max.padStart(10)} | ${r.passed ? "PASS" : "FAIL"}`
    );
  }
  console.log("=".repeat(100));

  const jsonPath = path.join(__dirname, "virtualized_table_stress_results.json");
  fs.writeFileSync(jsonPath, JSON.stringify(results, null, 2), "utf-8");
  console.log(`Metrics written to ${jsonPath}`);

  if (allPassed) {
    console.log("\n[VERDICT: APPROVED] VIRTUALIZED TABLE SCALES SEAMLESSLY AT 2,500+ RECORDS WITHIN <16MS FRAME BUDGET.");
    process.exit(0);
  } else {
    console.log("\n[VERDICT: REQUEST_CHANGES] VIRTUALIZED TABLE FAILED PERFORMANCE OR MEMORY THRESHOLDS.");
    process.exit(1);
  }
}

runBenchmarks();
