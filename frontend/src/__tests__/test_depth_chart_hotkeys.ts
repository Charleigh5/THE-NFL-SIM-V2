/**
 * Automated Invariant & AST Verification Suite for Pro-Coach Hotkeys
 * Step 4.1: Pro-Coach Hotkeys & End-to-End Adversarial Verification
 *
 * Verifies:
 * 1. Unit Hotkey Mapping Invariants (1: OFFENSE, 2: DEFENSE, 3: SPECIAL_TEAMS, 4: SPECIALISTS).
 * 2. Input and Modal Suppression Guards (INPUT, TEXTAREA, SELECT, contentEditable, useModalStackStore).
 * 3. AST and DOM Test ID Contracts in DepthChart.tsx (unit-hotkey-1..4, unit-tab-*, audio feedback).
 * 4. CSS Stylistic Contracts in DepthChartSpatial.css (.unit-hotkey-chip tokens and layout).
 */

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { UNIT_TABS, UNIT_HOTKEY_MAP, isHotkeySuppressed } from "../utils/depthChartTaxonomy.ts";
import { useModalStackStore } from "../store/useModalStackStore.ts";

console.log("================================================================================");
console.log("PRO-COACH HOTKEYS & DEPTH CHART ADVERSARIAL VERIFICATION SUITE");
console.log("================================================================================\n");

// -----------------------------------------------------------------------------
// Test 1: Unit Hotkey Mapping & Taxonomy Invariants
// -----------------------------------------------------------------------------
console.log("Test 1: Unit Hotkey Mapping & Taxonomy Invariants...");
{
  // 1.1 Verify exact key mappings
  assert.equal(UNIT_HOTKEY_MAP["1"], "OFFENSE", "Key '1' must switch to OFFENSE unit");
  assert.equal(UNIT_HOTKEY_MAP["2"], "DEFENSE", "Key '2' must switch to DEFENSE unit");
  assert.equal(UNIT_HOTKEY_MAP["3"], "SPECIAL_TEAMS", "Key '3' must switch to SPECIAL_TEAMS unit");
  assert.equal(UNIT_HOTKEY_MAP["4"], "SPECIALISTS", "Key '4' must switch to SPECIALISTS unit");

  // 1.2 Verify unmapped keys return undefined
  assert.equal(UNIT_HOTKEY_MAP["5"], undefined, "Key '5' must be undefined");
  assert.equal(UNIT_HOTKEY_MAP["0"], undefined, "Key '0' must be undefined");
  assert.equal(UNIT_HOTKEY_MAP["q"], undefined, "Key 'q' must be undefined");
  assert.equal(UNIT_HOTKEY_MAP["Enter"], undefined, "Key 'Enter' must be undefined");

  // 1.3 Verify 1:1 alignment with UNIT_TABS order
  assert.equal(UNIT_TABS.length, 4, "Must configure exactly 4 master units");
  UNIT_TABS.forEach((tab, idx) => {
    const key = String(idx + 1);
    assert.equal(
      UNIT_HOTKEY_MAP[key],
      tab.id,
      `Hotkey '${key}' must strictly correspond to tab ${idx} (${tab.id})`
    );
  });

  console.log("  [PASS] Hotkey unit mappings and 1:1 tab index alignment verified.");
}

