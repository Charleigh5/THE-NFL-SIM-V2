# Player System Technical Guide

This document serves as the technical reference for the Player Model in the Nano Banana Football Simulation Engine. It details the schema, attributes, statistical tracking, and RPG elements for every player position.

## Overview

The Player system is the core of the simulation. It combines:
1.  **Physical Attributes**: Used for physics-based calculations (momentum, tackling).
2.  **Skill Ratings**: Used for probability-based outcomes (catching, coverage).
3.  **RPG Elements**: Traits, XP, and progression logic.
4.  **Dynasty Mechanics**: Morale, contracts, and aging.

---

## Global Attributes
These attributes apply to every player regardless of position.

### Physical & Mental
| Attribute | Type | Description | System Usage |
|-----------|------|-------------|--------------|
| `speed` | 0-100 | Top speed potential. | Movement engine, pursuit angles. |
| `acceleration` | 0-100 | Rate of reaching top speed. | Burst off line, closing speed. |
| `strength` | 0-100 | Physical power. | Blocking, tackling force, shed block. |
| `agility` | 0-100 | Ability to change direction. | Juking, route cutting, coverage reaction. |
| `awareness` | 0-100 | AI decision making. | Reaction time to plays, reading defenses. |
| `stamina` | 0-100 | Energy pool. | fatigue accumulation, sub logic. |
| `injury_resistance` | 0-100 | Durability. | Injury probability roll after contact. |
| `morale` | 0-100 | Player happiness. | **Critical**: Affects team chemistry. Low morale triggers "Mutiny Cascades" in `SocialGraph`. |

### Contract & Status
| Attribute | Description |
|-----------|-------------|
| `contract_salary` | Annual cost in dollars. |
| `contract_years` | Remaining seasons. |
| `development_trait` | Growth potential (`NORMAL`, `STAR`, `SUPERSTAR`, `XFACTOR`). Affects XP multipliers in `OffseasonService`. |

---

## Offensive Positions

### Quarterback (QB)
The primary ball handler and decision maker.

**Key Attributes:**
*   **`throw_power`**: Maximum distance and velocity of throws.
    *   *Link*: Used in `PlayResolver` to determine if a deep pass is physically possible.
*   **`throw_accuracy_short/mid/deep`**: Probability modifiers for pass success at varying ranges.
    *   *Link*: `PlayResolver` selects the specific attribute based on target distance.
*   **`awareness`**: Speed of reading the defense.
*   **`arm_slot`**: Visual/Physics attribute (`OverTop`, `Sidearm`).
*   **`release_point_height`**: Height in feet. Affects ball trajectory start point.

**Progression Logic:**
*   Gains XP heavily from **Passing TDs** (50 XP) and **Yards** (0.5 XP).
*   Loses XP for **Interceptions** (-20 XP).

### Running Back (RB)
Ball carriers focused on evasion and power.

**Key Attributes:**
*   **`vision_cone_angle`**: (Degrees) The field of view where the AI can "see" defenders to react. Narrower cones mean missing open lanes.
*   **`break_tackle_threshold`**: (Float) The force (Newtons approx.) required to bring this player down.
    *   *Link*: Used in `AI.resolve_tackle` against defender's momentum.
*   **`carrying`**: (Implied via `strength`/`agility`) Ability to hold onto the ball.
*   **`catching`**: Ability to act as a receiver out of the backfield.

**Progression Logic:**
*   Gains XP from **Rush TDs** (40 XP) and **Rush Yards** (0.8 XP).

### Wide Receiver (WR) & Tight End (TE)
Pass catchers.

**Key Attributes:**
*   **`catching`**: Base probability to catch a clean pass.
*   **`route_running`**: Ability to create separation from defenders.
    *   *Link*: Used in `PlayResolver` vs. Defender's Coverage.
*   **`pass_block` / `run_block`**: TE specifically relies on these for dual-threat utility.

**Progression Logic:**
*   Gains XP from **Receptions**, **Yards**, and **TDs**.

### Offensive Line (OT, OG, C)
The protectors.

