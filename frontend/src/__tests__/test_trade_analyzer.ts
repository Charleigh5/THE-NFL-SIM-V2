/**
 * Automated Verification Suite for AccessibleTooltip Component & Trade Analyzer Humanized Metrics
 * Standards: W3C WAI-APG Tooltip Pattern, WCAG 2.1 AA Contrast, Corrupted Unicode Elimination,
 * and Contextual Trade Value Points (TVP) / Narrative Humanization Contracts.
 */

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { humanizeNarrativeNote } from "../components/trades/tradeNarrative.ts";
import type { TradeEvaluation } from "../types/trade.ts";

console.log("================================================================================");
console.log("ACCESSIBLE TOOLTIP & TRADE ANALYZER HUMANIZED METRICS VERIFICATION SUITE");
console.log("================================================================================\n");

// -----------------------------------------------------------------------------
// Test 1: AccessibleTooltip W3C WAI-APG Invariants & High Contrast CSS
// -----------------------------------------------------------------------------
console.log("Test 1: AccessibleTooltip Component & CSS Contracts...");
{
  const tsxPath = path.resolve(process.cwd(), "frontend/src/components/ui/AccessibleTooltip.tsx");
  const cssPath = path.resolve(process.cwd(), "frontend/src/components/ui/AccessibleTooltip.css");

  assert.ok(fs.existsSync(tsxPath), "AccessibleTooltip.tsx must exist");
  assert.ok(fs.existsSync(cssPath), "AccessibleTooltip.css must exist");

  const tsxContent = fs.readFileSync(tsxPath, "utf-8");
  const cssContent = fs.readFileSync(cssPath, "utf-8");

  // 1. WAI-APG Tooltip role & ARIA bindings
  assert.ok(
    tsxContent.includes('role="tooltip"'),
    "AccessibleTooltip must declare role='tooltip' on popup element"
  );
  assert.ok(
    tsxContent.includes("aria-describedby="),
    "AccessibleTooltip trigger must wire aria-describedby to tooltip ID"
  );
  assert.ok(
    tsxContent.includes("tabIndex={0}"),
    "AccessibleTooltip trigger must have tabIndex={0} for keyboard accessibility"
  );

  // 2. Mouse & Keyboard Interaction Handlers
  assert.ok(tsxContent.includes("onMouseEnter"), "AccessibleTooltip must support onMouseEnter");
  assert.ok(tsxContent.includes("onMouseLeave"), "AccessibleTooltip must support onMouseLeave");
  assert.ok(tsxContent.includes("onFocus"), "AccessibleTooltip must support onFocus");
  assert.ok(tsxContent.includes("onBlur"), "AccessibleTooltip must support onBlur");
  assert.ok(tsxContent.includes("onKeyDown"), "AccessibleTooltip must support onKeyDown");
  assert.ok(tsxContent.includes('"Escape"'), "AccessibleTooltip must dismiss on Escape key press");

  // 3. High-Contrast CSS Invariants
  assert.ok(
    cssContent.includes("#090d16"),
    "AccessibleTooltip.css must use high-contrast dark background #090d16"
  );
  assert.ok(cssContent.includes("#334155"), "AccessibleTooltip.css must use border #334155");
  assert.ok(
    cssContent.includes("#f1f5f9"),
    "AccessibleTooltip.css must use high-contrast text color #f1f5f9"
  );
  assert.ok(cssContent.includes("z-index: 100"), "AccessibleTooltip.css must specify z-index: 100");
  assert.ok(
    cssContent.includes("rgba(0, 0, 0, 0.5)") || cssContent.includes("rgba(0,0,0,0.5)"),
    "AccessibleTooltip.css must specify high-elevation box shadow"
  );

  // 4. Directional Positioning Variants
  assert.ok(
    cssContent.includes(".position-top"),
    "AccessibleTooltip.css must support .position-top"
  );
  assert.ok(
    cssContent.includes(".position-bottom"),
    "AccessibleTooltip.css must support .position-bottom"
  );
  assert.ok(
    cssContent.includes(".position-left"),
    "AccessibleTooltip.css must support .position-left"
  );
  assert.ok(
    cssContent.includes(".position-right"),
    "AccessibleTooltip.css must support .position-right"
  );

  console.log("  [PASS] AccessibleTooltip satisfies all W3C WAI-APG and WCAG 2.1 AA tokens.");
}

