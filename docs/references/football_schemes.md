# Football Schemes Data Extraction

**Source:** Gridiron Architect: Football Scheme Analysis (1970s-Present)
**Purpose:** Structured data for NFL SIM integration
**Extracted:** 2025-12-03

---

## DEFENSIVE SCHEMES

### 1. 4-3 DEFENSE

**Category:** Defense
**Primary Era:** 1950s-Present
**Context:** Both (NFL & NCAA)

#### Historical Meta: 4-3 Defense

- **Pioneer:** Tom Landry (New York Giants)
- **Inception Year:** Early 1950s (popularized)
- **Dominance Period:** 1950s-Present (remains a fundamental building block)

#### Strategic Profile: 4-3 Defense

- **Philosophy:** Create a balanced front that is stout against the run while providing four potential pass rushers. Relies on defined gap responsibilities, allowing players to play fast and attack.
- **Attribute Bias:** Balance, leaning towards Speed/Agility in modern iterations

#### Strengths: 4-3 Defense

- Strong pass rush from four down linemen without needing to blitz linebackers
- Clear one-gap assignments allow for aggressive, penetrating play from linemen
- Generally simpler for players to learn compared to two-gap 3-4 schemes

#### Weaknesses: 4-3 Defense

- Can be susceptible to interior runs if defensive tackles are mismatched or lose their gap
- With only three linebackers, can be out-leveraged by spread formations with multiple receivers
- Requires a specific type of player at each position, particularly an athletic 3-technique DT

#### Mitigation Strategy: 4-3 Defense

- Utilize "sub-packages" like Nickel (replacing a LB with a 5th DB) or Dime (6th DB) to counter pass-heavy and spread formations
- Shift the defensive line ('Under' or 'Over' fronts) to counter offensive strengths

#### Key Position Requirements: 4-3 Defense

##### 3-Technique Defensive Tackle (DT)

- High Strength
- High Block Shedding
- High Power Moves
- Elite Quickness for position
- Role: Engine of the defense, designed to disrupt the A and B gaps
- Prototype: Warren Sapp

##### Weakside Linebacker (WILL)

- High Speed
- High Agility
- High Tackling
- High Play Recognition
- Role: Cover ground, chase down runs, cover RBs/TEs in space
- Prototype: Derrick Brooks

##### Defensive Ends (DE)

- High Speed
- High Acceleration
- High Finesse Moves
- Role: Pure pass rushers responsible for one gap and QB contain

#### Game Theory (Simulation Logic): 4-3 Defense

**Best Against (High Success Rate):**

1. **Pro-Style / Power Run Offenses** - Four-man front can hold its own against heavy offensive lines, allowing linebackers to flow to the ball
2. **Dropback Passing Games** - Can generate pressure with just four rushers, allowing seven defenders to drop into coverage

**Worst Against (Low Success Rate):**

1. **Modern Spread Offenses (without sub-packages)** - Can be out-leveraged by 3x1 or 4-receiver sets, creating mismatches with linebackers on slot receivers
2. **Zone Read / RPO Heavy Schemes** - Puts one-gap defenders in conflict, forcing them to choose between the QB and RB, which can open up lanes

---

#### 4-3 VARIATION: Under Front

**Philosophy:** Shifts the defensive line _away_ from the offensive strength (typically the TE side). The 3-technique DT aligns on the weak side, and the Nose Tackle (1-tech) aligns on the strong side. Designed to create favorable one-on-one matchups for the weakside DE and funnel runs to the athletic WILL linebacker.

**Key Changes:**

- Strongside DE often plays a 5-technique
- SAM linebacker plays closer to the line of scrimmage, almost like a 3-4 OLB

---

#### 4-3 VARIATION: Over Front

**Philosophy:** Shifts the defensive line _towards_ the offensive strength. The 3-technique DT aligns on the strong side (TE side), with the 1-technique NT on the weak side. Creates a powerful front to stop strong-side runs.

---

#### 4-3 VARIATION: Tampa 2

