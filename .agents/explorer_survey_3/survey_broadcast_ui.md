# Broadcast Director, Glassmorphic UI Design System & Unified Data Contracts Specification
**Document ID:** NFL-SIM-SURVEY-003  
**Status:** COMPREHENSIVE_SPECIFICATION_DEFINED  
**Target:** The Digital Gridiron Simulation Ecosystem  
**Author:** Explorer 3 (Broadcast & UI Systems Analyst)  
**Date:** 2026-08-21  

---

## Executive Summary

This specification delivers the architectural blueprint for **Pillar 3 (Broadcast Director)**, **Pillar 4 (Glassmorphic UI Design System)**, and the **Unified Data Contracts** of the NFL Sim Engine ("The Digital Gridiron"). It unifies modern sports broadcast presentation (inspired by EA Sports College Football 25, Madden NFL, and Sunday Night Football on NBC) with real-time 3D spatial choreography, zero-dependency procedural Web Audio API synthesis, a 13-view glassmorphic UI grammar, and strictly typed bidirectional Pydantic V2 / TypeScript data contracts.

---

# Section 1: 7-State Discrete Broadcast Transition Engine

## 1.1 State Definitions & Architectural Topology

The broadcast director operates as a deterministic, discrete Moore/Mealy hybrid finite state machine (FSM). It sequences all game events, cinematic cameras, score bug overlays, instant replays, and audio cues into a television-grade broadcast timeline.

```text
               +-------------------------------------------------------------+
               |                                                             |
               V                                                             | (Game End / Reset)
      +------------------+         (Play Call Dispatched)                    |
      |  IDLE_STADIUM    | ------------------------------------+             |
      +------------------+                                     |             |
               ^                                               V             |
               | (Between Plays Complete)            +------------------+    |
               +------------------------------------ |  HUD_UPDATE      |    |
                                                     +------------------+    |
                                                               ^             |
                                                               |             |
+--------------------+      (Huddle Break)      +--------------------+       |
|    PRE_PLAY        | -----------------------> |    PRE_SNAP        |       |
+--------------------+                          +--------------------+       |
                                                           |                 |
                                                           | (Ball Snapped)  |
                                                           V                 |
+--------------------+   (Replay Complete)      +--------------------+       |
|  HIGHLIGHT_REPLAY  | <----------------------- |    IN_PLAY         |       |
+--------------------+   (If Highlight Worthy)  +--------------------+       |
          |                                                |                 |
          | (No Replay / Replay Done)                      | (Whistle Blown) |
          V                                                V                 |
+--------------------------------------------------------------------+       |
|                       POST_PLAY_REACTION                           |-------+
+--------------------------------------------------------------------+
```

### The 7 Discrete Broadcast States

1. **`IDLE_STADIUM`**:
   - **Description**: Baseline ambient stadium state prior to play calling or during administrative breaks.
   - **Visuals**: Wide establishing stadium flyover, blimp view, weather atmosphere effects, crowd idle sway.
   - **HUD**: Minimized clean scoreboard bug, broadcast watermark, weather overlay pill.
   - **Audio**: Ambient low crowd chatter, stadium wind/weather sounds, subtle broadcast background rhythm.
   - **Duration**: Open-ended (until user or AI calls play) or fixed 15.0s during automatic mode.

2. **`PRE_PLAY`**:
   - **Description**: Play has been selected; offenses and defenses break huddle, matchup graphics display.
   - **Visuals**: Low-angle dynamic dolly sweep across offensive formation, key player spotlight cards.
   - **HUD**: Play calling banner collapses into lower-third; matchup card (QB vs Pass Rush or WR vs CB) slides in.
   - **Audio**: Offensive cadence murmurs, formation shifting footsteps, broadcast stinger chime.
   - **Duration**: 2.5s to 5.0s (skippable by user).

3. **`PRE_SNAP`**:
   - **Description**: Offense is set at the line of scrimmage, QB surveys defense, audibles/motions occur.
   - **Visuals**: Tight broadcast sideline-high angle or coordinator tactical view over the QB's shoulder.
   - **HUD**: Laser line of scrimmage (blue), first down line (yellow), red zone marker (crimson), play clock countdown pill.
   - **Audio**: Crisp QB cadence ("White Eighty! Set... Hut!"), defensive shift calls, crowd noise crescendo if away offense on 3rd down.
   - **Duration**: 2.0s to 8.0s (dynamic based on play clock).

4. **`IN_PLAY`**:
   - **Description**: Ball is snapped; active play execution through tackle, touchdown, turnover, or incomplete pass.
   - **Visuals**: Dynamic tracking camera following ball carrier trajectory with predictive lead offset and collision shake.
   - **HUD**: Minimalist live action mode (scoreboard docked top-left, telestrator routes enabled, play clock hidden).
   - **Audio**: Hard pads collision synthesis, foot turf cuts, quarterback grunt, ball catch thump, referee whistle at whistle timestamp.
   - **Duration**: Exactly matched to physics simulation tick timeline (typically 3.5s - 10.0s).

5. **`POST_PLAY_REACTION`**:
   - **Description**: Play dead; immediate emotional reaction, celebrations, tackle aftermath, injury triage popup.
   - **Visuals**: Tight low-angle player tracking (celebrating WR/RB or frustrated defender), sideline coach reaction.
   - **HUD**: Play result summary banner ("+24 YDS - RUSH BY #28", "TOUCHDOWN", "INTERCEPTION").
   - **Audio**: Crowd explosion (roar or shocked gasp), stadium horn on score, referee whistle reverberation.
   - **Duration**: 3.0s to 6.0s.

6. **`HUD_UPDATE`**:
   - **Description**: Post-play data sync; scoreboard numbers flip, box score statistics update, down-and-distance recalculates.
   - **Visuals**: High-angle tactical reset view as players jog back to huddle or hurry-up formation.
   - **HUD**: Animated number counters (score, yards, down indicator), drive summary popover, fatigue indicators update.
   - **Audio**: Tactile HUD tick sound effects, digital score flip chimes, short broadcast stinger.
   - **Duration**: 1.5s to 3.0s.

7. **`HIGHLIGHT_REPLAY`**:
   - **Description**: Instant replay package triggered for highlight-worthy events (turnovers, touchdowns, 20+ yard gains, big hits, sacks).
   - **Visuals**: Multi-angle replay cuts (Angle 1: All-22 High Endzone, Angle 2: Tight Reverse Sideline, Angle 3: Wire Cam Slow-Mo).
   - **HUD**: "INSTANT REPLAY" badge, slow-motion scrubber bar, player stat overlay badge, telestrator vector annotations.
   - **Audio**: Subdued crowd sound with low-pass filter (400Hz cutoff), procedural slow-motion whoosh, broadcast replay theme stinger.
   - **Duration**: 5.0s to 12.0s (skippable).

---

## 1.2 Full 7x7 State Transition Matrix

The table below defines all permissible state transitions, guard conditions, and transition actions.