**Key Attributes:**
*   **`pass_block`**: Rating vs. Pass Rush.
    *   *Link*: `BlockingEngine.resolve_pass_block` compares this vs. Defender's `pass_rush_power`.
*   **`run_block`**: Rating vs. Block Shedding.
*   **`strength`**: Critical to avoid "Bull Rush" moves.

**Stats Tracked:**
*   **`pancakes`**: Times they flattened a defender.
*   **`sacks_allowed`**: Negative stat.

---

## Defensive Positions

### Defensive Line (DE, DT)
Pass rushers and run stuffers.

**Key Attributes:**
*   **`pass_rush_power`**: Ability to push the pocket (Bull Rush).
*   **`pass_rush_finesse`**: Ability to swim/spin past blockers.
*   **`block_shed`**: Ability to disengage from a block to make a tackle.
*   **`tackle`**: Ability to wrap up the ball carrier.

**Progression Logic:**
*   Huge XP bonuses for **Sacks** (100 XP) and **Tackles for Loss** (30 XP).

### Linebacker (LB)
Hybrid defenders.

**Key Attributes:**
*   **`play_recognition`**: Ability to distinguish Run vs. Pass early.
*   **`man_coverage` / `zone_coverage`**: Coverage skills.
*   **`tackle`** & **`hit_power`**: Stopping power. `hit_power` increases fumble chance.

### Defensive Back (CB, S)
Pass defenders.

**Key Attributes:**
*   **`man_coverage`**: Ability to stick to a receiver 1-on-1.
*   **`zone_coverage`**: Effectiveness in a designated area.
    *   *Link*: `DefenseEngine.resolve_zone_coverage` uses this + `awareness` to determine reaction speed.
*   **`catching`**: Ability to make Interceptions.

**Stats Tracked:**
*   **`interceptions`**, **`pass_deflections`**.

---

## Special Teams

### Kicker (K) & Punter (P)
**Key Attributes:**
*   **`kick_power`**: Max distance.
*   **`kick_accuracy`**: Probability of straight flight.

---

## System Interconnections

### 1. The Physics Engine (`backend/app/engine/ai.py`)
Unlike simple dice rolls, the game often uses physics.
*   **Tackling**: Uses `strength` and speed to calculate Momentum (`p = mv`).
*   **Break Tackle**: The runner's `break_tackle_threshold` is compared against the defender's effective momentum.

### 2. The RPG Engine (`backend/app/rpg`)
*   **Traits**: Special flags like `"DeepBall"` or `"BrickWall"` provide conditional boosts.
    *   *Example*: `"BrickWall"` adds +10 `pass_block` specifically when facing a Bull Rush.
*   **Progression**: `ProgressionEngine` calculates XP weekly. `DevelopmentTrait` (Star, XFactor) acts as a multiplier for how fast players grow.

### 3. The Society Engine (`backend/app/kernels/society`)
*   **Morale**: This is not just a cosmetic number. A low-morale player can trigger a **Mutiny Cascade** in the social graph, lowering the morale of teammates connected to them.

---

## Proposed Feature Enhancements

The following tables outline 5 recommended enhancements per position group to deepen gameplay, realism, and RPG progression.
**Special focus is placed on Inter-Positional Dynamics**, where one group's attribute directly influences the effectiveness of another group (e.g., a QB's traits improving the Offensive Line).

### 1. Offensive Enhancements