**Category:** Defensive Scheme (often from 4-3)
**Primary Era:** 1990s-2000s
**Context:** NFL

**Pioneer:** Tony Dungy / Monte Kiffin (Tampa Bay Buccaneers), with roots in the 1970s Pittsburgh Steelers "Steel Curtain" defense

**Philosophy:** A "bend-but-don't-break" zone defense that looks like Cover 2 but plays like Cover 3. Aims to prevent big plays by keeping two safeties deep, while using a uniquely athletic Middle Linebacker (MIKE) to drop deep into the middle hole, effectively creating a third deep defender against the pass.

**Attribute Bias:** Speed, IQ, Tackling. Players are often undersized for their positions but must be fast and intelligent.

**Key Position Requirements:**

**Middle Linebacker (MIKE)** - MOST IMPORTANT

- Elite Speed
- Elite Acceleration
- Elite Play Recognition
- Role: Cover the deep middle of the field
- Prototype: Derrick Brooks, Jack Lambert

##### Defensive Tackles (3-Tech)

- Exceptional Quickness
- High Power Moves
- Role: Generate interior pass rush without blitz help
- Prototype: Warren Sapp

##### Cornerbacks

- Excellent open-field tackling
- Physical in run support
- Zone discipline
- Note: Man coverage skill is less critical than zone discipline

**Game Theory:**

- **Best Against:** West Coast Offense (limits YAC and forces short throws), offenses reliant on big plays
- **Worst Against:** Offenses that attack the seams between the CB and Safety, or that isolate a TE/WR on the dropping MIKE linebacker. Strong inside running games can also gash the typically lighter defensive line.

---

#### 4-3 VARIATION: Wide-9 Technique

**Philosophy:** Not a full scheme, but a specific alignment for Defensive Ends. The DE aligns far outside the tackle or tight end (in the "9-technique" gap). The goal is to give the pass rusher a wider angle and a longer runway to build up speed and attack the offensive tackle, prioritizing QB pressure above all else.

**Strengths:**

- Creates one-on-one pass rush opportunities for elite speed rushers

**Weaknesses:**

- Creates a massive C-gap bubble that can be exploited by off-tackle runs and draws if the linebacker doesn't fill it correctly

**Roster Construction:**

- Requires a pure speed rusher at DE with elite Acceleration and Agility

---

### 2. 3-4 DEFENSE

**Category:** Defense
**Primary Era:** 1970s-Present
**Context:** Both (NFL & NCAA)

#### Historical Meta: 3-4 Defense

- **Pioneer:** Bud Wilkinson (University of Oklahoma) in the late 1940s. Chuck Fairbanks brought it to the NFL with the New England Patriots.
- **Inception Year:** ~1974 (NFL)
- **Dominance Period:** Became the predominant NFL defense in the late 1970s and early 1980s. Experienced a major resurgence in the 2000s and remains a core defensive philosophy. [ERA: 1970s-Present]

#### Strategic Profile: 3-4 Defense

- **Philosophy:** To confuse the offense by disguising the fourth pass rusher. With four linebackers, any of them can blitz, drop into coverage, or spy the QB, creating unpredictability. Uses larger defensive linemen to occupy blockers, freeing up linebackers to make plays.
- **Attribute Bias:** Strength and Size on the D-Line, Versatility at Linebacker

#### Strengths: 3-4 Defense

- Flexibility in blitz packages and coverage schemes
- Difficult for offensive lines to identify and block the fourth rusher
- Excellent against the run when employing a two-gap system

#### Weaknesses: 3-4 Defense

- Requires a rare and dominant Nose Tackle who can command a double team
- Can be vulnerable to spread offenses if linebackers are not athletic enough to cover in space
- Fewer dedicated pass rushers on the defensive line compared to a 4-3

#### Mitigation Strategy: 3-4 Defense

- Utilize hybrid OLB/DE players who can both rush the passer and play the run
- Employ zone blitzes to bring pressure from unexpected places while maintaining coverage integrity

#### Key Position Requirements: 3-4 Defense

