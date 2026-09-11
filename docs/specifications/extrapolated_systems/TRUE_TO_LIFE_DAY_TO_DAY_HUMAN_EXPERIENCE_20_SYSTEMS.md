<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025/2026 Production Standard
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, high emotional fidelity, strict types.
</system_context>

# TRUE-TO-LIFE NFL PLAYER & HUMAN EXPERIENCE: 20 DAY-TO-DAY LIFE SYSTEMS
## Extending the 4 Core Modules into Authentic Human & Personal Lived Experiences

---

## 🧭 PHILOSOPHICAL FOUNDATION: THE HUMAN BEHIND THE HELMET

Most sports simulations treat football players as bundles of numeric attributes (SPD, STR, AWR) and financial contracts. In reality, NFL players and coaches are human beings navigating extraordinary pressure, physical vulnerability, financial temptations, family upheaval, and the mundane daily routines of high-stakes corporate athletics.

This specification details **20 day-to-day life spin-off features**—5 for each of the 4 core modules—designed to immerse the user in the lived reality of an NFL player, coach, and family.

```text
                                  +-------------------------------------------------------------+
                                  |              THE HUMAN BEHIND THE HELMET                    |
                                  |         Day-to-Day Lived Experience of the NFL              |
                                  +-------------------------------------------------------------+
                                                                 |
              +--------------------------+-----------------------+-----------------------+--------------------------+
              |                          |                                               |                          |
              V                          V                                               V                          V
     +-----------------+        +-----------------+                             +-----------------+        +-----------------+
     |   MODULE 1      |        |   MODULE 2      |                             |   MODULE 3      |        |   MODULE 4      |
     |   Free Agency   |        |   Locker Room   |                             |   Medical Ctr   |        |   Sideline HUD  |
     |   Family & Life |        |   Facility Life |                             |   The Rehab Grind|       |   Sideline Emotion|
     +-----------------+        +-----------------+                             +-----------------+        +-----------------+
              |                          |                                               |                          |
     +--------+--------+        +--------+--------+                             +--------+--------+        +--------+--------+
     | 5 LIFE SYSTEMS: |        | 5 LIFE SYSTEMS: |                             | 5 LIFE SYSTEMS: |        | 5 LIFE SYSTEMS: |
     | 1.1 Relocation  |        | 2.1 6:30AM Day  |                             | 3.1 Rehab Island|        | 4.1 Surface Pad |
     | 1.2 Rookie Din  |        | 2.2 Fantasy/DMs |                             | 3.2 Whoop Sleep |        | 4.2 Blowups     |
     | 1.3 Podcasts    |        | 2.3 Anxiety Psych|                            | 3.3 Home Care   |        | 4.3 Freeze Heat |
     | 1.4 Moving Panic|        | 2.4 Cafeteria   |                             | 3.4 First Hit   |        | 4.4 Helmet Radio|
     | 1.5 Net Pay Real|        | 2.5 Hotel Curfew|                             | 3.5 Morning Ache|        | 4.5 Equip Swaps |
     +-----------------+        +-----------------+                             +-----------------+        +-----------------+
```

---

## 🏠 MODULE 1: FREE AGENCY & FINANCIAL TRANSITION (The Player & Family Life)

When an athlete signs a contract or gets traded, it is not merely numbers on a cap sheet. In 48 hours, an entire family is uprooted, mortgages are scrambled, children change schools, and unvetted financial hangers-on emerge.

### System 1.1: The 48-Hour Relocation & Family Logistics Hub
- **The Human Reality:** A player signs with a new team on Tuesday afternoon. By Thursday morning, he must report for physicals. His spouse is left behind packing moving boxes, searching for rentals in unfamiliar suburbs, finding pediatricians, and registering kids for schools while living out of a team hotel for 6 weeks.
- **In-Game Mechanics:**
  - When signing a free agent with a family, a **Relocation Stress Meter** ($0-100$) initializes based on distance from home and family status.
  - High relocation stress temporarily reduces practice focus by $-10\%$ during OTAs.
  - GM Action: Franchise can allocate "Player Concierge Services" (relocation coordinator, family housing stipends) that accelerate acclimation and earn $+15$ Player Loyalty.