| Position Group | Feature Name | Type | Description | Positional Dynamic / Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Quarterback** | `Pocket Presence` | Attribute | Determines the QB's ability to sense pressure without direct line-of-sight (avoiding "statue" sacks). | **Mitigates O-Line Failure**: Reduces sack frequency even when the **Offensive Line** loses a block, making average lines viable. |
| **Quarterback** | `Field General` | Trait | Increases success rate of audibles and hot routes on critical downs (3rd/4th). | **Boosts WR/OL**: Temporarily increases `Awareness` of **Receivers** (better separation) and **Line** (pickup blitz) pre-snap. |
| **Quarterback** | `Quick Release` | Attribute | The speed of the throwing animation from decision to release. | **Protects O-Line**: Negates elite **Pass Rushers** by getting the ball out before the rush can arrive, reducing pressure on Tackles. |
| **Quarterback** | `Scramble Willingness` | AI Tendency | Slider (0-100) dictating how often a QB abandons a clean pocket to run. | **Stresses Defense**: Forces **Linebackers** to spy the QB, opening up the middle of the field for **Tight Ends** and **Slot WRs**. |
| **Quarterback** | `Throw on Run` | Attribute | Mitigates accuracy penalties when the QB's velocity vector > 0. | **Extends Play**: Allows **WRs** time to run "Scramble Drill" routes when the initial play breaks down. |
| **Running Back** | `Patience` | Attribute | AI behavior governing how long a runner waits behind blockers before accelerating. | **Empowers Pulling Guards**: Gives **Offensive Linemen** time to execute slow-developing blocks (Traps/Sweeps) before the runner hits the gap. |
| **Running Back** | `Pass Pro Rating` | Attribute | Specific blocking rating for picking up blitzing LBs. | **Protects QB**: Directly counters blitzing **Linebackers**, giving the **Quarterback** critical extra seconds in the pocket. |
| **Running Back** | `Chip Block` | Trait | The RB "chips" (bumps) a Defensive End on their way out to a route. | **Helps Tackles**: Slows down the **Defensive End's** momentum, giving the **Offensive Tackle** an easier win on the edge. |
| **Running Back** | `Juke Efficiency` | Attribute | Determines how much momentum/speed is lost when performing a juke move. | **Isolates LBs**: Punishes **Linebackers** with low `Agility` by leaving them grasping at air in the open field. |
| **Running Back** | `Mismatch Nightmare` | Trait | Grants bonus Catching/Route Running when covered by a Linebacker. | **Stresses Defense**: Forces the defense to sub in a **Defensive Back** (Nickel/Dime), weakening their run defense vs the **O-Line**. |
| **WR / TE** | `Release` | Attribute | Ability to disengage from Press Coverage at the line of scrimmage. | **Timing with QB**: Ensures the receiver is at the spot the **Quarterback** expects on time; failure here causes the QB to hold the ball and get sacked. |
| **WR / TE** | `Clearout Specialist` | Trait | Tendency to run deep routes at max effort even if not the primary target. | **Opens Space for RB/TE**: Draws **Safeties** deep, clearing underneath zones for **Running Backs** and **Tight Ends**. |
| **WR / TE** | `Possession Receiver` | Trait | Bonus to `Catching` on 3rd down, but strictly limits YAC potential. | **Security for QB**: Provides a "Panic Button" option for the **Quarterback** when the pocket collapses. |
| **WR / TE** | `Blocking Tenacity` | Attribute | Determines how long a WR maintains a block downfield. | **Enables RB Home Runs**: Critical for outside runs; prevents **Cornerbacks** from setting the edge, turning 5-yard **RB** gains into 50-yard touchdowns. |
| **WR / TE** | `Route Specialist` | RPG | Unlocks proficiency tiers for specific routes (e.g., "Master" at Post patterns). | **Predictability**: Allows the **QB** to throw "blind" with high trust, effectively countering tight **Man Coverage**. |
| **Offensive Line** | `Communication` | Attribute | (Center Specific) The ability to identify the "Mike" LB and shift protection. | **Boosts Unit Awareness**: The **Center's** rating buffs the `Awareness` of **Guards/Tackles**, helping them pick up stunts/twists by the **DL**. |
| **Offensive Line** | `Unit Chemistry` | System | Passive bonus to Blocking stats for linemen who have started X consecutive games together. | **Unit Cohesion**: Makes a group of average players perform better than 5 unacquainted stars; critical for handling complex **Defensive Fronts**. |
| **Offensive Line** | `Pull Speed` | Attribute | Max speed specifically when executing Pull/Trap blocking assignments. | **Unlocks Playbook**: Enables specific run concepts (Power O, Counter) that require the lineman to beat the **Linebacker** to the spot. |
| **Offensive Line** | `Anchor` | Attribute | Resistance specifically to "Bull Rush" moves (distinct from raw Strength). | **Pocket Integrity**: Prevents the pocket from collapsing into the **QB's** face, allowing them to step up and throw. |
| **Offensive Line** | `Discipline` | Attribute | Reduces frequency of Holding and False Start penalties. | **Momentum Killer**: Low discipline kills drives, putting the **QB** in 1st & 20 situations that force predictable passing (easy for **Defense**). |

