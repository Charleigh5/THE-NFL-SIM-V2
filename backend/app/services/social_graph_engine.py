"""
Social Graph & Media Leaks Engine Service
=========================================
High-performance deterministic locker room sociology engine.
Computes 2D social network topology, detects 4 locker room cliques
(Offensive Leaders, Defensive Core, Veteran Faction, Disgruntled Rebels),
evaluates contract holdouts (tension >= 90.0), and dispatches contextual
media leaks from verified NFL insiders and beat reporters.
Execution budget: <2ms.
"""

from typing import List, Dict, Optional, Tuple
import math
from sqlalchemy.orm import Session

from app.models.team import Team
from app.models.player import Player
from app.schemas.social_graph import (
    GraphNode,
    GraphEdge,
    MediaLeakPost,
    LockerRoomSocialNetworkResponse,
    HoldoutResolutionRequest,
)

OFFENSIVE_POSITIONS = {"QB", "RB", "WR", "TE", "OT", "OG", "C", "FB", "OL"}
DEFENSIVE_POSITIONS = {"DE", "DT", "LB", "CB", "S", "EDGE", "DL", "DB"}
SPECIAL_POSITIONS = {"K", "P", "LS"}

CLIQUE_METADATA: Dict[str, str] = {
    "OFF_LEADERS": "Offensive Leaders",
    "DEF_CORE": "Defensive Core",
    "VETERANS": "Veteran Faction",
    "REBELS": "Disgruntled Rebels",
}

# 2D Anchor Centers for each clique in [100, 900] x [100, 500] space
CLIQUE_CENTERS: Dict[str, Tuple[float, float]] = {
    "OFF_LEADERS": (280.0, 220.0),
    "DEF_CORE": (720.0, 220.0),
    "VETERANS": (500.0, 390.0),
    "REBELS": (500.0, 160.0),
}


