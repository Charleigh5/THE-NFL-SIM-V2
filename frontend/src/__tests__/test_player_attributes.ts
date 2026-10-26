/**
 * Automated Verification Suite for Player Tactical Scheme Fit & Progressive Disclosure
 * Standards: Deterministic Invariants, Position Taxonomy Verification, DOM Test ID Contracts.
 */

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {
  calculateSchemeFit,
  getPrimaryTraits,
  getSecondaryTraits,
  ALL_NUMERIC_TRAITS,
} from "../utils/schemeFit.ts";
import type { Player } from "../services/api.ts";

console.log("================================================================================");
console.log("PLAYER TACTICAL SCHEME FIT & PROGRESSIVE DISCLOSURE VERIFICATION SUITE");
console.log("================================================================================\n");

// -----------------------------------------------------------------------------
// Test 1: Scheme Fit Computation Across Offensive and Defensive Positions
// -----------------------------------------------------------------------------
console.log("Test 1: Scheme Fit Computation Across Positions...");
{
  // 1.1 Defensive Secondary: CB Zone Coverage vs Man Coverage
  const cbZone: Partial<Player> = {
    position: "CB",
    zone_coverage: 95,
    man_coverage: 78,
    play_recognition: 92,
    speed: 94,
  };
  const resCbZone = calculateSchemeFit(cbZone);
  assert.equal(resCbZone.schemeName, "Cover 3 Zone");
  assert.ok(resCbZone.score >= 90, `CB Zone score ${resCbZone.score} should be >= 90`);
  assert.equal(resCbZone.badgeClass, "elite-fit");
  assert.equal(resCbZone.tagLabel, `${resCbZone.score}% • Cover 3 Zone`);

  const cbMan: Partial<Player> = {
    position: "CB",
    zone_coverage: 70,
    man_coverage: 92,
    play_recognition: 85,
    speed: 93,
  };
  const resCbMan = calculateSchemeFit(cbMan);
  assert.equal(resCbMan.schemeName, "Man Press Heavy");
  assert.ok(resCbMan.score >= 80, `CB Man score ${resCbMan.score} should be >= 80`);
  assert.ok(["elite-fit", "compatible-fit"].includes(resCbMan.badgeClass));

  // 1.2 Defensive Front: DL/DE/EDGE Pass Rush Styles
  const deSpeed: Partial<Player> = {
    position: "DE",
    pass_rush_finesse: 92,
    pass_rush_power: 76,
    speed: 88,
    block_shed: 82,
  };
  const resDeSpeed = calculateSchemeFit(deSpeed);
  assert.equal(resDeSpeed.schemeName, "Speed Rush 3-4");

  const dtPower: Partial<Player> = {
    position: "DT",
    pass_rush_finesse: 70,
    pass_rush_power: 94,
    strength: 95,
    block_shed: 90,
  };
  const resDtPower = calculateSchemeFit(dtPower);
  assert.equal(resDtPower.schemeName, "Power Gap 4-3");

  // 1.3 Linebackers: Tampa 2 Coverage vs Attacking Blitz
  const lbTampa: Partial<Player> = {
    position: "MLB",
    zone_coverage: 82,
    play_recognition: 88,
    tackle: 85,
  };
  const resLbTampa = calculateSchemeFit(lbTampa);
  assert.equal(resLbTampa.schemeName, "Tampa 2 Coverage");

  const lbBlitz: Partial<Player> = {
    position: "OLB",
    zone_coverage: 65,
    tackle: 90,
    pass_rush_power: 88,
    block_shed: 84,
  };
  const resLbBlitz = calculateSchemeFit(lbBlitz);
  assert.equal(resLbBlitz.schemeName, "Attacking Blitz LB");

  // 1.4 Offensive QB: Vertical Air Raid vs West Coast Rhythm
  const qbDeep: Partial<Player> = {
    position: "QB",
    throw_power: 96,
    throw_accuracy_short: 88,
    awareness: 85,
  };
  const resQbDeep = calculateSchemeFit(qbDeep);
  assert.equal(resQbDeep.schemeName, "Vertical Air Raid");

  const qbWestCoast: Partial<Player> = {
    position: "QB",
    throw_power: 84,
    throw_accuracy_short: 94,
    awareness: 90,
  };
  const resQbWestCoast = calculateSchemeFit(qbWestCoast);
  assert.equal(resQbWestCoast.schemeName, "West Coast Rhythm");

  // 1.5 Offensive RB: Outside Zone vs Power Gap Duo
  const rbOutside: Partial<Player> = {
    position: "RB",
    agility: 92,
    speed: 94,
    acceleration: 93,
  };
  const resRbOutside = calculateSchemeFit(rbOutside);
  assert.equal(resRbOutside.schemeName, "Outside Zone");

  const rbPower: Partial<Player> = {
    position: "RB",
    agility: 80,
    strength: 88,
    speed: 86,
    awareness: 80,
  };
  const resRbPower = calculateSchemeFit(rbPower);
  assert.equal(resRbPower.schemeName, "Power Gap Duo");

  // 1.6 Offensive WR/TE: Vertical Deep Threat vs Possession Weapon
  const wrDeep: Partial<Player> = {
    position: "WR",
    speed: 95,
    route_running: 90,
    catching: 88,
  };
  const resWrDeep = calculateSchemeFit(wrDeep);
  assert.equal(resWrDeep.schemeName, "Vertical Deep Threat");

  const tePossession: Partial<Player> = {
    position: "TE",
    speed: 82,
    catching: 90,
    route_running: 86,
    awareness: 85,
  };
  const resTePossession = calculateSchemeFit(tePossession);
  assert.equal(resTePossession.schemeName, "Possession / Slot Weapon");

  // 1.7 Offensive Line: Pass Heavy Spread vs Power Run Heavy
  const otPass: Partial<Player> = {
    position: "OT",
    pass_block: 94,
    run_block: 82,
    strength: 90,
    awareness: 88,
  };
  const resOtPass = calculateSchemeFit(otPass);
  assert.equal(resOtPass.schemeName, "Pass Heavy Spread");

  const ogRun: Partial<Player> = {
    position: "OG",
    pass_block: 80,
    run_block: 95,
    strength: 94,
    awareness: 86,
  };
  const resOgRun = calculateSchemeFit(ogRun);
  assert.equal(resOgRun.schemeName, "Power Run Heavy");

  // 1.8 Special Teams & Default Fallback
  const kSpecial: Partial<Player> = {
    position: "K",
    kick_power: 96,
    kick_accuracy: 92,
  };
  const resK = calculateSchemeFit(kSpecial);
  assert.equal(resK.schemeName, "Special Teams Core");

  const fallback = calculateSchemeFit(null);
  assert.equal(fallback.schemeName, "Balanced Pro Style");
  assert.equal(fallback.badgeClass, "neutral-fit");

  console.log("  [PASS] Scheme fit mapping matches position taxonomy and attribute thresholds.");
}

