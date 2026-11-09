/**
 * Automated Verification Suite for Depth Chart Tactical IA & Progressive Disclosure
 * Step 3.2: Positional Vacancy Alert Badges (Ticket 6)
 * Step 3.4: Sticky Roster Limit & Active Gameday Cap Bar (Ticket 10)
 * Standards: 46-Man Gameday Active Cap, 53-Man Franchise Roster, Tabular Numerals,
 * Underfilled Vacancy Alarms, AST and DOM Test ID Contracts.
 */

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {
  POSITION_CONFIGS,
  UNIT_TABS,
  isPlayerCompatibleWithPosition,
  isPositionUnderfilled,
  getUnderfilledAlertTitle,
  calculateGamedayRosterMetrics,
} from "../utils/depthChartTaxonomy.ts";

console.log("================================================================================");
console.log("DEPTH CHART TACTICAL IA & PROGRESSIVE DISCLOSURE VERIFICATION SUITE");
console.log("================================================================================\n");

// -----------------------------------------------------------------------------
// Test 1: Positional Target Count Comparison & Vacancy Alert Invariants
// -----------------------------------------------------------------------------
console.log("Test 1: Positional Target Count & Vacancy Alert Invariants...");
{
  // 1.1 Verify Position Taxonomy Completeness
  assert.equal(POSITION_CONFIGS.length, 23, "Must configure 23 distinct NFL/NCAA position slots");
  assert.equal(UNIT_TABS.length, 4, "Must configure 4 master depth chart units");

  // Verify each position defines positive targetCount and compatible positions
  for (const pos of POSITION_CONFIGS) {
    assert.ok(pos.code.length >= 1, `Position code must be defined: ${pos.code}`);
    assert.ok(pos.name.length >= 2, `Position name must be defined: ${pos.name}`);
    assert.ok(pos.targetCount > 0, `Target count must be > 0 for ${pos.code}`);
    assert.ok(
      pos.compatiblePositions.length >= 1,
      `Compatible positions must not be empty for ${pos.code}`
    );
  }

  // 1.2 Target Count Definitions for Core Positions
  const qbConfig = POSITION_CONFIGS.find((p) => p.code === "QB");
  assert.ok(qbConfig);
  assert.equal(qbConfig.targetCount, 3, "QB target count should be 3");

  const rbConfig = POSITION_CONFIGS.find((p) => p.code === "RB");
  assert.ok(rbConfig);
  assert.equal(rbConfig.targetCount, 3, "RB target count should be 3");

  const wrConfig = POSITION_CONFIGS.find((p) => p.code === "WR");
  assert.ok(wrConfig);
  assert.equal(wrConfig.targetCount, 5, "WR target count should be 5");

  const otConfig = POSITION_CONFIGS.find((p) => p.code === "OT");
  assert.ok(otConfig);
  assert.equal(otConfig.targetCount, 4, "OT target count should be 4");

  const cbConfig = POSITION_CONFIGS.find((p) => p.code === "CB");
  assert.ok(cbConfig);
  assert.equal(cbConfig.targetCount, 5, "CB target count should be 5");

  const kConfig = POSITION_CONFIGS.find((p) => p.code === "K");
  assert.ok(kConfig);
  assert.equal(kConfig.targetCount, 1, "K target count should be 1");

  // 1.3 Underfilled Position Logic (count < targetCount)
  assert.equal(isPositionUnderfilled(0, 3), true, "0 players with target 3 is underfilled");
  assert.equal(isPositionUnderfilled(1, 3), true, "1 player with target 3 is underfilled");
  assert.equal(isPositionUnderfilled(2, 3), true, "2 players with target 3 is underfilled");
  assert.equal(isPositionUnderfilled(3, 3), false, "3 players with target 3 is filled");
  assert.equal(isPositionUnderfilled(4, 3), false, "4 players with target 3 is surplus/filled");

  // 1.4 Title String Contract for Accessible Warning Badge
  assert.equal(
    getUnderfilledAlertTitle("QB", 2, 3),
    "QB is underfilled (2/3 target athletes)",
    "Warning title must follow contract: {pos.code} is underfilled ({count}/{pos.targetCount} target athletes)"
  );
  assert.equal(
    getUnderfilledAlertTitle("WR", 3, 5),
    "WR is underfilled (3/5 target athletes)",
    "WR underfilled title must match target count"
  );
  assert.equal(
    getUnderfilledAlertTitle("K", 0, 1),
    "K is underfilled (0/1 target athletes)",
    "Kicker underfilled title must match target count"
  );

  // 1.5 Multi-position Compatibility & Rotational Staffing
  // Test Quarterback
  assert.equal(isPlayerCompatibleWithPosition("QB", "QB", ["QB"]), true);
  assert.equal(isPlayerCompatibleWithPosition("WR", "QB", ["QB"]), false);

  // Test Slot Cornerback (Nickel) matches CB, S, FS, SS
  assert.equal(isPlayerCompatibleWithPosition("CB", "SLCB", ["CB", "S", "FS", "SS"]), true);
  assert.equal(isPlayerCompatibleWithPosition("FS", "SLCB", ["CB", "S", "FS", "SS"]), true);
  assert.equal(isPlayerCompatibleWithPosition("DT", "SLCB", ["CB", "S", "FS", "SS"]), false);

  // Test Offensive Tackle matches OL, OT, OG, LT, RT, C
  assert.equal(
    isPlayerCompatibleWithPosition("LT", "OT", ["OT", "OL", "OG", "LT", "RT", "C"]),
    true
  );
  assert.equal(
    isPlayerCompatibleWithPosition("OL", "OT", ["OT", "OL", "OG", "LT", "RT", "C"]),
    true
  );
  assert.equal(
    isPlayerCompatibleWithPosition("WR", "OT", ["OT", "OL", "OG", "LT", "RT", "C"]),
    false
  );

  console.log("  ✓ Positional target counts and underfilled comparison invariants verified.");
}