- **User Touchpoint:** A "Family Relocation & Concierge" card appears upon contract signing. GMs can choose housing packages (Executive Lease, Family Suburb Assistance) with instant family satisfaction ratings.
- **Key Schemas & Files:**
  - `backend/app/schemas/relocation.py` (`RelocationPackage`, `FamilyStressIndex`)
  - `frontend/src/components/freeAgency/RelocationConciergeModal.tsx`

---

### System 1.2: The "Rookie Dinner" & Entourage Financial Pressure Simulator
- **The Human Reality:** The infamous NFL tradition: veteran offensive linemen take rookies to high-end steakhouses, ordering \$3,000 bottles of wine and leaving a rookie 3rd-round pick with a \$28,000 bill. Meanwhile, childhood friends and distant cousins text asking for "seed money" for clothing lines and car washes.
- **In-Game Mechanics:**
  - Financial Stress Index: Tracks player liquidity vs burn rate.
  - Rookie Dinner Event: Veterans test rookie humility. If the rookie refuses or complains publicly, locker room chemistry suffers $-8$; if he pays without fuss, veteran trust increases $+15$.
  - Financial Literacy Counseling: GM can hire certified NFLPA financial advisors to shield young players from predatory advisers and family loans.
- **User Touchpoint:** An interactive event in the War Room showing the rookie's restaurant receipt with comedic itemized line items (Wagyu Tomahawk, 1996 Chateau Margaux) and options to intervene or let team culture handle it.
- **Key Schemas & Files:**
  - `backend/app/engine/society/financial_events.py`
  - `frontend/src/components/society/RookieDinnerEventModal.tsx`

---

### System 1.3: Off-Field Endorsements, Podcasting & Personal Brand Studio
- **The Human Reality:** Modern players (e.g. Travis Kelce, Micah Parsons, Amon-Ra St. Brown) run weekly podcasts, film national Subway commercials, and attend Paris Fashion Week on Tuesday off-days. Balancing stardom with 6:30 AM install meetings is a continuous tightrope.
- **In-Game Mechanics:**
  - Off-Field Brand Value ($0-100$) drives fan merchandise sales and local stadium attendance.
  - Fatigue Trade-Off: Players with high celebrity commitments lose $-5\%$ midweek recovery unless they have high `professionalism` ($\ge 80$).
  - Controversial Podcast Quotes: 5% chance weekly that an off-the-cuff quote on the player's personal podcast generates minor media friction or bulletin-board material for upcoming opponents.
- **User Touchpoint:** Front Office "Media & Brand Studio" showcasing player weekly podcasts, audience subscriber counts, and sponsor approvals.
- **Key Schemas & Files:**
  - `backend/app/schemas/branding.py` (`PodcastEpisode`, `SponsorshipDeal`)
  - `frontend/src/components/frontOffice/PlayerBrandStudio.tsx`

---

### System 1.4: Moving Day Panic & The Midnight Trade Call
- **The Human Reality:** The NFL trade deadline is ruthless. At 3:45 PM, a player is eating a protein bowl in the team cafeteria. At 3:52 PM, his agent calls: "You've been traded to Green Bay. You have a commercial flight at 7:00 PM." He has 30 minutes to empty his locker into trash bags, hug teammates, and call his partner.
- **In-Game Mechanics:**
  - Emotional Shock Modifier: In the first game following a mid-season trade, a player suffers a "Playbook Fog" penalty ($-10\%$ awareness, $-15\%$ route timing) unless they are an 8+ year veteran.
  - Locker Clean-out Cutscene: Cinematic farewell dialogue generated between the traded player and his closest positional teammate.
- **User Touchpoint:** When executing a trade in `TradeCenterPage.tsx`, an authentic "Moving Day Farewell" interstitial displays the player packing his gear with a personal farewell note to the fans.
- **Key Schemas & Files:**
  - `frontend/src/components/trades/MovingDayInterstitial.tsx`
  - `backend/app/services/trades/trade_psychology.py`

---