// -----------------------------------------------------------------------------
// Test 2: Scheme Fit Badge Tiering & Clamping Invariants
// -----------------------------------------------------------------------------
console.log("\nTest 2: Badge Tiering & Score Clamping...");
{
  // Score >= 90 -> elite-fit
  const elite = calculateSchemeFit({
    position: "QB",
    throw_power: 98,
    throw_accuracy_short: 96,
    awareness: 94,
  });
  assert.ok(elite.score >= 90, "Score should be >= 90");
  assert.equal(elite.badgeClass, "elite-fit");

  // Score 80-89 -> compatible-fit
  const compatible = calculateSchemeFit({
    position: "QB",
    throw_power: 84,
    throw_accuracy_short: 85,
    awareness: 82,
  });
  assert.ok(compatible.score >= 80 && compatible.score < 90, "Score should be in 80-89 range");
  assert.equal(compatible.badgeClass, "compatible-fit");

  // Score < 80 -> neutral-fit
  const neutral = calculateSchemeFit({
    position: "QB",
    throw_power: 60,
    throw_accuracy_short: 65,
    awareness: 60,
  });
  assert.ok(neutral.score < 80, "Score should be < 80");
  assert.equal(neutral.badgeClass, "neutral-fit");

  // Clamping: max 99, min 50
  const maxClamped = calculateSchemeFit({
    position: "QB",
    throw_power: 120,
    throw_accuracy_short: 120,
    awareness: 120,
  });
  assert.equal(maxClamped.score, 99, "Score must clamp to maximum 99");

  const minClamped = calculateSchemeFit({
    position: "QB",
    throw_power: 20,
    throw_accuracy_short: 20,
    awareness: 20,
  });
  assert.equal(minClamped.score, 50, "Score must clamp to minimum 50");

  console.log("  [PASS] Badge class assignments and score clamping conform strictly to spec.");
}