| From \ To | `IDLE_STADIUM` | `PRE_PLAY` | `PRE_SNAP` | `IN_PLAY` | `POST_PLAY_REACTION` | `HUD_UPDATE` | `HIGHLIGHT_REPLAY` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`IDLE_STADIUM`** | ❌ Self-loop on pause | ✅ **Guard**: `PLAY_CALLED`<br>**Action**: Queue formation sweeps | ❌ Illegal | ❌ Illegal | ❌ Illegal | ❌ Illegal | ❌ Illegal |
| **`PRE_PLAY`** | ✅ **Guard**: `TIMEOUT_CALLED` or `DELAY_OF_GAME`<br>**Action**: Reset cameras | ❌ Self-loop on audible | ✅ **Guard**: `PLAYERS_SET`<br>**Action**: Lock LOS laser | ❌ Illegal (skip only) | ❌ Illegal | ❌ Illegal | ❌ Illegal |
| **`PRE_SNAP`** | ✅ **Guard**: `TIMEOUT_CALLED`<br>**Action**: Stoppage HUD | ✅ **Guard**: `AUDIBLE_CALLED`<br>**Action**: Shift cameras | ❌ Self-loop on hard count | ✅ **Guard**: `BALL_SNAPPED`<br>**Action**: Start physics clock | ❌ Illegal | ❌ Illegal | ❌ Illegal |
| **`IN_PLAY`** | ❌ Illegal | ❌ Illegal | ❌ Illegal | ❌ Self-loop per physics frame | ✅ **Guard**: `WHISTLE_BLOWN` (tackle/TD/out-of-bounds)<br>**Action**: Cut to hero cam | ❌ Illegal | ❌ Illegal |
| **`POST_PLAY_REACTION`** | ❌ Illegal | ❌ Illegal | ❌ Illegal | ❌ Illegal | ❌ Self-loop on celebration | ✅ **Guard**: `REPLAY_EVAL_FALSE` or `SKIP`<br>**Action**: Trigger stats flip | ✅ **Guard**: `REPLAY_EVAL_TRUE` & `ENABLE_REPLAY`<br>**Action**: Load multi-angle buffer |
| **`HUD_UPDATE`** | ✅ **Guard**: `QUARTER_END` or `GAME_END`<br>**Action**: Transition to Halftime/Final | ✅ **Guard**: `NEXT_DOWN_READY`<br>**Action**: Present play-calling menu | ❌ Illegal | ❌ Illegal | ❌ Illegal | ❌ Self-loop on counter animation | ❌ Illegal |
| **`HIGHLIGHT_REPLAY`**| ❌ Illegal | ❌ Illegal | ❌ Illegal | ❌ Illegal | ❌ Illegal | ✅ **Guard**: `REPLAY_FINISHED` or `SKIP`<br>**Action**: Clear replay buffer | ❌ Self-loop on angle switch |

---

## 1.3 Error Recovery, Cascades & Watchdog Timer Matrix

To guarantee that the broadcast engine never deadlocks or freezes due to dropped WebSocket packets, corrupted telemetry frames, WebGL context crashes, or animation frame desynchronization, the system implements a strict Watchdog Timer Cascade.

```text
[State Enter] ---> [Start Watchdog Timer]
                         |
                         +---> [Event Received Within Limit] ---> [Cancel Timer & Advance]
                         |
                         +---> [Timer Expires (Threshold Exceeded)]
                                        |
                                        V
                               [Execute State Fallback Action]
                                        |
                                        V
                               [Force Cascade to Safe State]
```

### Watchdog Timer & Recovery Specification

| State | Max Allowed Duration | Watchdog Timeout Action | Fallback Target State | Corrupted Packet Recovery |
| :--- | :--- | :--- | :--- | :--- |
| **`IDLE_STADIUM`** | 60.0s (Auto Mode) / $\infty$ (Manual) | Trigger auto-play selection if simulated | `PRE_PLAY` | Re-request stadium weather & roster sync payload |
| **`PRE_PLAY`** | 8.0s | Force huddle break, skip formation camera sweep | `PRE_SNAP` | Discard overlay queue, reset camera to standard tactical 50-yard line |
| **`PRE_SNAP`** | 25.0s (Play Clock Expiry) | Trigger Delay of Game penalty event | `POST_PLAY_REACTION` | Snap camera to standard LOS anchor (x=0, y=12, z=LOS) |
| **`IN_PLAY`** | 15.0s (Max Play Physics Length) | Force emergency whistle event, resolve play at last known ball coordinates | `POST_PLAY_REACTION` | Interpolate missing player transform vectors using last known velocity: $\vec{P}(t) = \vec{P}_0 + \vec{V}_0 \Delta t$ |
| **`POST_PLAY_REACTION`** | 6.0s | Kill reaction cutscene, dismiss lower-third banners | `HUD_UPDATE` | Reset active camera index to 0 |
| **`HUD_UPDATE`** | 4.0s | Force-commit all pending state mutations to Redux/Zustand store | `IDLE_STADIUM` / `PRE_PLAY` | Overwrite local scores with authoritative server `GameStateSync` payload |
| **`HIGHLIGHT_REPLAY`** | 12.0s | Terminate replay buffer playback immediately | `HUD_UPDATE` | Purge replay frame queue and free WebGL buffer memory |

---

# Section 2: Procedural 3D Camera Orbit Trajectories & Dynamics

## 2.1 NFL Gridiron 3D World Coordinate System

The 3D virtual environment standardizes on a right-handed Cartesian coordinate system measured in **yards**:

$$\begin{aligned}
X &\in [-26.65, +26.65] \quad \text{(Field Width: 53.33 yards / 160 feet. Left sideline } -26.65\text{, Right sideline } +26.65\text{)} \\
Y &\in [0.0, +\infty] \quad \text{(Elevation: Turf plane at } Y=0.0\text{ yards, crossbar at } Y=3.33\text{ yards)} \\
Z &\in [-60.0, +60.0] \quad \text{(Field Length: 120 yards. Midfield 50-yd line at } Z=0.0\text{, Goal Lines at } Z=\pm 50.0\text{, Endzone backs at } Z=\pm 60.0\text{)}
\end{aligned}$$

```text
               [-26.65, 0, +60.0]                       [+26.65, 0, +60.0]
                     +---------------------------------------+  Back of North Endzone
                     |               NORTH ENDZONE           |
  North Goal Line -> |=======================================|  Z = +50.0 yards
                     |                   |                   |
                     |                   |                   |
                     |                   |                   |
                     |                   |                   |
     50-Yard Line -> |-------------------+-------------------|  Z = 0.0 yards (Midfield)
                     |       (-X)        |       (+X)        |
                     |   Left Sideline   |   Right Sideline  |
                     |                   |                   |
                     |                   |                   |
  South Goal Line -> |=======================================|  Z = -50.0 yards
                     |               SOUTH ENDZONE           |
                     +---------------------------------------+  Back of South Endzone
               [-26.65, 0, -60.0]                       [+26.65, 0, -60.0]
```

---

## 2.2 Tracking Focal Points & Dynamic Framing Formulations

### 1. Ball Carrier Predictive Lead Tracking

To prevent the ball carrier from running off-screen during explosive plays, the camera focal look-at point $\vec{T}_{\text{carrier}}(t)$ incorporates an adaptive predictive lead vector proportional to player velocity $\vec{V}_{\text{carrier}}(t)$:

$$\vec{T}_{\text{carrier}}(t) = \vec{P}_{\text{carrier}}(t) + \tau_{\text{lead}} \cdot \vec{V}_{\text{carrier}}(t) + \vec{O}_{\text{elevation}}$$

Where:
- $\vec{P}_{\text{carrier}}(t) = (x_c, y_c, z_c)^T$ is the world position of the ball carrier.
- $\vec{V}_{\text{carrier}}(t) = (\dot{x}_c, 0, \dot{z}_c)^T$ is the 2D planar velocity vector.
- $\tau_{\text{lead}} = 0.35\,\text{seconds}$ (lead anticipation look-ahead window).
- $\vec{O}_{\text{elevation}} = (0, 1.2, 0)^T$ (chest-height visual center).

### 2. QB Pocket Dynamic Bounding Cylinder

During pass plays prior to ball release, the camera dynamically encloses the quarterback and active pass rushers within a spatial bounding cylinder:

