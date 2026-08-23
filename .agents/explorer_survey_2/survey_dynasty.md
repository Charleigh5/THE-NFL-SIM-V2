# Architectural Specification & Technical Blueprint: Dynasty RPG Progression & Front Office Empire Economics (Pillar 2)

**Document ID:** NFL-SIM-P2-DYNASTY-001  
**Status:** ARCHITECTURAL_BLUEPRINT  
**Author:** Explorer 2 (Dynasty & Economics Systems Analyst)  
**System Milestone:** Pillar 2 / Phase 5 & Phase 11 Unification  
**Target Domain:** Dynasty RPG, Franchise Progression, Capology Mathematics, Medical Triage, and Emergent Narrative DAGs  

---

## 1. Executive Summary & Problem Exposition

Modern franchise simulation games face a persistent trade-off between superficial RPG mechanics (rigid stat meters, uncalibrated progression, linear aging) and brittle front-office balance (exploitable trade AI, simplistic salary caps, repetitive linear storylines). 

The goal of **Pillar 2: Dynasty RPG Progression & Front Office Empire Economics** in *The Digital Gridiron* is to deliver a mathematically rigorous, deterministic, and emergent simulation ecosystem. This architecture models:
1. **Dynamic Developmental Traits & Zone Abilities**: Tiered XP multipliers, milestone evolutions, and age/injury devolution vectors with strict league-wide rarity caps.
2. **Bifurcated Age Curves**: Distinct physical decay vs. mental preservation curves tailored across 8 positional groupings.
3. **Surplus-Value Trade Valuation**: Multi-chart draft pick valuation (Jimmy Johnson, Rich Hill, Fitzgerald-Spielberger) married with salary surplus value theory and situational GM archetype logic.
4. **CBA-Compliant Capology**: Precise multi-year proration, dead money acceleration, simple restructures ("kick the can"), post-June 1 splits, void year amortizations, and the 89% four-year cash spending floor.
5. **Multi-Vector Medical Triage**: Anatomical health maps, fatigue risk compounding, injection/brace risk-reward trade-offs, and probabilistic escalation dynamics.
6. **Directed Acyclic Graph (DAG) Narrative Engine**: Non-linear, context-driven storylines with multi-week branching state mutations across player morale, locker room chemistry, coaching trust, and owner pressure.

---

## 2. Dynamic Player Developmental Traits & Ability Matrix

### 2.1 Trait Tiers & Progression Mechanics

Player development operates on four canonical tiers, establishing distinct progression trajectories and ability capacity:

| Trait Tier | League Distribution | Weekly XP Multiplier | Ability Slots (Passive / Active) | Breakout Game Probability | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NORMAL** | ~65.0% | $1.00\times$ | 0 Passive / 0 Active | $2.0\%$ per game | Baseline NFL player. Steady progression based on playtime and practice. |
| **STAR** | ~22.0% | $1.25\times$ | 1 Passive / 0 Active | $6.0\%$ per game | Quality starter / high-upside young player. Faster developmental curve. |
| **SUPERSTAR** | ~10.0% | $1.50\times$ | 2 Passive / 1 Active | $12.0\%$ per game | Pro Bowl caliber talent. Unlocks specialized passive traits and high-tier perks. |
| **X-FACTOR** | ~3.0% (Soft Cap: 45-55) | $2.00\times$ | 3 Passive / 1 "Zone" Ability | $20.0\%$ per game | Franchise cornerstone. Features signature "In The Zone" game-day state triggers. |

```
                                  [ DRAFT / ROOKIE GEN ]
                                             │
                       ┌─────────────────────┼─────────────────────┐
                       ▼                     ▼                     ▼
                 NORMAL (65%)            STAR (22%)         SUPERSTAR (10%)
                  [1.0x XP]              [1.25x XP]            [1.5x XP]
                       │                     │                     │
                       │ (Pro Bowl / Top 15) │ (All-Pro / Top 5)   │ (MVP / OPOY / DPOY)
                       ▼                     ▼                     ▼
                  STAR (22%)           SUPERSTAR (10%)       X-FACTOR (3%)
                       │                     │               [Zone Ability]
                       │                     │                     │
                       └─────────────────────┴─────────────────────┘
                                             │
                             [ DEVOLUTION TRIGGERS ]
                                             │
                        ┌────────────────────┼────────────────────┐
                        ▼                    ▼                    ▼
                 Grade 3 Injury      Post-Age-30 Decay     Prolonged Bench
                 (-1 Tier Roll)       (Sub-Starter DVOA)   (<20% Snap Share)
```

### 2.2 In-The-Zone Mechanics (X-Factor Activation)

X-Factor players possess a game-day state machine called the **Zone Engine**. When a player meets an on-field statistical criterion, they enter the **ZONE_ACTIVE** state, boosting specific ratings until a knockout condition occurs.

```
       [ ZONE_INACTIVE ] ──( 3 Cons. 20+ Yd Passes / 2 Sacks )──► [ ZONE_ACTIVE ]
              ▲                                                           │
              │                                                           │
              └────────( Sack Taken / Interception / TFL )────────────────┘
```

#### Zone Activation & Knockout Matrix
| Position Group | Zone Ability Name | Activation Criterion (In-Game) | Knockout Condition | Zone Effect |
| :--- | :--- | :--- | :--- | :--- |
| **QB (Field General)** | *Blitz Radar* | 3 consecutive completions of 15+ air yards | 1 Sack taken or Interception | Highlights unblocked pass rushers pre-snap; +15 Awareness |
| **QB (Gunslinger)** | *Bazooka* | 2 completions of 40+ air yards | 1 Interception thrown | Maximum throw distance increased +15 yards; +10 Throw Velocity |
| **RB (Power)** | *Wrecking Ball* | 3 broken tackles in a single half | 1 Tackle for Loss | 85% success rate on first truck/stiff arm move per play |
| **RB (Elusive)** | *First One Free* | 3 rushes of 10+ yards | 1 Tackle for Loss | First spin or juke move is guaranteed broken tackle |
| **WR/TE** | *Double Me* | 2 contested catches of 20+ yards | 1 Dropped pass or Incompletion | Wins 90% of 1-on-1 contested aggressive catches in single coverage |
| **EDGE / DE** | *Unstoppable Force* | 2 sacks or 3 QB hits in a game | 2 consecutive run plays to opposite side | First pass rush move against single blocking wins instantly |
| **DT / Run Stuffer** | *Brick Wall* | 2 Tackles for Loss on run plays | Offense completes 3 consecutive passes | Offense cannot pancake or double-team move; sheds blocks 2x faster |
| **CB / S** | *Shutdown* | 2 pass breakups or 1 Interception | Gives up reception of 25+ yards | Tightens man coverage window by 40%; +20% Interception catch rate |

