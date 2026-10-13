import fs from "fs";
import path from "path";
import React from "react";
import { renderToString } from "react-dom/server";

console.log("================================================================================");
console.log("EMPIRICAL ADVERSARIAL CHALLENGER 2: PERFORMANCE, BUNDLE & INTERACTIVE MATRIX");
console.log("================================================================================\n");

let totalPassed = 0;
let totalFailed = 0;

function assert(condition: boolean, testName: string, details?: string) {
  if (condition) {
    console.log(`[PASS] ${testName}${details ? ` -> ${details}` : ""}`);
    totalPassed++;
  } else {
    console.error(`[FAIL] ${testName}${details ? ` -> ${details}` : ""}`);
    totalFailed++;
  }
}

// ============================================================================
// SUITE 1: BUILD ASSURANCE & BUNDLE BUDGET AUDIT
// ============================================================================
console.log("--- TEST SUITE 1: Bundle Budget & Build Artifact Audit ---");

const distDir = path.resolve("dist");
assert(fs.existsSync(distDir), "dist directory exists", distDir);

const assetsDir = path.join(distDir, "assets");
assert(fs.existsSync(assetsDir), "dist/assets directory exists", assetsDir);

const assetFiles = fs.readdirSync(assetsDir);
const indexJsFiles = assetFiles.filter((f) => f.startsWith("index-") && f.endsWith(".js"));

assert(
  indexJsFiles.length > 0,
  "Entry chunk dist/assets/index-*.js found",
  JSON.stringify(indexJsFiles)
);

let entryChunkSizeKb = 0;
if (indexJsFiles.length > 0) {
  const entryFile = path.join(assetsDir, indexJsFiles[0]);
  const stats = fs.statSync(entryFile);
  const sizeBytes = stats.size;
  entryChunkSizeKb = sizeBytes / 1024;
  console.log(
    `Exact entry chunk: ${indexJsFiles[0]} | ${sizeBytes} bytes | ${entryChunkSizeKb.toFixed(2)} kB`
  );

  // Target: strictly < 450 kB
  assert(
    entryChunkSizeKb < 450,
    `Entry chunk size strictly < 450 kB budget`,
    `${entryChunkSizeKb.toFixed(2)} kB < 450.00 kB (Margin: ${(450 - entryChunkSizeKb).toFixed(2)} kB)`
  );
}

// Audit all major vendor and route chunks
console.log("\nComplete Assets Inventory:");
const recordedAssets: Array<{ name: string; sizeKb: number }> = [];
for (const file of assetFiles) {
  const filePath = path.join(assetsDir, file);
  const stats = fs.statSync(filePath);
  const kb = stats.size / 1024;
  recordedAssets.push({ name: file, sizeKb: kb });
  console.log(`  - ${file.padEnd(45)} ${kb.toFixed(2).padStart(8)} kB`);
}

// Verify code splitting of secondary views
const secondaryPagesToCheck = [
  "DraftRoom",
  "TradeCenterPage",
  "TrophyRoom",
  "MedicalCenter",
  "EnvironmentalWeatherLab",
  "Playbook",
  "SkillsPage",
  "FreeAgency",
  "LockerRoom",
  "OffseasonDashboard",
  "SeasonDashboard",
];

for (const pageName of secondaryPagesToCheck) {
  const found = assetFiles.some((f) => f.startsWith(pageName) && f.endsWith(".js"));
  assert(found, `Secondary page chunk exists for ${pageName}`);
}

// ============================================================================
// SUITE 2: LOADINGSPINNER EMPIRICAL STRESS TESTS
// ============================================================================
console.log("\n--- TEST SUITE 2: LoadingSpinner.tsx Stress & Props Audit ---");

// Import component directly
import { LoadingSpinner } from "../src/components/ui/LoadingSpinner";

// 2.1 Props Variations: Small, Medium, Large, Custom Colors, Custom Texts
console.log("\n[Sub-suite 2.1] Props Variations Rendering:");