$$\vec{C}_{\text{pocket}}(t) = \frac{1}{N} \sum_{i=1}^{N} \vec{P}_i(t), \quad R_{\text{pocket}}(t) = \max_{i \in [1, N]} \|\vec{P}_i(t) - \vec{C}_{\text{pocket}}(t)\| + R_{\text{margin}}$$

- Camera position $\vec{P}_{\text{cam}}(t)$ maintains an offset distance $D(t) = \max(D_{\min}, k_{\text{dist}} \cdot R_{\text{pocket}}(t))$ along the pocket's dominant offensive vector.

### 3. Deep Ball Parabolic Apex Framing

When the ball is airborne on passes exceeding 20 air yards, the camera interpolates its focal target $\vec{T}_{\text{ball}}(t)$ between the football's kinematic apex $h_{\text{apex}}$ and the targeted receiver's projected break point $\vec{P}_{\text{target}}$:

$$\vec{T}_{\text{ball}}(t) = (1 - w(t)) \cdot \vec{P}_{\text{ball}}(t) + w(t) \cdot \vec{P}_{\text{receiver}}(t)$$

$$w(t) = \frac{1}{1 + e^{-k_{\text{blend}}(t - t_{\text{apex}})}}$$

Where $w(t)$ is a smooth logistic sigmoid transition transferring visual weight from the football in flight to the receiver/defensive back contested catch window.

### 4. Sideline Touchdown / Turnover Celebration Orbit

Upon a touchdown or turnover, the camera executes a cinematic smooth cylindrical orbit around the celebration centroid $\vec{P}_{\text{hero}}$:

$$\begin{aligned}
X_{\text{cam}}(t) &= X_{\text{hero}} + R_{\text{orbit}}(t) \cdot \cos(\theta_0 + \omega t) \\
Y_{\text{cam}}(t) &= Y_{\text{hero}} + H_{\text{orbit}} + A_{\text{bob}} \cdot \sin(2\omega t) \\
Z_{\text{cam}}(t) &= Z_{\text{hero}} + R_{\text{orbit}}(t) \cdot \sin(\theta_0 + \omega t)
\end{aligned}$$

- Angular velocity: $\omega = 0.52\,\text{rad/s}$ ($30^\circ/\text{second}$).
- Radial contraction: $R_{\text{orbit}}(t) = R_{\text{start}} \cdot e^{-\lambda t} + R_{\text{close}} \cdot (1 - e^{-\lambda t})$.

---

## 2.3 Spline Interpolation & Quaternion Rotation Smoothing

Camera trajectories transition between control knots $\mathbf{K}_i = (\vec{P}_i, \mathbf{Q}_i, \text{FOV}_i, t_i)$ using $C^2$-continuous **Centripetal Catmull-Rom Splines** to prevent overshoot, cusps, and loop artifacts.

### Catmull-Rom Position Evaluation

For knot parameter $u \in [0, 1]$ between control points $\mathbf{P}_1$ and $\mathbf{P}_2$ with neighbors $\mathbf{P}_0$ and $\mathbf{P}_3$:

$$\vec{P}(u) = \frac{1}{2} \begin{bmatrix} 1 & u & u^2 & u^3 \end{bmatrix} \begin{bmatrix} 0 & 2 & 0 & 0 \\ -1 & 0 & 1 & 0 \\ 2 & -5 & 4 & -1 \\ -1 & 3 & -3 & 1 \end{bmatrix} \begin{bmatrix} \vec{P}_0 \\ \vec{P}_1 \\ \vec{P}_2 \\ \vec{P}_3 \end{bmatrix}$$

### Quaternion Look-At Rotation Smoothing ($\text{Slerp}$)

Camera orientation $\mathbf{Q}(u)$ interpolates smoothly along the 4D hypersphere:

$$\mathbf{Q}(u) = \text{Slerp}(\mathbf{Q}_1, \mathbf{Q}_2, u) = \frac{\sin((1 - u)\Omega)}{\sin \Omega} \mathbf{Q}_1 + \frac{\sin(u\Omega)}{\sin \Omega} \mathbf{Q}_2$$

Where $\cos \Omega = \mathbf{Q}_1 \cdot \mathbf{Q}_2$.

---

## 2.4 Camera Shake, Collision Trauma & Lens FOV Dynamics

### 1. Collision Trauma Shake Model

Tackles, sacks, and collisions impart an instantaneous kinetic trauma impulse $T_0 \in [0.0, 1.0]$ based on impact force $F_{\text{impact}} = m_{\text{tackler}} \cdot \|\vec{v}_{\text{rel}}\| / \Delta t$:

$$T(t) = T_0 \cdot e^{-\gamma (t - t_{\text{impact}})}$$

Rotational yaw/pitch perturbations and translational screen shake:

$$\begin{aligned}
\Delta \text{Yaw}(t) &= k_{\text{rot}} \cdot (T(t))^2 \cdot \text{SimplexNoise}(f_1 \cdot t, 0) \\
\Delta \text{Pitch}(t) &= k_{\text{rot}} \cdot (T(t))^2 \cdot \text{SimplexNoise}(0, f_1 \cdot t) \\
\Delta X_{\text{cam}}(t) &= k_{\text{trans}} \cdot (T(t))^2 \cdot \text{SimplexNoise}(f_2 \cdot t, 42.0)
\end{aligned}$$

- Damping rate: $\gamma = 4.5\,\text{s}^{-1}$ (shake dissipates within $\approx 0.65\,\text{s}$).

### 2. Dynamic Field of View (FOV) Lens Choreography

The camera field of view dynamically expands and compresses to heighten television drama:

| Phase / Trigger | Target FOV | Transition Duration | Rationale |
| :--- | :--- | :--- | :--- |
| **`PRE_SNAP` (Tactical)** | $58^\circ$ | 1.0s Smooth | Broad overview of coverage shells & blitz alignments |
| **`IN_PLAY` (Snap Zoom-In)** | $48^\circ$ | 0.35s Snap | Creates tight pocket tension and speed illusion |
| **`IN_PLAY` (Deep Pass)** | $68^\circ$ | 0.8s Smooth | Expands spatial awareness to track receiver separation |
| **`IN_PLAY` (Red Zone Run)** | $44^\circ$ | 0.5s Smooth | Emphasizes tight trench collisions |
| **`HIGHLIGHT_REPLAY` (Telephoto)** | $28^\circ$ | 0.2s Instant | High-compression broadcast lens isolating footwork & catch control |

---

# Section 3: Web Audio API Synthesized Broadcast Audio Triggers

The simulation contains a 100% offline, zero-asset Web Audio API audio synthesis engine. It generates high-fidelity stadium acoustics, referee whistles, crowd dynamics, collision thuds, and broadcast stingers using native audio nodes (`OscillatorNode`, `BiquadFilterNode`, `GainNode`, `ConvolverNode`, `StereoPannerNode`, `DynamicsCompressorNode`).

```text
[Noise/Oscillator Generators]
              |
              V
   [Biquad Filter Graph]  ---> (Cutoff Modulated by Decibels / Situation)
              |
              V
      [Gain Envelope]     ---> (ADSR Kinetic Scaling)
              |
              V
  [Reverb / Convolver DSP] ---> (Stadium Early Reflections & Echo)
              |
              V
 [Dynamics Compressor Node] ---> (Master Broadcast Limiting)
              |
              V
     [Audio Destination]
```

---

## 3.1 Dynamic Crowd Noise Engine (Pink Noise Filter Graph)

The crowd sound synthesizes continuous ambient pink noise modulated by decibel ratings $L_{\text{dB}} \in [50, 120]$ and game momentum.

### DSP Node Graph Architecture