### 2.3 Comprehensive Ability Catalog & Unlock Matrices

Abilities are purchased via accumulated player XP ($XP_{\text{invest}}$) and require meeting positional, level, and attribute thresholds:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ABILITY UNLOCK PIPELINE                            │
│                                                                             │
│  [ Player Level >= L_min ] ──► [ Attribute >= Attr_min ] ──► [ Spend XP ]   │
│               │                                                   │         │
│               ▼                                                   ▼         │
│         Position Check                                     Slot Check       │
│      (Eligible Positions)                              (Max Slots Per Tier) │
└─────────────────────────────────────────────────────────────────────────────┘
```

```json
{
  "ability_catalog": [
    {
      "key": "pre_snap_diagnostician",
      "name": "Pre-Snap Diagnostician",
      "tier": "GOLD",
      "category": "MENTAL",
      "positions": ["QB"],
      "level_req": 10,
      "xp_cost": 5000,
      "attr_reqs": {"awareness": 88},
      "effects": {
        "coverage_reveal_probability": 0.85,
        "audible_latency_reduction_sec": 2.0,
        "disguise_penetration_bonus": 12.0
      }
    },
    {
      "key": "anchor_master",
      "name": "Anchor Master",
      "tier": "GOLD",
      "category": "PHYSICAL_TECHNIQUE",
      "positions": ["OT", "OG", "C"],
      "level_req": 8,
      "xp_cost": 4000,
      "attr_reqs": {"strength": 86, "pass_block": 84},
      "effects": {
        "bull_rush_resistance": 0.45,
        "pocket_integrity_retention": 0.30,
        "pancake_immunity": 1.0
      }
    },
    {
      "key": "island_enforcer",
      "name": "Island Enforcer",
      "tier": "ELITE",
      "category": "COVERAGE",
      "positions": ["CB"],
      "level_req": 14,
      "xp_cost": 7500,
      "attr_reqs": {"man_coverage": 90, "speed": 92},
      "effects": {
        "press_win_rate_delta": 0.25,
        "receiver_separation_suppression": 0.35,
        "reaction_lag_reduction_ms": 65.0
      }
    },
    {
      "key": "route_technician_pro",
      "name": "Route Technician Pro",
      "tier": "GOLD",
      "category": "RECEIVING",
      "positions": ["WR", "TE"],
      "level_req": 9,
      "xp_cost": 4500,
      "attr_reqs": {"route_running": 88, "agility": 86},
      "effects": {
        "cut_break_separation_bonus_yards": 0.75,
        "option_route_read_accuracy": 0.95,
        "press_escape_speed_mult": 1.20
      }
    },
    {
      "key": "trench_commander",
      "name": "Trench Commander",
      "tier": "SILVER",
      "category": "LEADERSHIP",
      "positions": ["C", "MLB"],
      "level_req": 6,
      "xp_cost": 3000,
      "attr_reqs": {"awareness": 82},
      "effects": {
        "unit_awareness_boost": 4.0,
        "blown_assignment_reduction": 0.20,
        "stunt_recognition_bonus": 0.25
      }
    }
  ]
}
```

### 2.4 Performance-Based Evolution & Devolution Algorithms

At the end of each season (or dynamically via mid-season Breakout Events), players are evaluated for developmental tier modification.

#### Evolution Scoring Function
For player $i$ at position $p$:
$$E_i = w_{\text{prod}} \cdot \text{Z-Score}(\text{EPA}_i) + w_{\text{vol}} \cdot \left(\frac{\text{Snaps}_i}{\text{TeamSnaps}}\right) + A_{\text{awards}} + M_{\text{milestone}}$$

Where:
- $A_{\text{awards}} = +4.0$ for MVP/OPOY/DPOY; $+2.5$ for 1st Team All-Pro; $+1.5$ for Pro Bowl.
- $M_{\text{milestone}} = +1.0$ for statistical thresholds (e.g., 4,000 pass yds, 1,200 rush yds, 12 sacks, 6 INTs).

$$\text{Tier Upgrade Rule}: \begin{cases} 
\text{NORMAL} \to \text{STAR} & \text{if } E_i \ge 2.50 \text{ or Top 15 at position} \\
\text{STAR} \to \text{SUPERSTAR} & \text{if } E_i \ge 4.50 \text{ or Pro Bowl selection} \\
\text{SUPERSTAR} \to \text{X-FACTOR} & \text{if } E_i \ge 6.50 \text{ or 1st Team All-Pro / MVP}
\end{cases}$$

#### Devolution & Regression Triggers
Devolution rolls are executed during offseason processing:
1. **Catastrophic Injury Trigger**:
   $$P(\text{Devolve}_{\text{injury}}) = 0.35 + 0.05 \times \max(0, \text{Age} - 27) + 0.10 \times (\text{Severity} - 7)$$
2. **Sub-Starter Performance Decay**:
   If a Star/Superstar plays $< 20\%$ of snaps (and was healthy) or generates an EPA in the bottom 25th percentile of the position for two consecutive seasons:
   $$\text{Tier}_{t+1} = \max(\text{NORMAL}, \text{Tier}_t - 1)$$
3. **X-Factor Soft Cap Pruning**:
   If total league X-Factors exceed $55$, the lowest-rated X-Factors who failed to achieve Pro Bowl honors in season $t$ are devolved to Superstar until the count is $\le 50$.

---

## 3. Mathematical Age Curve Progression & Regression Models

### 3.1 Positional Window Parameterization

Athletic careers follow non-linear trajectories where physical capabilities decay as power functions while mental attributes accumulate logarithmically.

```
Rating
  100 ┌───────────────────────────────────────────────────────────┐
      │                   Mental/Awareness Curve                  │
   90 │              /────────────────────────────\               │
      │    Physical /                              \              │
   80 │    Curve   /                                \             │
      │           /                                  \            │
   70 │          /                                    \ Physical  │
      │         /                                      \ Decay    │
   60 │        /                                        \         │
      │       /                                          \        │
   50 └──────┴───────┴───────┴───────┴───────┴───────┴────┴───────┘
     Age:   21      24      27      30      33      36   39
