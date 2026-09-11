/**
 * Automated Verification Suite for Generic Entity Slices & Normalization Architecture
 * Standards: Deterministic invariants, O(1) mutations, re-render containment.
 */

import assert from "node:assert/strict";
import {
  createInitialEntityState,
  createEntitySliceActions,
} from "../store/slices/createEntitySlice.ts";
import { computeFilteredPlayers } from "../utils/filterFreeAgents.ts";
import type { FreeAgentMarketPlayer } from "../types/offseason.ts";
import type { EntityState } from "../types/entityState.ts";

console.log("================================================================================");
console.log("FRONTEND NORMALIZED ENTITY SLICE & PERFORMANCE VERIFICATION SUITE");
console.log("================================================================================\n");

// Helper to create mock store state container
function createTestStore() {
  let state: EntityState<FreeAgentMarketPlayer, number> =
    createInitialEntityState<FreeAgentMarketPlayer, number>();

  const actions = createEntitySliceActions<FreeAgentMarketPlayer, number>((updater) => {
    state = {
      ...state,
      ...updater(state),
    };
  });

  return {
    getState: () => state,
    actions,
  };
}

// 1. Initial State Invariant
console.log("Test 1: Initial Entity State Invariants...");
{
  const store = createTestStore();
  const s = store.getState();
  assert.deepEqual(s.byId, {});
  assert.deepEqual(s.allIds, []);
  assert.equal(s.selectedId, null);
  assert.equal(s.isLoading, false);
  assert.equal(s.error, null);
  console.log("  [PASS] Initial state has empty byId, allIds, null selectedId.");
}

// 2. SetAll & Deduplication Invariant
console.log("\nTest 2: SetAll with Ingestion & Deduplication...");
{
  const store = createTestStore();
  const mockPlayers: FreeAgentMarketPlayer[] = [
    {
      player_id: 101,
      player_name: "Jordan Love",
      position: "QB",
      overall_rating: 89,
      age: 26,
      projected_aav: 45000000,
      projected_years: 4,
      tier: "Tier 1",
      top_interested_teams: ["GB", "LV"],
    },
    {
      player_id: 102,
      player_name: "Saquon Barkley",
      position: "RB",
      overall_rating: 92,
      age: 27,
      projected_aav: 13000000,
      projected_years: 3,
      tier: "Tier 1",
      top_interested_teams: ["PHI", "HOU"],
    },
    {
      player_id: 101, // Duplicate ID with updated rating
      player_name: "Jordan Love (Updated)",
      position: "QB",
      overall_rating: 90,
      age: 26,
      projected_aav: 46000000,
      projected_years: 4,
      tier: "Tier 1",
      top_interested_teams: ["GB", "LV"],
    },
  ];

  store.actions.setAll(mockPlayers, (p) => p.player_id);
  const s = store.getState();

  assert.equal(s.allIds.length, 2, "Duplicate player_id 101 should be deduplicated in allIds");
  assert.deepEqual(s.allIds, [101, 102]);
  assert.equal(s.byId[101].player_name, "Jordan Love (Updated)");
  assert.equal(s.byId[102].player_name, "Saquon Barkley");
  console.log("  [PASS] SetAll successfully deduped entities and populated byId dictionary.");
}

// 3. UpsertOne Invariant
console.log("\nTest 3: UpsertOne (Insert New + Update Existing)...");
{
  const store = createTestStore();
  const playerA: FreeAgentMarketPlayer = {
    player_id: 201,
    player_name: "Justin Jefferson",
    position: "WR",
    overall_rating: 99,
    age: 25,
    projected_aav: 35000000,
    projected_years: 4,
    tier: "Tier 1",
    top_interested_teams: ["MIN"],
  };

  store.actions.upsertOne(playerA, (p) => p.player_id);
  assert.equal(store.getState().allIds.length, 1);
  assert.equal(store.getState().byId[201].overall_rating, 99);

  // Update existing
  const playerAUpdated = { ...playerA, overall_rating: 100 };
  store.actions.upsertOne(playerAUpdated, (p) => p.player_id);
  assert.equal(store.getState().allIds.length, 1, "allIds should not grow on update");
  assert.equal(store.getState().byId[201].overall_rating, 100);
  console.log("  [PASS] UpsertOne handles both clean insertion and in-place update.");
}