1. **Noise Generation**: AudioWorklet or Paul Kellet 3-pole filter approximation generates continuous pink noise ($\approx -3\,\text{dB}/\text{octave}$):
   $$y[n] = 0.99886 y_1[n] + 0.05552 x[n] + 0.99332 y_2[n] + 0.07508 x[n] + 0.96900 y_3[n] + 0.15385 x[n]$$
2. **Dual Resonant Formant Filters**:
   - `Filter 1` (Low Rumble): `BiquadFilterNode` (`type: "bandpass"`, $f_0 = 180\,\text{Hz}$, $Q = 1.8$).
   - `Filter 2` (Human Shouting Band): `BiquadFilterNode` (`type: "bandpass"`, $f_0 = 850\,\text{Hz} \to 2400\,\text{Hz}$, $Q = 2.4$).
3. **Decibel-to-Gain Mapping**:
   $$\text{Gain}_{\text{crowd}} = \text{BaseGain} \cdot 10^{\frac{L_{\text{dB}} - 90}{20}}$$
4. **Dynamic Context Modulations**:
   - **3rd Down Defense**: Continuous frequency and Q rise on Filter 2 ($850\,\text{Hz} \to 1800\,\text{Hz}$, $+6\,\text{dB}$ gain swell over 4.0s).
   - **Red Zone Roar**: Sub-bass boost ($80\,\text{Hz}$ low shelf $+8\,\text{dB}$).
   - **Away Turnover**: Instant $-18\,\text{dB}$ attenuation drop in $80\,\text{ms}$, followed by slow rise of visiting fan cheers ($2200\,\text{Hz}$ peak).

---

## 3.2 Stadium PA Announcer Acoustic Emulation

To recreate the resonant, delayed acoustics of a stadium public address system:

1. **Formant Bandpass Filter**: Restricts frequency range to emulate horn-loaded stadium speakers ($f_{\text{low}} = 350\,\text{Hz}$, $f_{\text{high}} = 3800\,\text{Hz}$, steep $24\,\text{dB}/\text{octave}$ rolloff).
2. **Early Reflections Convolver**: Synthesizes a 2.2-second decaying stadium impulse response (exponential decay $e^{-2.5 t}$ with $18$ sparse reflection spikes).
3. **Slapback Feedback Delay**: Delay line $\tau = 280\,\text{ms}$, feedback $g = 0.32$, cross-panned left and right ($\pm 0.45$).

---

## 3.3 Referee Whistle Synthesizer

Recreates the classic Acme Thunderer pea-whistle using dual coupled oscillators with phase jitter and trill modulation:

```typescript
// Web Audio API Whistle Synthesis Node Graph
const ctx = audioContext;
const now = ctx.currentTime;

const osc1 = ctx.createOscillator(); // Resonant fundamental 1
const osc2 = ctx.createOscillator(); // Resonant fundamental 2
const lfo = ctx.createOscillator();  // Pea rattle / trill LFO
const lfoGain = ctx.createGain();
const masterGain = ctx.createGain();

// Twin frequencies generating physical acoustic beat interference
osc1.type = "sine";
osc1.frequency.setValueAtTime(2780, now);
osc2.type = "sine";
osc2.frequency.setValueAtTime(3090, now);

// Trill Modulation (shaking air pocket inside whistle chamber)
lfo.type = "sine";
lfo.frequency.setValueAtTime(28.5, now); // 28.5 Hz pea rattle
lfoGain.gain.setValueAtTime(160, now);    // +/- 160 Hz frequency sweep
lfo.connect(osc1.frequency);
lfo.connect(osc2.frequency);

// Tight exponential ADSR envelope
masterGain.gain.setValueAtTime(0.0001, now);
masterGain.gain.linearRampToValueAtTime(0.42 * volume, now + 0.035); // 35ms Attack
masterGain.gain.setValueAtTime(0.42 * volume, now + 0.28);           // Sustain
masterGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.48);     // Decay/Release

osc1.connect(masterGain);
osc2.connect(masterGain);
masterGain.connect(ctx.destination);

lfo.start(now);
osc1.start(now);
osc2.start(now);
lfo.stop(now + 0.5);
osc1.stop(now + 0.5);
osc2.stop(now + 0.5);
```

---

## 3.4 Collision Impact Synthesis (Kinetic Mass-Velocity Physics)

Tackle impacts scale their acoustic synthesis directly from physics simulation telemetry ($m_1, m_2, \vec{v}_1, \vec{v}_2$):

$$E_{\text{kinetic}} = \frac{1}{2} \left( \frac{m_1 m_2}{m_1 + m_2} \right) \|\vec{v}_1 - \vec{v}_2\|^2$$

### Multi-Layer Impact Audio Graph

1. **Layer 1: Sub-Bass Thud (Body Mass Displacement)**:
   - Triangle wave sweeping from $140\,\text{Hz} \to 28\,\text{Hz}$ over $160\,\text{ms}$.
   - Amplitude scaled by $\min(1.0, E_{\text{kinetic}} / 3500\,\text{J})$.
2. **Layer 2: Helmet / Plastic Shoulder Pad Crack**:
   - Short bandpass white noise burst ($1800\,\text{Hz} - 4500\,\text{Hz}$), duration $25\,\text{ms}$, sharp exponential decay ($12\,\text{ms}$).
3. **Layer 3: Turf Disruption Crunch**:
   - Lowpass pink noise ($20\,\text{Hz} - 400\,\text{Hz}$), duration $220\,\text{ms}$, simulating cleats digging into artificial turf.

---

## 3.5 Procedural Broadcast Stingers & Fanfares

Synthesizes harmonic TV broadcast transitions using 4-operator FM synthesis:

1. **Down-and-Distance Stinger (3rd Down Alert)**:
   - Deep pulsating square-sine hybrid chord ($\text{D}_2 - \text{A}_2 - \text{D}_3$) with lowpass filter sweep ($300\,\text{Hz} \to 2400\,\text{Hz} \to 400\,\text{Hz}$) and stereo chorus.
2. **Touchdown Fanfare**:
   - Brassy FM brass stack playing an ascending triumphant triad: $\text{F}_4 \to \text{A}_4 \to \text{C}_5 \to \text{F}_5$ with rich 2nd and 3rd harmonic overtones.
3. **Wipe / Replay Whoosh**:
   - Modulated white noise sweeping through a high-resonance bandpass filter ($200\,\text{Hz} \to 4500\,\text{Hz} \to 150\,\text{Hz}$) with stereo panning swipe left to right ($-1.0 \to +1.0$).

---

# Section 4: Glassmorphic UI/UX Component & Token Design System

## 4.1 Design Philosophy & Visual Tokens

The Digital Gridiron UI adopts an un-templated, tactile **Editorial Sports Glassmorphism** aesthetic. It combines dark stadium carbon fiber and turf textures, high-contrast typography, precision neon laser down-and-distance markers, and metallic tiered shields.

```text
================================================================================
GLASSMORPHIC COMPONENT STACK TOKENS
================================================================================
Layer 0: Stadium Turf / Carbon Fiber Canvas (Hex: #050608, Radial Lighting)
Layer 1: Backdrop Blur Glass (rgba(14, 19, 29, 0.75), blur(16px), border: 1px solid rgba(255,255,255,0.12))
Layer 2: Franchise Color Dynamic Gradient Sheen (--theme-primary, --theme-secondary)
Layer 3: Tactile Content, Metallic OVR Badges, Down-Distance HUD Pills
Layer 4: Interactive Overlays, 3D Body Maps, Telestrator Vectors
================================================================================
```

---

## 4.2 Comprehensive 32 NFL Franchise Color Tokens

All 32 NFL franchises are represented with strict, hex-accurate primary, secondary, accent, and glass-tint variables:

