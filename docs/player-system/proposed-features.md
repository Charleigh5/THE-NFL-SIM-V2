# Proposed Feature Enhancements

The following lists outline 5 recommended enhancements per position group to deepen gameplay, realism, and RPG progression.
**Special focus is placed on Inter-Positional Dynamics**, where one group's attribute directly influences the effectiveness of another group (e.g., a QB's traits improving the Offensive Line).

## Offensive Enhancements

### Quarterback

- **`Pocket Presence`** (Attribute)

  - **Description**: Determines the QB's ability to sense pressure without direct line-of-sight (avoiding "statue" sacks).
  - **Positional Dynamic / Impact**: **Mitigates O-Line Failure**: Reduces sack frequency even when the **Offensive Line** loses a block, making average lines viable.

- **`Field General`** (Trait)

  - **Description**: Increases success rate of audibles and hot routes on critical downs (3rd/4th).
  - **Positional Dynamic / Impact**: **Boosts WR/OL**: Temporarily increases `Awareness` of **Receivers** (better separation) and **Line** (pickup blitz) pre-snap.

- **`Quick Release`** (Attribute)

  - **Description**: The speed of the throwing animation from decision to release.
  - **Positional Dynamic / Impact**: **Protects O-Line**: Negates elite **Pass Rushers** by getting the ball out before the rush can arrive, reducing pressure on Tackles.

- **`Scramble Willingness`** (AI Tendency)

  - **Description**: Slider (0-100) dictating how often a QB abandons a clean pocket to run.
  - **Positional Dynamic / Impact**: **Stresses Defense**: Forces **Linebackers** to spy the QB, opening up the middle of the field for **Tight Ends** and **Slot WRs**.

- **`Throw on Run`** (Attribute)
  - **Description**: Mitigates accuracy penalties when the QB's velocity vector > 0.
  - **Positional Dynamic / Impact**: **Extends Play**: Allows **WRs** time to run "Scramble Drill" routes when the initial play breaks down.

### Running Back

- **`Patience`** (Attribute)

  - **Description**: AI behavior governing how long a runner waits behind blockers before accelerating.
  - **Positional Dynamic / Impact**: **Empowers Pulling Guards**: Gives **Offensive Linemen** time to execute slow-developing blocks (Traps/Sweeps) before the runner hits the gap.

- **`Pass Pro Rating`** (Attribute)

  - **Description**: Specific blocking rating for picking up blitzing LBs.
  - **Positional Dynamic / Impact**: **Protects QB**: Directly counters blitzing **Linebackers**, giving the **Quarterback** critical extra seconds in the pocket.

- **`Chip Block`** (Trait)

  - **Description**: The RB "chips" (bumps) a Defensive End on their way out to a route.
  - **Positional Dynamic / Impact**: **Helps Tackles**: Slows down the **Defensive End's** momentum, giving the **Offensive Tackle** an easier win on the edge.

- **`Juke Efficiency`** (Attribute)

  - **Description**: Determines how much momentum/speed is lost when performing a juke move.
  - **Positional Dynamic / Impact**: **Isolates LBs**: Punishes **Linebackers** with low `Agility` by leaving them grasping at air in the open field.

- **`Mismatch Nightmare`** (Trait)
  - **Description**: Grants bonus Catching/Route Running when covered by a Linebacker.
  - **Positional Dynamic / Impact**: **Stresses Defense**: Forces the defense to sub in a **Defensive Back** (Nickel/Dime), weakening their run defense vs the **O-Line**.

### WR / TE

- **`Release`** (Attribute)

  - **Description**: Ability to disengage from Press Coverage at the line of scrimmage.
  - **Positional Dynamic / Impact**: **Timing with QB**: Ensures the receiver is at the spot the **Quarterback** expects on time; failure here causes the QB to hold the ball and get sacked.

- **`Clearout Specialist`** (Trait)

  - **Description**: Tendency to run deep routes at max effort even if not the primary target.
  - **Positional Dynamic / Impact**: **Opens Space for RB/TE**: Draws **Safeties** deep, clearing underneath zones for **Running Backs** and **Tight Ends**.

- **`Possession Receiver`** (Trait)

  - **Description**: Bonus to `Catching` on 3rd down, but strictly limits YAC potential.
  - **Positional Dynamic / Impact**: **Security for QB**: Provides a "Panic Button" option for the **Quarterback** when the pocket collapses.

- **`Blocking Tenacity`** (Attribute)

  - **Description**: Determines how long a WR maintains a block downfield.
  - **Positional Dynamic / Impact**: **Enables RB Home Runs**: Critical for outside runs; prevents **Cornerbacks** from setting the edge, turning 5-yard **RB** gains into 50-yard touchdowns.

- **`Route Specialist`** (RPG)
  - **Description**: Unlocks proficiency tiers for specific routes (e.g., "Master" at Post patterns).
  - **Positional Dynamic / Impact**: **Predictability**: Allows the **QB** to throw "blind" with high trust, effectively countering tight **Man Coverage**.

### Offensive Line

- **`Communication`** (Attribute)

  - **Description**: (Center Specific) The ability to identify the "Mike" LB and shift protection.
  - **Positional Dynamic / Impact**: **Boosts Unit Awareness**: The **Center's** rating buffs the `Awareness` of **Guards/Tackles**, helping them pick up stunts/twists by the **DL**.

- **`Unit Chemistry`** (System)

  - **Description**: Passive bonus to Blocking stats for linemen who have started X consecutive games together.
  - **Positional Dynamic / Impact**: **Unit Cohesion**: Makes a group of average players perform better than 5 unacquainted stars; critical for handling complex **Defensive Fronts**.