```

#### Master Positional Age Matrix
| Pos Group | Athletic Peak Start | Athletic Peak End | Physical Decay Coeff ($\alpha$) | Mental Peak Start | Mental Decay Start | Hard Retirement Age |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **QB** | 25 | 30 | 0.015 | 29 | 37 | 42 |
| **RB** | 22 | 26 | 0.065 | 24 | 28 | 32 |
| **WR** | 24 | 28 | 0.040 | 27 | 32 | 35 |
| **TE** | 25 | 29 | 0.035 | 27 | 33 | 36 |
| **OT** | 26 | 31 | 0.028 | 28 | 34 | 38 |
| **OG/C** | 26 | 31 | 0.025 | 28 | 35 | 38 |
| **EDGE** | 24 | 28 | 0.045 | 27 | 32 | 35 |
| **DT** | 25 | 29 | 0.035 | 27 | 33 | 36 |
| **LB** | 24 | 28 | 0.042 | 26 | 32 | 34 |
| **CB** | 23 | 27 | 0.055 | 26 | 30 | 33 |
| **S** | 24 | 29 | 0.038 | 27 | 33 | 35 |
| **K/P** | 27 | 36 | 0.010 | 28 | 40 | 45 |

### 3.2 Continuous Mathematical Models

#### 3.2.1 Physical Attribute Decay Function
For any physical attribute $P_k \in \{\text{Speed}, \text{Acceleration}, \text{Agility}, \text{Throw Power}, \text{Jump}\}$ at age $t$:

$$P_k(t) = P_k(\text{peak}) \cdot \Phi_{\text{phys}}(t, \text{pos}) \cdot \Omega_{\text{injury}}$$

$$\Phi_{\text{phys}}(t, \text{pos}) = \begin{cases}
1.0 - \beta_{\text{grow}} \cdot \left(\frac{t_{\text{peak\_start}} - t}{t_{\text{peak\_start}} - 20}\right)^{1.2} & \text{if } t < t_{\text{peak\_start}} \\
1.0 & \text{if } t_{\text{peak\_start}} \le t \le t_{\text{peak\_end}} \\
1.0 - \alpha_{\text{pos}} \cdot (t - t_{\text{peak\_end}})^{1.45} & \text{if } t > t_{\text{peak\_end}}
\end{cases}$$

Where:
- $\beta_{\text{grow}} \approx 0.08$ (Young development gap).
- $\alpha_{\text{pos}}$ is the positional physical decay coefficient from Section 3.1.
- $\Omega_{\text{injury}} = \prod_{j} (1.0 - \delta_{\text{perm}, j})$ represents cumulative permanent injury degradation.

#### 3.2.2 Mental & Technical Attribute Evolution Function
For any cognitive/technical attribute $M_j \in \{\text{Awareness}, \text{Play Recognition}, \text{Pass Block}, \text{Route Running}, \text{Throw Accuracy}\}$:

$$M_j(t) = \min\left(99, M_{j,\text{init}} + \Delta M_{\text{exp}}(t)\right) \cdot \Psi_{\text{senile}}(t, \text{pos})$$

$$\Delta M_{\text{exp}}(t) = K_{\text{pos}} \cdot \ln\left(1 + \frac{\text{CareerSnaps}(t)}{800}\right) \cdot \mu_{\text{dev\_trait}}$$

$$\Psi_{\text{senile}}(t, \text{pos}) = \begin{cases}
1.0 & \text{if } t \le t_{\text{mental\_decay}} \\
1.0 - 0.020 \cdot (t - t_{\text{mental\_decay}})^2 & \text{if } t > t_{\text{mental\_decay}}
\end{cases}$$

#### 3.2.3 Deterministic Position Composite (OVR)
The composite overall rating is computed via non-linear weighted sum:
$$\text{OVR}(t) = \sum_{k} w_k(\text{pos}) \cdot P_k(t) + \sum_{j} w_j(\text{pos}) \cdot M_j(t)$$

*Key Behavioral Consequence:* A 35-year-old pocket QB whose Speed decays from $84 \to 68$ maintains a $90+$ OVR because Throw Accuracy Deep ($92$), Awareness ($98$), and Pre-Snap Read ($96$) offset the athletic decay. Conversely, a 30-year-old running back experiences catastrophic OVR reduction ($91 \to 78$) due to heavy weighting on Speed and Acceleration.

---

## 4. Trade Equity Evaluation Algorithms & Surplus Value Theory

### 4.1 Unified Draft Capital Multi-Chart Model

Draft pick valuations blend traditional historical charts with empirical surplus value curves:

```
Value (Pts)
 3500 ┌───────────────────────────────────────────────────────────┐
 3000 │* Jimmy Johnson Chart (Aggressive Top 5 Curve)             │
 2500 │ \                                                         │
 2000 │  \   - - - Fitzgerald-Spielberger Surplus Value           │
 1500 │   \                                                       │
 1000 │    \___                                                   │
  500 │        \_______                                           │
    0 └────┴───────┴───────┴───────┴───────┴───────┴───────┴──────┘
 Pick:     1      32      64      96     128     160     192    224