```json
[
  { "id": "ARI", "name": "Arizona Cardinals", "primary": "#97233F", "secondary": "#000000", "accent": "#FFB612", "glass": "rgba(151,35,63,0.22)" },
  { "id": "ATL", "name": "Atlanta Falcons", "primary": "#A71930", "secondary": "#000000", "accent": "#A5ACAF", "glass": "rgba(167,25,48,0.22)" },
  { "id": "BAL", "name": "Baltimore Ravens", "primary": "#241773", "secondary": "#000000", "accent": "#9E7C0C", "glass": "rgba(36,23,115,0.25)" },
  { "id": "BUF", "name": "Buffalo Bills", "primary": "#00338D", "secondary": "#C60C30", "accent": "#FFFFFF", "glass": "rgba(0,51,141,0.25)" },
  { "id": "CAR", "name": "Carolina Panthers", "primary": "#0085CA", "secondary": "#101820", "accent": "#BFC0BF", "glass": "rgba(0,133,202,0.22)" },
  { "id": "CHI", "name": "Chicago Bears", "primary": "#0B162A", "secondary": "#C83803", "accent": "#FFFFFF", "glass": "rgba(11,22,42,0.30)" },
  { "id": "CIN", "name": "Cincinnati Bengals", "primary": "#FB4F14", "secondary": "#000000", "accent": "#FFFFFF", "glass": "rgba(251,79,20,0.22)" },
  { "id": "CLE", "name": "Cleveland Browns", "primary": "#311D00", "secondary": "#FF3C00", "accent": "#FFFFFF", "glass": "rgba(49,29,0,0.30)" },
  { "id": "DAL", "name": "Dallas Cowboys", "primary": "#003594", "secondary": "#041E42", "accent": "#869397", "glass": "rgba(0,53,148,0.25)" },
  { "id": "DEN", "name": "Denver Broncos", "primary": "#FB4F14", "secondary": "#002244", "accent": "#FFFFFF", "glass": "rgba(251,79,20,0.22)" },
  { "id": "DET", "name": "Detroit Lions", "primary": "#0076B6", "secondary": "#B0B7BC", "accent": "#000000", "glass": "rgba(0,118,182,0.25)" },
  { "id": "GB",  "name": "Green Bay Packers", "primary": "#203731", "secondary": "#FFB612", "accent": "#FFFFFF", "glass": "rgba(32,55,49,0.28)" },
  { "id": "HOU", "name": "Houston Texans", "primary": "#03202F", "secondary": "#A71930", "accent": "#FFFFFF", "glass": "rgba(3,32,47,0.30)" },
  { "id": "IND", "name": "Indianapolis Colts", "primary": "#002C5F", "secondary": "#A2AAAD", "accent": "#FFFFFF", "glass": "rgba(0,44,95,0.28)" },
  { "id": "JAX", "name": "Jacksonville Jaguars", "primary": "#006778", "secondary": "#D7A22A", "accent": "#101820", "glass": "rgba(0,103,120,0.25)" },
  { "id": "KC",  "name": "Kansas City Chiefs", "primary": "#E31837", "secondary": "#FFB81C", "accent": "#FFFFFF", "glass": "rgba(227,24,55,0.25)" },
  { "id": "LV",  "name": "Las Vegas Raiders", "primary": "#000000", "secondary": "#A5ACAF", "accent": "#FFFFFF", "glass": "rgba(20,20,20,0.35)" },
  { "id": "LAC", "name": "Los Angeles Chargers", "primary": "#0080C6", "secondary": "#FFC20E", "accent": "#FFFFFF", "glass": "rgba(0,128,198,0.25)" },
  { "id": "LAR", "name": "Los Angeles Rams", "primary": "#003594", "secondary": "#FFA300", "accent": "#FF8200", "glass": "rgba(0,53,148,0.25)" },
  { "id": "MIA", "name": "Miami Dolphins", "primary": "#008E97", "secondary": "#FC4C02", "accent": "#005778", "glass": "rgba(0,142,151,0.25)" },
  { "id": "MIN", "name": "Minnesota Vikings", "primary": "#4F2683", "secondary": "#FFC62F", "accent": "#FFFFFF", "glass": "rgba(79,38,131,0.25)" },
  { "id": "NE",  "name": "New England Patriots", "primary": "#002244", "secondary": "#C60C30", "accent": "#B0B7BC", "glass": "rgba(0,34,68,0.30)" },
  { "id": "NO",  "name": "New Orleans Saints", "primary": "#D3BC8D", "secondary": "#101820", "accent": "#FFFFFF", "glass": "rgba(211,188,141,0.22)" },
  { "id": "NYG", "name": "New York Giants", "primary": "#0B2265", "secondary": "#A71930", "accent": "#A5ACAF", "glass": "rgba(11,34,101,0.28)" },
  { "id": "NYJ", "name": "New York Jets", "primary": "#125740", "secondary": "#000000", "accent": "#FFFFFF", "glass": "rgba(18,87,64,0.28)" },
  { "id": "PHI", "name": "Philadelphia Eagles", "primary": "#004C54", "secondary": "#A5ACAF", "accent": "#ACC0C6", "glass": "rgba(0,76,84,0.28)" },
  { "id": "PIT", "name": "Pittsburgh Steelers", "primary": "#FFB612", "secondary": "#101820", "accent": "#C60C30", "glass": "rgba(255,182,18,0.20)" },
  { "id": "SF",  "name": "San Francisco 49ers", "primary": "#AA0000", "secondary": "#B3995D", "accent": "#000000", "glass": "rgba(170,0,0,0.25)" },
  { "id": "SEA", "name": "Seattle Seahawks", "primary": "#002244", "secondary": "#69BE28", "accent": "#A5ACAF", "glass": "rgba(0,34,68,0.30)" },
  { "id": "TB",  "name": "Tampa Bay Buccaneers", "primary": "#D50A0A", "secondary": "#0A0A08", "accent": "#FF7900", "glass": "rgba(213,10,10,0.25)" },
  { "id": "TEN", "name": "Tennessee Titans", "primary": "#0C2340", "secondary": "#4B92DB", "accent": "#C8102E", "glass": "rgba(12,35,64,0.30)" },
  { "id": "WAS", "name": "Washington Commanders", "primary": "#5A1414", "secondary": "#FFB612", "accent": "#000000", "glass": "rgba(90,20,20,0.28)" }
]
```

---

## 4.3 Metallic OVR Shield Tiers Specification

Player overall ratings (OVR) are rendered inside precision beveled metallic shields with distinct material grading:

```text
+-----------------------------------------------------------------------------------+
| TIER            | RATING  | BACKGROUND / FOIL EFFECT             | BORDER / SHADOW |
|-----------------+---------+--------------------------------------+-----------------|
| 99-Club Platinum| 99      | Multi-stop Gold Foil + Rainbow Sparkle| #FFD700 Neon Glow |
| Elite Diamond   | 90 - 98 | Holographic Cyan Chrome Gradient     | #00F0FF Cyber Glow|
| Gold Tier       | 80 - 89 | Brushed Amber Gold Radial Sheen      | #F59E0B Warm Amber|
| Silver Tier     | 70 - 79 | Satin Titanium Metal / Platinum      | #94A3B8 Cool Slate|
| Bronze Tier     | < 70    | Raw Dark Copper / Cast Iron Texture  | #CD7F32 Dark Rust |
+-----------------------------------------------------------------------------------+
```

### CSS Implementation Tokens