### 2. Defensive Enhancements

| Position Group | Feature Name | Type | Description | Positional Dynamic / Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Defensive Line** | `First Step` | Attribute | Reaction time to the snap (distinct from Acceleration). | **Disrupts Mesh Point**: Can blow up handoffs before they happen, forcing the **RB** to redirect into the arms of waiting **Linebackers**. |
| **Defensive Line** | `Eat Blocks` | Trait | (DT Specific) Tendency/Skill to occupy double teams effectively without giving ground. | **Frees Linebackers**: Keeps the **Offensive Guards** occupied, allowing **Linebackers** to scrape and tackle the **RB** untouched. |
| **Defensive Line** | `Gap Integrity` | Attribute | Ability to resist being "sealed" or pushed out of assigned run lane. | **Funnels to Help**: Forces the **RB** to cut back into the teeth of the defense (where **LBs/Safeties** are waiting) rather than finding a hole. |
| **Defensive Line** | `Bat Ball` | Trait | AI tendency to jump/swat passes if rush is stalled. | **Counters Quick Game**: Negates the **QB's** "Quick Release" advantage by blocking passing lanes at the source. |
| **Defensive Line** | `Intimidation` | System | Sacks/Hits lower the Morale and Attributes of the opposing O-Line for a short duration. | **Breaks Will**: Lowers the opposing **O-Line's** blocking ratings, leading to a cascade of pressure that ruins the **QB's** rhythm. |
| **Linebacker** | `Green Dot` | Trait | (MLB Specific) Relays defensive play calls and adjustments. | **Prevents Blown Coverage**: Reduces the chance of **Secondary (DBs)** miscommunication, preventing wide-open **WR** touchdowns. |
| **Linebacker** | `Coverage Disguise` | Attribute | Delays the QB's AI recognition of Man vs. Zone coverage. | **Baits QB**: Tricks the **Quarterback** into making dangerous throws that **Safeties** can intercept. |
| **Linebacker** | `Blitz Timing` | Attribute | Effectiveness/Speed boost on delayed blitzes (waiting for gap to open). | **Overloads O-Line**: Exploits communication breakdowns in the **Offensive Line**, creating free rushers at the **QB**. |
| **Linebacker** | `Run Fit` | Attribute | Ability to read the "spill" vs "box" logic of the Defensive Line. | **Complementary Football**: Works in tandem with **DL**; if DL spills outside, LB scrapes; if DL boxes inside, LB fills. |
| **Linebacker** | `The Enforcer` | Trait | Increased Fumble Caused chance on big hits / Tackle sound effect. | **Fear Factor**: Causes **WRs** crossing the middle to drop passes (hearing footsteps) even before contact. |
| **Defensive Back** | `Press` | Attribute | Ability to jam WR at the line, disrupting timing. | **Helps Pass Rush**: Disrupts the timing of the route, forcing the **QB** to hold the ball longer, leading to coverage sacks for the **DL**. |
| **Defensive Back** | `Ball Tracking` | Attribute | AI ability to play the ball in the air (turn head) vs playing the receiver (face guarding). | **Turnover Generation**: Turns potential PIs into Interceptions, giving the **Offense** short fields. |
| **Defensive Back** | `Coverage Shell` | System | (Safety) Pre-snap alignment that disguises the true coverage (Cover 2 looks like Cover 3). | **Protects Corners**: Allows **Cornerbacks** to play aggressively underneath, knowing the **Safety** help is disguised but present. |
| **Defensive Back** | `Pick Artist` | Trait | Significantly higher catch rate on Interception opportunities. | **Game Swing**: Capitalizes on **QB** mistakes forced by **DL** pressure. |
| **Defensive Back** | `Run Support` | Tendency | Willingness to abandon coverage responsibilities to tackle a runner. | **Last Line of Defense**: A Safety with high Run Support acts as an extra **Linebacker**, shutting down **RB** breakouts. |