// -----------------------------------------------------------------------------
// Test 2: Roster Limit & Gameday Active Calculations (NFL Invariants)
// -----------------------------------------------------------------------------
console.log("\nTest 2: Roster Limit & Gameday Active Calculations...");
{
  // 2.1 Empty Roster Edge Case
  const emptyMetrics = calculateGamedayRosterMetrics(0, 20_000_000);
  assert.equal(emptyMetrics.gamedayActive, 0, "Gameday active for empty roster must be 0");
  assert.equal(emptyMetrics.inactive, 0, "Inactive scratches for empty roster must be 0");
  assert.equal(emptyMetrics.totalRoster, 0, "Total roster for empty roster must be 0");
  assert.equal(emptyMetrics.capRoomMillions, "20.0");
  assert.equal(emptyMetrics.capRoomFormatted, "$20.0M");

  // 2.2 Depleted Roster (< 46 players)
  const depletedMetrics = calculateGamedayRosterMetrics(40, 15_500_000);
  assert.equal(
    depletedMetrics.gamedayActive,
    40,
    "40 players should all be active on gameday (min 40, 46)"
  );
  assert.equal(
    depletedMetrics.inactive,
    0,
    "Inactive count must be 0 when roster <= 46 (max 0, 40-46)"
  );
  assert.equal(depletedMetrics.totalRoster, 40);
  assert.equal(depletedMetrics.capRoomMillions, "15.5");
  assert.equal(depletedMetrics.capRoomFormatted, "$15.5M");

  // 2.3 Exact 46-Man Gameday Active Threshold
  const exact46Metrics = calculateGamedayRosterMetrics(46, 18_400_000);
  assert.equal(exact46Metrics.gamedayActive, 46, "Exact 46 players gives 46 gameday active");
  assert.equal(exact46Metrics.inactive, 0, "Exact 46 players leaves 0 inactive scratches");
  assert.equal(exact46Metrics.totalRoster, 46);
  assert.equal(exact46Metrics.capRoomMillions, "18.4");
  assert.equal(exact46Metrics.capRoomFormatted, "$18.4M");

  // 2.4 Standard Full 53-Man Active Roster (46 Active + 7 Inactive Scratches)
  const full53Metrics = calculateGamedayRosterMetrics(53, 12_000_000);
  assert.equal(full53Metrics.gamedayActive, 46, "Standard 53-man roster caps gameday active at 46");
  assert.equal(
    full53Metrics.inactive,
    7,
    "Standard 53-man roster has exactly 7 inactive scratches (53 - 46)"
  );
  assert.equal(full53Metrics.totalRoster, 53, "Total roster is 53");
  assert.equal(full53Metrics.capRoomMillions, "12.0");
  assert.equal(full53Metrics.capRoomFormatted, "$12.0M");

  // 2.5 Overfilled Preseason Roster (60 players)
  const campMetrics = calculateGamedayRosterMetrics(60, 5_250_000);
  assert.equal(campMetrics.gamedayActive, 46, "Active cap remains 46 even with 60 players");
  assert.equal(campMetrics.inactive, 14, "Inactive scratch count is 14 (60 - 46)");
  assert.equal(campMetrics.totalRoster, 60);
  assert.equal(campMetrics.capRoomMillions, "5.3");
  assert.equal(campMetrics.capRoomFormatted, "$5.3M");

  // 2.6 Zero and Negative Cap Room formatting
  const zeroCap = calculateGamedayRosterMetrics(53, 0);
  assert.equal(zeroCap.capRoomMillions, "0.0");
  assert.equal(zeroCap.capRoomFormatted, "$0.0M");

  console.log(
    "  ✓ Roster limit, gameday active/inactive caps, and salary room conversions verified."
  );
}