**Nose Tackle (NT)** - CRITICAL

- Elite Strength
- Elite Toughness
- High Block Shedding
- High Balance
- Size: Often 330lbs+
- Role: Absorb double teams and control the A-gaps (Two-Gap System)

##### Outside Linebackers (OLB/Edge)

- High Versatility
- Blend of Power Moves and Finesse Moves
- High Speed
- Ability to drop into Zone Coverage
- Role: Primary pass rushers of the scheme

##### Defensive Ends (DE) (3-4)

- High Strength
- High Size (280-300lbs)
- Role: In a two-gap system, they are essentially interior linemen responsible for controlling offensive tackles, not rushing the passer

#### Game Theory (Simulation Logic): 3-4 Defense

**Best Against (High Success Rate):**

1. **Pro-Style Offenses** - Can disguise pressure and confuse protection schemes
2. **Run-Heavy Offenses** - Two-gap system excels at stopping the run

**Worst Against (Low Success Rate):**

1. **Modern Spread Offenses** - If linebackers are not athletic enough to cover in space
2. **Quick Passing Games** - Fewer dedicated pass rushers can allow QB time to throw

---

#### 3-4 VARIATION: Two-Gap System (Fairbanks/Bullough/Belichick)

**Philosophy:** A "read and react" system. The three defensive linemen are responsible for controlling the offensive linemen in front of them and defending _two_ gaps. Their job is not to penetrate, but to occupy blockers and hold the point of attack, allowing the four linebackers to read the play and flow to the ball unblocked. Classic "bend-but-don't-break" defense.

**Attribute Bias:** Strength, Size, Discipline

---

#### 3-4 VARIATION: One-Gap System (Wade Phillips Style)

**Philosophy:** An aggressive, attacking system. The three defensive linemen are responsible for shooting _one_ gap. Creates disruption and penetration in the backfield. Relies on more athletic, slightly smaller linemen than a two-gap system. The linebackers then clean up whatever gets through.

**Attribute Bias:** Quickness, Agility, Power Moves

---

### 3. HYBRID DEFENSES

**Category:** Defense
**Primary Era:** 2000s-Present
**Context:** Both (especially College)

**Overview:** Hybrid defenses evolved to counter the rise of pass-heavy spread offenses. They sacrifice size for speed and versatility, often blurring the lines between traditional positions.

---

#### HYBRID VARIATION: 3-3-5 Defense (3-3 Stack)

**Philosophy:** A high-risk, high-reward defense that uses three down linemen, three stacked linebackers, and five defensive backs. Core tenets are speed, versatility, and deception. Aims to confuse offenses with multiple blitzes and coverages from the same pre-snap look.

**Attribute Bias:** Speed, Agility, Versatility

**Strengths:**

- Extremely flexible against formations
- Easy to disguise blitzes and coverages
- Puts maximum team speed on the field

**Weaknesses:**

- Vulnerable to power running games up the middle and off-tackle runs (e.g., Buck Sweep) if the smaller linemen and linebackers get washed out
- The edges are a primary weak point

**Key Position Requirements:**

**Hybrid Overhangs (SS/LB)** - KEY TO THE DEFENSE

- High Agility
- High Speed
- High Tackling
- Role: Often converted safeties or small linebackers who must be able to cover slot receivers man-to-man but also be physical enough to set the edge against the run

##### Stacked Linebackers

- Athletic enough to blitz from depth
- Cover ground from sideline to sideline
- Fill gaps aggressively

**Game Theory:**

- **Best Against:** Spread, Air Raid, and pass-happy offenses that it can confuse and overwhelm with pressure
- **Worst Against:** Power running schemes (I-Form, Double TE) that can exploit its smaller personnel at the point of attack

---

#### HYBRID VARIATION: 4-2-5 Defense (Nickel Base)

**Philosophy:** A modern adaptation designed to be a base defense against spread offenses. Uses a standard 4-man defensive line, but removes one traditional linebacker for a fifth defensive back, often a hybrid Safety/Linebacker type. Allows the defense to maintain a solid run-stopping box (6 defenders) while having the speed and coverage ability to handle 3 or 4 WR sets.

