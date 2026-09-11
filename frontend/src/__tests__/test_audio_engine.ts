/**
 * Unit & Invariant Test Suite: Web Audio Engine & Spatial DSP
 * =============================================================
 * Validates mathematical acoustic modeling, stereo panning clamping,
 * kinetic momentum hit intensity profiles, EPA crowd reaction classification,
 * and headless API safety invariants.
 */

import {
  calculateSpatialPan,
  calculateHitIntensity,
  classifyCrowdReaction,
  soundEffects,
} from "../services/soundEffects.ts";

function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(`[ASSERTION_FAILED] ${message}`);
  }
}

function assertEquals<T>(actual: T, expected: T, message: string): void {
  if (actual !== expected) {
    throw new Error(`[EQUALS_FAILED] ${message} - Expected: ${String(expected)}, Received: ${String(actual)}`);
  }
}

function assertInRange(val: number, min: number, max: number, message: string): void {
  if (val < min || val > max) {
    throw new Error(`[RANGE_FAILED] ${message} - Value ${val} not in [${min}, ${max}]`);
  }
}

console.log("================================================================================");
console.log("🏃 RUNNING TASK-021: WEB AUDIO & SPATIAL DSP INVARIANT VERIFICATION SUITE");
console.log("================================================================================");

// --- TEST 1: Spatial Stereo Panning Coordinate Invariants ---
console.log("\n[TEST 1] Spatial Stereo Panning Coordinate Invariants");
{
  // Midfield (60 yd) must be center (0.0)
  const midPan = calculateSpatialPan(60);
  assertEquals(midPan, 0, "Midfield x=60 must yield pan=0.0");

  // Left Endzone (0 yd) must be -0.85
  const leftPan = calculateSpatialPan(0);
  assertEquals(leftPan, -0.85, "Left Endzone x=0 must yield pan=-0.85");

  // Right Endzone (120 yd) must be +0.85
  const rightPan = calculateSpatialPan(120);
  assertEquals(rightPan, 0.85, "Right Endzone x=120 must yield pan=+0.85");

  // Intermediate yardlines
  const own30Pan = calculateSpatialPan(30);
  assertEquals(own30Pan, -0.425, "x=30 must yield pan=-0.425");

  const opp30Pan = calculateSpatialPan(90);
  assertEquals(opp30Pan, 0.425, "x=90 must yield pan=+0.425");

  // Out-of-bounds coordinate clamping
  const negativeClamp = calculateSpatialPan(-50);
  assertEquals(negativeClamp, -0.85, "Negative coordinate must clamp to -0.85");

  const overflowClamp = calculateSpatialPan(200);
  assertEquals(overflowClamp, 0.85, "Coordinate > 120 must clamp to +0.85");

  console.log("  ✅ 1.1 Center, left endzone, and right endzone panning verified.");
  console.log("  ✅ 1.2 Boundary coordinate clamping strictly bounded in [-0.85, 0.85].");
}

// --- TEST 2: Kinetic Collision Momentum & Frequency Scaling Invariants ---
console.log("\n[TEST 2] Kinetic Collision Momentum & Frequency Scaling Invariants");
{
  const lightHit = calculateHitIntensity(300, 0.5);
  const midHit = calculateHitIntensity(850, 0.5);
  const heavyHit = calculateHitIntensity(2400, 0.5);

  // Gain scaling
  assert(lightHit.gain < midHit.gain, "Gain must increase with momentum");
  assert(midHit.gain < heavyHit.gain, "Gain must increase with momentum");

  // Sub-bass frequency must decrease with higher momentum (deeper acoustic resonance)
  assert(
    lightHit.subFreq > heavyHit.subFreq,
    `Sub-bass freq must decrease with momentum (Light: ${lightHit.subFreq}Hz vs Heavy: ${heavyHit.subFreq}Hz)`
  );
  assertInRange(heavyHit.subFreq, 95, 115, "Heavy hit sub-bass must reach deep register (95-115Hz)");

  // Snap transient frequency must increase with higher momentum (sharper pad clack)
  assert(
    lightHit.snapFreq < heavyHit.snapFreq,
    `Snap transient freq must increase with momentum (Light: ${lightHit.snapFreq}Hz vs Heavy: ${heavyHit.snapFreq}Hz)`
  );

  // Volume modulation: volume=0 yields gain=0
  const mutedHit = calculateHitIntensity(1500, 0.0);
  assertEquals(mutedHit.gain, 0, "Zero base volume must yield zero gain");

  // Extreme momentum clamping [200, 3000]
  const underflow = calculateHitIntensity(50, 0.5);
  const minHit = calculateHitIntensity(200, 0.5);
  assertEquals(underflow.gain, minHit.gain, "Momentum < 200 must clamp to 200");

  const overflow = calculateHitIntensity(5000, 0.5);
  const maxHit = calculateHitIntensity(3000, 0.5);
  assertEquals(overflow.gain, maxHit.gain, "Momentum > 3000 must clamp to 3000");

  console.log("  ✅ 2.1 Sub-bass frequency strictly monotonic decreasing with momentum.");
  console.log("  ✅ 2.2 Snap transient frequency strictly monotonic increasing with momentum.");
  console.log("  ✅ 2.3 Volume scaling and extreme momentum boundary clamping verified.");
}