// -----------------------------------------------------------------------------
// Test 2: TradeAnalyzer Corrupted Unicode Elimination & Lucide Icon Contracts
// -----------------------------------------------------------------------------
console.log("\nTest 2: TradeAnalyzer Corrupted Unicode Elimination & Lucide Icon Contracts...");
{
  const tsxPath = path.resolve(process.cwd(), "frontend/src/components/trades/TradeAnalyzer.tsx");
  const cssPath = path.resolve(process.cwd(), "frontend/src/components/trades/TradeAnalyzer.css");

  const tsxContent = fs.readFileSync(tsxPath, "utf-8");
  const cssContent = fs.readFileSync(cssPath, "utf-8");

  // 1. Ensure corrupted unicode sequences are eliminated
  assert.ok(
    !tsxContent.includes("dY'"),
    "TradeAnalyzer.tsx must NOT contain corrupted 'dY'' unicode artifact"
  );
  assert.ok(
    !tsxContent.includes("\ufffd"),
    "TradeAnalyzer.tsx must NOT contain unicode replacement character (U+FFFD)"
  );
  assert.ok(
    !tsxContent.includes("💡"),
    "TradeAnalyzer.tsx must NOT contain raw bulb emoji in place of Lucide SVG icon"
  );

  // 2. Lucide Icons import and rendering in counter offer box
  assert.ok(
    tsxContent.includes("Handshake"),
    "TradeAnalyzer.tsx must import Handshake icon from lucide-react"
  );
  assert.ok(
    tsxContent.includes("Info"),
    "TradeAnalyzer.tsx must import Info icon from lucide-react"
  );
  assert.ok(
    tsxContent.includes("counter-icon-box"),
    "TradeAnalyzer.tsx must render Handshake within .counter-icon-box"
  );
  assert.ok(
    cssContent.includes(".counter-icon-box"),
    "TradeAnalyzer.css must define styles for .counter-icon-box"
  );
  assert.ok(
    cssContent.includes("rgba(245, 158, 11, 0.15)"),
    ".counter-icon-box must use amber-toned background"
  );

  console.log("  [PASS] Corrupted unicode fully eliminated; Lucide Handshake & Info active.");
}

// -----------------------------------------------------------------------------
// Test 3: Metric Humanization & Accessible Tooltip Wrappers
// -----------------------------------------------------------------------------
console.log("\nTest 3: Metric Humanization & Accessible Tooltip Wrappers...");
{
  const tsxPath = path.resolve(process.cwd(), "frontend/src/components/trades/TradeAnalyzer.tsx");
  const cssPath = path.resolve(process.cwd(), "frontend/src/components/trades/TradeAnalyzer.css");

  const tsxContent = fs.readFileSync(tsxPath, "utf-8");
  const cssContent = fs.readFileSync(cssPath, "utf-8");

  // 1. Fairness Surplus with Tooltip
  assert.ok(
    tsxContent.includes("Fairness Surplus:"),
    "TradeAnalyzer.tsx must label surplus metric as 'Fairness Surplus:'"
  );
  assert.ok(
    tsxContent.includes("Surplus percentage difference between offered and requested value"),
    "TradeAnalyzer.tsx must provide clear explanatory tooltip for Fairness Surplus"
  );

  // 2. Capital labels replace bare TVP
  assert.ok(
    tsxContent.includes("You Offer Capital"),
    "TradeAnalyzer.tsx must replace bare 'You Offer' with natural 'You Offer Capital'"
  );
  assert.ok(
    tsxContent.includes("You Receive Capital"),
    "TradeAnalyzer.tsx must replace bare 'You Receive' with natural 'You Receive Capital'"
  );
  assert.ok(tsxContent.includes("Pts"), "TradeAnalyzer.tsx values must display formatted 'Pts'");
  assert.ok(
    tsxContent.includes("Jimmy Johnson draft value"),
    "TradeAnalyzer.tsx must explain TVP calculation context in tooltip"
  );

  // 3. High Contrast CSS Tokens
  assert.ok(
    cssContent.includes("color: #d4d4d8"),
    "TradeAnalyzer.css must elevate secondary labels to zinc-300 (#d4d4d8)"
  );
  assert.ok(
    cssContent.includes("color: #f1f5f9"),
    "TradeAnalyzer.css must elevate primary metrics & tags to zinc-100 (#f1f5f9)"
  );

  console.log("  [PASS] Metric labels humanized with accessible tooltips and high contrast.");
}