### 3. Special Teams Enhancements

| Position Group | Feature Name | Type | Description | Positional Dynamic / Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Kicker / Punter** | `Ice in Veins` | Trait | Negates the "icing the kicker" mechanic (shaking meter/camera). | **Reliability**: Guarantees points in clutch situations, taking pressure off the **Offense** to score TDs. |
| **Kicker / Punter** | `Hang Time` | Attribute | Determines time ball is in air; affects coverage team arrival time. | **Coverage Aid**: High hang time allows **Gunners** to reach the returner before the catch, preventing big returns. |
| **Kicker / Punter** | `Coffin Corner` | Attribute | Accuracy specifically for punts landing inside the 20-yard line. | **Field Position**: Pins the opponent deep, drastically increasing the **Defense's** chance of scoring a Safety or forcing a 3-and-out. |
| **Kicker / Punter** | `Return Vision` | Attribute | (For Returners) AI ability to spot lanes and set up blocks. | **Flip the Field**: A good return gives the **Offense** a short field, increasing scoring probability. |
| **Gunner** | `Vice` | Role | (Gunner Specific) Ability to beat double-team blocks on the outside. | **Forces Fair Catch**: Disrupts the **Return Team's** blocking scheme, forcing the Returner to signal fair catch. |

---

## Proposed RPG & Leveling Overhaul

This section proposes deep RPG progression systems designed to give each position a unique developmental path. These features move beyond simple attribute increases, offering **Unlockable Mechanics** and **Specialization Trees**.

### 1. Offensive Positions

| Position | Feature Name | Mechanism | XP Cost / Requirement | Positional Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Quarterback** | `Film Study Master` | **Unlockable Ability**: Reveals one defensive coverage shell (Man/Zone) pre-snap after standing in the pocket for 2 seconds. | Level 10 + 5000 XP | Drastically increases pre-snap read accuracy, reducing interceptions. |
| **Quarterback** | `The Architect` | **Skill Tree**: Allows the QB to create custom "Hot Routes" that are not in the standard playbook. | Level 15 + "High IQ" Trait | Gives the user strategic flexibility to exploit specific defensive weaknesses. |
| **Running Back** | `Combo Breaker` | **Passive Mastery**: Consecutive successful jukes/spins cost 50% less stamina. | Level 8 + Agility > 90 | Allows elite backs to string together highlight-reel runs without tiring immediately. |
| **Running Back** | `Bell Cow Certification` | **Badge**: Increases injury resistance and stamina recovery rate during the 4th quarter. | 200 Carries in a single season | Essential for "Power Back" builds to remain effective in "Close Out" scenarios. |
| **Wide Receiver** | `Route Artist` | **Skill Tree**: Unlocks "Elite" animations for specific cuts (e.g., Whip Route, Comeback) that create instant separation. | Level 5 per route type | Turns average speed receivers into reliable targets through technical perfection. |
| **Wide Receiver** | `Security Blanket` | **Relationship Mechanic**: Catch rate increases by 10% on 3rd downs if the throwing QB has >80 Chemistry. | 3 Seasons with same QB | Encourages keeping QB-WR duos together for long-term dynasty benefits. |
| **Tight End** | `Seam Buster` | **Active Ability**: Bonus speed for 2 seconds when releasing vertically up the hash marks. | Level 12 + Speed > 80 | Forces defenses to respect the TE as a vertical threat, opening up underneath routes. |
| **Tight End** | `Sixth Lineman` | **Stance Toggle**: Can toggle between a "Receiver Stance" (Agility bonus) and "Blocking Stance" (Strength bonus) pre-snap. | Level 5 | Adds tactical depth; allows the TE to dynamically adjust to the defensive front. |
| **Offensive Tackle** | `Island Survivor` | **Mastery**: Negates the "Pass Rush Move" bonus of edge rushers when in 1-on-1 isolation (no TE help). | Level 20 + Pass Block > 90 | Allows the offense to slide protection *away* from this tackle, helping the rest of the line. |
| **Offensive Tackle** | `Technique Doctor` | **Mentorship**: Grants a passive +5 Pass Block bonus to the adjacent Guard. | Level 10 Veteran (>30yo) | Makes veteran tackles valuable mentors for rookie guards. |
| **Offensive Guard** | `Pull Train` | **Physics Modifier**: Increases impact force by 20% when hitting a defender while moving (pulling). | Level 8 + Strength > 85 | Critical for "Power Run" schemes; turns the Guard into a lead blocker weapon. |
| **Offensive Guard** | `Pocket Anchor` | **Stance Upgrade**: Cannot be pushed back more than 1 yard by a Bull Rush, ensuring pocket integrity. | Level 12 | Prevents the QB from being unable to step up, countering high-strength DTs. |
| **Center** | `Line General` | **Pre-Snap Ability**: Can identify the "Mike" LB to reset blocking assignments for the whole line. | Level 15 + Awareness > 90 | Nullifies defensive blitz confusion; acts as a direct counter to "Coverage Disguise". |
| **Center** | `Snap Perfection` | **Passive**: Reduces shotgun snap fumble chance to 0% and increases snap velocity. | Level 5 | Subtle but vital enhancement for "Shotgun Heavy" offenses to maintain timing. |