- **`Pull Speed`** (Attribute)

  - **Description**: Max speed specifically when executing Pull/Trap blocking assignments.
  - **Positional Dynamic / Impact**: **Unlocks Playbook**: Enables specific run concepts (Power O, Counter) that require the lineman to beat the **Linebacker** to the spot.

- **`Anchor`** (Attribute)

  - **Description**: Resistance specifically to "Bull Rush" moves (distinct from raw Strength).
  - **Positional Dynamic / Impact**: **Pocket Integrity**: Prevents the pocket from collapsing into the **QB's** face, allowing them to step up and throw.

- **`Discipline`** (Attribute)
  - **Description**: Reduces frequency of Holding and False Start penalties.
  - **Positional Dynamic / Impact**: **Momentum Killer**: Low discipline kills drives, putting the **QB** in 1st & 20 situations that force predictable passing (easy for **Defense**).

## Defensive Enhancements

### Defensive Line

- **`First Step`** (Attribute)

  - **Description**: Reaction time to the snap (distinct from Acceleration).
  - **Positional Dynamic / Impact**: **Disrupts Mesh Point**: Can blow up handoffs before they happen, forcing the **RB** to redirect into the arms of waiting **Linebackers**.

- **`Eat Blocks`** (Trait)

  - **Description**: (DT Specific) Tendency/Skill to occupy double teams effectively without giving ground.
  - **Positional Dynamic / Impact**: **Frees Linebackers**: Keeps the **Offensive Guards** occupied, allowing **Linebackers** to scrape and tackle the **RB** untouched.

- **`Gap Integrity`** (Attribute)

  - **Description**: Ability to resist being "sealed" or pushed out of assigned run lane.
  - **Positional Dynamic / Impact**: **Funnels to Help**: Forces the **RB** to cut back into the teeth of the defense (where **LBs/Safeties** are waiting) rather than finding a hole.

- **`Bat Ball`** (Trait)

  - **Description**: AI tendency to jump/swat passes if rush is stalled.
  - **Positional Dynamic / Impact**: **Counters Quick Game**: Negates the **QB's** "Quick Release" advantage by blocking passing lanes at the source.

- **`Intimidation`** (System)
  - **Description**: Sacks/Hits lower the Morale and Attributes of the opposing O-Line for a short duration.
  - **Positional Dynamic / Impact**: **Breaks Will**: Lowers the opposing **O-Line's** blocking ratings, leading to a cascade of pressure that ruins the **QB's** rhythm.

### Linebacker

- **`Green Dot`** (Trait)

  - **Description**: (MLB Specific) Relays defensive play calls and adjustments.
  - **Positional Dynamic / Impact**: **Prevents Blown Coverage**: Reduces the chance of **Secondary (DBs)** miscommunication, preventing wide-open **WR** touchdowns.

- **`Coverage Disguise`** (Attribute)

  - **Description**: Delays the QB's AI recognition of Man vs. Zone coverage.
  - **Positional Dynamic / Impact**: **Baits QB**: Tricks the **Quarterback** into making dangerous throws that **Safeties** can intercept.

- **`Blitz Timing`** (Attribute)

  - **Description**: Effectiveness/Speed boost on delayed blitzes (waiting for gap to open).
  - **Positional Dynamic / Impact**: **Overloads O-Line**: Exploits communication breakdowns in the **Offensive Line**, creating free rushers at the **QB**.

- **`Run Fit`** (Attribute)

  - **Description**: Ability to read the "spill" vs "box" logic of the Defensive Line.
  - **Positional Dynamic / Impact**: **Complementary Football**: Works in tandem with **DL**; if DL spills outside, LB scrapes; if DL boxes inside, LB fills.

- **`The Enforcer`** (Trait)
  - **Description**: Increased Fumble Caused chance on big hits / Tackle sound effect.
  - **Positional Dynamic / Impact**: **Fear Factor**: Causes **WRs** crossing the middle to drop passes (hearing footsteps) even before contact.

### Defensive Back

- **`Press`** (Attribute)

  - **Description**: Ability to jam WR at the line, disrupting timing.
  - **Positional Dynamic / Impact**: **Helps Pass Rush**: Disrupts the timing of the route, forcing the **QB** to hold the ball longer, leading to coverage sacks for the **DL**.

- **`Ball Tracking`** (Attribute)

  - **Description**: AI ability to play the ball in the air (turn head) vs playing the receiver (face guarding).
  - **Positional Dynamic / Impact**: **Turnover Generation**: Turns potential PIs into Interceptions, giving the **Offense** short fields.

- **`Coverage Shell`** (System)

  - **Description**: (Safety) Pre-snap alignment that disguises the true coverage (Cover 2 looks like Cover 3).
  - **Positional Dynamic / Impact**: **Protects Corners**: Allows **Cornerbacks** to play aggressively underneath, knowing the **Safety** help is disguised but present.

- **`Pick Artist`** (Trait)

  - **Description**: Significantly higher catch rate on Interception opportunities.
  - **Positional Dynamic / Impact**: **Game Swing**: Capitalizes on **QB** mistakes forced by **DL** pressure.

- **`Run Support`** (Tendency)
  - **Description**: Willingness to abandon coverage responsibilities to tackle a runner.
  - **Positional Dynamic / Impact**: **Last Line of Defense**: A Safety with high Run Support acts as an extra **Linebacker**, shutting down **RB** breakouts.