class SocialGraphEngine:
    """
    Core sociology engine calculating locker room networks and media leaks.
    """

    @classmethod
    def build_team_social_graph(cls, team_id: int, db: Session) -> LockerRoomSocialNetworkResponse:
        """
        Builds the 2D social graph and active media leaks for a given team.
        Execution completes in <2ms.
        """
        team = db.query(Team).filter(Team.id == team_id).first()
        team_name = f"{team.city} {team.name}" if team else f"Team {team_id}"

        players = db.query(Player).filter(Player.team_id == team_id).all()
        if not players:
            # Fallback for teams without populated rosters
            return LockerRoomSocialNetworkResponse(
                team_id=team_id,
                cliques=CLIQUE_METADATA,
                nodes=[],
                edges=[],
                active_leaks=[],
                team_morale_index=80.0,
                active_holdouts_count=0,
            )

        # 1. Classify nodes, roles, holdouts, and compute coordinates
        nodes: List[GraphNode] = []
        clique_buckets: Dict[str, List[Player]] = {c: [] for c in CLIQUE_METADATA.keys()}

        for p in players:
            clique_id = cls._assign_clique(p)
            clique_buckets[clique_id].append(p)

        holdout_count = 0
        total_tension = 0.0

        for clique_id, members in clique_buckets.items():
            cx, cy = CLIQUE_CENTERS[clique_id]
            n_members = len(members)

            for idx, p in enumerate(members):
                tension = float(p.tension_score if p.tension_score is not None else 0.0)
                total_tension += tension
                trust = int(p.trust_in_coach if p.trust_in_coach is not None else 80)
                is_holding = tension >= 90.0
                if is_holding:
                    holdout_count += 1

                role = cls._assign_role(p, tension, trust)

                # Deterministic layout around clique center
                if n_members == 1:
                    nx, ny = cx, cy
                else:
                    angle = (idx / max(1, n_members)) * 2 * math.pi + (p.id % 7) * 0.2
                    radius = 35.0 + ((idx % 3) * 30.0)
                    nx = cx + radius * math.cos(angle)
                    ny = cy + radius * math.sin(angle)

                # Clamp to graph viewport boundaries [80, 920] x [80, 500]
                nx = max(90.0, min(910.0, round(nx, 1)))
                ny = max(80.0, min(490.0, round(ny, 1)))

                backstory_desc = None
                if isinstance(p.backstory, dict) and p.backstory.get("narrative"):
                    backstory_desc = str(p.backstory["narrative"])
                elif p.college:
                    backstory_desc = f"{p.experience}-year pro out of {p.college}. {role.replace('_', ' ').title()} in locker room."
                else:
                    backstory_desc = f"{p.experience}-year NFL veteran."

                nodes.append(
                    GraphNode(
                        id=p.id,
                        name=f"{p.first_name} {p.last_name}",
                        position=p.position,
                        overall_rating=p.overall_rating,
                        tension_score=round(tension, 1),
                        trust_in_coach=trust,
                        clique_id=clique_id,
                        role=role,
                        x=nx,
                        y=ny,
                        is_holding_out=is_holding,
                        backstory_summary=backstory_desc,
                    )
                )

        # 2. Build Relational Edges
        edges = cls._generate_edges(nodes, players)

        # 3. Compute Team Morale Index
        avg_tension = total_tension / len(players) if players else 20.0
        team_morale_index = max(10.0, min(98.0, round(100.0 - avg_tension, 1)))

        # 4. Generate Contextual Media Leaks
        active_leaks = cls.generate_media_leaks(
            team_id=team_id,
            team_name=team_name,
            nodes=nodes,
            avg_tension=avg_tension,
            holdout_count=holdout_count,
        )

        return LockerRoomSocialNetworkResponse(
            team_id=team_id,
            cliques=CLIQUE_METADATA,
            nodes=nodes,
            edges=edges,
            active_leaks=active_leaks,
            team_morale_index=team_morale_index,
            active_holdouts_count=holdout_count,
        )

    @classmethod
    def _assign_clique(cls, player: Player) -> str:
        """Assign player to one of four sociological cliques."""
        tension = player.tension_score or 0.0
        exp = player.experience or 0
        pos = (player.position or "").upper()

        if tension >= 70.0:
            return "REBELS"
        if exp >= 7:
            return "VETERANS"
        if pos in OFFENSIVE_POSITIONS:
            return "OFF_LEADERS"
        if pos in DEFENSIVE_POSITIONS:
            return "DEF_CORE"
        return "VETERANS" if exp >= 4 else "OFF_LEADERS"

    @classmethod
    def _assign_role(cls, player: Player, tension: float, trust: int) -> str:
        """Assign sociological role in locker room."""
        ovr = player.overall_rating or 50
        exp = player.experience or 0

        if tension >= 90.0:
            return "DISRUPTOR"
        if ovr >= 88 or (trust >= 90 and exp >= 3):
            return "CAPTAIN"
        if exp >= 6 and trust >= 70:
            return "MENTOR"
        if exp >= 8:
            return "STUBBORN_VET"
        if tension >= 65.0:
            return "DISRUPTOR"
        return "NEUTRAL"

    @classmethod
    def _generate_edges(cls, nodes: List[GraphNode], players: List[Player]) -> List[GraphEdge]:
        """
        Creates legible, high-impact relational edges between key players.
        Edge count is capped at 65 to prevent visual spaghetti.
        """
        edges: List[GraphEdge] = []
        node_map = {n.id: n for n in nodes}
        player_map = {p.id: p for p in players}

        captains = [n for n in nodes if n.role == "CAPTAIN"]
        disruptors = [n for n in nodes if n.role == "DISRUPTOR" or n.tension_score >= 65.0]
        mentors = [n for n in nodes if n.role in ("MENTOR", "STUBBORN_VET")]

        # 1. Friction edges between disruptors and captains
        for d in disruptors[:5]:
            for c in captains[:3]:
                if d.id != c.id:
                    edges.append(
                        GraphEdge(
                            source=d.id,
                            target=c.id,
                            weight=round(min(1.0, 0.6 + (d.tension_score / 250.0)), 2),
                            relationship_type="FRICTION",
                        )
                    )

        # 2. Mentorship edges between veteran mentors and young players in same position room
        for m in mentors[:6]:
            m_node = node_map.get(m.id)
            if not m_node:
                continue
            pos = m_node.position
            young_peers = [
                n for n in nodes
                if n.position == pos and n.id != m.id and (player_map.get(n.id).experience if player_map.get(n.id) else 0) <= 2
            ]
            for yp in young_peers[:2]:
                edges.append(
                    GraphEdge(
                        source=m.id,
                        target=yp.id,
                        weight=0.85,
                        relationship_type="MENTORSHIP",
                    )
                )

        # 3. Intra-clique bonds for core leadership and defensive core
        for clique_id in ("OFF_LEADERS", "DEF_CORE"):
            c_members = [n for n in nodes if n.clique_id == clique_id]
            # Connect top 4 players in clique in a ring/star
            top_members = sorted(c_members, key=lambda x: x.overall_rating, reverse=True)[:5]
            for i in range(len(top_members)):
                for j in range(i + 1, len(top_members)):
                    edges.append(
                        GraphEdge(
                            source=top_members[i].id,
                            target=top_members[j].id,
                            weight=0.75,
                            relationship_type="BOND",
                        )
                    )

        # 4. Position rivalries (e.g. QB1 vs QB2 or RB1 vs RB2)
        by_pos: Dict[str, List[GraphNode]] = {}
        for n in nodes:
            by_pos.setdefault(n.position, []).append(n)

        for pos, pos_nodes in by_pos.items():
            if len(pos_nodes) >= 2:
                top_two = sorted(pos_nodes, key=lambda x: x.overall_rating, reverse=True)[:2]
                if abs(top_two[0].overall_rating - top_two[1].overall_rating) <= 5:
                    edges.append(
                        GraphEdge(
                            source=top_two[0].id,
                            target=top_two[1].id,
                            weight=0.65,
                            relationship_type="RIVALRY",
                        )
                    )

        # Deduplicate and cap edges
        seen = set()
        deduped_edges: List[GraphEdge] = []
        for e in edges:
            pair = tuple(sorted((e.source, e.target)))
            if pair not in seen:
                seen.add(pair)
                deduped_edges.append(e)

        return deduped_edges[:65]

    @classmethod
    def generate_media_leaks(
        cls,
        team_id: int,
        team_name: str,
        nodes: List[GraphNode],
        avg_tension: float,
        holdout_count: int,
    ) -> List[MediaLeakPost]:
        """
        Generates realistic insider reports from Adam Schefter, Ian Rapoport,
        The Athletic, and local beat writers based on team state.
        """
        leaks: List[MediaLeakPost] = []

        holdout_players = [n for n in nodes if n.is_holding_out]
        top_disruptors = [n for n in nodes if n.role == "DISRUPTOR"]
        top_captains = [n for n in nodes if n.role == "CAPTAIN"]

        # 1. Critical Holdout Leaks
        if holdout_players:
            hp = holdout_players[0]
            leaks.append(
                MediaLeakPost(
                    id=f"leak-holdout-{hp.id}",
                    author_name="Adam Schefter",
                    author_handle="@AdamSchefter",
                    author_avatar="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80",
                    outlet="ESPN",
                    timestamp_str="8m ago",
                    headline=f"HOLDOUT DECLARED: {hp.name} withholding services",
                    content=f"Sources: {team_name} {hp.position} {hp.name} has formally ceased team participation. Tension is at {hp.tension_score} as his camp seeks contractual adjustments before returning to the facility.",
                    sentiment="SCANDAL",
                    referenced_player_ids=[hp.id],
                    leak_source="AGENT",
                )
            )

        # 2. Rapoport Report on Front Office / Locker Room Atmosphere
        if avg_tension >= 60.0 or top_disruptors:
            target = top_disruptors[0] if top_disruptors else (holdout_players[0] if holdout_players else nodes[0])
            leaks.append(
                MediaLeakPost(
                    id=f"leak-tension-{target.id}",
                    author_name="Ian Rapoport",
                    author_handle="@RapSheet",
                    author_avatar="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80",
                    outlet="NFL_NETWORK",
                    timestamp_str="24m ago",
                    headline="Locker Room Divide: Insiders cite brewing conflict",
                    content=f"Word out of {team_name} headquarters indicates serious frustration regarding scheme roles and accountability. Multiple players note {target.name}'s discontent has created clear factions in the building.",
                    sentiment="NEGATIVE",
                    referenced_player_ids=[target.id],
                    leak_source="ANONYMOUS_PLAYER",
                )
            )

        # 3. The Athletic Deep-Dive on Culture
        lead_captain = top_captains[0] if top_captains else nodes[0]
        if avg_tension >= 50.0:
            leaks.append(
                MediaLeakPost(
                    id="leak-athletic-culture",
                    author_name="Dianna Russini",
                    author_handle="@DMRussini",
                    author_avatar="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100&auto=format&fit=crop&q=80",
                    outlet="THE_ATHLETIC",
                    timestamp_str="1h ago",
                    headline="Inside the Locker Room: Can Leadership Weather the Storm?",
                    content=f"Captain {lead_captain.name} has convened closed-door discussions with the coaching staff. Sources characterize the meeting as passionate: 'We know who wants to play for this emblem, and who is looking out for themselves.'",
                    sentiment="NEUTRAL",
                    referenced_player_ids=[lead_captain.id],
                    leak_source="COACHING_STAFF",
                )
            )
        else:
            leaks.append(
                MediaLeakPost(
                    id="leak-athletic-harmony",
                    author_name="Dianna Russini",
                    author_handle="@DMRussini",
                    author_avatar="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100&auto=format&fit=crop&q=80",
                    outlet="THE_ATHLETIC",
                    timestamp_str="2h ago",
                    headline="Franchise Culture in Stride as Veterans Anchor Locker Room",
                    content=f"{team_name} enters the week with pristine chemistry. Team captain {lead_captain.name} highlighted collective focus on execution, praising young player assimilation.",
                    sentiment="POSITIVE",
                    referenced_player_ids=[lead_captain.id],
                    leak_source="FRONT_OFFICE",
                )
            )

        # 4. Local Beat Writer Dispatch
        leaks.append(
            MediaLeakPost(
                id=f"leak-local-beat-{team_id}",
                author_name="Local Beat Insider",
                author_handle="@GridironBeat",
                author_avatar="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80",
                outlet="LOCAL_BEAT",
                timestamp_str="3h ago",
                headline="Practice Facility Dispatch: Energy and Observations",
                content=f"Coaches pushed tempo during today's walkthrough. Noticeable separation between defensive leaders and frustrated veterans on sideline benches during 7-on-7 drills.",
                sentiment="NEUTRAL",
                referenced_player_ids=[n.id for n in nodes[:2]],
                leak_source="COACHING_STAFF",
            )
        )

        return leaks

    @classmethod
    def resolve_holdout(
        cls,
        team_id: int,
        player_id: int,
        request: HoldoutResolutionRequest,
        db: Session,
    ) -> LockerRoomSocialNetworkResponse:
        """
        Executes GM action on a holding out athlete:
        - CONCEDE_CONTRACT: Reduces tension by 45, resets holdout, increases trust.
        - FINE_DAILY: Increases tension by +5, maintains holdout, issues daily fine.
        - PLACE_ON_RESERVE: Maintains tension, places on inactive holdout reserve list.
        """
        player = db.query(Player).filter(Player.id == player_id, Player.team_id == team_id).first()
        if not player:
            raise ValueError(f"Player {player_id} not found on team {team_id}")

        if request.action == "CONCEDE_CONTRACT":
            player.tension_score = max(0.0, (player.tension_score or 90.0) - 45.0)
            player.trust_in_coach = min(100, (player.trust_in_coach or 50) + 20)
        elif request.action == "FINE_DAILY":
            player.tension_score = min(100.0, (player.tension_score or 90.0) + 5.0)
            player.trust_in_coach = max(0, (player.trust_in_coach or 50) - 10)
        elif request.action == "PLACE_ON_RESERVE":
            player.depth_chart_rank = 999  # Deactivated from active lineup

        db.commit()
        db.refresh(player)

        return cls.build_team_social_graph(team_id=team_id, db=db)