```

#### Pick Valuation Formula
For overall pick $p \in [1, 260]$:
$$V_{\text{pick}}(p) = \left[ w_{\text{JJ}} \cdot V_{\text{JJ}}(p) + w_{\text{RH}} \cdot V_{\text{RichHill}}(p) + w_{\text{FS}} \cdot V_{\text{OTC}}(p) \right] \cdot \tau_{\text{top10}}(p)$$

Where:
- $V_{\text{JJ}}(p) = 3000 \cdot e^{-0.015 \cdot (p - 1)}$ (Calibrated to classical Jimmy Johnson chart).
- $V_{\text{RichHill}}(p) = 1000 \cdot p^{-0.65}$ (Modern Rich Hill points chart).
- $V_{\text{OTC}}(p) = \text{SurplusWAR}(p) \times \$8.5\text{M}$ (Fitzgerald-Spielberger empirical draft curve).
- Weights: $w_{\text{JJ}} = 0.30, w_{\text{RH}} = 0.40, w_{\text{FS}} = 0.30$.
- Top-10 Premium: $\tau_{\text{top10}}(p) = 1.20$ if $p \le 10$, else $1.00$.

#### Future Pick Discounting
Future draft picks are discounted by a compound time preference rate $d = 0.18$ plus a uncertainty penalty:
$$V_{\text{future}}(r, \Delta y) = V_{\text{pick}}\left(\text{MidRoundPick}(r)\right) \cdot (1 - d)^{\Delta y}$$
*Rule:* Picks beyond $\Delta y = 3$ years are strictly illegal per NFL Constitution.

### 4.2 Surplus Value Theory for Player Contracts

A player's true trade equity is not merely their Overall rating, but the **Contract Surplus Value ($S_i$)**: the economic differential between on-field production and cash cost.

$$S_i = \sum_{t=1}^{Y_{\text{rem}}} \frac{\text{OnFieldMarketValue}(OVR_i, \text{Pos}_i, t) - \text{CashObligation}_i(t)}{(1 + \rho)^{t-1}}$$

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            SURPLUS VALUE SPECTRUM                            │
│                                                                              │
│  [ ROOKIE SCALE SUPERSTAR ] ──► Huge Positive Surplus (+30M/yr) ──► Massive  │
│  (e.g., C.J. Stroud Year 2)                                         Trade Pts│
│                                                                              │
│  [ FAIR MARKET VETERAN ]   ──► Neutral Surplus (0M/yr)          ──► Modest   │
│  (e.g., Top-Paid LT)                                                Trade Pts│
│                                                                              │
│  [ ALBATROSS VETERAN ]     ──► Negative Surplus (-15M/yr)       ──► Requires │
│  (e.g., Aging 76 OVR Safety)                                        "Sweetener│
└──────────────────────────────────────────────────────────────────────────────┘
```

#### Surplus Value Calculation Parameters
1. **On-Field Production Value ($V_{\text{prod}}$)**:
   $$V_{\text{prod}}(OVR, \text{pos}) = \text{TopPosAAV}(\text{pos}) \times \left(\frac{\max(60, OVR) - 60}{39}\right)^{2.4}$$
2. **Contract Cash Cost ($C_{\text{cash}}$)**:
   $$C_{\text{cash}}(t) = \text{BaseSalary}_t + \text{RosterBonus}_t + \text{WorkoutBonus}_t$$
   *(Note: Prorated signing bonus already paid is a sunk cost for trading team, creating immense dead cap for the seller but free asset value for the buyer).*

### 4.3 Total Trade Package Valuation & Situational Multipliers

For a trade offer between Team A and Team B:
$$\text{PackageValue} = \sum_{p \in \text{Players}} V_{\text{player}}(p) + \sum_{k \in \text{Picks}} \left(\frac{V_{\text{pick}}(k)}{30.0}\right)$$

$$V_{\text{player}}(p) = \left[ \frac{(OVR - 50)^{1.65}}{2.0} \right] \cdot \text{PosMult} \cdot \text{AgeMult} \cdot \text{SurplusMult}(S_p) \cdot \text{FlightRiskMult}$$

#### Situational Multiplier Matrix
| Team Strategic Posture | Record / Outlook | Veteran Star Multiplier ($OVR \ge 85$) | Young Prospect Multiplier ($\le 24$) | Draft Pick Valuation Multiplier | Salary Dump Absorption Appetite |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CONTENDER (Win-Now)** | $W \ge 0.65$ | $1.35\times$ | $0.85\times$ | $0.80\times$ | None (Cap strapped) |
| **BALANCED** | $0.40 \le W < 0.65$ | $1.00\times$ | $1.00\times$ | $1.00\times$ | Neutral |
| **REBUILDER** | $W < 0.40$ | $0.65\times$ | $1.40\times$ | $1.45\times$ | High (Takes bad contracts for Day 2 picks) |
| **QB_PANIC (Bradford Rule)** | Starter QB on IR | $2.00\times$ (on starting caliber QBs) | $1.10\times$ | $0.70\times$ | Desperate |

---

## 5. Salary Cap Optimization Models & CBA Accounting Mechanics

### 5.1 Cap Growth & Baseline Thresholds

Per the real-world financial threshold analysis (1994–2025 data table), the NFL Salary Cap expands with a historical Compound Annual Growth Rate (CAGR) of **6.97%**:

$$\text{SalaryCap}(Y) = \text{SalaryCap}(2025) \cdot (1 + 0.0697)^{Y - 2025}, \quad \text{where } \text{SalaryCap}(2025) = \$279,200,000$$

### 5.2 Bonus Proration & Multi-Year Ledger

Signing bonuses and guaranteed option bonuses are amortized evenly over the lesser of the contract length or **5 years**:

$$\text{AnnualProration}(t) = \frac{B_{\text{signing}}}{\min(L_{\text{contract}}, 5)}$$