// --- TEST 3: EPA-Driven Resonant Crowd Reaction Classifier ---
console.log("\n[TEST 3] EPA-Driven Resonant Crowd Reaction Classifier");
{
  // Positive explosive plays
  assertEquals(classifyCrowdReaction(1.5), "ROAR", "+1.5 EPA must trigger ROAR");
  assertEquals(classifyCrowdReaction(4.2), "ROAR", "Touchdown (+4.2 EPA) must trigger ROAR");

  // Negative turnover / sack plays
  assertEquals(classifyCrowdReaction(-1.5), "GROAN", "-1.5 EPA must trigger GROAN");
  assertEquals(classifyCrowdReaction(-3.8), "GROAN", "Interception (-3.8 EPA) must trigger GROAN");

  // Neutral / standard gain plays
  assertEquals(classifyCrowdReaction(0.0), "MURMUR", "0.0 EPA must trigger MURMUR");
  assertEquals(classifyCrowdReaction(0.8), "MURMUR", "Standard 4-yd run (+0.8 EPA) must trigger MURMUR");
  assertEquals(classifyCrowdReaction(-0.6), "MURMUR", "Incomplete pass (-0.6 EPA) must trigger MURMUR");

  console.log("  ✅ 3.1 Positive explosive EPA swings (>= 1.5) map strictly to ROAR.");
  console.log("  ✅ 3.2 Negative turnover EPA swings (<= -1.5) map strictly to GROAN.");
  console.log("  ✅ 3.3 Neutral game flow maps strictly to MURMUR.");
}

// --- TEST 4: Engine Configuration & State Mutation Invariants ---
console.log("\n[TEST 4] Engine Configuration & State Mutation Invariants");
{
  // Volume clamping
  soundEffects.setVolume(0.75);
  assertEquals(soundEffects.getVolume(), 0.75, "Volume getter must match set value");

  soundEffects.setVolume(-0.5);
  assertEquals(soundEffects.getVolume(), 0.0, "Negative volume must clamp to 0.0");

  soundEffects.setVolume(1.8);
  assertEquals(soundEffects.getVolume(), 1.0, "Volume > 1 must clamp to 1.0");

  // Mute toggle
  soundEffects.setMuted(true);
  assertEquals(soundEffects.getMuted(), true, "Mute getter must reflect true");

  soundEffects.setMuted(false);
  assertEquals(soundEffects.getMuted(), false, "Mute getter must reflect false");

  // Feature toggles
  soundEffects.setSpatialAudioEnabled(false);
  assertEquals(soundEffects.getSpatialAudioEnabled(), false, "Spatial audio toggle verified");

  soundEffects.setCrowdEnabled(false);
  assertEquals(soundEffects.getCrowdEnabled(), false, "Crowd audio toggle verified");

  soundEffects.setSfxEnabled(false);
  assertEquals(soundEffects.getSfxEnabled(), false, "SFX audio toggle verified");

  // Restore defaults
  soundEffects.setSpatialAudioEnabled(true);
  soundEffects.setCrowdEnabled(true);
  soundEffects.setSfxEnabled(true);
  soundEffects.setVolume(0.5);

  const cfg = soundEffects.getConfig();
  assertEquals(cfg.volume, 0.5, "Config snapshot volume verified");
  assertEquals(cfg.spatialAudioEnabled, true, "Config snapshot spatial audio verified");
  assertEquals(cfg.crowdEnabled, true, "Config snapshot crowd verified");
  assertEquals(cfg.sfxEnabled, true, "Config snapshot SFX verified");

  console.log("  ✅ 4.1 Volume clamping [0.0, 1.0] and mute state verified.");
  console.log("  ✅ 4.2 Spatial, crowd, and SFX feature toggles verified.");
  console.log("  ✅ 4.3 Snapshot configuration getter matches internal state.");
}

// --- TEST 5: Headless / Node Safety & Method Invocation Invariants ---
console.log("\n[TEST 5] Headless / Node Safety & Method Invocation Invariants");
{
  // Calling synthesizers in Node (where AudioContext is not present) must be 100% no-op safe
  let threwError = false;
  try {
    soundEffects.playSpatialHit(45, 26.65, 1200);
    soundEffects.playSpatialWhistle(70);
    soundEffects.playCadence("hut");
    soundEffects.playCadence("audible");
    soundEffects.playCadence("set");
    soundEffects.updateCrowdIntensity(3.5, 0.85);
    soundEffects.updateCrowdIntensity(-2.0, 0.15);
    soundEffects.playStadiumHorn();
    soundEffects.playSnap();
  } catch (err) {
    threwError = true;
    console.error(err);
  }

  assertEquals(threwError, false, "All audio methods must run safely in headless / SSR environments without throwing");
  console.log("  ✅ 5.1 Zero unhandled exceptions during headless method execution.");
  console.log("  ✅ 5.2 Formant cadence calls ('hut', 'audible', 'set') execute safely.");
}

// --- TEST 6: Micro-Benchmark Performance Stress Test ---
console.log("\n[TEST 6] Micro-Benchmark Performance Stress Test");
{
  const iterations = 5000;
  const start = performance.now();

  for (let i = 0; i < iterations; i++) {
    const x = (i % 120);
    calculateSpatialPan(x);
    calculateHitIntensity(400 + (i % 2000), 0.5);
    classifyCrowdReaction((i % 10) - 5);
  }

  const durationMs = performance.now() - start;
  const usPerOp = (durationMs / iterations) * 1000;

  console.log(`  ⏱️  5,000 full DSP mathematical evaluations: ${durationMs.toFixed(3)} ms`);
  console.log(`  ⚡ Latency per mathematical derivation: ${usPerOp.toFixed(3)} μs`);

  assert(durationMs < 10.0, `5,000 DSP derivations must execute in < 10ms (Actual: ${durationMs.toFixed(3)}ms)`);
  console.log("  ✅ 6.1 Performance budget satisfied (<0.002ms per derivation).");
}

console.log("\n================================================================================");
console.log("🏆 ALL 6/6 AUDIO & SPATIAL DSP INVARIANT TESTS PASSED VERBATIM");
console.log("================================================================================");
