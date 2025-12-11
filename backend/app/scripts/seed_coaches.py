"""
Seed Coaches Script
===================
Seeds the database with 2025 NFL coaching staff data.

Usage:
    python -m app.scripts.seed_coaches
"""

import sys
from pathlib import Path
from sqlalchemy.orm import Session

# Add backend directory to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.core.database import SessionLocal
from app.models.team import Team
from app.models.coach import Coach
from app.data.coaches import COACHES_DB


def seed_coaches():
    """
    Seed all coaching staff for 32 NFL teams.

    Creates Head Coach, Offensive Coordinator, and Defensive Coordinator
    for each team with their playbook schemes and philosophy.
    """
    db: Session = SessionLocal()
    try:
        print("Seeding coaches...")
        coaches_created = 0
        coaches_updated = 0

        for team_abbr, staff_data in COACHES_DB.items():
            # Find the team
            team = db.query(Team).filter(Team.abbreviation == team_abbr).first()
            if not team:
                print(f"  ⚠️  Team {team_abbr} not found in database. Skipping...")
                continue

            # Define coaching roles to create/update
            roles = [
                ("Head Coach", staff_data.head_coach, staff_data.playbook_offense.value, staff_data.playbook_defense.value),
                ("Offensive Coordinator", staff_data.offensive_coordinator, staff_data.playbook_offense.value, None),
                ("Defensive Coordinator", staff_data.defensive_coordinator, None, staff_data.playbook_defense.value),
            ]

            for role, coach_data, off_scheme, def_scheme in roles:
                # Check if coach already exists for this team/role
                existing = db.query(Coach).filter(
                    Coach.team_id == team.id,
                    Coach.role == role
                ).first()

                philosophy_dict = {
                    "run_pass_ratio": staff_data.philosophy.run_pass_ratio,
                    "blitz_frequency": staff_data.philosophy.blitz_frequency,
                    "aggressiveness": staff_data.philosophy.aggressiveness,
                    "tempo": staff_data.philosophy.tempo,
                }

                if existing:
                    # Update existing coach
                    existing.first_name = coach_data.first_name
                    existing.last_name = coach_data.last_name
                    if off_scheme:
                        existing.playbook_offense = off_scheme
                    if def_scheme:
                        existing.playbook_defense = def_scheme
                    if role == "Head Coach":
                        existing.philosophy = philosophy_dict
                    coaches_updated += 1
                else:
                    # Create new coach
                    new_coach = Coach(
                        first_name=coach_data.first_name,
                        last_name=coach_data.last_name,
                        role=role,
                        team_id=team.id,
                        playbook_offense=off_scheme if off_scheme else None,
                        playbook_defense=def_scheme if def_scheme else None,
                        philosophy=philosophy_dict if role == "Head Coach" else {},
                        offense_rating=70 if role in ["Head Coach", "Offensive Coordinator"] else 50,
                        defense_rating=70 if role in ["Head Coach", "Defensive Coordinator"] else 50,
                        development_rating=65,
                    )
                    db.add(new_coach)
                    coaches_created += 1

            print(f"  ✓ {team_abbr}: {staff_data.head_coach.last_name} (HC), "
                  f"{staff_data.offensive_coordinator.last_name} (OC), "
                  f"{staff_data.defensive_coordinator.last_name} (DC)")

        db.commit()
        print(f"\n✅ Coaches seeded successfully!")
        print(f"   Created: {coaches_created}")
        print(f"   Updated: {coaches_updated}")

    except Exception as e:
        print(f"❌ Error seeding coaches: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_coaches()