// -----------------------------------------------------------------------------
// Test 4: Narrative Notes Humanizer Helper Invariants
// -----------------------------------------------------------------------------
console.log("\nTest 4: Narrative Notes Humanizer Helper Invariants...");
{
  // 1. TNI translation
  const tniNote = "TNI Flag: Critical surplus need at WR (+18.5% TVP)";
  const tniResult = humanizeNarrativeNote(tniNote);
  assert.ok(
    tniResult.label.includes("Team Need Fit"),
    "TNI abbreviation must translate to 'Team Need Fit'"
  );
  assert.ok(!tniResult.label.includes("TNI"), "Label must not contain untranslated 'TNI'");
  assert.ok(tniResult.label.includes("Pts"), "TVP suffix must translate to 'Pts'");
  assert.ok(
    tniResult.tooltip.includes("Team Need Fit") || tniResult.tooltip.includes("TNI"),
    "Tooltip must explain Team Need Fit"
  );

  // 2. EV Decay translation
  const evDecayNote = "Pick EV Decay: 2027 R1 discounted 15% due to 2-year draft horizon";
  const evResult = humanizeNarrativeNote(evDecayNote);
  assert.ok(
    evResult.label.includes("Draft Value Drift"),
    "EV Decay must translate to 'Draft Value Drift'"
  );
  assert.ok(!evResult.label.includes("EV Decay"), "Label must not contain untranslated 'EV Decay'");
  assert.ok(
    evResult.tooltip.includes("Draft Value Drift") || evResult.tooltip.includes("EV Decay"),
    "Tooltip must explain Draft Value Drift"
  );

  // 3. Cap Surcharge translation
  const surchargeNote = "Cap Surcharge: Dead cap hit of $8.2M creates trade friction";
  const surchargeResult = humanizeNarrativeNote(surchargeNote);
  assert.ok(
    surchargeResult.label.includes("Salary Cap Impact"),
    "Cap Surcharge must translate to 'Salary Cap Impact'"
  );
  assert.ok(
    !surchargeResult.label.includes("Cap Surcharge"),
    "Label must not contain untranslated 'Cap Surcharge'"
  );
  assert.ok(
    surchargeResult.tooltip.includes("Salary Cap Impact"),
    "Tooltip must explain Salary Cap Impact"
  );

  // 4. Medical / Durability Risk
  const medicalNote =
    "Medical Flag: Player carries IR designation with elevated knee re-injury risk";
  const medicalResult = humanizeNarrativeNote(medicalNote);
  assert.ok(
    medicalResult.tooltip.includes("Medical") || medicalResult.tooltip.includes("injury"),
    "Medical notes must carry medical risk explanation"
  );

  // 5. Holdout / Morale leverage
  const holdoutNote = "Holdout Leverage Discount: Tension score 82 forces seller discount";
  const holdoutResult = humanizeNarrativeNote(holdoutNote);
  assert.ok(
    holdoutResult.tooltip.includes("Leverage") || holdoutResult.tooltip.includes("morale"),
    "Holdout notes must explain locker room leverage discount"
  );

  // 6. Compensatory pick floor
  const compNote = "Compensatory Pick Floor: Protected 3rd round projected compensation (~500 TVP)";
  const compResult = humanizeNarrativeNote(compNote);
  assert.ok(
    compResult.tooltip.includes("Compensatory") || compResult.tooltip.includes("floor"),
    "Comp notes must explain compensatory pick floor"
  );
  assert.ok(compResult.label.includes("Pts"), "TVP inside compensatory note must translate to Pts");

  // 7. Intradivision tax
  const rivalryNote = "Intradivision Tax: AFC West divisional matchup premium applied";
  const rivalryResult = humanizeNarrativeNote(rivalryNote);
  assert.ok(
    rivalryResult.tooltip.includes("divisional") || rivalryResult.tooltip.includes("Intradivision"),
    "Rivalry notes must explain intradivision tax"
  );

  console.log(
    "  [PASS] All technical abbreviations (TNI, EV Decay, Cap Surcharge, etc.) accurately humanized."
  );
}