```
Example: $50M Signing Bonus on a 5-Year Contract ($279.2M Cap)
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│    Year 1    │    Year 2    │    Year 3    │    Year 4    │    Year 5    │
├──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ $10.0M Pror. │ $10.0M Pror. │ $10.0M Pror. │ $10.0M Pror. │ $10.0M Pror. │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

### 5.3 Dead Cap Acceleration Mathematics

When a player is terminated or traded prior to contract expiration, unamortized bonus proration accelerates immediately:

```
Contract Timeline (Cut After Year 2):
Year 1 (Paid)     Year 2 (Paid)     Year 3 (Unamortized) Year 4 (Unamortized) Year 5 (Unamortized)
[$10M Proration]  [$10M Proration]  [$10M Proration]     [$10M Proration]     [$10M Proration]
                                    └─────────────────────────┬────────────────────────┘
                                                              │
                                            ACCELERATES INTO DEAD MONEY ($30M)
```

#### Pre-June 1 Cut / Trade Formula
All remaining unamortized prorations accelerate into the current league year $T$:
$$\text{DeadCap}_T = \sum_{t=T}^{L} \text{Proration}_t + \text{GuaranteedBaseSalary}_T$$
$$\text{ImmediateCapSavings}_T = \text{CapHit}_T - \text{DeadCap}_T$$

#### Post-June 1 Designation Formula (Max 2 Per Team / League Year)
Splits the dead cap penalty across two fiscal league years:
$$\text{DeadCap}_T = \text{Proration}_T + \text{GuaranteedBaseSalary}_T$$
$$\text{DeadCap}_{T+1} = \sum_{t=T+1}^{L} \text{Proration}_t$$
*Financial Timing:* The cap space relief does not credit to the team's ledger until **June 2nd at 12:01 AM EST**.

### 5.4 Contract Restructuring Formulas ("Kick the Can")

A Simple Restructure converts base salary into a signing bonus to create immediate relief while inflating future year commitments:

```
BEFORE RESTRUCTURE (Year 1 of 4 Remaining):
Year 1 Base: $25.0M | Proration: $5.0M ──► Cap Hit = $30.0M

EXECUTE RESTRUCTURE:
Convert $23.8M of Base Salary to Signing Bonus (Leave $1.2M Vet Min)
Prorate $23.8M over 4 years = $5.95M / year

AFTER RESTRUCTURE:
Year 1: Base ($1.2M)  + Old Pror ($5.0M) + New Pror ($5.95M) = $12.15M (SAVINGS: +$17.85M)
Year 2: Base ($25.0M) + Old Pror ($5.0M) + New Pror ($5.95M) = $35.95M (INFLATION: +$5.95M)
Year 3: Base ($25.0M) + Old Pror ($5.0M) + New Pror ($5.95M) = $35.95M (INFLATION: +$5.95M)
Year 4: Base ($25.0M) + Old Pror ($5.0M) + New Pror ($5.95M) = $35.95M (INFLATION: +$5.95M)
```

#### Restructure Equation
$$\Delta \text{CapSpace}_T = (S_{\text{base}, T} - S_{\text{vet\_min}}) \cdot \left(1 - \frac{1}{\min(Y_{\text{rem}}, 5)}\right)$$
$$\text{FutureCapHitIncrease}_t = \frac{S_{\text{base}, T} - S_{\text{vet\_min}}}{\min(Y_{\text{rem}}, 5)}, \quad \forall t \in [T+1, T + \min(Y_{\text{rem}}, 5) - 1]$$

### 5.5 Void Year Amortization Mechanics

Teams append dummy years ("void years") to stretch signing bonus amortization across the full 5-year CBA limit.
- **Contract Reality:** 2-year active playing commitment with 3 void years.
- **Amortization:** Bonus divided by 5.
- **Void Acceleration Trigger:** On the final day of League Year 2, the contract automatically voids, triggering an instant acceleration of all 3 remaining prorations into Year 3 dead money.

### 5.6 Rollover Cap & 89% Cash Floor Accounting

#### Rollover Equation
Teams may carry over $100\%$ of unused adjusted cap space from Year $T-1$ to Year $T$:
$$\text{EffectiveCap}_{i, T} = \text{BaseCap}_T + \text{Rollover}_{i, T-1} + \text{AdjustmentCredits}$$

#### CBA 4-Year Cash Spending Floor Rule
Teams must spend at least $89.0\%$ of cumulative base salary caps in actual cash over rolling 4-year windows:
$$\sum_{t=1}^{4} \text{CashSpent}_{i, t} \ge 0.89 \times \sum_{t=1}^{4} \text{BaseCap}_t$$
*Enforcement:* If $\text{Shortfall} > 0$, the league assesses an automatic penalty and distributes the cash deficit directly to players on the roster during that cycle.

---

## 6. Medical Injury Triage Protocols & Risk-Reward Mechanics

### 6.1 Anatomical Body Part Vulnerability Matrix

The simulation tracks integrity across 8 discrete anatomical regions:

```
                      [ 1. HEAD / CONCUSSION ]
                                 │
                      [ 2. NECK / C-SPINE ]
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
  [ 3. SHOULDER/ARM ]     [ 4. TORSO/RIBS ]      [ 3. SHOULDER/ARM ]
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                   ┌─────────────┴─────────────┐
                   ▼                           ▼
          [ 5. KNEE (ACL/MCL) ]       [ 5. KNEE (ACL/MCL) ]
                   │                           │
          [ 6. HAMSTRING/GROIN ]      [ 6. HAMSTRING/GROIN ]
                   │                           │
          [ 7. ANKLE (HIGH/LOW) ]     [ 7. ANKLE (HIGH/LOW) ]
                   │                           │
          [ 8. ACHILLES TENDON ]      [ 8. ACHILLES TENDON ]