// -----------------------------------------------------------------------------
// Test 3: AST & DOM Test ID Contracts in DepthChart.tsx
// -----------------------------------------------------------------------------
console.log("\nTest 3: AST & DOM Test ID Contracts in DepthChart.tsx...");
{
  const tsxPath = path.resolve(process.cwd(), "frontend/src/pages/DepthChart.tsx");
  assert.ok(fs.existsSync(tsxPath), "DepthChart.tsx must exist");
  const tsxContent = fs.readFileSync(tsxPath, "utf-8");

  // 3.1 Persistent Sticky HUD Container & Test ID
  assert.ok(
    tsxContent.includes('data-testid="gameday-roster-hud"'),
    "DepthChart.tsx must render element with data-testid='gameday-roster-hud'"
  );
  assert.ok(
    tsxContent.includes("depth-roster-hud"),
    "DepthChart.tsx HUD must include class 'depth-roster-hud'"
  );
  assert.ok(
    tsxContent.includes("sticky top-0 z-30"),
    "DepthChart.tsx HUD must have 'sticky top-0 z-30' classes"
  );

  // 3.2 HUD Metric Content & Calculations
  assert.ok(
    tsxContent.includes("GAMEDAY ACTIVE:"),
    "DepthChart.tsx HUD must render 'GAMEDAY ACTIVE:' label"
  );
  assert.ok(
    tsxContent.includes("{rosterMetrics.gamedayActive}") ||
      tsxContent.includes("{Math.min(roster.length, 46)}"),
    "DepthChart.tsx HUD must compute gameday active metric"
  );

  assert.ok(tsxContent.includes("INACTIVE:"), "DepthChart.tsx HUD must render 'INACTIVE:' label");
  assert.ok(
    tsxContent.includes("{rosterMetrics.inactive}") ||
      tsxContent.includes("{Math.max(0, roster.length - 46)}"),
    "DepthChart.tsx HUD must compute inactive metric"
  );

  assert.ok(
    tsxContent.includes("TOTAL ROSTER:"),
    "DepthChart.tsx HUD must render 'TOTAL ROSTER:' label"
  );
  assert.ok(
    tsxContent.includes("{rosterMetrics.totalRoster}") || tsxContent.includes("{roster.length}"),
    "DepthChart.tsx HUD must display total roster count"
  );

  assert.ok(tsxContent.includes("CAP ROOM:"), "DepthChart.tsx HUD must render 'CAP ROOM:' label");
  assert.ok(
    tsxContent.includes("rosterMetrics.capRoomFormatted") ||
      tsxContent.includes("(currentTeam.salary_cap_space / 1_000_000).toFixed(1)}M"),
    "DepthChart.tsx HUD must compute and display formatted cap room"
  );

  // 3.3 Tabular Numerals Font Formatting
  assert.ok(
    tsxContent.includes("font-mono tabular-nums"),
    "DepthChart.tsx HUD must enforce font-mono tabular-nums for metric alignment"
  );

  // 3.4 Color Highlight Badges on HUD
  assert.ok(
    tsxContent.includes("text-emerald-400"),
    "GAMEDAY ACTIVE metric must use emerald highlight"
  );
  assert.ok(tsxContent.includes("text-amber-400"), "INACTIVE metric must use amber highlight");
  assert.ok(tsxContent.includes("text-cyan-400"), "TOTAL ROSTER metric must use cyan highlight");

  // 3.5 Positional Vacancy Alert Badges on Position Tabs
  assert.ok(
    tsxContent.includes("data-testid={`underfilled-badge-${pos.code}`}"),
    "DepthChart.tsx must render underfilled-badge-${pos.code} on vacancy alerts"
  );
  assert.ok(
    tsxContent.includes("underfilled-pos-badge"),
    "DepthChart.tsx must apply 'underfilled-pos-badge' class"
  );
  assert.ok(
    tsxContent.includes("border border-amber-500/50 bg-amber-500/20 text-amber-300 font-bold"),
    "DepthChart.tsx badge must apply amber styling tokens"
  );
  assert.ok(
    tsxContent.includes("title={alertTitle}") ||
      tsxContent.includes(
        "title={`${pos.code} is underfilled (${count}/${pos.targetCount} target athletes)`}"
      ),
    "DepthChart.tsx badge must declare accessible title warning"
  );
  assert.ok(
    tsxContent.includes("AlertTriangle"),
    "DepthChart.tsx must import and render AlertTriangle icon inside vacancy warning badge"
  );

  console.log("  ✓ DepthChart.tsx AST, DOM test IDs, and calculation expressions verified.");
}