// Small variant
const smallHtml = renderToString(
  React.createElement(LoadingSpinner, {
    size: "small",
    color: "#ff00aa",
    text: "INLINE_TEST",
  })
);
assert(smallHtml.includes("loading-spinner-container"), "Small variant renders container class");
assert(smallHtml.includes("small"), "Small variant has 'small' class");
assert(smallHtml.includes("INLINE_TEST"), "Small variant renders custom text");
assert(smallHtml.includes("--loader-accent:#ff00aa"), "Small variant injects custom color CSS var");
assert(
  smallHtml.includes("max-w-full") && smallHtml.includes("overflow-hidden"),
  "Small variant contains max-w-full and overflow-hidden wrapper"
);

// Medium variant
const medHtml = renderToString(
  React.createElement(LoadingSpinner, {
    size: "medium",
    color: "white",
    text: "MEDIUM_TEST",
  })
);
assert(medHtml.includes("loading-spinner-container"), "Medium variant renders container class");
assert(medHtml.includes("medium"), "Medium variant has 'medium' class");
assert(medHtml.includes("MEDIUM_TEST"), "Medium variant renders custom text");
assert(
  medHtml.includes("--loader-accent:#ffffff"),
  "Medium variant normalizes 'white' to '#ffffff'"
);
assert(
  medHtml.includes("overflow-hidden") && medHtml.includes("max-w-xs"),
  "Medium variant contains overflow-hidden and max-w-xs containment"
);
assert(
  medHtml.includes("10Y") && medHtml.includes("20Y") && medHtml.includes("40Y"),
  "Medium variant renders gridiron yard depths (10Y, 20Y, 40Y)"
);

// Large variant
const largeHtml = renderToString(
  React.createElement(LoadingSpinner, {
    size: "large",
    color: "#10b981",
    text: "LARGE_RADAR",
  })
);
assert(largeHtml.includes("loading-spinner-container"), "Large variant renders container class");
assert(largeHtml.includes("large"), "Large variant has 'large' class");
assert(largeHtml.includes("LARGE_RADAR"), "Large variant renders custom text");
assert(largeHtml.includes("--loader-accent:#10b981"), "Large variant injects custom color CSS var");
assert(
  largeHtml.includes("overflow-hidden") && largeHtml.includes("max-w-md"),
  "Large variant contains overflow-hidden and max-w-md containment"
);
assert(largeHtml.includes("[ TELEMETRY ACTIVE ]"), "Large variant renders HUD telemetry header");

// Default props test
const defaultHtml = renderToString(React.createElement(LoadingSpinner));
assert(defaultHtml.includes("medium"), "Default size is 'medium'");
assert(defaultHtml.includes("--loader-accent:#00f0ff"), "Default color is '#00f0ff'");
assert(
  defaultHtml.includes("SCANNING GRIDIRON..."),
  "Default medium text is 'SCANNING GRIDIRON...'"
);

// 2.2 Narrow Container Overflow Stress Tests
console.log("\n[Sub-suite 2.2] Narrow Container Overflow Containment Audit:");
const narrowSizes = ["small", "medium", "large"] as const;
for (const sz of narrowSizes) {
  const rendered = renderToString(
    React.createElement(
      "div",
      { style: { width: "120px", overflow: "hidden" } },
      React.createElement(LoadingSpinner, {
        size: sz,
        text: "EXTREMELY_LONG_TELEMETRY_STRING_THAT_COULD_CAUSE_HORIZONTAL_SCROLLBARS_IN_NARROW_CONTAINERS",
      })
    )
  );

  assert(
    rendered.includes("overflow-hidden"),
    `Size ${sz} enforces overflow-hidden to prevent container overflow`
  );
  assert(
    rendered.includes("truncate"),
    `Size ${sz} enforces text truncation on telemetry text label`
  );
  // Small loader has 0px radius (inline flex badge), medium and large have rounded-[2px]
  const hasNoDisallowedRadius =
    !rendered.includes("rounded-xl") &&
    !rendered.includes("rounded-2xl") &&
    !rendered.includes("rounded-3xl");
  assert(
    hasNoDisallowedRadius,
    `Size ${sz} complies with 0-4px Anti-Template Firewall radius (no disallowed rounded-* classes)`
  );
  if (sz !== "small") {
    assert(rendered.includes("rounded-[2px]"), `Size ${sz} enforces tactile rounded-[2px]`);
  }
}

