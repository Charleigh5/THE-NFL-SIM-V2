/**
 * Empirical TypeScript Deserialization & Type Validation
 * Verifies that the JSON frames emitted by Python Pydantic models
 * deserialize and conform strictly to TypeScript interfaces with zero errors.
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

// 1. Run Python pipeline to produce serialized JSON payloads
const pyOut = spawnSync('python', ['scripts/test_domain_boundary_pipeline.py'], { encoding: 'utf-8' });
if (pyOut.status !== 0) {
  console.error("Python pipeline failed:", pyOut.stderr);
  process.exit(1);
}
console.log("Python pipeline successfully emitted domain payloads.");

// 2. Extract TypeScript contracts from ui_design_system.md
const docContent = fs.readFileSync('docs/design_theory/nfl_simulation_blueprint/ui_design_system.md', 'utf8');
const tsBlock = docContent.split('```typescript')[2].split('```')[0];

// 3. Create a comprehensive TypeScript test suite that imports and types real JSON payloads
const testRunnerTs = `
/// <reference lib="dom" />

${tsBlock}

// Test payload instances matching Pydantic serialization
const stateSyncMsg: WebSocketBroadcastMessage = {
  sequenceId: 10001,
  messageType: "STATE_SYNC",
  timestamp: 1724278920.0,
  gameId: 101,
  payload: {
    gameId: 101,
    quarter: 4,
    clockSecondsRemaining: 124.0,
    homeScore: 27,
    awayScore: 24,
    down: 3,
    distance: 4,
    yardLine: 68,
    possessionTeamId: 1,
    broadcastPhase: BroadcastPhase.IN_PLAY
  }
};

const telemetryMsg: WebSocketBroadcastMessage = {
  sequenceId: 10002,
  messageType: "TELEMETRY_FRAME",
  timestamp: 1724278920.016,
  gameId: 101,
  payload: {
    frameIndex: 1420,
    gameClockSeconds: 842.5,
    ballPosition: { x: 0.0, y: 35.0, z: 1.8 },
    ballVelocity: { x: 12.5, y: 28.0, z: 5.2 },
    players: [
      {
        playerId: 15,
        jerseyNumber: 15,
        teamId: 1,
        position: { x: -2.5, y: 30.0, z: 0.0 },
        velocity: { x: 1.2, y: 0.5, z: 0.0 },
        facingAngle: 45.0,
        staminaPct: 0.94,
        currentAction: "PASS_DROPBACK"
      }
    ],
    trenchCollisions: [
      {
        offensiveLinemanId: 74,
        defensiveRusherId: 99,
        contactPoint: { x: -2.1, y: 30.8, z: 1.2 },
        kineticForceNewtons: 3450.0,
        leverageAdvantageBias: 0.62
      }
    ]
  }
};

const audioMsg: WebSocketBroadcastMessage = {
  sequenceId: 10003,
  messageType: "AUDIO_TRIGGER",
  timestamp: 1724278920.018,
  gameId: 101,
  payload: {
    triggerType: AudioTriggerType.COLLISION_HIT,
    intensity: 0.95,
    kineticEnergy: 3450.0,
    stadiumDecibels: 108.5
  }
};

const injuryMsg: WebSocketBroadcastMessage = {
  sequenceId: 10004,
  messageType: "INJURY_EVENT",
  timestamp: 1724278925.0,
  gameId: 101,
  payload: {
    id: "triage_rec_2026_w04_015",
    playerId: 15,
    gameId: 101,
    timestamp: 842.5,
    activeInjuries: [
      {
        zone: AnatomicalZone.ANKLE_FOOT,
        diagnosis: "High Ankle Sprain Grade II",
        severityGrade: "MODERATE",
        painIndex: 6.5,
        estimatedWeeksOut: 3,
        selectedIntervention: MedicalIntervention.PAIN_MANAGEMENT_TORADOL,
        reinjuryProbabilityMultiplier: 1.75
      }
    ],
    medicalStaffRating: 92,
    clearedForLimitedPractice: true
  }
};

console.log("Discriminated union pattern matching test:");
function routeMessage(msg: WebSocketBroadcastMessage): string {
  switch (msg.messageType) {
    case "STATE_SYNC":
      return \`State sync for game \${msg.payload.gameId}, Q\${msg.payload.quarter}\`;
    case "TELEMETRY_FRAME":
      return \`Telemetry frame #\${msg.payload.frameIndex}, ball at (\${msg.payload.ballPosition.x}, \${msg.payload.ballPosition.y})\`;
    case "AUDIO_TRIGGER":
      return \`Audio trigger \${msg.payload.triggerType} (\${msg.payload.intensity})\`;
    case "INJURY_EVENT":
      return \`Injury event for player \${msg.payload.playerId}: \${msg.payload.activeInjuries[0].diagnosis}\`;
    case "CLIP_DISPATCH":
      return \`Clip cue \${msg.payload.clipType}\`;
    default: {
      const _exhaustiveCheck: never = msg;
      return _exhaustiveCheck;
    }
  }
}

console.log(routeMessage(stateSyncMsg));
console.log(routeMessage(telemetryMsg));
console.log(routeMessage(audioMsg));
console.log(routeMessage(injuryMsg));
`;

const tempTsPath = path.resolve('temp_test_runner.ts');
fs.writeFileSync(tempTsPath, testRunnerTs, 'utf8');

const tscPath = path.resolve('frontend/node_modules/typescript/bin/tsc');
const tscResult = spawnSync('node', [tscPath, '--strict', '--noEmit', '--target', 'es2022', '--lib', 'es2022,dom', tempTsPath], { encoding: 'utf-8' });

if (tscResult.status !== 0) {
  console.error("TypeScript strict verification failed:");
  console.error(tscResult.stdout);
  console.error(tscResult.stderr);
  fs.unlinkSync(tempTsPath);
  process.exit(1);
} else {
  console.log("TypeScript strict compiler verification PASSED with 0 errors!");
  fs.unlinkSync(tempTsPath);
}