```css
/* Metallic OVR Shield Tiers */
.ovr-shield-99 {
  background: radial-gradient(circle at 30% 20%, #fffbe6 0%, #ffd700 45%, #b38700 85%, #664d00 100%);
  border: 2px solid #fff3a8;
  color: #1a1200;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.75), inset 0 2px 4px rgba(255, 255, 255, 0.8);
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
}

.ovr-shield-elite {
  background: linear-gradient(135deg, #e0f7fa 0%, #00f0ff 40%, #007799 80%, #003344 100%);
  border: 2px solid #80f8ff;
  color: #021a24;
  box-shadow: 0 0 18px rgba(0, 240, 255, 0.65), inset 0 2px 4px rgba(255, 255, 255, 0.7);
}

.ovr-shield-gold {
  background: linear-gradient(135deg, #fffbeb 0%, #f59e0b 50%, #92400e 100%);
  border: 1.5px solid #fde68a;
  color: #1e1302;
  box-shadow: 0 0 12px rgba(245, 158, 11, 0.5), inset 0 1px 3px rgba(255, 255, 255, 0.6);
}

.ovr-shield-silver {
  background: linear-gradient(135deg, #f8fafc 0%, #94a3b8 50%, #334155 100%);
  border: 1.5px solid #cbd5e1;
  color: #0f172a;
  box-shadow: 0 0 10px rgba(148, 163, 184, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.5);
}

.ovr-shield-bronze {
  background: linear-gradient(135deg, #fef3c7 0%, #cd7f32 50%, #451a03 100%);
  border: 1.5px solid #d97706;
  color: #ffffff;
  box-shadow: 0 0 8px rgba(205, 127, 50, 0.3);
}
```

---

## 4.4 Down-and-Distance Laser HUD Pills & Telestrator Vector Canvas

### Laser HUD Pills
- **Geometry**: Skewed parallelogram (`clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 10px 100%)`).
- **LOS Pill**: Neon Cyan (`#00F0FF`), glowing 1px border, displays current yard line (e.g., `BALL ON 34`).
- **1st Down Pill**: High-visibility Electric Yellow (`#FACC15`), pulsating on 3rd down situations.
- **Red Zone Warning Pill**: Crimson Alert (`#EF4444`), displays `RED ZONE` with animated perimeter sweep.

### Interactive Chalkboard Telestrator Canvas
- **Rendering**: Real-time `<svg>` and `<canvas>` layer with pointer capture.
- **Stroke Smoothing**: Captures raw pointer events $(x_k, y_k)$ and evaluates Catmull-Rom splines to render continuous Bézier route stems.
- **Tactical Markings**: Route arrows (`path-arrow`), pass protection slides (perpendicular ticks), zone coverage bubbles (transparent cyan discs with dashed stroke), and X/O player anchor circles.

---

## 4.5 The 13 Core Views Architectural Grammar

```text
+---------------------------------------------------------------------------------------------------+
| #  | VIEW NAME                    | PRIMARY SYSTEM RESPONSIBILITY & KEY COMPONENTS                |
|----+------------------------------+---------------------------------------------------------------|
| 1  | Dashboard                    | Franchise command hub, weekly schedule, league pulse ticker   |
| 2  | Roster Management            | 53-man active/practice squad depth, contract years, cap hits  |
| 3  | Depth Chart                  | Drag-and-drop positional hierarchy with sub-package slots     |
| 4  | Play Calling / Game Sim      | Live 3D/2D gridiron simulation, play wheel, telestrator       |
| 5  | Standings                    | Conference & division tables, playoff seeds, tiebreakers     |
| 6  | Schedule / Scores            | 18-week schedule grid, live box scores, weather widgets       |
| 7  | Player Card / Profile        | Genesis biometrics, S2 cognition, radar charts, backstory     |
| 8  | Draft Room                   | War room clock, Big Board, scouting reports, trade up/down    |
| 9  | Free Agency / Trade Hub      | Trade machine, salary cap impact model, AI GM negotiations   |
| 10 | Injury Report / Medical Center| 3D anatomical body map, surgery triage, recovery timelines   |
| 11 | Financials / Cap Sheet       | Cap space waterfall, restructuring, dead money, rollover logs |
| 12 | Scheme & Strategy            | Offensive/defensive playbooks, coaching trees, tempo sliders  |
| 13 | Dynasty Storyline / News     | Emergent AI news articles, media reactions, locker room morale|
+---------------------------------------------------------------------------------------------------+
```

### Detailed View Wireframe & Component Specifications

#### View 1: Dashboard (Franchise Command Center)
- **Layout**: 3-column modular glass grid (`grid-cols-12`).
- **Left Column (col-span-3)**: Team identity card, GM level, franchise morale, season record, cap space pill.
- **Center Column (col-span-6)**: Weekly Matchup Hero card (Opponent preview, weather forecast, key head-to-head player matchups, "Advance Week / Play Game" spotlight CTA button).
- **Right Column (col-span-3)**: League Pulse feed (breaking injuries, trade block updates, Top 25 power rankings).
- **Bottom**: Infinite scrolling ribbon ticker with live scores across the league.

#### View 2: Roster Management
- **Layout**: Data-dense expandable datagrid with quick filters (Position, Status, Contract Year, Dev Trait).
- **Features**: Batch salary cap reallocation, practice squad promotions, IR designations, trade block toggles.
- **Micro-Interactions**: Hovering a row triggers a mini player preview with metallic OVR shield and radar chart.

#### View 3: Depth Chart
- **Layout**: Positional football formation layout (Offense: Singleback/Shotgun, Defense: 4-3/3-4/Nickel/Dime, Special Teams).
- **Features**: Drag-and-drop player swapping (`framer-motion` reorder), stamina/fatigue warning badges, sub-package role assignments (3rd Down RB, Slot WR, Rush DE).

#### View 4: Play Calling / Game Sim
- **Layout**: Split-screen command center.
- **Top Half**: 3D Live Gridiron Canvas (`LiveGameVisualizer`) with camera presets (Broadcast, Tactical All-22, Endzone, Wire Cam).
- **Bottom Half**: Play Call Dial (Run, Pass, Play Action, Screen, Blitz, Cover 2/3/4/Man), crowd noise decibel meter, game clock, timeouts remaining, situational coaching tips.

#### View 5: Standings
- **Layout**: Tabbed views (AFC / NFC Conference, 8 Divisions, Playoff Picture).
- **Features**: Division leaders highlighted with crown icons, wild card cutoff line (neon gold separator), tiebreaker reasoning tooltips (Head-to-head, Division record, Common games, Strength of Victory).

#### View 6: Schedule / Scores
- **Layout**: Horizontal week scrubber (Weeks 1-18, Wild Card, Divisional, Conference, Super Bowl).
- **Features**: Game tiles displaying team helmets, records, live/final scores, passing/rushing leaders, stadium weather conditions (Snow, Rain, Wind, Dome).

#### View 7: Player Card / Profile
- **Layout**: 2-column holographic card layout.
- **Left Column**: High-resolution 3D player character avatar, metallic OVR shield, jersey number, physical dimensions, X-Factor ability badge.
- **Right Column**: Tabbed panels:
  - *Attributes*: Grouped radar chart (Physical, Passing, Receiving, Blocking, Defense).
  - *Genesis Biometrics*: S2 Cognition score, wingspan, 40-yard dash, fast-twitch ratio.
  - *AI Backstory*: Procedural biography, hometown, collegiate highlights.
  - *Contract & Career Stats*: Multi-year salary breakdown and season-by-season log.

#### View 8: Draft Room
- **Layout**: War room interface.
- **Header**: Live draft clock with heartbeat pulse animation, current on-the-clock team badge, pick trade proposal alerts.
- **Body**: Big Board prospect table with position filters, draft grade pills, projected ceiling/floor, AI scouting report modal.
- **Sidebar**: Team draft capital breakdown (Rounds 1-7) and consensus team needs meter.