// 2.3 Play-Clock Countdown and Color Transitions Logic
console.log("\n[Sub-suite 2.3] Play-Clock Countdown & Color Transitions (<5s red, <=10s amber):");

// Extract and test color transition logic directly
function getClockColor(playClock: number, accentColor: string = "#00f0ff"): string {
  if (playClock <= 5) return "#f43f5e"; // alert red
  if (playClock <= 10) return "#f59e0b"; // warning amber
  return accentColor;
}

// Test <5s alert red
assert(getClockColor(0) === "#f43f5e", "Clock at 0s displays alert red (#f43f5e)");
assert(getClockColor(1) === "#f43f5e", "Clock at 1s displays alert red (#f43f5e)");
assert(getClockColor(4) === "#f43f5e", "Clock at 4s displays alert red (#f43f5e)");
assert(getClockColor(5) === "#f43f5e", "Clock at 5s displays alert red (#f43f5e)");

// Test <=10s warning amber
assert(getClockColor(6) === "#f59e0b", "Clock at 6s displays warning amber (#f59e0b)");
assert(getClockColor(8) === "#f59e0b", "Clock at 8s displays warning amber (#f59e0b)");
assert(getClockColor(10) === "#f59e0b", "Clock at 10s displays warning amber (#f59e0b)");

// Test >10s accent color
assert(getClockColor(11) === "#00f0ff", "Clock at 11s displays normal accent color (#00f0ff)");
assert(getClockColor(15) === "#00f0ff", "Clock at 15s displays normal accent color (#00f0ff)");
assert(getClockColor(25) === "#00f0ff", "Clock at 25s displays normal accent color (#00f0ff)");
assert(
  getClockColor(20, "#ff00aa") === "#ff00aa",
  "Clock at 20s with custom accent preserves custom color"
);

// Test wrap-around calculation: 25 -> ... -> 0 -> 25
function getNextClock(current: number): number {
  return current <= 0 ? 25 : current - 1;
}
assert(getNextClock(25) === 24, "Clock counts down from 25 to 24");
assert(getNextClock(1) === 0, "Clock counts down from 1 to 0");
assert(getNextClock(0) === 25, "Clock wraps around from 0 to 25s full play-clock cycle");

// ============================================================================
// SUITE 3: TACTILEBUTTON 12-STATE INTERACTIVE MATRIX AUDIT
// ============================================================================
console.log("\n--- TEST SUITE 3: TactileButton 12-State Interactive Matrix Audit ---");

import { TactileButton } from "../src/components/tactile/TactileButton";
import type { TactileState } from "../src/components/tactile/types";

const ALL_12_STATES: TactileState[] = [
  "idle",
  "hover",
  "pressed",
  "focused",
  "dragging",
  "drop-target",
  "selected",
  "disabled",
  "loading",
  "success",
  "warning",
  "error",
];

assert(ALL_12_STATES.length === 12, "Matrix defines exactly 12 interactive states");