// 4. UpdateOne & Referential Stability (Re-render Containment)
console.log("\nTest 4: UpdateOne & Referential Stability of Siblings...");
{
  const store = createTestStore();
  const p1: FreeAgentMarketPlayer = {
    player_id: 301,
    player_name: "Patrick Mahomes",
    position: "QB",
    overall_rating: 99,
    age: 29,
    projected_aav: 50000000,
    projected_years: 5,
    tier: "Tier 1",
    top_interested_teams: ["KC"],
  };
  const p2: FreeAgentMarketPlayer = {
    player_id: 302,
    player_name: "Travis Kelce",
    position: "TE",
    overall_rating: 93,
    age: 35,
    projected_aav: 15000000,
    projected_years: 2,
    tier: "Tier 2",
    top_interested_teams: ["KC"],
  };

  store.actions.setAll([p1, p2], (p) => p.player_id);
  const stateBefore = store.getState();
  const kelceRefBefore = stateBefore.byId[302];

  // Mutate Mahomes only
  store.actions.updateOne(301, { overall_rating: 100 });
  const stateAfter = store.getState();
  const mahomesAfter = stateAfter.byId[301];
  const kelceRefAfter = stateAfter.byId[302];

  assert.equal(mahomesAfter.overall_rating, 100);
  assert.equal(
    kelceRefBefore,
    kelceRefAfter,
    "CRITICAL: Sibling entity reference MUST remain strictly identical (prev === next) to prevent re-render cascades!"
  );
  console.log("  [PASS] Referential stability verified: Sibling player reference remained 100% identical.");
}

// 5. RemoveOne & Selection Cleanup
console.log("\nTest 5: RemoveOne & Selection Cleanup Invariants...");
{
  const store = createTestStore();
  const p1: FreeAgentMarketPlayer = {
    player_id: 401,
    player_name: "Derrick Henry",
    position: "RB",
    overall_rating: 91,
    age: 30,
    projected_aav: 9000000,
    projected_years: 2,
    tier: "Tier 2",
    top_interested_teams: ["BAL"],
  };

  store.actions.setAll([p1], (p) => p.player_id);
  store.actions.setSelectedId(401);
  assert.equal(store.getState().selectedId, 401);

  // Remove player
  store.actions.removeOne(401);
  const s = store.getState();
  assert.equal(s.allIds.length, 0);
  assert.equal(s.byId[401], undefined);
  assert.equal(s.selectedId, null, "selectedId must reset to null when selected player is removed");
  console.log("  [PASS] RemoveOne purged entity and reset active selection without dangling pointer.");
}