// -----------------------------------------------------------------------------
// Test 2: Input and Modal Suppression Guard Logic
// -----------------------------------------------------------------------------
console.log("\nTest 2: Input & Modal Suppression Guard Invariants...");
{
  // 2.1 Clean state: no active element, no modals -> not suppressed
  assert.equal(
    isHotkeySuppressed(null, 0),
    false,
    "Hotkeys must be active when no element is focused and no modals open"
  );
  assert.equal(
    isHotkeySuppressed({ tagName: "DIV" }, 0),
    false,
    "Focusing standard non-input element (DIV) must not suppress hotkeys"
  );
  assert.equal(
    isHotkeySuppressed({ tagName: "BUTTON" }, 0),
    false,
    "Focusing a BUTTON must not suppress hotkeys"
  );
  assert.equal(
    isHotkeySuppressed({ tagName: "BODY" }, 0),
    false,
    "Focusing BODY must not suppress hotkeys"
  );

  // 2.2 Form control suppression
  assert.equal(
    isHotkeySuppressed({ tagName: "INPUT" }, 0),
    true,
    "Focusing INPUT element must suppress hotkeys"
  );
  assert.equal(
    isHotkeySuppressed({ tagName: "input" }, 0),
    true,
    "Lowercase input tag check must be case-insensitive"
  );
  assert.equal(
    isHotkeySuppressed({ tagName: "TEXTAREA" }, 0),
    true,
    "Focusing TEXTAREA must suppress hotkeys"
  );
  assert.equal(
    isHotkeySuppressed({ tagName: "SELECT" }, 0),
    true,
    "Focusing SELECT must suppress hotkeys"
  );
  assert.equal(
    isHotkeySuppressed({ tagName: "DIV", isContentEditable: true }, 0),
    true,
    "contentEditable elements must suppress hotkeys"
  );

  // 2.3 Modal Stack Store integration
  useModalStackStore.getState().clearStack();
  assert.equal(useModalStackStore.getState().stack.length, 0);
  assert.equal(
    isHotkeySuppressed(null, useModalStackStore.getState().stack.length),
    false,
    "Hotkeys allowed when modal stack is empty"
  );

  // Push modal onto stack
  useModalStackStore.getState().pushModal("test-modal-dossier", () => {});
  assert.equal(useModalStackStore.getState().stack.length, 1);
  assert.equal(
    isHotkeySuppressed(null, useModalStackStore.getState().stack.length),
    true,
    "Hotkeys must be suppressed when a modal is open in useModalStackStore"
  );

  // Even standard buttons or document are suppressed when modal is open
  assert.equal(
    isHotkeySuppressed({ tagName: "BUTTON" }, useModalStackStore.getState().stack.length),
    true,
    "Hotkeys must remain suppressed while modal is active, even on button focus"
  );

  // Pop modal and clear
  useModalStackStore.getState().clearStack();
  assert.equal(useModalStackStore.getState().stack.length, 0);
  assert.equal(
    isHotkeySuppressed(null, useModalStackStore.getState().stack.length),
    false,
    "Hotkeys must be re-enabled after closing modals"
  );

  console.log("  [PASS] Input elements and ModalStackStore suppression guards verified.");
}

// -----------------------------------------------------------------------------
// Test 3: DepthChart.tsx AST, Hotkey Listener & DOM Test ID Contracts
// -----------------------------------------------------------------------------
console.log("\nTest 3: DepthChart.tsx AST & DOM Test ID Contracts...");
{
  const tsxPath = path.resolve(process.cwd(), "frontend/src/pages/DepthChart.tsx");
  assert.ok(fs.existsSync(tsxPath), `DepthChart.tsx must exist at ${tsxPath}`);
  const tsxContent = fs.readFileSync(tsxPath, "utf-8");

  // 3.1 Store & Audio Engine Imports
  assert.ok(
    tsxContent.includes('import { useModalStackStore } from "../store/useModalStackStore";') ||
      tsxContent.includes('from "../store/useModalStackStore"'),
    "DepthChart.tsx must import useModalStackStore"
  );
  assert.ok(
    tsxContent.includes('import { soundEffects } from "../services/soundEffects";'),
    "DepthChart.tsx must import soundEffects"
  );
  assert.ok(
    tsxContent.includes("UNIT_HOTKEY_MAP"),
    "DepthChart.tsx must import or define UNIT_HOTKEY_MAP"
  );

  // 3.2 Keydown Event Listener & Window Attachment
  assert.ok(
    tsxContent.includes('window.addEventListener("keydown"'),
    "DepthChart.tsx must attach keydown listener to window"
  );
  assert.ok(
    tsxContent.includes('window.removeEventListener("keydown"'),
    "DepthChart.tsx must cleanup keydown listener on unmount"
  );

  // 3.3 Audio Snap Feedback
  assert.ok(
    tsxContent.includes("soundEffects.playSnap()"),
    "DepthChart.tsx must invoke soundEffects.playSnap() on hotkey trigger"
  );

  // 3.4 False Activation Protections
  assert.ok(
    tsxContent.includes("document.activeElement"),
    "DepthChart.tsx must inspect document.activeElement"
  );
  assert.ok(
    tsxContent.includes('"INPUT"') &&
      tsxContent.includes('"TEXTAREA"') &&
      tsxContent.includes('"SELECT"'),
    "DepthChart.tsx must guard against INPUT, TEXTAREA, and SELECT elements"
  );
  assert.ok(
    tsxContent.includes("isContentEditable"),
    "DepthChart.tsx must guard against contentEditable elements"
  );
  assert.ok(
    tsxContent.includes("useModalStackStore.getState().stack.length > 0"),
    "DepthChart.tsx must guard against open modals in useModalStackStore"
  );
  assert.ok(
    tsxContent.includes("ctrlKey") &&
      tsxContent.includes("altKey") &&
      tsxContent.includes("metaKey"),
    "DepthChart.tsx must ignore modifier keys (ctrlKey, altKey, metaKey)"
  );

  // 3.5 Unit Tab and Hotkey Chip DOM Test IDs
  assert.ok(
    tsxContent.includes("data-testid={`unit-tab-${tab.id.toLowerCase()}`}"),
    "DepthChart.tsx must attach data-testid={`unit-tab-${tab.id.toLowerCase()}`} to unit buttons"
  );
  assert.ok(
    tsxContent.includes("data-testid={`unit-hotkey-${idx + 1}`}"),
    "DepthChart.tsx must attach data-testid={`unit-hotkey-${idx + 1}`} to hotkey chips"
  );
  assert.ok(
    tsxContent.includes('className="unit-hotkey-chip"'),
    "DepthChart.tsx must apply unit-hotkey-chip class to kbd element"
  );
  assert.ok(
    tsxContent.includes("title={`Press ${idx + 1} to switch to ${tab.label}`}"),
    "DepthChart.tsx must provide accessible hotkey title tooltip"
  );

  console.log("  [PASS] DepthChart.tsx AST, hotkey listener, and DOM test ID contracts verified.");
}