```

#### Vulnerability & Impairment Parameters
| Body Region | Vulnerable Positions | Typical Diagnoses | Base Snap Risk ($\kappa_{\text{body}}$) | Severity Range | Attribute Impairment Profile |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Head** | RB, LB, S, CB | Concussion, Micro-trauma | $0.00035$ | 2 – 6 | $-20$ Awareness, $-15$ Play Recognition |
| **Neck / C-Spine** | DT, DE, OT, OG | Stinger, Nerve Compression | $0.00015$ | 3 – 8 | $-15$ Strength, $-10$ Tackle |
| **Shoulder / Arm** | QB, DE, WR | Labrum Tear, Rotator Cuff, AC Joint | $0.00045$ | 2 – 8 | $-20$ Throw Power, $-15$ Pass Rush Power |
| **Torso / Ribs** | QB, RB, WR | Fractured Ribs, Oblique Strain | $0.00030$ | 1 – 5 | $-10$ Throw Acc Deep, $-10$ Break Tackle |
| **Knee** | ALL (High: RB, WR, CB) | ACL Tear, MCL Sprain, Meniscus | $0.00055$ | 3 – 10 | $-25$ Speed, $-30$ Agility, $-20$ Acceleration |
| **Hamstring / Groin**| WR, CB, RB | Muscle Strain, Avulsion Tear | $0.00060$ | 1 – 6 | $-18$ Speed, $-15$ Acceleration |
| **Ankle** | OL, DL, RB, WR | High Ankle Sprain, Inversion Sprain | $0.00050$ | 1 – 7 | $-12$ Agility, $-15$ Run Block / Pass Rush |
| **Achilles Tendon** | RB, EDGE, CB | Rupture, Tendinitis | $0.00018$ | 6 – 10 | $-35$ Speed, $-35$ Acceleration (Season Ending) |

### 6.2 Per-Play Injury Probability Formula

For player $i$ participating in snap $s$:
$$P(\text{Injury}_{i, s}) = P_{\text{base}} \cdot \mu_{\text{play}} \cdot \mu_{\text{pos}} \cdot \mu_{\text{age}} \cdot \mu_{\text{dur}} \cdot \mu_{\text{fatigue}}(f) \cdot \mu_{\text{staff}} \cdot \mu_{\text{wear}}$$

Where:
- $P_{\text{base}} = 0.0015$ (Calibrated for ~1.5 injuries per 150 team snaps).
- $\mu_{\text{play}}$: SACK ($1.50$), HIP_DROP ($20.0$), SCRAMBLE ($1.20$), STANDARD ($1.00$).
- $\mu_{\text{fatigue}}(f) = 1.0 + \max\left(0, \frac{f - 50}{50}\right) \times 0.65$.
- Short Week Penalty (Thursday Night): $\mu_{\text{wear}} = 1.25$.
- High Touchload Penalty (RB touches $> 25$ in game): $+30\%$ soft-tissue risk.

### 6.3 Playing Through Injury & Escalation Dynamics

```
                           [ INJURY OCCURS ]
                                   │
              ┌────────────────────┴────────────────────┐
              ▼                                         ▼
      Severity <= 7                             Severity >= 8
    (Minor/Moderate)                              (Severe)
              │                                         │
     Toughness Check                               [ Mandatory ]
   (T >= Threshold OR Ragknow)                     [ IR Placed ]
              │
    ┌─────────┴─────────┐
    ▼                   ▼
 [ BENCH / REST ]   [ PLAY THROUGH ]
 (Normal Recovery)      │
                        ├──────────────────────────────────────┐
                        ▼                                      ▼
               [ STANDARD PLAY ]                     [ MEDICAL INTERVENTION ]
               - Base Penalty Applied                 - Toradol (0% Penalty)
               - 2% Escalation Risk/Snap              - 5% Escalation Risk/Snap
```

#### Playing-Through Escalation Function
When an injured player is active on field:
$$P(\text{Escalate}) = 0.020 \cdot \text{Severity} \cdot \left(1 - 0.30 \frac{\text{Toughness}}{100}\right) \cdot \mu_{\text{intervention}}$$

$$\text{If Escalate} \implies \text{NewSeverity} = \min(10, \text{Severity} + \text{UniformRandom}(1, 2))$$

#### Medical Intervention Trade-Off Engine
1. **Toradol / Cortisone Injection**:
   - *Advantage:* Suppresses $100\%$ of on-field attribute penalties for 4 quarters.
   - *Risk:* $\mu_{\text{intervention}} = 2.50\times$; $+15\%$ chance of transforming a Grade 2 sprain into a Grade 3 full ligament tear.
2. **Orthopedic Brace / Heavy Taping**:
   - *Advantage:* Reduces re-injury and escalation probability by $40\%$ ($\mu_{\text{intervention}} = 0.60$).
   - *Penalty:* Fixed physical penalty of $-3$ Speed and $-4$ Agility while equipped.
3. **Surgical vs. Conservative Rehab Pathway**:
   - *Surgical:* Adds $+4$ weeks to recovery time, but resets reinjury recurrence risk to baseline ($< 2.0\%$).
   - *Conservative:* Returns player $3$ weeks earlier, but leaves a persistent recurrence risk floor of $18.0\%$ for the remainder of the season.

---

## 7. Emergent Storyline Event Graphs (DAG Architecture)

### 7.1 Directed Acyclic Graph (DAG) State Engine

Narrative drama emerges through a directed graph $G = (V, E)$, where vertices $V$ represent story decision nodes and edges $E$ represent conditional transitions driven by simulation context (win streaks, snap shares, contract surplus, media pressure).

```
                      [ NODE 0: CONTRACT_DISPUTE_TRIGGER ]
                      (Player Surplus < -10M, Morale < 40)
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
     [ NODE 1: OTA_HOLDOUT ]                        [ NODE 2: PRIVATE_TRADE_REQ ]
     (Passionate Personality)                       (Reserved Personality)
            │                                               │
     ┌──────┴──────┐                                 ┌──────┴──────┐
     ▼             ▼                                 ▼             ▼
[ NODE 3:     [ NODE 4:                         [ NODE 5:     [ NODE 6:
 PUBLIC_LEAK ] FRANCHISE_TAG_STANDOFF ]          SECRET_TALKS ] EXTENSION_SIGNED ]