**Hybrid Roles:** The fifth DB is often called a "Rover," "Spur," or "Nickel" and is a key versatile player. This player must be a hybrid of a strong safety and an outside linebacker.

**Key Position Requirements:**

##### Rover/Spur/Nickel

- Coverage skills of a safety
- Tackling/run-support instincts of a linebacker
- High Play Recognition
- High Tackling
- High Agility
- Prototype: Troy Polamalu

---

#### HYBRID VARIATION: 5-2 / Bear Front

**Philosophy:** To cover all three interior offensive linemen (Center and both Guards) with down linemen. This prevents the guards from pulling or climbing to the second level to block linebackers, freeing the LBs to attack the ball carrier. It is an explicitly run-stopping front.

**Alignment:**

- Nose Tackle over the center (0-tech)
- Two Defensive Tackles over the guards (e.g., 2i or 3-tech)
- Two OLBs/DEs line up on the edge

**Game Theory:**

- **Best Against:** Inside zone and gap-scheme running plays
- **Worst Against:** Quick passing games that attack the perimeter, as it often leaves cornerbacks in one-on-one situations with less safety help

---

## OFFENSIVE SCHEMES

### 1. WEST COAST OFFENSE

**Category:** Offense
**Primary Era:** 1980s-Present
**Context:** Both (Primarily NFL)

#### Historical Meta: West Coast Offense

- **Pioneer:** Bill Walsh (Cincinnati Bengals / San Francisco 49ers)
- **Inception Year:** 1970s (developed), 1980s (popularized)
- **Dominance Period:** The 1980s and 1990s with the 49ers dynasty. Its principles are now integrated into almost every modern NFL playbook. [ERA: 1980s-Present]

#### Strategic Profile: West Coast Offense

- **Philosophy:** To use short, horizontal passes as an extension of the running game. The goal is to stretch the defense horizontally, create mismatches, and get the ball to playmakers in space to maximize Yards After Catch (YAC). It is a rhythm and timing-based offense.
- **Attribute Bias:** IQ, Accuracy, Agility

#### Strengths: West Coast Offense

- High-percentage, efficient passing game that controls the clock
- Minimizes risk for the QB with quick throws
- Effective against aggressive pass rushes by getting the ball out fast

#### Weaknesses: West Coast Offense

- Requires extreme precision and timing between the QB and receivers
- Can struggle to generate explosive plays if defenses can tackle well in space
- Vulnerable to physical defenses that can disrupt receivers' routes at the line of scrimmage

#### Mitigation Strategy: West Coast Offense

- Integrate play-action passes off the successful short passing game to create downfield opportunities
- Use motion and varied formations to create favorable matchups pre-snap

#### Key Position Requirements: West Coast Offense

##### Quarterback (QB)

- Elite Short Accuracy
- Elite Decision Making
- High IQ
- Note: Arm strength is secondary to timing and intelligence
- Prototype: Joe Montana

##### Running Back (RB)

- High Catching
- High Route Running
- High Agility
- Role: Dual-threat who can run between the tackles and be a primary receiver out of the backfield
- Prototype: Roger Craig

##### Wide Receivers (WR)

- High Route Running
- High Agility
- Good Hands
- Role: Precise route runners who can create separation in short areas

#### Game Theory (Simulation Logic): West Coast Offense

**Best Against (High Success Rate):**

1. **Aggressive, Blitz-Heavy Defenses** - Gets the ball out before the pass rush can arrive
2. **Man-to-Man Coverage** - Exploits matchups with precise routes and picks/rubs

**Worst Against (Low Success Rate):**

1. **Tampa 2 Defense** - Fast, zone-based defense that limits YAC, keeps everything in front, and rallies to tackle
2. **Physical Press-Man Defenses** - Can disrupt the timing of the routes and throw off the entire offensive rhythm

---

### 2. AIR CORYELL