// -----------------------------------------------------------------------------
// Test 3: Primary Positional Attributes Taxonomy & Determinism
// -----------------------------------------------------------------------------
console.log("\nTest 3: Primary vs Secondary Trait Taxonomy & Determinism...");
{
  const testPositions = [
    "QB",
    "RB",
    "FB",
    "WR",
    "TE",
    "OL",
    "OT",
    "OG",
    "C",
    "DL",
    "DE",
    "DT",
    "EDGE",
    "LB",
    "MLB",
    "OLB",
    "CB",
    "S",
    "FS",
    "SS",
    "DB",
    "K",
    "P",
    "LS",
  ];

  for (const pos of testPositions) {
    const primary = getPrimaryTraits(pos);
    assert.equal(primary.length, 4, `Position ${pos} must have exactly 4 primary traits`);

    const secondary = getSecondaryTraits(pos);
    assert.equal(
      secondary.length,
      ALL_NUMERIC_TRAITS.length - 4,
      `Position ${pos} must have exactly ${ALL_NUMERIC_TRAITS.length - 4} secondary traits`
    );

    // Assert disjoint sets (no overlap)
    const primaryKeys = new Set(primary.map((t) => t.key));
    for (const sec of secondary) {
      assert.ok(
        !primaryKeys.has(sec.key),
        `Primary trait ${String(sec.key)} should not appear in secondary traits for ${pos}`
      );
    }
  }

  // Determinism check
  const firstQB = getPrimaryTraits("QB");
  const secondQB = getPrimaryTraits("QB");
  assert.deepEqual(firstQB, secondQB, "Repeated getPrimaryTraits calls must be deterministic");

  console.log(
    "  [PASS] Exactly 4 primary traits per position, 16 disjoint secondary traits, 100% deterministic."
  );
}

// -----------------------------------------------------------------------------
// Test 4: Source Contract & Test ID Invariants in PlayerModal
// -----------------------------------------------------------------------------
console.log("\nTest 4: Source File Test IDs & Accessibility Contracts...");
{
  const modalPath = path.resolve(process.cwd(), "frontend/src/components/ui/PlayerModal.tsx");
  const cssPath = path.resolve(process.cwd(), "frontend/src/components/ui/PlayerModal.css");

  assert.ok(fs.existsSync(modalPath), "PlayerModal.tsx must exist");
  assert.ok(fs.existsSync(cssPath), "PlayerModal.css must exist");

  const modalSource = fs.readFileSync(modalPath, "utf-8");
  const cssSource = fs.readFileSync(cssPath, "utf-8");

  // Required Test IDs
  const requiredTestIds = [
    'data-testid="scheme-fit-badge"',
    'data-testid="primary-attributes-grid"',
    "data-testid={`primary-trait-${trait.key}`}",
    'data-testid="full-traits-disclosure"',
    'data-testid="player-speed"',
    'data-testid="player-strength"',
  ];

  for (const testId of requiredTestIds) {
    assert.ok(
      modalSource.includes(testId),
      `PlayerModal.tsx must contain required contract selector: ${testId}`
    );
  }

  // Progressive Disclosure markup contracts
  assert.ok(
    modalSource.includes("<details"),
    "PlayerModal.tsx must render accessible <details> element"
  );
  assert.ok(
    modalSource.includes("<summary"),
    "PlayerModal.tsx must render accessible <summary> element"
  );
  assert.ok(
    modalSource.includes("scheme-fit-badge"),
    "PlayerModal.tsx must bind scheme-fit-badge class"
  );
  assert.ok(
    modalSource.includes("calculateSchemeFit"),
    "PlayerModal.tsx must import and call calculateSchemeFit"
  );

  // CSS Class Contracts
  const requiredCssClasses = [
    ".scheme-fit-badge",
    ".scheme-fit-badge.elite-fit",
    ".scheme-fit-badge.compatible-fit",
    ".scheme-fit-badge.neutral-fit",
    ".primary-attributes-grid",
    ".primary-attribute-card",
    ".full-traits-disclosure",
    ".traits-summary",
    ".secondary-traits-grid",
  ];

  for (const cssClass of requiredCssClasses) {
    assert.ok(
      cssSource.includes(cssClass),
      `PlayerModal.css must define required styling class: ${cssClass}`
    );
  }

  console.log(
    "  [PASS] All DOM test IDs, accessibility elements, and CSS classes present in source."
  );
}

console.log("\n================================================================================");
console.log("ALL PLAYER SCHEME FIT & PROGRESSIVE DISCLOSURE INVARIANTS PASSED (100% GREEN)");
console.log("================================================================================\n");