### 2. Defensive Positions

| Position | Feature Name | Mechanism | XP Cost / Requirement | Positional Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Defensive End** | `Edge Threat` | **Stance Modifier**: Can choose a "Wide 9" alignment to sacrifice run defense for a massive speed rush bonus. | Level 10 | Forces the offense to chip with a RB or keep a TE in to block. |
| **Defensive End** | `Spin Cycle` | **Animation Unlock**: Unlocks a "Elite Spin Move" that is twice as fast as the default. | Level 8 + Finesse > 85 | Gives speed rushers a reliable counter to heavy, slow Offensive Tackles. |
| **Defensive Tackle** | `Grave Digger` | **Physics Modifier**: Increases the "Pile Up" radius on tackles, effectively clogging two gaps at once. | Level 12 + Weight > 320lbs | Essential for 3-4 Nose Tackles; frees up LBs to roam freely. |
| **Defensive Tackle** | `Interior Disruptor` | **Passive**: 15% chance to instantly shed a block if the QB steps up into the pocket. | Level 15 | Punishes QBs for holding the ball too long; creates interior pressure. |
| **Linebacker** | `Field Commander` | **Vision Cone**: Expands the "Fog of War" reveal radius for the entire defense. | Level 18 + Awareness > 95 | The defensive equivalent of a QB; ensures the team is never surprised by formations. |
| **Linebacker** | `Lurker` | **Jump Mechanic**: Allows for "Super Jumps" to intercept passes meant for players 5-10 yards behind them. | Level 10 + Jump > 90 | Shuts down the intermediate middle of the field; terrifies QBs throwing slants/posts. |
| **Cornerback** | `Island King` | **Isolation Bonus**: Stats increase by +5 when no Safety help is visible on their side of the field. | Level 20 + Man Cov > 95 | Allows the coordinator to blitz heavily, trusting this corner to win 1-on-1. |
| **Cornerback** | `Route Jumper` | **Prediction System**: If the WR runs the same route 3 times in a game, the CB gets a 50% "Jump Route" bonus on the 4th. | Level 12 + Play Rec > 85 | Punishes repetitive offensive play-calling; forces diversity in attack. |
| **Safety** | `Hit Stick Master` | **Physics Event**: Tackles have a 20% higher chance to cause an incompletion (jarring ball loose) upon impact. | Level 8 + Hit Power > 90 | Makes going over the middle dangerous; turns completions into drops. |
| **Safety** | `Robber Role` | **AI Behavior**: Unlocks the "Robber" zone assignment (floating in short middle) to trap crossing routes. | Level 14 | Adds a complex coverage shell that confuses QBs expecting open middle zones. |

### 3. Special Teams Positions