**Category:** Offense
**Primary Era:** 1970s-1980s
**Context:** NFL

#### Historical Meta: Air Coryell

- **Pioneer:** Don Coryell (San Diego Chargers)
- **Inception Year:** Late 1970s
- **Dominance Period:** Late 1970s to mid-1980s. The Chargers led the NFL in passing yards for a record six straight years (1978-83). Its principles of vertical passing are a staple of modern offenses. [ERA: 1970s-1980s]

#### Strategic Profile: Air Coryell

- **Philosophy:** To stretch the field vertically with complex, timing-based deep passing routes. Uses a power running game to set up play-action and attacks all levels of the defense, aiming for explosive plays.
- **Attribute Bias:** Strength (O-Line), Arm Strength (QB), Speed (WR)

#### Strengths: Air Coryell

- Generates explosive, game-changing plays through the air
- Forces defenses to defend the entire field, which opens up the running game and intermediate routes
- Utilizes a numbered route tree, making play calls efficient

#### Weaknesses: Air Coryell

- Requires elite pass protection to allow deep routes to develop
- Puts immense pressure on the QB to make difficult deep throws
- High-risk, high-reward; can lead to turnovers and stalled drives if timing is off

#### Mitigation Strategy: Air Coryell

- Utilize a versatile TE who can attack the middle of the field to punish defenses that play deep
- Establish a strong power running game to force safeties to creep up, opening deep shots

#### Key Position Requirements: Air Coryell

##### Quarterback (QB) (Air Coryell)

- Elite Deep Accuracy
- Elite Arm Strength
- High Toughness (to stand in the pocket)
- Prototype: Dan Fouts

##### Outside Wide Receivers (X, Z)

- Elite Speed
- High Deep Route Running
- High Ball Skills
- Role: Win one-on-one matchups downfield

##### Offensive Tackles (LT, RT)

- Elite Pass Blocking
- High Strength
- High Balance
- Role: Protect the QB on long-developing plays

##### Hybrid Role: "Move" Tight End

- Size of a TE
- Route-running and receiving skills of a WR
- Role: Create mismatches in the middle of the field
- Prototype: Kellen Winslow Sr.

#### Game Theory (Simulation Logic): Air Coryell

**Best Against (High Success Rate):**

1. **Base Cover 3 / Single-High Safety Defenses** - Creates one-on-one matchups on the outside for deep shots
2. **Run-Stopping Defenses (e.g., Bear Front)** - Can exploit one-on-one coverage on the outside when the defense sells out to stop the run

**Worst Against (Low Success Rate):**

1. **Cover 2 / Cover 4 Defenses** - Two or more deep safeties can take away the deep pass and force the offense to dink and dunk
2. **Defenses with Elite Pass Rushing DEs** - Can disrupt the timing of deep routes before they develop

---

### 3. SPREAD / AIR RAID OFFENSE

**Category:** Offense
**Primary Era:** 1990s-Present
**Context:** Both (Originated in College)

#### Historical Meta: Spread / Air Raid

- **Pioneer:** Hal Mumme & Mike Leach (Iowa Wesleyan, Valdosta State, Kentucky)
- **Inception Year:** Late 1980s / Early 1990s
- **Dominance Period:** Became a dominant force in college football in the 2000s and its concepts have heavily influenced the NFL in the 2010s and beyond. [ERA: 2000s-Present]

#### Strategic Profile: Spread / Air Raid

- **Philosophy:** "Throw short as many times as possible to people who can score." Use horizontal and vertical space to create simple reads for the QB. Relies on a small number of plays run out of multiple formations at a high tempo to overwhelm and fatigue the defense.
- **Attribute Bias:** Speed, Agility, Stamina

#### Strengths: Spread / Air Raid

- Simplifies reads for the QB
- Up-tempo pace prevents defensive substitutions and wears down opponents
- Spreads the defense out, creating favorable one-on-one matchups and running lanes

#### Weaknesses: Spread / Air Raid

