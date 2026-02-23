#!/usr/bin/env python3
"""
Social Graph Module
===================
Models relationships and social dynamics within a team.

Phase 6: SOCIETY Locker Room Dynamics
- Relationship tracking (friendships, rivalries)
- Clique detection
- Leadership influence
- Chemistry calculation
"""

from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# ENUMS
# ============================================================================


class RelationshipType(str, Enum):
    """Types of social connections."""

    FRIEND = "FRIEND"  # Boosts morale, chemistry
    RIVAL = "RIVAL"  # Boosts competition, splits locker room
    SCHOLAR = "SCHOLAR"  # Mentor/Mentee (boosts XP)
    ENEMY = "ENEMY"  # Lowers chemistry, toxic
    NEUTRAL = "NEUTRAL"


class CliqueType(str, Enum):
    """Types of social cliques."""

    OFFENSE = "OFFENSE"
    DEFENSE = "DEFENSE"
    VETERANS = "VETERANS"
    ROOKIES = "ROOKIES"
    PARTY_CREW = "PARTY_CREW"
    GAMERS = "GAMERS"
    RELIGIOUS = "RELIGIOUS"


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class Relationship:
    """A connection between two entities."""

    source_id: str
    target_id: str
    type: RelationshipType
    strength: float = 0.5  # 0.0 to 1.0
    established_date: int = 0  # Game week established

    @property
    def is_positive(self) -> bool:
        return self.type in [RelationshipType.FRIEND, RelationshipType.SCHOLAR]


@dataclass
class SocialNode:
    """A node in the social graph (Player/Coach)."""

    entity_id: str
    cliques: set[CliqueType] = field(default_factory=set)
    leadership_score: float = 50.0  # 0-100 influence
    morale: float = 50.0  # 0-100 happiness

    # Derived
    influence_radius: float = 1.0


# ============================================================================
# SOCIAL GRAPH ENGINE
# ============================================================================


class SocialGraph:
    """
    Manages social dynamics of a team.

    Functions:
    - Tracks relationships
    - Calculates locker room chemistry
    - Identifies cliques
    - Resolves conflicts
    """

    def __init__(self, team_id: str):
        self.team_id = team_id
        self.nodes: dict[str, SocialNode] = {}
        self.edges: dict[str, list[Relationship]] = {}  # Adjacency list

    def add_node(
        self,
        entity_id: str,
        leadership: float = 50.0,
        morale: float = 50.0,
    ) -> SocialNode:
        """Add a person to the social graph."""
        node = SocialNode(entity_id=entity_id, leadership_score=leadership, morale=morale)
        self.nodes[entity_id] = node
        if entity_id not in self.edges:
            self.edges[entity_id] = []
        return node

    def add_relationship(
        self,
        source_id: str,
        target_id: str,
        rel_type: RelationshipType,
        strength: float = 0.5,
    ) -> Relationship:
        """Create a relationship edge."""
        rel = Relationship(source_id, target_id, rel_type, strength)

        # Ensure nodes exist
        if source_id not in self.nodes:
            self.add_node(source_id)
        if target_id not in self.nodes:
            self.add_node(target_id)

        self.edges[source_id].append(rel)
        return rel

    def get_chemistry_score(self) -> float:
        """
        Calculate overall team chemistry (0-100).

        Based on:
        - Ratio of positive to negative relationships
        - Average morale
        - Clique cohesion
        """
        if not self.nodes:
            return 50.0

        total_rels = 0
        positive_rels = 0.0
        negative_rels = 0.0

        for rels in self.edges.values():
            for r in rels:
                total_rels += 1
                if r.is_positive:
                    positive_rels += r.strength
                elif r.type == RelationshipType.ENEMY:
                    negative_rels += r.strength

        # Base chemistry from morale
        avg_morale = sum(n.morale for n in self.nodes.values()) / len(self.nodes)

        # Relationship modifier
        if total_rels > 0:
            rel_score = (positive_rels - negative_rels * 2) / total_rels
            # Map -1..1 to 0..100ish adjustment
            rel_mod = rel_score * 20
        else:
            rel_mod = 0

        return max(0, min(100, avg_morale + rel_mod))

    def assign_cliques(self, member_traits: dict[str, list[str]]) -> None:
        """
        Assign cliques based on traits.

        Args:
            member_traits: Dict of entity_id -> list of trait strings
        """
        for pid, node in self.nodes.items():
            traits = member_traits.get(pid, [])

            # Logic to assign cliques based on traits
            if "Rookie" in traits:
                node.cliques.add(CliqueType.ROOKIES)
            elif "Veteran" in traits:
                node.cliques.add(CliqueType.VETERANS)

            if "Gamer" in traits:
                node.cliques.add(CliqueType.GAMERS)

            if "PartyAnimal" in traits:
                node.cliques.add(CliqueType.PARTY_CREW)

            # Default positional cliques (would be passed in traits in real system)
            if "Offense" in traits:
                node.cliques.add(CliqueType.OFFENSE)
            elif "Defense" in traits:
                node.cliques.add(CliqueType.DEFENSE)

    def resolve_conflicts(self) -> list[str]:
        """
        Identify and resolve locker room conflicts.

        Returns:
            List of resolution messages.
        """
        resolutions = []
        for pid, node in self.nodes.items():
            # Check for Enemy relationships
            rels = self.edges.get(pid, [])
            enemies = [r for r in rels if r.type == RelationshipType.ENEMY]

            for enemy_rel in enemies:
                # Basic resolution logic: High leadership leader intervenes
                leader = self._find_influential_leader(pid)
                if leader and leader.entity_id != enemy_rel.target_id:
                    # Leader mediates
                    enemy_rel.strength *= 0.8  # Conflict reduces

                    status = "squashed" if enemy_rel.strength < 0.2 else "mediated"
                    if enemy_rel.strength < 0.2:
                        enemy_rel.type = RelationshipType.NEUTRAL

                    resolutions.append(
                        f"Leader {leader.entity_id} {status} beef between {pid} and {enemy_rel.target_id}"
                    )
        return resolutions

    def _find_influential_leader(self, target_pid: str) -> SocialNode | None:
        """Find a leader who can influence the target."""
        # Simplified: Find highest leadership node in same clique
        target = self.nodes.get(target_pid)
        if not target:
            return None

        best_leader = None
        max_leadership = 0.0

        for pid, node in self.nodes.items():
            if pid == target_pid:
                continue

            # Check shared clique
            if not node.cliques.isdisjoint(target.cliques):
                if node.leadership_score > max_leadership:
                    max_leadership = node.leadership_score
                    best_leader = node

        return best_leader if max_leadership > 70 else None