| Position | Feature Name | Mechanism | XP Cost / Requirement | Positional Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Kicker** | `Clutch Kicker` | **Meter Modifier**: The "Accuracy Zone" on the kick meter does not shrink in the 4th quarter or OT. | Level 10 + "Ice in Veins" | Makes game-winning kicks purely skill-based rather than RNG-punishing. |
| **Kicker** | `Calibration` | **Active Prep**: Can "warm up" on the sideline to temporarily boost accuracy by 5% for the next drive. | Level 5 | Adds a sideline management mini-game aspect. |
| **Punter** | `Pin Point` | **UI Upgrade**: Shows the exact landing spot trajectory preview for "Coffin Corner" punts. | Level 12 + Accuracy > 90 | Turns punting into a precise weapon for field position battles. |
| **Punter** | `Fake Specialist` | **Skill Tree**: Increases passing/running stats specifically for "Fake Punt" plays. | Level 8 | Forces the defense to play "Punt Safe" defense, weakening their return game. |

---

## Positional Identity & Customization

To enhance the visual distinctiveness and realism of the simulation, each position group adheres to strict jersey numbering conventions and features unique visual accessories.

### 1. Offensive Identity

| Position Group | Jersey Number Range | Common Accessories | Visual Aesthetic Note |
| :--- | :--- | :--- | :--- |
| **Quarterback** | **1-19** | Towel (Waist), Hand Warmer (Waist), Wristband (Playcall), Flak Jacket (Torso), Visor (Clear/Tinted). | Typically lightly padded torso for mobility; distinct wrist equipment for play-calling. |
| **Running Back** | **0-49, 80-89** | Tinted Visor, Turf Tape (Arms), Arm Sleeves (Padded), Gloves (Super Sticky), Mouthguard (Dangling). | Heavy leg padding/thigh pads often visible; frequent use of arm protection vs turf burns. |
| **Wide Receiver** | **0-49, 80-89** | Gloves (Custom Designs), Towel (Slim), Mouthguard (Pacifier style), Visor (Mirror/Tinted), Leg Sleeves. | "Swag" heavy position; minimal padding to maximize speed; flashy footwear. |
| **Tight End** | **0-49, 80-89** | Gloves (Heavy Duty), Elbow Pads, Knee Braces (Optional), Visor (Clear). | Hybrid aesthetic; larger than WRs but sleeker than Linemen; often wear gloves designed for both blocking and catching. |
| **Offensive Line** | **50-79** | Knee Braces (Standard), Elbow Pads (Padded), Neck Roll (Retro/Power), Gloves (Padded Paws), Finger Tape. | Bulky silhouette; heavy knee bracing is standard for injury prevention; minimal skin exposure. |

### 2. Defensive Identity

| Position Group | Jersey Number Range | Common Accessories | Visual Aesthetic Note |
| :--- | :--- | :--- | :--- |
| **Defensive Line** | **50-79, 90-99** | Arm Braces (Hinged), Neck Roll (Butterfly), Facemask (Multi-bar/Custom), Gloves (Lineman), Club Cast. | Intimidating profiles; custom facemasks to prevent eye gouging; arm bracing common for trench warfare. |
| **Linebacker** | **0-59, 90-99** | Neck Roll, Visor (Dark), Tight Sleeves, Gloves, Turf Tape. | The "Gladiator" look; balanced padding; dark visors common for hiding eye movement. |
| **Defensive Back** | **0-49** | Arm Sleeves (Compression), Leg Sleeves, Visor (Mirror), Towel, Backplate (Exposed). | Sleek, aerodynamic; similar to WRs but often with exposed backplates for spine protection. |

### 3. Special Teams Identity

| Position Group | Jersey Number Range | Common Accessories | Visual Aesthetic Note |
| :--- | :--- | :--- | :--- |
| **Kicker / Punter** | **0-49, 90-99** | One-bar Facemask (Classic), Soccer Cleats, Wristband (Notes), Thigh Pad (Slim). | Minimalist padding; often wear different cleats on kicking vs plant foot; distinctive single-bar facemasks. |