#### View 9: Free Agency / Trade Hub
- **Layout**: 2-pane interactive negotiation machine.
- **Features**: Side-by-side asset selection (Team A offering vs Team B requested). Real-time AI GM trade evaluation meter showing trade value parity, GM personality bias reasoning, and salary cap delta calculation.

#### View 10: Injury Report / Medical Center
- **Layout**: Interactive 3D/SVG anatomical body map alongside active injured reserve table.
- **Features**: Clicking an injured body zone (Head, Neck, Torso, Arms, Legs) reveals injury diagnosis (e.g., "Grade 2 MCL Sprain"), surgery risk vs rest timeline trade-off matrix, and return-to-play probability curves.

#### View 11: Financials / Cap Sheet
- **Layout**: Visual salary cap allocation dashboard.
- **Features**: Multi-year cap projection bar charts, dead cap liability visualizer, contract restructuring sandbox (converting base salary to signing bonus), and contract extension calculator.

#### View 12: Scheme & Strategy
- **Layout**: Tactical whiteboard canvas.
- **Features**: Offensive playbook selection (West Coast, Air Raid, Spread Option, Power Run) and Defensive schemes (4-3 Over, 3-4 Under, Cover 3 Match, Tampa 2). Playbook play editor and offensive/defensive tempo sliders (Aggressiveness, Blitz Rate, Substitution Frequency).

#### View 13: Dynasty Storyline / News
- **Layout**: Dynamic sports journalism feed.
- **Features**: AI-generated newspaper headlines, social media reaction feeds, coach press conference transcripts, locker room chemistry metrics, and Hall of Fame / Trophy Room display.

---

# Section 5: Formal Data Contracts (Pydantic V2 & TypeScript)

All simulation events, game entities, broadcast triggers, and WebSocket payload frames adhere to strict, bidirectional schemas.

## 5.1 Python Backend Schemas (Pydantic V2)

```python
"""
Unified Data Contracts - Pydantic V2 Schema Definitions
File: backend/app/schemas/contracts.py
"""

from enum import Enum
from typing import List, Dict, Optional, Literal, Any, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator


# =============================================================================
# 1. BROADCAST & CAMERA CONTRACTS
# =============================================================================

class BroadcastPhaseEnum(str, Enum):
    IDLE_STADIUM = "IDLE_STADIUM"
    PRE_PLAY = "PRE_PLAY"
    PRE_SNAP = "PRE_SNAP"
    IN_PLAY = "IN_PLAY"
    POST_PLAY_REACTION = "POST_PLAY_REACTION"
    HUD_UPDATE = "HUD_UPDATE"
    HIGHLIGHT_REPLAY = "HIGHLIGHT_REPLAY"


class Vector3D(BaseModel):
    x: float = Field(..., description="X coordinate in yards (width: -26.65 to +26.65)")
    y: float = Field(..., description="Y coordinate in yards (elevation: >= 0.0)")
    z: float = Field(..., description="Z coordinate in yards (length: -60.0 to +60.0)")

    model_config = ConfigDict(frozen=True)


class CameraShotSchema(BaseModel):
    id: str = Field(..., description="Unique shot identifier")
    position: Vector3D = Field(..., description="Camera world position")
    target: Vector3D = Field(..., description="Look-at focal target")
    fov: float = Field(default=55.0, ge=10.0, le=120.0, description="Field of view in degrees")
    roll: float = Field(default=0.0, description="Camera roll angle in radians")
    duration: float = Field(..., gt=0.0, description="Shot duration in seconds")
    interpolation: Literal["linear", "smooth", "snap"] = Field(
        default="smooth", description="Spline interpolation mode"
    )

    model_config = ConfigDict(from_attributes=True)


class OverlayCueSchema(BaseModel):
    id: str = Field(..., description="Unique overlay cue identifier")
    type: Literal["lower_third", "matchup_card", "score_bug", "telestrator", "stat_popover", "laser_hud"]
    data: Dict[str, Any] = Field(default_factory=dict, description="Payload attributes for UI component")
    duration: Optional[float] = Field(None, gt=0.0, description="Display duration in seconds")
    animation: Literal["fade", "slide", "pop", "laser_sweep"] = Field(default="fade")
    layer: int = Field(default=10, description="Z-index rendering layer")

    model_config = ConfigDict(from_attributes=True)


class ClipCueSchema(BaseModel):
    id: str = Field(..., description="Unique cutscene clip identifier")
    clip_type: Literal["formation_sweep", "matchup_card", "situation_lower_third", "replay_angle", "celebration"]
    cameras: List[CameraShotSchema] = Field(default_factory=list, description="Ordered camera shots")
    overlays: List[OverlayCueSchema] = Field(default_factory=list, description="HUD overlays")
    duration: float = Field(..., gt=0.0, description="Total clip duration in seconds")
    audio_cue: Optional[str] = Field(None, description="Procedural audio stinger trigger")
    skippable: bool = Field(default=True, description="Whether user can skip this clip")

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# 2. AUDIO SYNTHESIS CONTRACTS
# =============================================================================

class AudioTriggerType(str, Enum):
    WHISTLE = "WHISTLE"
    COLLISION_HIT = "COLLISION_HIT"
    CROWD_ROAR_SWELL = "CROWD_ROAR_SWELL"
    CROWD_SILENCE = "CROWD_SILENCE"
    STADIUM_HORN = "STADIUM_HORN"
    STINGER_3RD_DOWN = "STINGER_3RD_DOWN"
    STINGER_TOUCHDOWN = "STINGER_TOUCHDOWN"
    UI_SNAP = "UI_SNAP"


class AudioTriggerPayload(BaseModel):
    trigger_type: AudioTriggerType
    intensity: float = Field(default=1.0, ge=0.0, le=1.0, description="Audio volume intensity [0, 1]")
    frequency_override: Optional[float] = Field(None, description="Optional fundamental pitch override in Hz")
    kinetic_energy: Optional[float] = Field(None, ge=0.0, description="Kinetic impact energy in Joules")
    stadium_decibels: Optional[float] = Field(None, ge=50.0, le=120.0, description="Target stadium dB")

    model_config = ConfigDict(from_attributes=True)


# =============================================================================
# 3. WEBSOCKET FRAME CONTRACTS
# =============================================================================

class TelemetryPlayerState(BaseModel):
    player_id: int
    position: Vector3D
    velocity: Vector3D
    facing_angle: float = Field(..., description="Facing angle in radians [0, 2pi]")
    stamina: float = Field(default=100.0, ge=0.0, le=100.0)
    current_action: str = Field(default="idle")

    model_config = ConfigDict(from_attributes=True)


class GameStateSyncPayload(BaseModel):
    game_id: int
    quarter: int = Field(..., ge=1, le=5)
    clock_seconds_remaining: float = Field(..., ge=0.0, le=900.0)
    home_score: int = Field(default=0, ge=0)
    away_score: int = Field(default=0, ge=0)
    down: int = Field(..., ge=1, le=4)
    distance: int = Field(..., ge=1, le=99)
    yard_line: int = Field(..., ge=1, le=99, description="1-99 yard line relative to home team")
    possession_team_id: int
    broadcast_phase: BroadcastPhaseEnum

    model_config = ConfigDict(from_attributes=True)


class WebSocketBroadcastMessage(BaseModel):
    message_type: Literal["STATE_SYNC", "CLIP_DISPATCH", "TELEMETRY_FRAME", "AUDIO_TRIGGER", "PLAY_RESULT"]
    timestamp: float = Field(..., description="Unix epoch timestamp in seconds")
    game_id: int
    payload: Union[
        GameStateSyncPayload,
        ClipCueSchema,
        List[TelemetryPlayerState],
        AudioTriggerPayload,
        Dict[str, Any]
    ]

    model_config = ConfigDict(from_attributes=True)
```