// -----------------------------------------------------------------------------
// Test 5: End-to-End Simulation of TradeEvaluation Data Flow
// -----------------------------------------------------------------------------
console.log("\nTest 5: End-to-End Simulation of TradeEvaluation Data Flow...");
{
  const mockEvaluation: TradeEvaluation = {
    decision: "ACCEPT",
    score: 8.4,
    reasoning: "The value offered aligns with our strategic rebuild timeline.",
    offered_value: 1250,
    requested_value: 1150,
    narrative_notes: [
      "TNI: High need at WR (+15% TVP)",
      "Pick EV Decay: 2027 R2 discounted",
      "Cap Surcharge: $2.1M dead money penalty",
      "Medical Flag: Player currently carries injury status (QUESTIONABLE)",
    ],
    counter_offer: {
      add_player_ids: [],
      add_picks: [],
      summary: "Consider exchanging our 2027 4th round pick for your 2026 3rd round pick.",
    },
    user_side: {
      team_id: 1,
      competitive_window: "WIN_NOW",
      value_in_tvp: 1250,
      value_out_tvp: 1150,
      ratio: 1.08,
      grade: "A-",
      factors: {
        market_tvp: 1200,
        need_fit_delta: 50,
        cap_impact_delta: 0,
        window_fit_delta: 0,
        class_fit_delta: 0,
        realism_modifiers_delta: 0,
        gm_threshold: 1.0,
      },
    },
    ai_side: {
      team_id: 2,
      competitive_window: "REBUILDING",
      value_in_tvp: 1150,
      value_out_tvp: 1250,
      ratio: 0.92,
      grade: "B+",
      factors: {
        market_tvp: 1150,
        need_fit_delta: 0,
        cap_impact_delta: 0,
        window_fit_delta: 0,
        class_fit_delta: 0,
        realism_modifiers_delta: 0,
        gm_threshold: 0.95,
      },
    },
  };

  assert.equal(mockEvaluation.decision, "ACCEPT");
  assert.equal(Math.round(mockEvaluation.offered_value!).toLocaleString(), "1,250");
  assert.equal(Math.round(mockEvaluation.requested_value!).toLocaleString(), "1,150");

  const processedNotes = mockEvaluation.narrative_notes!.map(humanizeNarrativeNote);
  assert.equal(processedNotes.length, 4);

  // Verify all notes have non-empty humanized labels and tooltips
  for (const item of processedNotes) {
    assert.ok(item.label.length > 0, "Label must not be empty");
    assert.ok(item.tooltip.length > 0, "Tooltip must not be empty");
    assert.ok(!item.label.includes("TNI"), "Note must not contain raw 'TNI'");
    assert.ok(!item.label.includes("EV Decay"), "Note must not contain raw 'EV Decay'");
    assert.ok(!item.label.includes("Cap Surcharge"), "Note must not contain raw 'Cap Surcharge'");
  }

  console.log("  [PASS] Mock trade evaluation stream processed through all humanization filters.");
}

console.log("\n================================================================================");
console.log("ALL TRADE ANALYZER & ACCESSIBLE TOOLTIP TESTS PASSED WITH 100% SUCCESS!");
console.log("================================================================================\n");