### System 1.5: The Net Pay Realist & "Jock Tax" Financial Dashboard
- **The Human Reality:** Fans see a "\$10 Million Contract" headline and assume the player has \$10M in the bank. In truth, after the 37% federal bracket, state income tax, city "jock taxes" (filed in every away state they play in), 3% agent fee, 1.5% financial advisor fee, and NFLPA dues, the player takes home less than \$4.8M.
- **In-Game Mechanics:**
  - Itemized Paystub Generator: Breaks down every game check with deductions for Jock Taxes in away game venues (e.g. California away games taxing 13.3% of that week's game check).
  - Financial Discontent Trigger: Younger players with low financial literacy who suddenly face a massive surprise tax bill develop financial anxiety, boosting `greed` tension.
- **User Touchpoint:** Interactive "Player Paystub Inspector" allowing the user to view the exact net take-home calculation of any player contract with line-item disclosures.
- **Key Schemas & Files:**
  - `backend/app/services/capology/jock_tax_calculator.py`
  - `frontend/src/components/freeAgency/ItemizedPaystubModal.tsx`

---

## 🏢 MODULE 2: LOCKER ROOM & FACILITY LIFE (The Normal Day-to-Day Routine)

The NFL is a 7:00 AM to 5:00 PM corporate job inside a high-security athletic facility. The real drama unfolds over cold brew coffee, position meeting pop quizzes, and locker room social hierarchies.

### System 2.1: The 6:30 AM Facility Routine & Install Pop-Quiz Engine
- **The Human Reality:** Wednesday morning. 6:30 AM. Players scan their biometric keycards, weigh in at the nutrition desk, grab breakfast, and walk into the offensive install meeting. The coordinator points the laser pointer at a 2nd-year safety: "Third down, bunch right, what is your check?" Getting it wrong means running laps or losing starter snaps.
- **In-Game Mechanics:**
  - Weekly Preparation Sharpness ($0-100$): Dictated by meeting attendance, sleep metrics, and play-calling IQ.
  - Install Pop-Quiz Event: Coordinator tests players on the opponent's blitz tendencies. High awareness players boost the offensive unit's audibling speed on Sunday.
  - Tardiness Discipline: Late players trigger immediate automated CBA fines (\$1,000 to \$5,000) that can either build accountability or breed resentment.
- **User Touchpoint:** A Wednesday "Install Meeting Room" interactive screen where users observe the coordinator questioning players with instant reaction animations.
- **Key Schemas & Files:**
  - `backend/app/engine/society/facility_routine.py`
  - `frontend/src/components/society/InstallMeetingScreen.tsx`

---

### System 2.2: Fantasy Football Bettor Harassment & Social Media Burner Engine
- **The Human Reality:** A wide receiver drops a pass in the 4th quarter. Within 10 minutes, his Instagram comments and Twitter DMs are flooded with thousands of vile messages from angry fantasy football managers and sports bettors who lost money on his props. Some players delete the apps; others create secret burner accounts to fire back at 2:00 AM.
- **In-Game Mechanics:**
  - Social Media Vitriol Meter: Spikes following dropped passes, blown coverages, or missed field goals in prime-time games.
  - Burner Account Incident: High `paranoia` / high `ego` players have a $15\%$ chance of getting caught arguing with fans on an anonymous burner account, creating a PR headache.
  - Mental Focus Shield: GM can provide dedicated social media managers and digital detox protocols to restore player poise.
- **User Touchpoint:** An incoming notification feed featuring simulated DM screenshots and options for the GM to issue a PR statement or organize a digital detox.
- **Key Schemas & Files:**
  - `backend/app/engine/society/social_media_toxicity.py`
  - `frontend/src/components/society/BurnerAccountAlertModal.tsx`

---

### System 2.3: Sports Psychology & Gameday Anxiety Sanctuary
- **The Human Reality:** Behind the tough exterior, NFL players deal with intense performance anxiety, pre-game vomiting (common for Hall of Fame players like Jim Kelly and Patrick Mahomes), fear of career-ending injury, and the suffocating pressure of 70,000 screaming fans.
- **In-Game Mechanics:**
  - Gameday Composure Rating: Determines how well a player performs under sudden momentum swings or early turnovers.
  - Breathwork & Sports Psychology Consultations: Scheduling weekly sessions with the team sports psychologist raises baseline resilience by $+12$ and prevents late-game fourth-quarter choking.
- **User Touchpoint:** A calming "Mindfulness & Mental Performance" suite in the facility tab showing player stress levels and relaxation therapy schedules.
- **Key Schemas & Files:**
  - `backend/app/services/society/sports_psychology_service.py`
  - `frontend/src/components/society/MentalHealthSuite.tsx`

---

### System 2.4: Cafeteria Social Hierarchy & Unwritten Locker Room Codes
- **The Human Reality:** The team dining hall is high school with millionaires. The offensive line claims two long tables in the back; the defensive backs play dominoes in the corner; the specialists sit quietly by the smoothie bar. Where a rookie sits and whether he observes unwritten rules (e.g., never step on the team logo on the carpet) dictates whether the locker room accepts him.
- **In-Game Mechanics:**
  - Facility Harmony Index: Measures cohesion across positional cliques.
  - Unwritten Rule Violations: Stepping on the carpet crest or playing loud music in the recovery room triggers a peer confrontation that the Team Captain resolves.
- **User Touchpoint:** An interactive architectural top-down map of the facility dining hall showing group seating clusters and chemistry spillover buffs.
- **Key Schemas & Files:**
  - `backend/app/engine/society/cafeteria_dynamics.py`
  - `frontend/src/components/society/FacilityDiningMap.tsx`

---

### System 2.5: Saturday Night Away Hotel Curfew & Roommate Bond
- **The Human Reality:** On Saturday evening before an away game, the team stays in a sequestered suburban Marriott. Team chapel/Bible study at 7:00 PM, snack buffet at 8:30 PM, and hard curfew at 11:00 PM. Security guards sit by the elevators, and coaches knock on doors with clipboards.
- **In-Game Mechanics:**
  - Curfew Adherence Check: A player with low professionalism has a $3\%$ risk of a curfew violation (slipping out or having unauthorized guests), causing benching or heavy fines.
  - Roommate Chemistry Bonus: Roommates paired across complementary positions (e.g. QB + Center, CB + Free Safety) gain $+8\%$ communication synergy on field.
- **User Touchpoint:** Friday evening travel roster management where the coach manually pairs hotel room assignments and checks off the 11:00 PM security report.
- **Key Schemas & Files:**
  - `backend/app/engine/society/hotel_curfew_service.py`
  - `frontend/src/components/society/RoommateAssignmentModal.tsx`

---

## 🏥 MODULE 3: THE MEDICAL CENTER & REHABILITATION (The Human Pain)

Injuries in pro football are not numbers in a medical report; they are physically agonizing, mentally isolating journeys where players feel disconnected from their brotherhood while enduring relentless physical therapy.

### System 3.1: The "Rehab Island" Isolation & Identity Crisis
- **The Human Reality:** When a player tears an ACL, he goes from the idol of thousands to "Rehab Island". While the team laughs and runs drills on the practice field under the sun, the injured player sits inside a quiet training room with an ice compression cuff on his knee, wondering if he will ever run full speed again.
- **In-Game Mechanics:**
  - Alienation Penalty: Injured players on IR for $> 4$ weeks lose $-15\%$ connection to team chemistry and face depression risks that slow physical tissue healing by $20\%$.
  - "Sideline Presence" Countermeasure: Inviting injured veterans to travel on away trips and stand on the sideline with headsets keeps their morale at $+20$ and accelerates recovery.
- **User Touchpoint:** An "Injured Player Well-Being" card in `MedicalCenter.tsx` with options to assign mentor duties or travel passes to keep them connected to the team.
- **Key Schemas & Files:**
  - `backend/app/services/medical/rehab_psychology.py`
  - `frontend/src/components/medical/RehabIslandStatusCard.tsx`

---

### System 3.2: Biometric Sleep, Nutrition & Recovery Tracking (Whoop/Oura/Hyperbaric)
- **The Human Reality:** Elite athletes do not just lift weights; their entire 24-hour cycle is measured. They wear biometric bands tracking REM sleep percentages, heart rate variability (HRV), skin temperature, and drink tailored electrolyte shakes concocted by team dietitians.
- **In-Game Mechanics:**
  - Daily Biometric Strain & Recovery Matrix: Sleep hours + HRV + Caloric Balance dictate weekly muscle recovery speed.
  - Sleep Deprivation Events: A player who welcomed a newborn child at 3:00 AM arrives with a low HRV score ($-15\%$ cognitive reaction time).
- **User Touchpoint:** A high-tech "Biometric Telemetry Deck" displaying real-time HRV recovery gauges, sleep performance rings, and nutrition compliance charts for the 53-man roster.
- **Key Schemas & Files:**
  - `backend/app/schemas/biometrics_telemetry.py`
  - `frontend/src/components/medical/BiometricTelemetryDeck.tsx`

---

### System 3.3: Family Caretaking & The Post-Surgery Home Burden
- **The Human Reality:** After major surgery (rotator cuff, ankle fusion), a 310-pound offensive lineman cannot walk up stairs, take a shower unassisted, or pick up his infant daughter. His partner becomes a full-time nurse, changing wound dressings, driving him to PT, and managing emotional volatility caused by pain medication.
- **In-Game Mechanics:**
  - Home Support Factor: Players with strong family support systems experience $25\%$ fewer surgical complications and adhere to rehab protocols more consistently.
  - Home Health Care Grant: The franchise can authorize in-home nursing support, reducing home caregiver fatigue and improving player healing rates.
- **User Touchpoint:** A post-op recovery profile displaying the player's home recovery status, caregiver assistance, and comfort levels.
- **Key Schemas & Files:**
  - `backend/app/schemas/home_recovery.py`
  - `frontend/src/components/medical/HomeCareStatusModal.tsx`

---

### System 3.4: Return-to-Contact Psychological Hurdle & Hesitation Modeling
- **The Human Reality:** Being "medically cleared" is only half the battle. When a running back returns from an ACL tear, his brain screams at him not to plant his foot on a wet field. If he hesitates for a split second, he gets tackled for a 3-yard loss.
- **In-Game Mechanics:**
  - Hesitation Factor ($\eta$): Starts at $35\%$ upon clearance and decays by $5\%$ per full-contact practice session.
  - On-Field Impact: High hesitation slows cut acceleration by $-20\%$ and reduces break-tackle efficiency until the player takes his first true big hit.
  - The "First Hit" Breakthrough: Surviving a major tackle in game action clears the psychological block, resetting hesitation to $0.0$.
- **User Touchpoint:** A "Confidence in Joint" slider in the medical clearance screen indicating whether the athlete feels ready or needs another week of non-contact work.
- **Key Schemas & Files:**
  - `backend/app/engine/medical/hesitation_engine.py`
  - `frontend/src/components/medical/ReturnToContactAssessment.tsx`

---

### System 3.5: The Morning Ache & Chronic Veteran Body Maintenance
- **The Human Reality:** A 10-year veteran offensive guard does not simply get out of bed on Monday morning. His fingers are crooked, his knees pop like bubble wrap, and his back requires 30 minutes of heating pads and foam rollers before he can stand upright.
- **In-Game Mechanics:**
  - Chronic Wear Index: Increases each year in the league, reducing Monday/Tuesday practice energy.
  - "Veteran Rest Days": Veteran stars over age 30 can be granted "Wednesday Veteran Days Off", preserving their joints for Sunday while younger backups get first-team practice reps.
- **User Touchpoint:** A "Practice Load Management" schedule in `TrainingCenter.tsx` allowing 1-click Wednesday rest day passes for seasoned veterans.
- **Key Schemas & Files:**
  - `backend/app/services/training/load_management.py`
  - `frontend/src/components/training/VeteranLoadManagementCard.tsx`

---

## 🏟️ MODULE 4: SIDELINE EMOTION & GAMEDAY CHAOS (The Raw Gameday Reality)

Gameday on the sideline is a sensory overload of adrenaline, freezing temperatures, tablet video scrubbing, screaming coaches, and equipment emergencies.

### System 4.1: Microsoft Surface Tablet Overhead Breakdown & Frantic Adjustments
- **The Human Reality:** Between offensive drives, the quarterback and pass game coordinator sit on the bench huddled over Microsoft Surface tablets, frantically swiping through black-and-white aerial stills to diagnose why the safety rotated down into Cover 3 instead of Cover 2.
- **In-Game Mechanics:**
  - Sideline Film Adjustment Buff: Spending sideline time reviewing tablet photos grants $+15\%$ blitz pickup awareness on the subsequent offensive drive.
  - Tablet Frustration: In high-tension games, frustrated quarterbacks have a $2\%$ chance of slamming the tablet on the bench, triggering camera cutaways.
- **User Touchpoint:** An interactive "Tablet Overhead Analysis" drawer popping up during changes of possession displaying aerial coverage diagrams.
- **Key Schemas & Files:**
  - `backend/app/engine/simulation/sideline_adjustments.py`
  - `frontend/src/components/game/SurfaceTabletView.tsx`

---

### System 4.2: Sideline Heated Confrontations & Player-Coach Blowups
- **The Human Reality:** A wide receiver running wide open all game doesn't get a target. On the sideline, he slams his helmet against the turf, gets in the offensive coordinator's face, and yells: "Throw me the damn ball!" A veteran tackle steps in to separate them while the head coach grabs the headset.
- **In-Game Mechanics:**
  - Sideline Blowup Trigger: Occurs when high `ego` star targets $< 2$ through 3 quarters while team trails.
  - Instant Coach Intervention: User has 10 seconds to choose a response:
    - *Back the Coordinator*: Restores coach authority; player pouts on bench.
    - *Promise the Next Drive*: Increases player focus by $+10$; mandates targeted pass on next possession.
    - *Bench for Conduct*: Maintains discipline; loses star weapon.
- **User Touchpoint:** A cinematic sideline prompt with high-intensity audio and 3 immediate coaching action buttons.
- **Key Schemas & Files:**
  - `backend/app/engine/simulation/sideline_blowup.py`
  - `frontend/src/components/game/SidelineConfrontationModal.tsx`

---

### System 4.3: Weather Brutality: Benches, Heaters & Frozen Fingers
- **The Human Reality:** Playing in -5 degree wind chill at Lambeau Field in December is pure torture. Hands go numb within 3 minutes; players huddle around giant propane torpedo heaters, drink hot chicken broth, and slather petroleum jelly on bare arms to block the biting wind.
- **In-Game Mechanics:**
  - Thermal Comfort Meter: When ambient temp $< 25^\circ\text{F}$, ball security degrades by $-25\%$ unless players use sideline thermal heaters and hand-warmer pouches.
  - Halftime IV Hydration: In extreme Florida heat ($> 95^\circ\text{F}$), players lose 8-10 lbs of water weight, requiring halftime IV saline infusions to prevent cramping.
- **User Touchpoint:** Animated sideline weather environmental widgets showing glowing torpedo heaters, shivering avatars, and sideline hot beverage meters.
- **Key Schemas & Files:**
  - `backend/app/engine/physics/sideline_thermal_engine.py`
  - `frontend/src/components/game/SidelineThermalWidget.tsx`

---

### System 4.4: Green-Dot Helmet Radio Failure & Sideline Signal Chaos
- **The Human Reality:** The defensive captain has a "green dot" sticker on his helmet with a speaker connected to the defensive coordinator in the coach's box. With 14 seconds on the play clock in a loud stadium, the radio static cuts out. The middle linebacker desperately waves his arms looking at the sideline for hand signals.
- **In-Game Mechanics:**
  - Radio Malfunction Event: $1\%$ chance per quarter of a 30-second headset communication failure.
  - Sideline Hand-Signal Fallback: Forces offensive/defensive units to rely on sideline placards and arm gestures, introducing a $-10\%$ execution delay and vulnerability to sign-stealing.
- **User Touchpoint:** An amber "COMMUNICATION BREAKDOWN" alert flashing on the HUD with simplified visual play cards.
- **Key Schemas & Files:**
  - `backend/app/engine/simulation/helmet_radio_service.py`
  - `frontend/src/components/game/RadioStaticAlert.tsx`

---

### System 4.5: Emergency Sideline Equipment Swaps & Rapid Spat Taping
- **The Human Reality:** A running back's face mask gets bent in a violent goal-line pile-up. He has 40 seconds before the next play. Equipment managers sprint with cordless power drills, replacing the mask in 25 seconds flat. Meanwhile, a cornerback gets his cleats swapped from 1/2-inch to 3/4-inch studs because of sudden rain.
- **In-Game Mechanics:**
  - Equipment Malfunction Triage: Broken chin straps, cleat blowouts, torn jerseys. If equipment cannot be repaired in 40 seconds, the team must burn a timeout or substitute the backup.
  - Cleat Adjustment Buff: Swapping cleat stud length on a wet field restores $+15\%$ change-of-direction traction.
- **User Touchpoint:** A sideline equipment bench tray showing quick cleat/helmet repair status bars.
- **Key Schemas & Files:**
  - `backend/app/engine/simulation/equipment_triage.py`
  - `frontend/src/components/game/EquipmentStaffBench.tsx`

---

## 📊 SUMMARY: 20 TRUE-TO-LIFE SYSTEM SPECIFICATION INDEX

| Mod | Life System ID | Human Reality Focus | Core Gameplay Impact | Primary UI / Component |
| :--- | :--- | :--- | :--- | :--- |
| **M1** | **1.1** | **48-Hour Relocation & Family** | Stress reduces OTA focus; concierge buffs loyalty | `RelocationConciergeModal.tsx` |
| M1 | **1.2** | **Rookie Dinner & Entourages** | Steakhouse bills, loan requests & wealth guidance | `RookieDinnerEventModal.tsx` |
| M1 | **1.3** | **Podcasts & Brand Stardom** | Merchandise revenue vs weekly fatigue trade-offs | `PlayerBrandStudio.tsx` |
| M1 | **1.4** | **Midnight Trade Moving Panic** | Immediate locker clean-outs & playbook fog | `MovingDayInterstitial.tsx` |
| M1 | **1.5** | **Net Take-Home Jock Taxes** | Itemized check deductions in away states | `ItemizedPaystubModal.tsx` |
| **M2** | **2.1** | **6:30 AM Install Pop-Quizzes** | Morning meeting sharpness & tardiness fines | `InstallMeetingScreen.tsx` |
| M2 | **2.2** | **Fantasy Bettor Hate & Burners** | Social vitriol, DM harassment & secret accounts | `BurnerAccountAlertModal.tsx` |
| M2 | **2.3** | **Sports Psychology & Anxiety** | Pre-game vomiting, composure & breathwork | `MentalHealthSuite.tsx` |
| M2 | **2.4** | **Dining Hall Hierarchy & Codes** | Where cliques sit & unwritten locker room laws | `FacilityDiningMap.tsx` |
| M2 | **2.5** | **Saturday Night Away Curfew** | 11 PM room checks & roommate chemistry synergy | `RoommateAssignmentModal.tsx` |
| **M3** | **3.1** | **Rehab Island Loneliness** | Post-op isolation, mental health & sideline passes | `RehabIslandStatusCard.tsx` |
| M3 | **3.2** | **Biometric Sleep & Telemetry** | Whoop/Oura HRV sleep scores & newborn fatigue | `BiometricTelemetryDeck.tsx` |
| M3 | **3.3** | **Family Post-Op Home Burden** | Spouse as full-time nurse & home health grants | `HomeCareStatusModal.tsx` |
| M3 | **3.4** | **Return-to-Contact Hesitation** | Psychological fear of planting foot until first hit | `ReturnToContactAssessment.tsx` |
| M3 | **3.5** | **Chronic Veteran Morning Ache** | Monday arthritis, foam rolling & Wednesday off-days | `VeteranLoadManagementCard.tsx` |
| **M4** | **4.1** | **Surface Tablet Sideline Film** | Huddling on benches over overhead defense photos | `SurfaceTabletView.tsx` |
| M4 | **4.2** | **Heated Sideline Blowups** | Star WR helmet slams, screaming & coach choices | `SidelineConfrontationModal.tsx` |
| M4 | **4.3** | **Freezing Weather Torpedo Heaters** | Frozen fingers, petroleum jelly & chicken broth | `SidelineThermalWidget.tsx` |
| M4 | **4.4** | **Helmet Radio Green-Dot Failure** | Static on headset & emergency sideline hand signals | `RadioStaticAlert.tsx` |
| M4 | **4.5** | **Equipment Drills & Cleat Swaps** | Cordless drills fixing face masks in 25 seconds | `EquipmentStaffBench.tsx` |

---