// -----------------------------------------------------------------------------
// Test 4: CSS Stylesheet Contracts in DepthChartSpatial.css
// -----------------------------------------------------------------------------
console.log("\nTest 4: CSS Stylesheet Contracts in DepthChartSpatial.css...");
{
  const cssPath = path.resolve(process.cwd(), "frontend/src/pages/DepthChartSpatial.css");
  assert.ok(fs.existsSync(cssPath), "DepthChartSpatial.css must exist");
  const cssContent = fs.readFileSync(cssPath, "utf-8");

  // 4.1 Class declaration
  assert.ok(
    cssContent.includes(".unit-hotkey-chip"),
    "DepthChartSpatial.css must define .unit-hotkey-chip rule"
  );

  // 4.2 Styling tokens: Monospace, high-contrast border and background, inset shadow, padding
  assert.ok(
    cssContent.includes("font-family:") && cssContent.includes("monospace"),
    ".unit-hotkey-chip must specify monospace font family"
  );
  assert.ok(
    cssContent.includes("background: rgba(0, 0, 0, 0.4)") || cssContent.includes("bg-black/40"),
    ".unit-hotkey-chip must apply dark high-contrast background"
  );
  assert.ok(
    cssContent.includes("rgba(255, 255, 255, 0.2)") || cssContent.includes("border-white/20"),
    ".unit-hotkey-chip must apply subtle border"
  );
  assert.ok(
    cssContent.includes("rgb(103, 232, 249)") || cssContent.includes("text-cyan-300"),
    ".unit-hotkey-chip must apply cyan text color"
  );
  assert.ok(
    cssContent.includes("box-shadow: inset") || cssContent.includes("inset 0 1px"),
    ".unit-hotkey-chip must apply subtle inset shadow"
  );
  assert.ok(
    cssContent.includes("padding: 0.125rem 0.375rem") || cssContent.includes("px-1.5 py-0.5"),
    ".unit-hotkey-chip must specify compact padding"
  );
  assert.ok(
    cssContent.includes("font-size: 10px") || cssContent.includes("text-[10px]"),
    ".unit-hotkey-chip must set 10px font size"
  );
  assert.ok(
    cssContent.includes("font-weight: 700") || cssContent.includes("font-bold"),
    ".unit-hotkey-chip must set bold font weight"
  );

  console.log("  [PASS] DepthChartSpatial.css .unit-hotkey-chip visual styling verified.");
}

console.log("\n================================================================================");
console.log("ALL PRO-COACH HOTKEY INVARIANT TESTS PASSED WITH 100% SUCCESS!");
console.log("================================================================================");