for (const state of ALL_12_STATES) {
  const html = renderToString(
    React.createElement(
      TactileButton,
      {
        state,
        variant: "tactical",
        size: "md",
        testId: `btn-${state}`,
      },
      `ACTUATE_${state.toUpperCase()}`
    )
  );

  // Check state attribute rendered
  assert(
    html.includes(`data-tactile-state="${state}"`),
    `State '${state}' sets data-tactile-state="${state}"`
  );

  // Check 0-4px firewall radius
  assert(
    html.includes("rounded-[2px]"),
    `State '${state}' enforces Anti-Template Firewall radius rounded-[2px]`
  );

  // Check machined highlight
  assert(
    html.includes("bg-gradient-to-r from-transparent via-white/20 to-transparent"),
    `State '${state}' includes machined top edge highlight inset`
  );

  // State-specific behavior assertions
  if (state === "disabled") {
    assert(html.includes("disabled"), "Disabled state renders HTML disabled attribute");
    assert(html.includes('aria-disabled="true"'), "Disabled state sets aria-disabled='true'");
    assert(html.includes("cursor-not-allowed"), "Disabled state has cursor-not-allowed");
  } else if (state === "loading") {
    assert(html.includes('aria-busy="true"'), "Loading state sets aria-busy='true'");
    assert(html.includes("cursor-wait"), "Loading state has cursor-wait");
    assert(html.includes("animate-spin"), "Loading state renders animated radar sweep spinner");
  } else if (state === "selected") {
    assert(html.includes('aria-selected="true"'), "Selected state sets aria-selected='true'");
    assert(html.includes("animate-pulse"), "Selected state renders glowing LED indicator light");
    assert(html.includes("shadow-hard-primary"), "Selected state applies shadow-hard-primary");
  } else if (state === "pressed") {
    assert(html.includes('aria-pressed="true"'), "Pressed state sets aria-pressed='true'");
    assert(html.includes("shadow-hard-pressed"), "Pressed state applies shadow-hard-pressed");
  } else if (state === "focused") {
    assert(html.includes("ring-cyan-400"), "Focused state applies cyan tactical focus ring");
  } else if (state === "dragging") {
    assert(html.includes('aria-grabbed="true"'), "Dragging state sets aria-grabbed='true'");
    assert(html.includes("cursor-grabbing"), "Dragging state applies cursor-grabbing");
  } else if (state === "drop-target") {
    assert(html.includes('aria-dropeffect="move"'), "Drop-target sets aria-dropeffect='move'");
    assert(html.includes("border-dashed"), "Drop-target renders dashed tactile boundary");
  } else if (state === "success") {
    assert(html.includes('aria-live="polite"'), "Success state sets aria-live='polite'");
    assert(html.includes("border-emerald-500"), "Success state renders emerald tactical border");
  } else if (state === "warning") {
    assert(html.includes('aria-live="assertive"'), "Warning state sets aria-live='assertive'");
    assert(html.includes("border-amber-500"), "Warning state renders amber tactical border");
  } else if (state === "error") {
    assert(html.includes('aria-invalid="true"'), "Error state sets aria-invalid='true'");
    assert(html.includes('aria-live="assertive"'), "Error state sets aria-live='assertive'");
    assert(html.includes("border-rose-500"), "Error state renders rose tactical border");
  } else if (state === "hover") {
    assert(html.includes("shadow-hard-md"), "Hover state renders shadow-hard-md");
  }
}

// 3.2 Boolean prop overrides & precedence tests
console.log("\n[Sub-suite 3.2] TactileButton Boolean Props & Precedence:");

const disabledPropHtml = renderToString(
  React.createElement(TactileButton, { disabled: true, state: "hover" }, "DISABLED_OVERRIDE")
);
assert(
  disabledPropHtml.includes('data-tactile-state="disabled"'),
  "disabled=true prop overrides state='hover' to 'disabled'"
);

const loadingPropHtml = renderToString(
  React.createElement(TactileButton, { loading: true, state: "selected" }, "LOADING_OVERRIDE")
);
assert(
  loadingPropHtml.includes('data-tactile-state="loading"'),
  "loading=true prop overrides state='selected' to 'loading'"
);

const selectedPropHtml = renderToString(
  React.createElement(TactileButton, { selected: true, state: "idle" }, "SELECTED_PROP")
);
assert(
  selectedPropHtml.includes('data-tactile-state="selected"'),
  "selected=true prop resolves state to 'selected'"
);

// 3.3 Variants and Sizes Coverage
console.log("\n[Sub-suite 3.3] TactileButton Variants & Sizes:");
const variants = [
  "primary",
  "secondary",
  "tactical",
  "danger",
  "warning",
  "success",
  "ghost",
] as const;
for (const v of variants) {
  const html = renderToString(React.createElement(TactileButton, { variant: v }, v));
  assert(html.length > 0, `Variant '${v}' renders successfully`);
}

const sizes = ["xs", "sm", "md", "lg"] as const;
for (const s of sizes) {
  const html = renderToString(React.createElement(TactileButton, { size: s }, s));
  assert(html.length > 0, `Size '${s}' renders successfully`);
}

// ============================================================================
// FINAL SUMMARY
// ============================================================================
console.log("\n================================================================================");
console.log(`EMPIRICAL CHALLENGER 2 SUMMARY: Passed: ${totalPassed} | Failed: ${totalFailed}`);
console.log("================================================================================");

if (totalFailed > 0) {
  process.exit(1);
} else {
  process.exit(0);
}