// 6. Deterministic Filter Engine
console.log("\nTest 6: High-Performance Filter Engine (computeFilteredPlayers)...");
{
  const players: FreeAgentMarketPlayer[] = [
    { player_id: 1, player_name: "Lamar Jackson", position: "QB", overall_rating: 97, age: 27, projected_aav: 52000000, projected_years: 5, tier: "Tier 1", top_interested_teams: ["BAL"] },
    { player_id: 2, player_name: "Christian McCaffrey", position: "RB", overall_rating: 98, age: 28, projected_aav: 16000000, projected_years: 3, tier: "Tier 1", top_interested_teams: ["SF"] },
    { player_id: 3, player_name: "Fred Warner", position: "MLB", overall_rating: 96, age: 28, projected_aav: 20000000, projected_years: 4, tier: "Tier 1", top_interested_teams: ["SF"] },
    { player_id: 4, player_name: "Justin Tucker", position: "K", overall_rating: 91, age: 35, projected_aav: 6000000, projected_years: 2, tier: "Tier 2", top_interested_teams: ["BAL"] },
    { player_id: 5, player_name: "Sam Darnold", position: "QB", overall_rating: 81, age: 27, projected_aav: 10000000, projected_years: 1, tier: "Tier 3", top_interested_teams: ["MIN"] },
  ];

  const byId = Object.fromEntries(players.map((p) => [p.player_id, p]));
  const allIds = players.map((p) => p.player_id);

  // Filter by Unit: OFF
  const offFilter = computeFilteredPlayers(byId, allIds, "OFF", "ALL", "");
  assert.deepEqual(offFilter.filteredIds, [1, 2, 5], "OFF unit should match QB, RB, and QB");

  // Filter by Unit: DEF
  const defFilter = computeFilteredPlayers(byId, allIds, "DEF", "ALL", "");
  assert.deepEqual(defFilter.filteredIds, [3], "DEF unit should match MLB");

  // Filter by Unit: ST
  const stFilter = computeFilteredPlayers(byId, allIds, "ST", "ALL", "");
  assert.deepEqual(stFilter.filteredIds, [4], "ST unit should match K");

  // Filter by Position: QB + Tier: Tier 1
  const qbTier1 = computeFilteredPlayers(byId, allIds, "QB", "Tier 1", "");
  assert.deepEqual(qbTier1.filteredIds, [1], "QB Tier 1 should match Lamar Jackson only");

  // Search Query
  const searchQuery = computeFilteredPlayers(byId, allIds, "ALL", "ALL", "mccaffrey");
  assert.deepEqual(searchQuery.filteredIds, [2]);

  console.log("  [PASS] Unit, position, tier, and search query filters execute deterministically.");
}

// 7. Large-Scale Stress Benchmark (2,500 Entities)
console.log("\nTest 7: Large-Scale Benchmark (2,500 Entities)...");
{
  const store = createTestStore();
  const largeRoster: FreeAgentMarketPlayer[] = [];
  const positions = ["QB", "RB", "WR", "TE", "OT", "OG", "C", "DE", "DT", "LB", "CB", "S", "K", "P"];

  for (let i = 1; i <= 2500; i++) {
    const pos = positions[i % positions.length];
    largeRoster.push({
      player_id: i,
      player_name: `Athlete Record ${i}`,
      position: pos,
      overall_rating: 60 + (i % 40),
      age: 21 + (i % 15),
      projected_aav: 1000000 * (1 + (i % 25)),
      projected_years: 1 + (i % 5),
      tier: `Tier ${(i % 4) + 1}`,
      top_interested_teams: ["NE", "MIA", "BUF", "NYJ"],
    });
  }

  const startIngest = performance.now();
  store.actions.setAll(largeRoster, (p) => p.player_id);
  const ingestTimeMs = performance.now() - startIngest;

  const startFilter = performance.now();
  const filterResult = computeFilteredPlayers(
    store.getState().byId,
    store.getState().allIds,
    "OFF",
    "Tier 1",
    "record 1"
  );
  const filterTimeMs = performance.now() - startFilter;

  const startUpdates = performance.now();
  for (let i = 1; i <= 100; i++) {
    store.actions.updateOne(i, { overall_rating: 99 });
  }
  const updateTimeMs = performance.now() - startUpdates;

  console.log(`  -> Ingestion Latency (2,500 entities): ${ingestTimeMs.toFixed(3)} ms`);
  console.log(`  -> Filter Execution Latency (2,500 entities): ${filterTimeMs.toFixed(3)} ms (matched ${filterResult.filteredIds.length})`);
  console.log(`  -> 100 Atomic Dictionary Updates: ${updateTimeMs.toFixed(3)} ms (${(updateTimeMs / 100).toFixed(4)} ms/op)`);

  assert.ok(ingestTimeMs < 50.0, "Ingest of 2,500 entities must complete under 50ms");
  assert.ok(filterTimeMs < 10.0, "Filter over 2,500 entities must complete under 10ms");
  assert.ok(updateTimeMs < 15.0, "100 updates must complete under 15ms");

  console.log("  [PASS] All performance latency ceilings successfully met!");
}

console.log("\n================================================================================");
console.log("ALL 7 ENTITY SLICE & NORMALIZATION TESTS PASSED WITH 100% SUCCESS!");
console.log("================================================================================\n");