- Can be one-dimensional and struggle in bad weather
- Relies on skill players winning individual matchups
- Vulnerable to defenses with athletic defensive backs who can tackle in space and disrupt timing

#### Mitigation Strategy: Spread / Air Raid

- Incorporate a simple but effective run game (like inside zone) to keep the defense honest
- Adapt concepts based on personnel strengths rather than rigidly sticking to the playbook

#### Key Position Requirements: Spread / Air Raid

##### Quarterback (QB) (Spread/Air Raid)

- High Short Accuracy
- High Decision Making
- High Stamina
- Role: Make quick reads and distribute the ball efficiently

**Slot Receivers (Y, H)** - PRIMARY WEAPONS

- Elite Agility
- High Route Running
- Good Hands
- Role: Win matchups in space

##### Offensive Linemen

- High Agility
- High Stamina
- Note: Often uses wider splits and must be athletic enough to pass protect frequently and operate at a high tempo. Size and power are less critical.

#### Game Theory (Simulation Logic): Spread / Air Raid

**Best Against (High Success Rate):**

1. **Base 4-3 / 3-4 Defenses** - Spreads out bigger, slower linebackers and forces them to cover in space
2. **Complex, Disguised Defenses** - The fast tempo and simple reads prevent the defense from getting set and executing complex schemes

**Worst Against (Low Success Rate):**

1. **Nickel/Dime Defenses with good tacklers** - Matches speed with speed and can limit yards after the catch
2. **Press-Man Coverage** - Can disrupt the timing and rhythm of the quick passing game

#### NFL vs. NCAA Nuances

The Air Raid is fundamentally different at the two levels:

**NCAA:** With wider hash marks and generally less athletic defenders, the pure "spread-to-pass" philosophy is highly effective.

**NFL:** Defenses are faster and more disciplined. Therefore, NFL "Air Raid" concepts are usually blended with more traditional pro-style run games and protections. The core principles of spacing and simple reads remain, but they are part of a more balanced attack.

---

### 4. RPO / PISTOL OFFENSE

**Category:** Offense
**Primary Era:** 2010s-Present
**Context:** Both

#### Historical Meta: RPO / Pistol

- **Pioneer (Pistol):** Chris Ault (University of Nevada)
- **Pioneer (RPO):** Rich Rodriguez (West Virginia), with roots in earlier option football
- **Inception Year:** Pistol (~2004), RPO (~Early 2000s, popularized 2010s)
- **Dominance Period:** The RPO became a staple of college football in the 2010s and was adopted by the NFL, famously used by the Philadelphia Eagles in their Super Bowl LII run. The Pistol provides a versatile backfield set for modern offenses. [ERA: 2010s-Present]

#### Strategic Profile: RPO / Pistol

**Philosophy (RPO):** To put a single defensive player (the "read key," usually a linebacker or safety) in a no-win situation. The QB reads this defender post-snap and decides whether to hand off, throw a quick pass, or run. It turns the QB into a "point guard" distributing the ball to the open option.

**Philosophy (Pistol):** To combine the advantages of the shotgun (QB can see the defense) and under-center (downhill running game). The RB's alignment directly behind the QB allows for a powerful north-south run threat that is difficult to achieve from a traditional shotgun set.

**Attribute Bias:** IQ, Decision Making, Versatility

#### Strengths: RPO / Pistol

- **RPO:** Maximizes offensive efficiency by ensuring the offense is never in a "bad" play. Exploits aggressive defenses.
- **Pistol:** Creates a balanced offense that can effectively run downhill or pass without tipping its hand pre-snap.

#### Weaknesses: RPO / Pistol

- **RPO:** Requires a QB with excellent and rapid decision-making skills. Can lead to turnovers if the read is incorrect.
- **Pistol:** The RB's deeper alignment can sometimes make the timing of outside runs and quick passes to the flat slightly slower.

#### Key Position Requirements: RPO / Pistol

##### Quarterback (QB) (RPO/Pistol)

- Elite Decision Making
- High IQ
- Credible threat to run (for QB-run RPOs)
- High Short Accuracy