```

### 7.2 Core Narrative Subgraphs

#### 1. Contract Holdout & Trade Demand Arc
- **Root Trigger:** Contract Year remaining, Player OVR $\ge 84$, Market Surplus $S_i \ge \$12\text{M}$, Morale $< 50$.
- **Pathways:**
  - *Node A (Camp Holdout):* Daily fines accrued, team chemistry $-5\%$, weekly media pressure $+10$.
  - *Node B (Hold-in / "Soft Tissue" Phantom Injury):* Player attends meetings, refuses to practice, avoids fines.
  - *Resolution Nodes:* 
    - Full Max Extension (+15 Morale, $-12\text{M}$ Cap Space).
    - Trade Block Execution (Dispatched to GM Trade AI).
    - Franchise Tag Standoff (Player sits out Weeks 1–10).

#### 2. Scheme Mismatch & Coordinator Clashing Arc
- **Root Trigger:** Scheme fit score $< 60$ for key starter ($OVR \ge 80$).
- **Pathways:**
  - Performance slump ($\text{EPA} < -0.15$) $\to$ Sideline yelling match during nationally televised game $\to$ Anonymous coordinator leaks to media.
  - *Resolution Nodes:*
    - Coordinator changes playbook focus (+Scheme Fit, Coordinator Morale $-10$).
    - Player benched for developmental rookie (Rookie XP $+50\%$, Veteran demands release).
    - Offseason Coordinator Firing / Head Coach ultimatum.

#### 3. Mentor Synergy vs. Rookie Quarterback Friction
- **Root Trigger:** Team with Veteran QB ($OVR \ge 78$, Age $\ge 33$) drafts Round 1 QB ($OVR \ge 74$).
- **Pathways:**
  - *Synergy Path (Veteran has 'Mentor' Trait):* Rookie gains $+25\%$ XP per week, Awareness $+5$; Veteran accepts transition role.
  - *Friction Path (Veteran has 'Gunslinger / Mercenary' Personality):* Veteran refuses to assist rookie in film room; media runs weekly QB controversy polls; Locker room splits into offensive factions.

---

## 8. Formal Data Contracts (Pydantic V2 & TypeScript)

### 8.1 Pydantic V2 Schemas (Backend Models)

```python
"""
Pillar 2 Data Contracts: Dynasty RPG, Capology, and Narrative DAG
File: backend/app/schemas/dynasty_contracts.py
"""

from __future__ import annotations
from typing import List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class DevelopmentTier(str, Enum):
    NORMAL = "NORMAL"
    STAR = "STAR"
    SUPERSTAR = "SUPERSTAR"
    XFACTOR = "XFACTOR"


