
---

## Proposed Feature Enhancements

The following tables outline 5 recommended enhancements per position group to deepen gameplay, realism, and RPG progression.

### 1. Offensive Enhancements

| Position Group | Feature Name | Type | Description | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Quarterback** | `Pocket Presence` | Attribute | Determines the QB's ability to sense pressure without direct line-of-sight (avoiding "statue" sacks). | Adds skill gap between veterans and rookies; makes O-Line play more impactful. |
| **Quarterback** | `Audible Mastery` | Trait | Increases success rate of changing plays at the line against crowd noise/home field advantage. | Rewards high-IQ QBs and adds strategic layer to away games. |
| **Quarterback** | `Leadership Aura` | Passive | Boosts the `Awareness` and `Blocking` stats of the Offensive Line. | Simulates the intangible impact of a franchise leader rallying the troops. |
| **Quarterback** | `Scramble Willingness` | AI Tendency | Slider (0-100) dictating how often a QB abandons a clean pocket to run. | differentiates between "Mobile" (runs designed plays) and "Improv" (runs when play breaks down) QBs. |
| **Quarterback** | `Throw on Run` | Attribute | Mitigates accuracy penalties when the QB's velocity vector > 0. | Essential for modern offense simulation; prevents mobile QBs from being overpowered or useless. |
| **Running Back** | `Patience` | Attribute | AI behavior governing how long a runner waits behind blockers before accelerating. | Distinguishes between "slasher" backs (hit hole fast) and "patient" backs (Wait for blocks like Le'Veon Bell). |
| **Running Back** | `Pass Pro Rating` | Attribute | Specific blocking rating for picking up blitzing LBs. | Makes 3rd-down backs valuable even if they aren't elite catchers; adds risk/reward to using power backs on passing downs. |
| **Running Back** | `Wear & Tear` | System | Progressive stat degradation (Speed/Agility) based on accumulated hits in a game. | forces usage of RB committees; simulates the physical toll of a "workhorse" role. |
| **Running Back** | `Juke Efficiency` | Attribute | Determines how much momentum/speed is lost when performing a juke move. | High agility isn't enough; this separates elite elusive backs who maintain top speed while cutting. |
| **Running Back** | `Mismatch Nightmare` | Trait | Grants bonus Catching/Route Running when covered by a Linebacker. | Encourages defensive coordinators to use Dime/Nickel packages vs elite receiving backs. |
| **WR / TE** | `Release` | Attribute | Ability to disengage from Press Coverage at the line of scrimmage. | Critical for realism; fast WRs can be neutralized by physical CBs if their Release is low. |
| **WR / TE** | `Spectacular Catch` | Attribute | Probability of triggering special animations (one-handed, diving) on uncatchable balls. | Creates "highlight reel" moments and differentiates superstars from reliable possession receivers. |
| **WR / TE** | `Possession Receiver` | Trait | Bonus to `Catching` on 3rd down, but strictly limits YAC potential (immediate tuck). | Gives value to slow, reliable veterans (the "safety blanket" TE). |
| **WR / TE** | `Blocking Tenacity` | Attribute | Determines how long a WR maintains a block downfield. | Crucial for outside run game; makes "blocking WRs" a legitimate roster strategy. |
| **WR / TE** | `Route Specialist` | RPG | Unlocks proficiency tiers for specific routes (e.g., "Master" at Post patterns). | Adds RPG depth; players aren't just "good at everything," they have specific roles. |
| **Offensive Line** | `Footwork` | Attribute | Speed of recovering balance after losing an initial block interaction. | Prevents instant sacks from one bad roll; allows elite linemen to recover. |
| **Offensive Line** | `Unit Chemistry` | System | Passive bonus to Blocking stats for linemen who have started X consecutive games together. | Simulates the reality that O-Line performance is about communication and familiarity, not just individual talent. |
| **Offensive Line** | `Pull Speed` | Attribute | Max speed specifically when executing Pull/Trap blocking assignments. | Makes athletic linemen valuable for specific schemes (Power/Counter runs) vs heavy plodders (Zone/Gap). |
| **Offensive Line** | `Anchor` | Attribute | Resistance specifically to "Bull Rush" moves (distinct from raw Strength). | Allows smaller, technically sound Centers to survive against massive Nose Tackles. |
| **Offensive Line** | `Discipline` | Attribute | Reduces frequency of Holding and False Start penalties. | Adds a "hidden cost" to cheap, low-rated linemen beyond just allowing sacks. |

### 2. Defensive Enhancements

| Position Group | Feature Name | Type | Description | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Defensive Line** | `First Step` | Attribute | Reaction time to the snap (distinct from Acceleration). | Simulates elite edge rushers who "jump the snap"; creates havoc in backfield immediately. |
| **Defensive Line** | `Motor` | Attribute | Reduces stamina drain and maintains effectiveness in 4th Quarter. | Differentiates "high effort" players from those who take plays off; vital for late-game situations. |
| **Defensive Line** | `Gap Integrity` | Attribute | Ability to resist being "sealed" or pushed out of assigned run lane. | Crucial for run defense simulation; prevents DL from just chasing stats and leaving holes. |
| **Defensive Line** | `Bat Ball` | Trait | AI tendency to jump/swat passes if rush is stalled. | Adds counter-play to quick passing games where sacks are impossible. |
| **Defensive Line** | `Intimidation` | System | Sacks/Hits lower the Morale and Attributes of the opposing O-Line for a short duration. | Simulates the psychological effect of a dominant pass rush "breaking" an offensive line. |
| **Linebacker** | `Lateral Pursuit` | Trait | Speed bonus specifically when moving parallel to the line of scrimmage. | Makes LBs effective against outside zones and sweeps without needing WR-level top speed. |
| **Linebacker** | `Coverage Disguise` | Attribute | Delays the QB's AI recognition of Man vs. Zone coverage. | Adds chess-match element; high IQ LBs can bait QBs into bad throws. |
| **Linebacker** | `Blitz Timing` | Attribute | Effectiveness/Speed boost on delayed blitzes (waiting for gap to open). | Rewards complex defensive schemes over simple "send the house" strategies. |
| **Linebacker** | `Shed Finesse` | Attribute | Ability to slip blocks (swim/rip) vs WRs/TEs specifically. | Differentiates LBs who can play in space vs "Thumpers" who just blow up fullbacks. |
| **Linebacker** | `The Enforcer` | Trait | Increased Fumble Caused chance on big hits / Tackle sound effect. | Adds identity to physical LBs; forces offense to be careful running near them. |
| **Defensive Back** | `Press` | Attribute | Ability to jam WR at the line, disrupting timing. | Counterpart to WR "Release"; essential for aggressive man-coverage schemes. |
| **Defensive Back** | `Ball Tracking` | Attribute | AI ability to play the ball in the air (turn head) vs playing the receiver (face guarding). | Reduces Pass Interference calls; distinguishes "Ball Hawks" from pure "Lockdown" corners. |
| **Defensive Back** | `Recovery Speed` | Attribute | "Catch-up" mechanics speed boost when trailing a receiver. | Allows corners to play aggressively knowing they can recover if beaten initially. |
| **Defensive Back** | `Pick Artist` | Trait | Significantly higher catch rate on Interception opportunities. | Turns PBUs (Pass Breakups) into Turnovers; game-changing ability. |
| **Defensive Back** | `Run Support` | Tendency | Willingness to abandon coverage responsibilities to tackle a runner. | Risk/Reward mechanic; stops the run but susceptible to Play Action. |

### 3. Special Teams Enhancements

| Position Group | Feature Name | Type | Description | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Kicker / Punter** | `Ice in Veins` | Trait | Negates the "icing the kicker" mechanic (shaking meter/camera). | Makes elite kickers invaluable in close games. |
| **Kicker / Punter** | `Hang Time` | Attribute | Determines time ball is in air; affects coverage team arrival time. | Low hang time = longer returns; adds strategy to punting (distance vs air time). |
| **Kicker / Punter** | `Coffin Corner` | Attribute | Accuracy specifically for punts landing inside the 20-yard line. | A tactical weapon for field position battles. |
| **Kicker / Punter** | `Return Vision` | Attribute | (For Returners) AI ability to spot lanes and set up blocks. | Makes the Return Specialist a unique role, not just "fastest guy on team". |
| **Kicker / Punter** | `Gunner Ace` | Role | Buffs to Speed/Tackling for players assigned to "Gunner" slots. | Gives roster spots to special teams specialists (like Matthew Slater). |