##### Running Back (RB) (RPO/Pistol)

- High Vision
- High Acceleration
- Must be able to hit the hole quickly in the run game
- Also be a threat as a receiver

#### Game Theory (Simulation Logic): RPO / Pistol

**Best Against (High Success Rate):**

1. **Aggressive, Flow-to-the-Ball Defenses** - The RPO punishes linebackers who commit to the run too quickly by throwing into the space they vacate
2. **Defenses that are weak at the second level** - Puts linebackers and safeties in constant conflict

**Worst Against (Low Success Rate):**

1. **Disciplined Man Coverage Defenses** - Man coverage removes the "conflict" for many defenders, as their assignment is simply to cover their man. This forces the offense to win one-on-one matchups.
2. **Defenses with hyper-athletic LBs/Safeties** - Players who are fast enough to play their run fit and still recover to their pass coverage zone can disrupt RPOs

#### NFL vs. NCAA Nuances (RPO)

**CRITICAL DISTINCTION:** This is one of the most critical distinctions. The NCAA allows offensive linemen to be up to 3 yards downfield on a pass play, while the NFL restricts them to 1 yard. This has massive implications:

**NCAA RPOs:**

- Can be paired with slower-developing, downfield passing concepts because the linemen can legally block further downfield

**NFL RPOs:**

- Must be paired with very quick, horizontal passes (slants, bubbles, flats) to avoid an illegal man downfield penalty
- This makes them more restrictive and easier for disciplined NFL defenses to counter

---

## NFL vs. NCAA - CORE SIMULATION DIFFERENCES

Translating schemes between college and the pros is not a 1:1 process. The following environmental factors must be accounted for in any simulation logic.

### Player Attributes

**NCAA (College):**

- Wider talent disparity
- Elite players vs. average players on the same field
- Speed is a separator

**NFL (Professional):**

- Condensed talent pool
- Everyone is big, strong, and fast
- Intelligence, technique, and discipline become primary separators

**Simulation Impact:**

- NFL players should have a much higher "floor" for physical attributes
- College players have a wider range
- An NFL player's IQ and Technique ratings are more impactful

---

### Field Hash Marks

**NCAA (College):**

- Wider hash marks create a large "field" side and a short "boundary" side

**NFL (Professional):**

- Narrower hash marks make the field more balanced and less situational

**Simulation Impact:**

- In NCAA simulation, offenses can gain a significant advantage by attacking the wide side of the field
- This factor is minimized in the NFL

---

### Key Rules (RPO)

**NCAA (College):**

- Offensive linemen can be 3 yards downfield on a pass

**NFL (Professional):**

- Offensive linemen can only be 1 yard downfield on a pass

**Simulation Impact:**

- Significantly limits the types of pass plays that can be attached to RPOs in the NFL
- College RPOs can have more vertical pass options

---

### Scheme Diversity

**NCAA (College):**

- Extremely diverse
- Gimmicky or niche offenses (e.g., Triple Option, pure Air Raid) can succeed due to talent gaps and less preparation time for opponents

**NFL (Professional):**

- More homogenous
- While schemes vary, they are all complex and must be sound against elite talent
- Gimmicks are quickly exposed

**Simulation Impact:**

- College game logic should allow for a wider variety of viable playbooks
- NFL logic should favor well-rounded, multiple schemes

---

### QB Role

**NCAA (College):**

- Often a primary ball carrier in Spread/Option systems
- A QB's Speed and Agility can be a scheme's foundation

**NFL (Professional):**

- Primarily a passer
- While mobile QBs are valuable, they are rarely used as high-volume designed runners due to injury risk

**Simulation Impact:**

- Designed QB runs should be far more frequent and effective in the NCAA simulation
- In the NFL, QB runs should be more situational (scrambles, occasional options)

---

## SPECIAL TEAMS

**NOTE:** The source document does not contain any information about special teams schemes, formations, strengths, or weaknesses. Special teams data would need to be sourced from a different document.