// -----------------------------------------------------------------------------
// Test 4: CSS Stylesheet Contracts in DepthChartSpatial.css
// -----------------------------------------------------------------------------
console.log("\nTest 4: CSS Stylesheet Contracts in DepthChartSpatial.css...");
{
  const cssPath = path.resolve(process.cwd(), "frontend/src/pages/DepthChartSpatial.css");
  assert.ok(fs.existsSync(cssPath), "DepthChartSpatial.css must exist");
  const cssContent = fs.readFileSync(cssPath, "utf-8");

  // 4.1 Sticky Roster HUD Styling
  assert.ok(
    cssContent.includes(".depth-roster-hud"),
    "DepthChartSpatial.css must define .depth-roster-hud rule"
  );
  assert.ok(
    cssContent.includes("position: sticky;"),
    ".depth-roster-hud must define position: sticky"
  );
  assert.ok(cssContent.includes("top: 0;"), ".depth-roster-hud must define top: 0");
  assert.ok(
    cssContent.includes("backdrop-filter: blur"),
    ".depth-roster-hud must define backdrop-filter: blur"
  );
  assert.ok(
    cssContent.includes("border-bottom: 1px solid rgba(255, 255, 255, 0.12);"),
    ".depth-roster-hud must define subtle bottom border"
  );

  // 4.2 Mobile Responsiveness
  assert.ok(
    cssContent.includes("@media (max-width: 768px)") && cssContent.includes(".depth-roster-hud"),
    "DepthChartSpatial.css must include mobile responsive query for .depth-roster-hud"
  );

  // 4.3 Positional Vacancy Alert Badge & Amber Pulse Animation
  assert.ok(
    cssContent.includes(".underfilled-pos-badge"),
    "DepthChartSpatial.css must define .underfilled-pos-badge"
  );
  assert.ok(
    cssContent.includes("amberPulse"),
    "DepthChartSpatial.css must link underfilled-pos-badge to amberPulse animation"
  );
  assert.ok(
    cssContent.includes("@keyframes amberPulse"),
    "DepthChartSpatial.css must define @keyframes amberPulse"
  );

  // 4.4 Reduced Motion Accessibility
  assert.ok(
    cssContent.includes("@media (prefers-reduced-motion: reduce)") &&
      cssContent.includes(".underfilled-pos-badge"),
    "DepthChartSpatial.css must disable vacancy badge animation under prefers-reduced-motion"
  );

  console.log(
    "  ✓ DepthChartSpatial.css rules, animations, and accessibility media queries verified."
  );
}

console.log("\n================================================================================");
console.log("ALL DEPTH CHART TACTICAL IA & PROGRESSIVE DISCLOSURE TESTS PASSED (100%)");
console.log("================================================================================");
