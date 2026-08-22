"""
Coaching Dynasty & Staff Chemistry Service
===========================================
Manages 3-branch coaching skill trees (Scheme Tactics, Player Development, Program Culture)
and multi-coach staff synergy calculations.
"""

from typing import Dict, List, Optional
from app.schemas.deep_dive import (
    CoachingBranch,
    CoachingSkillNode,
    StaffSynergyBreakdown,
    CoachDynastyProfile,
)


class CoachingDynastyService:
    """Service managing coaching dynasty progression, tree unlocks, and staff chemistry."""

    def __init__(self):
        self._tree_catalog = self._initialize_tree_catalog()

    def _initialize_tree_catalog(self) -> Dict[str, CoachingSkillNode]:
        """Define complete 3-branch coaching tree node definitions."""
        return {
            # --- Branch 1: Scheme & Tactics ---
            "SCHEME_DISGUISE_I": CoachingSkillNode(
                id="SCHEME_DISGUISE_I",
                name="Pre-Snap Disguise",
                branch=CoachingBranch.SCHEME_TACTICS,
                tier=1,
                sp_cost=1,
                bonus_description="+5% pre-snap coverage misdirection against opposing QBs",
                stat_multiplier=1.05,
            ),
            "SCHEME_MATCHUP_NIGHTMARE": CoachingSkillNode(
                id="SCHEME_MATCHUP_NIGHTMARE",
                name="Iso-Mismatches",
                branch=CoachingBranch.SCHEME_TACTICS,
                tier=2,
                sp_cost=2,
                bonus_description="+8% route win rate for slot receivers and tight ends",
                prerequisites=["SCHEME_DISGUISE_I"],
                stat_multiplier=1.08,
            ),
            "SCHEME_FOURTH_DOWN_ALGO": CoachingSkillNode(
                id="SCHEME_FOURTH_DOWN_ALGO",
                name="Analytics 4th-Down Edge",
                branch=CoachingBranch.SCHEME_TACTICS,
                tier=3,
                sp_cost=3,
                bonus_description="+12% conversion probability on 4th & 2 or less",
                prerequisites=["SCHEME_MATCHUP_NIGHTMARE"],
                stat_multiplier=1.12,
            ),
            "SCHEME_CHAMPIONSHIP_INSTALL": CoachingSkillNode(
                id="SCHEME_CHAMPIONSHIP_INSTALL",
                name="Master Playbook Architect",
                branch=CoachingBranch.SCHEME_TACTICS,
                tier=4,
                sp_cost=5,
                bonus_description="Tier 4 Mastery: 0 playbook unfamiliarity penalty for all new free agents",
                prerequisites=["SCHEME_FOURTH_DOWN_ALGO"],
                stat_multiplier=1.15,
            ),

            # --- Branch 2: Player Development ---
            "DEV_ROOKIE_ONBOARDING": CoachingSkillNode(
                id="DEV_ROOKIE_ONBOARDING",
                name="Rookie Fast-Track",
                branch=CoachingBranch.DEVELOPMENT,
                tier=1,
                sp_cost=1,
                bonus_description="+15% XP gain for Year 1 rookies during training camp",
                stat_multiplier=1.15,
            ),
            "DEV_TRENCH_DEVELOPER": CoachingSkillNode(
                id="DEV_TRENCH_DEVELOPER",
                name="Trench Whisperer",
                branch=CoachingBranch.DEVELOPMENT,
                tier=2,
                sp_cost=2,
                bonus_description="+10% pass-rush & run-block progression for OL/DL",
                prerequisites=["DEV_ROOKIE_ONBOARDING"],
                stat_multiplier=1.10,
            ),
            "DEV_STAR_MAKER": CoachingSkillNode(
                id="DEV_STAR_MAKER",
                name="X-Factor Catalyst",
                branch=CoachingBranch.DEVELOPMENT,
                tier=3,
                sp_cost=3,
                bonus_description="+20% higher chance for Star dev traits to elevate to Superstar",
                prerequisites=["DEV_TRENCH_DEVELOPER"],
                stat_multiplier=1.20,
            ),
            "DEV_FOUNTAIN_OF_YOUTH": CoachingSkillNode(
                id="DEV_FOUNTAIN_OF_YOUTH",
                name="Age Defier",
                branch=CoachingBranch.DEVELOPMENT,
                tier=4,
                sp_cost=5,
                bonus_description="Tier 4 Mastery: Reduces age-related physical regression by 50% for veterans 30+",
                prerequisites=["DEV_STAR_MAKER"],
                stat_multiplier=1.50,
            ),

            # --- Branch 3: Program & Culture ---
            "CULTURE_LOCKER_ROOM_UNITY": CoachingSkillNode(
                id="CULTURE_LOCKER_ROOM_UNITY",
                name="Brotherhood Culture",
                branch=CoachingBranch.PROGRAM_CULTURE,
                tier=1,
                sp_cost=1,
                bonus_description="-50% morale penalty after tough divisional losses",
                stat_multiplier=1.05,
            ),
            "CULTURE_CAP_DISCIPLINE": CoachingSkillNode(
                id="CULTURE_CAP_DISCIPLINE",
                name="Hometown Loyalty Discount",
                branch=CoachingBranch.PROGRAM_CULTURE,
                tier=2,
                sp_cost=2,
                bonus_description="Re-signing players grant a 5% hometown contract discount",
                prerequisites=["CULTURE_LOCKER_ROOM_UNITY"],
                stat_multiplier=1.05,
            ),
            "CULTURE_PRIME_TIME_SWAGGER": CoachingSkillNode(
                id="CULTURE_PRIME_TIME_SWAGGER",
                name="Big Game Mentality",
                branch=CoachingBranch.PROGRAM_CULTURE,
                tier=3,
                sp_cost=3,
                bonus_description="+3 OVR boost to all starters in playoff and primetime night games",
                prerequisites=["CULTURE_CAP_DISCIPLINE"],
                stat_multiplier=1.10,
            ),
            "CULTURE_DYNASTY_GRAVITAS": CoachingSkillNode(
                id="CULTURE_DYNASTY_GRAVITAS",
                name="Dynasty Magnet",
                branch=CoachingBranch.PROGRAM_CULTURE,
                tier=4,
                sp_cost=5,
                bonus_description="Tier 4 Mastery: Elite free agents prioritize your franchise in Free Agency Wave 1",
                prerequisites=["CULTURE_PRIME_TIME_SWAGGER"],
                stat_multiplier=1.25,
            ),
        }

    def get_coach_profile(
        self,
        coach_id: str,
        name: str,
        role: str,
        level: int = 12,
        current_sp: int = 4,
        unlocked_node_ids: Optional[List[str]] = None,
    ) -> CoachDynastyProfile:
        """Construct full dynasty profile with tree nodes."""
        unlocked_set = set(unlocked_node_ids or ["SCHEME_DISGUISE_I", "DEV_ROOKIE_ONBOARDING", "CULTURE_LOCKER_ROOM_UNITY"])
        nodes = {}
        for nid, template in self._tree_catalog.items():
            node = template.model_copy()
            node.unlocked = nid in unlocked_set
            nodes[nid] = node

        return CoachDynastyProfile(
            coach_id=coach_id,
            name=name,
            role=role,
            level=level,
            current_sp=current_sp,
            total_sp_earned=level * 2,
            archetype="Tactical Mastermind" if "SCHEME_DISGUISE_I" in unlocked_set else "Program Builder",
            tree_nodes=nodes,
        )

    def unlock_node(
        self,
        profile: CoachDynastyProfile,
        node_id: str,
    ) -> bool:
        """
        Attempt to purchase/unlock a coaching tree node.
        Enforces SP availability and prerequisite DAG dependencies.
        """
        if node_id not in profile.tree_nodes:
            return False

        node = profile.tree_nodes[node_id]
        if node.unlocked:
            return False

        if profile.current_sp < node.sp_cost:
            return False

        # Verify all prerequisites are unlocked
        for prereq_id in node.prerequisites:
            prereq_node = profile.tree_nodes.get(prereq_id)
            if not prereq_node or not prereq_node.unlocked:
                return False

        # Apply unlock
        node.unlocked = True
        profile.current_sp -= node.sp_cost
        return True

    def calculate_staff_synergy(
        self,
        hc_scheme: str, # e.g. "WEST_COAST"
        oc_scheme: str, # e.g. "WEST_COAST" or "AIR_RAID"
        dc_scheme: str, # e.g. "COVER_3_ZONE"
        hc_id: str = "HC-01",
        oc_id: str = "OC-01",
        dc_id: str = "DC-01",
    ) -> StaffSynergyBreakdown:
        """
        Calculates organizational chemistry based on scheme compatibility.
        """
        # Offensive synergy
        if hc_scheme == oc_scheme:
            off_score = 95
            off_note = f"Perfect Scheme Lock ({hc_scheme}): +10% play-call execution speed"
        elif "SPREAD" in hc_scheme and "SPREAD" in oc_scheme:
            off_score = 85
            off_note = "Harmonious Spread Philosophies: +5% quick-read accuracy"
        else:
            off_score = 70
            off_note = "Scheme Hybridization: Balanced concepts with minor communication overhead"

        # Defensive synergy
        def_score = 88
        def_note = f"Defensive Autonomy ({dc_scheme}): DC has complete tactical control"

        overall_score = int(round((off_score * 0.55) + (def_score * 0.45)))

        perks = []
        if overall_score >= 90:
            perks.append("Apex Staff Synergy (+5% team OVR in 4th Quarter)")
        if off_score >= 90:
            perks.append("Play-Caller Telepathy (Redzone TD% +8%)")
        if def_score >= 85:
            perks.append("Cohesive Blitz Package (Sack Rate +6%)")

        return StaffSynergyBreakdown(
            head_coach_id=hc_id,
            offensive_coord_id=oc_id,
            defensive_coord_id=dc_id,
            offensive_synergy_score=off_score,
            defensive_synergy_score=def_score,
            overall_chemistry_score=overall_score,
            active_synergy_perks=perks,
            scheme_alignment_notes=[off_note, def_note],
        )


coaching_dynasty_service = CoachingDynastyService()