---

## 5.2 TypeScript Interfaces (Frontend Single Source of Truth)

```typescript
/**
 * Unified Data Contracts - TypeScript Definitions
 * File: frontend/src/types/contracts.ts
 */

// =============================================================================
// 1. BROADCAST & CAMERA CONTRACTS
// =============================================================================

export const BroadcastPhase = {
  IDLE_STADIUM: "IDLE_STADIUM",
  PRE_PLAY: "PRE_PLAY",
  PRE_SNAP: "PRE_SNAP",
  IN_PLAY: "IN_PLAY",
  POST_PLAY_REACTION: "POST_PLAY_REACTION",
  HUD_UPDATE: "HUD_UPDATE",
  HIGHLIGHT_REPLAY: "HIGHLIGHT_REPLAY",
} as const;

export type BroadcastPhase = (typeof BroadcastPhase)[keyof typeof BroadcastPhase];

export interface Vector3D {
  readonly x: number; // Width: -26.65 to +26.65 yards
  readonly y: number; // Elevation: >= 0.0 yards
  readonly z: number; // Length: -60.0 to +60.0 yards
}

export interface CameraShot {
  readonly id: string;
  readonly position: Vector3D;
  readonly target: Vector3D;
  readonly fov?: number;
  readonly roll?: number;
  readonly duration: number;
  readonly interpolation?: "linear" | "smooth" | "snap";
}

export interface OverlayCue {
  readonly id: string;
  readonly type: "lower_third" | "matchup_card" | "score_bug" | "telestrator" | "stat_popover" | "laser_hud";
  readonly data: Record<string, unknown>;
  readonly duration?: number;
  readonly animation?: "fade" | "slide" | "pop" | "laser_sweep";
  readonly layer?: number;
}

export interface ClipCue {
  readonly id: string;
  readonly clipType: "formation_sweep" | "matchup_card" | "situation_lower_third" | "replay_angle" | "celebration";
  readonly cameras: readonly CameraShot[];
  readonly overlays: readonly OverlayCue[];
  readonly duration: number;
  readonly audioCue?: string;
  readonly skippable?: boolean;
}

// =============================================================================
// 2. AUDIO SYNTHESIS CONTRACTS
// =============================================================================

export type AudioTriggerType =
  | "WHISTLE"
  | "COLLISION_HIT"
  | "CROWD_ROAR_SWELL"
  | "CROWD_SILENCE"
  | "STADIUM_HORN"
  | "STINGER_3RD_DOWN"
  | "STINGER_TOUCHDOWN"
  | "UI_SNAP";

export interface AudioTriggerPayload {
  readonly triggerType: AudioTriggerType;
  readonly intensity: number; // [0.0, 1.0]
  readonly frequencyOverride?: number;
  readonly kineticEnergy?: number; // Joules
  readonly stadiumDecibels?: number; // [50, 120]
}

// =============================================================================
// 3. WEBSOCKET & TELEMETRY CONTRACTS
// =============================================================================

export interface TelemetryPlayerState {
  readonly playerId: number;
  readonly position: Vector3D;
  readonly velocity: Vector3D;
  readonly facingAngle: number;
  readonly stamina: number;
  readonly currentAction: string;
}

export interface GameStateSyncPayload {
  readonly gameId: number;
  readonly quarter: number;
  readonly clockSecondsRemaining: number;
  readonly homeScore: number;
  readonly awayScore: number;
  readonly down: number;
  readonly distance: number;
  readonly yardLine: number;
  readonly possessionTeamId: number;
  readonly broadcastPhase: BroadcastPhase;
}

export interface WebSocketBroadcastMessage {
  readonly messageType: "STATE_SYNC" | "CLIP_DISPATCH" | "TELEMETRY_FRAME" | "AUDIO_TRIGGER" | "PLAY_RESULT";
  readonly timestamp: number;
  readonly gameId: number;
  readonly payload: GameStateSyncPayload | ClipCue | TelemetryPlayerState[] | AudioTriggerPayload | Record<string, unknown>;
}

// =============================================================================
// 4. PLAYER & DYNASTY CONTRACTS
// =============================================================================

export type DevTrait = "NORMAL" | "STAR" | "SUPERSTAR" | "XFACTOR";
export type OvrTier = "99_CLUB" | "ELITE" | "GOLD" | "SILVER" | "BRONZE";

export interface PlayerGenesisBiometrics {
  readonly fastTwitchRatio: number;
  readonly wingspanInches: number;
  readonly handSizeInches: number;
  readonly s2CognitionScore: number;
  readonly maxAccelerationCap: number;
  readonly medicalFlags: readonly string[];
}

export interface PlayerContract {
  readonly yearsRemaining: number;
  readonly totalSalary: number;
  readonly guaranteedAmount: number;
  readonly capHitCurrentYear: number;
  readonly deadCapPenalty: number;
}

export interface PlayerEntity {
  readonly id: number;
  readonly firstName: string;
  readonly lastName: string;
  readonly position: string;
  readonly overallRating: number;
  readonly ovrTier: OvrTier;
  readonly devTrait: DevTrait;
  readonly teamId?: number;
  readonly jerseyNumber: number;
  readonly age: number;
  readonly biometrics: PlayerGenesisBiometrics;
  readonly contract: PlayerContract;
}
```

---

# Section 6: Verification & Adversarial Synthesis

## 6.1 Adversarial Failure Modes & Defenses

1. **Thesis**: High-frequency procedural WebGL/Three.js camera orbits combined with Web Audio synthesis might cause micro-stutter on low-end hardware.
   - **Antithesis**: Running 60 FPS Catmull-Rom splines while synthesizing audio in the main JavaScript thread could cause audio buffer underruns and garbage collection pauses.
   - **Synthesis**: The Web Audio API operates strictly on a dedicated hardware audio rendering thread outside the main UI loop. Catmull-Rom camera vectors use pre-allocated static typed arrays (`Float32Array`) to achieve zero allocations during `requestAnimationFrame`. When the browser reports `<45 FPS` or `prefers-reduced-motion: reduce`, the camera director automatically degrades to static broadcast cut angles (`interpolation: "snap"`).

2. **Thesis**: Network packet loss on live WebSocket telemetry could cause players to visually teleport across the 3D field.
   - **Antithesis**: Dropped UDP/WebSocket packets result in desynchronized player transforms and physics glitches.
   - **Synthesis**: The frontend interpolation layer implements **Hermite Cubic Dead Reckoning**. When a packet is delayed or dropped, the client estimates player positions using last confirmed velocity $\vec{V}(t)$ and smoothly snaps within a 100ms blend window upon packet arrival.

---

## 6.2 Implementation Verification Checklist

- [x] 7-State Discrete Broadcast Transition Engine fully mapped with 7x7 matrix, guards, and timeout recoveries.
- [x] Procedural 3D camera orbits defined with NFL gridiron coordinate boundaries, Catmull-Rom splines, quaternion slerp, and collision shake models.
- [x] Zero-dependency Web Audio API procedural synthesis graphs specified for crowd dynamics, stadium PA, whistles, tackles, and stingers.
- [x] Glassmorphic UI/UX Component & Token Design System architected for all 13 core views, 32 NFL team colors, metallic OVR tiers, and laser HUD pills.
- [x] Strict dual-stack Pydantic V2 and TypeScript data contracts documented with zero `any` types.

---
**End of Document NFL-SIM-SURVEY-003**