class ZoneAbilityStatus(str, Enum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    KNOCKED_OUT = "KNOCKED_OUT"


class AbilityDefinitionSchema(BaseModel):
    key: str
    name: str
    tier: Literal["COMMON", "SILVER", "GOLD", "ELITE"]
    category: Literal["MENTAL", "PHYSICAL_TECHNIQUE", "COVERAGE", "RECEIVING", "TRENCH", "LEADERSHIP"]
    position_requirements: List[str]
    level_requirement: int = Field(ge=1, le=30)
    xp_cost: int = Field(ge=500, le=15000)
    attribute_requirements: Dict[str, int] = Field(default_factory=dict)
    effects: Dict[str, float] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class PlayerDynastyProfile(BaseModel):
    player_id: int
    development_tier: DevelopmentTier = DevelopmentTier.NORMAL
    xp: int = Field(ge=0, default=0)
    level: int = Field(ge=1, default=1)
    skill_points: int = Field(ge=0, default=0)
    equipped_passive_abilities: List[str] = Field(default_factory=list)
    zone_ability_key: Optional[str] = None
    zone_status: ZoneAbilityStatus = ZoneAbilityStatus.INACTIVE
    hidden_potential_revealed: bool = False
    true_potential: int = Field(ge=40, le=99, default=75)

    model_config = ConfigDict(from_attributes=True)


class ContractYearDetail(BaseModel):
    year_index: int
    league_year: int
    base_salary: int
    signing_bonus_proration: int
    roster_bonus: int = 0
    workout_bonus: int = 0
    guaranteed_base: bool = False
    is_void_year: bool = False

    @property
    def cap_hit(self) -> int:
        return self.base_salary + self.signing_bonus_proration + self.roster_bonus + self.workout_bonus

    @property
    def cash_outlay(self) -> int:
        return 0 if self.is_void_year else (self.base_salary + self.roster_bonus + self.workout_bonus)


class CapOptimizationProposal(BaseModel):
    player_id: int
    action_type: Literal["SIMPLE_RESTRUCTURE", "POST_JUNE_1_CUT", "EXTEND_WITH_VOID_YEARS"]
    immediate_cap_savings: int
    dead_cap_current_year: int
    dead_cap_next_year: int
    future_inflation_per_year: int
    void_years_added: int = 0


class MedicalTriageRecord(BaseModel):
    player_id: int
    affected_body_part: Literal["HEAD", "NECK", "SHOULDER", "TORSO", "KNEE", "HAMSTRING", "ANKLE", "ACHILLES"]
    severity_grade: int = Field(ge=1, le=10)
    weeks_remaining: int
    is_playable: bool
    toradol_injected: bool = False
    brace_equipped: bool = False
    reinjury_recurrence_risk: float = Field(ge=0.0, le=1.0)
    active_attribute_penalties: Dict[str, int] = Field(default_factory=dict)


class DAGStorylineNode(BaseModel):
    node_id: str
    arc_name: str
    headline: str
    narrative_text: str
    initiator_player_id: Optional[int] = None
    affected_team_id: int
    options: List[DAGStorylineChoice]

    model_config = ConfigDict(from_attributes=True)


class DAGStorylineChoice(BaseModel):
    choice_id: str
    button_label: str
    target_node_id: Optional[str] = None  # None indicates arc resolution
    state_mutations: Dict[str, Any] = Field(default_factory=dict)
    probability_weight: float = 1.0
```

### 8.2 TypeScript Interfaces (Frontend Client)

```typescript
/**
 * Pillar 2 Frontend Data Contracts: Dynasty RPG & Empire Economics
 * File: frontend/src/types/dynasty.ts
 */

export type DevelopmentTier = 'NORMAL' | 'STAR' | 'SUPERSTAR' | 'XFACTOR';
export type ZoneAbilityStatus = 'INACTIVE' | 'ACTIVE' | 'KNOCKED_OUT';

export interface AbilityDefinition {
  key: string;
  name: string;
  tier: 'COMMON' | 'SILVER' | 'GOLD' | 'ELITE';
  category: 'MENTAL' | 'PHYSICAL_TECHNIQUE' | 'COVERAGE' | 'RECEIVING' | 'TRENCH' | 'LEADERSHIP';
  positionRequirements: string[];
  levelRequirement: number;
  xpCost: number;
  attributeRequirements: Record<string, number>;
  effects: Record<string, number>;
}

export interface PlayerDynastyState {
  playerId: number;
  developmentTier: DevelopmentTier;
  xp: number;
  level: number;
  skillPoints: number;
  equippedPassives: string[];
  zoneAbilityKey?: string;
  zoneStatus: ZoneAbilityStatus;
  hiddenPotentialRevealed: boolean;
  scoutedPotentialRange: [number, number];
}

export interface CapologyLedgerItem {
  playerId: number;
  playerName: string;
  position: string;
  baseSalary: number;
  proratedBonus: number;
  rosterBonus: number;
  capHit: number;
  cashOutlay: number;
  deadMoneyIfCutPreJune1: number;
  deadMoneyIfCutPostJune1: number;
  restructureSavingsPossible: number;
}

export interface MedicalTriageState {
  playerId: number;
  bodyPart: 'HEAD' | 'NECK' | 'SHOULDER' | 'TORSO' | 'KNEE' | 'HAMSTRING' | 'ANKLE' | 'ACHILLES';
  severityGrade: number;
  weeksToRecovery: number;
  canPlayThrough: boolean;
  toradolActive: boolean;
  braceEquipped: boolean;
  recurrenceRiskPct: number;
  penalties: Record<string, number>;
}

export interface DAGStorylinePrompt {
  nodeId: string;
  arcName: string;
  headline: string;
  narrativeText: string;
  initiatorPlayerName?: string;
  initiatorPlayerOvr?: number;
  choices: {
    choiceId: string;
    label: string;
    consequencesSummary: string;
    moraleDelta: number;
    capDelta: number;
  }[];
}
```

---

## 9. Adversarial Synthesis & Algorithmic Resilience

### 9.1 The "New Orleans Saints" Cap Trap (Anti-Exploit Protection)

```
                       [ CONTINUOUS RESTRUCTURING ]
                                    │
                                    ▼
                      [ KICK CAN DOWN THE ROAD ]
                                    │
                                    ▼
                   [ YEAR 4: SALARY CAP EXCEEDED ]
                                    │
            ┌───────────────────────┴───────────────────────┐
            ▼                                               ▼
 [ RESTRUCTURE IMPOSSIBLE ]                     [ CANNOT CUT PLAYERS ]
 (Base Salary = Vet Min)                        (Dead Cap > Cap Hit)
            │                                               │
            └───────────────────────┬───────────────────────┘
                                    │
                                    ▼
                        [ FINANCIAL DEADLOCK ]
```

#### Exploit Attack
In casual simulation games, users repeatedly restructure $100\%$ of eligible veteran contracts annually, generating artificial cap space without paying consequences until massive dead money concentrations paralyze the roster.

#### Superior Synthesis Mitigation
1. **Restructure Escalation Surcharge:** Each consecutive year a player is restructured, a $15\%$ compounding proration risk penalty is applied to their trade flight risk.
2. **Cap Insolvency Penalty Routine:** If a team enters the new league year over the Cap Ceiling and cannot reach legality via veteran cuts or standard restructures:
   - The engine automatically triggers **Forced Involuntary Releases** of the highest-paid non-guaranteed assets.
   - The franchise forfeits its earliest available Round 1 draft pick as an administrative penalty.
   - Team Prestige drops by $-25$ points, causing incoming Free Agents to demand a $+20\%$ premium.

### 9.2 Package Trade Cheese & Pick Hoarding

#### Exploit Attack
Users package multiple low-tier assets (e.g., three 70 OVR depth players and two 5th-round picks) to acquire a high-end 88 OVR starter from AI general managers who simply sum linear point totals.

#### Superior Synthesis Mitigation
1. **Package Concentration Discount:**
   $$V_{\text{package}}(\text{assets}) = \max_{a \in \text{assets}}(V(a)) + 0.60 \cdot V(\text{second}) + 0.25 \cdot \sum_{i=3}^{N} V(a_i)$$
2. **Roster Slot Opportunity Cost:** For every player incoming beyond 1, the AI deducts the replacement cost of cutting a current depth player.

### 9.3 Computational Complexity & Time Budgets

| Operation | Target Time Complexity | Execution Budget | Benchmark Performance |
| :--- | :--- | :--- | :--- |
| **Weekly Training XP Batch** | $O(N_{\text{players}})$ | $< 15\text{ ms}$ for 2,000 players | Fast vector update |
| **Multi-Year Cap Ledger Projection** | $O(T \cdot N_{\text{contracts}})$ | $< 5\text{ ms}$ for 32 teams $\times$ 5 years | In-memory arithmetic |
| **Trade Proposal Evaluation** | $O(N_{\text{assets}} \log N)$ | $< 2\text{ ms}$ per evaluation | Sub-millisecond response |
| **DAG Storyline Graph Walk** | $O(V + E)$ | $< 1\text{ ms}$ per team weekly | Single-pass evaluation |

---

## 10. Summary & Handoff Reference

This comprehensive specification completes the survey and architectural design requirements for **Pillar 2: Dynasty RPG Progression & Front Office Empire Economics**. It supplies deterministic mathematical models, formal schemas, parameter catalogs, and anti-exploit safeguards ready for production implementation.
