import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";

// Types (should eventually be moved to types/coach.ts)
const CoachTier = {
  LEGEND: "LEGEND",
  ELITE: "ELITE",
  VETERAN: "VETERAN",
  DEVELOPING: "DEVELOPING",
  ROOKIE: "ROOKIE",
} as const;

type CoachTier = (typeof CoachTier)[keyof typeof CoachTier];

const CoachArchetype = {
  GENERALIST: "GENERALIST",
  QB_GURU: "QB_GURU",
  OL_MASTER: "OL_MASTER",
  RUN_GAME_SPECIALIST: "RUN_GAME_SPECIALIST",
  RECEIVING_COACH: "RECEIVING_COACH",
  DB_WHISPERER: "DB_WHISPERER",
  PASS_RUSH_SPECIALIST: "PASS_RUSH_SPECIALIST",
  LB_GURU: "LB_GURU",
  SPECIAL_TEAMS_ACE: "SPECIAL_TEAMS_ACE",
} as const;

type CoachArchetype = (typeof CoachArchetype)[keyof typeof CoachArchetype];

interface CoachCardProps {
  name: string;
  role: string;
  tier: CoachTier | string;
  archetype: CoachArchetype | string;
  playbookOffense?: string;
  playbookDefense?: string;
  experience: number;
}

const CardContainer = styled(motion.div)<{ tier: string }>`
  background: rgba(30, 30, 35, 0.9);
  border-radius: 12px;
  padding: 16px;
  width: 320px;
  position: relative;
  overflow: hidden;
  border: 1px solid ${(props) => getTierBorderColor(props.tier)};
  box-shadow: 0 4px 20px ${(props) => getTierGlow(props.tier)};

  display: flex;
  flex-direction: column;
  gap: 12px;
`;

const TierBadge = styled.div<{ tier: string }>`
  position: absolute;
  top: 12px;
  right: 12px;
  background: ${(props) => getTierColor(props.tier)};
  color: ${(props) => (props.tier === "LEGEND" || props.tier === "ELITE" ? "#000" : "#fff")};
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
`;

const CoachName = styled.h3`
  margin: 0;
  color: #fff;
  font-size: 1.25rem;
  font-weight: 700;
  font-family: "Outfit", sans-serif;
`;

const CoachRole = styled.div`
  color: #aaa;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: -8px;
`;

const ArchetypeSection = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 10px;
  margin-top: 8px;
`;

const Label = styled.div`
  font-size: 0.7rem;
  color: #888;
  text-transform: uppercase;
  margin-bottom: 4px;
`;

const Value = styled.div`
  font-size: 0.95rem;
  color: #e0e0e0;
  font-weight: 600;
`;

const StatGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-top: 4px;
`;

// Helper functions for tier visualization
const getTierColor = (tier: string) => {
  switch (tier) {
    case "LEGEND":
      return "#FFD700"; // Gold
    case "ELITE":
      return "#E0E0E0"; // Silver-ish (Platinum)
    case "VETERAN":
      return "#CD7F32"; // Bronze
    case "DEVELOPING":
      return "#4CAF50"; // Green
    case "ROOKIE":
      return "#2196F3"; // Blue
    default:
      return "#757575";
  }
};

const getTierBorderColor = (tier: string) => {
  switch (tier) {
    case "LEGEND":
      return "rgba(255, 215, 0, 0.5)";
    case "ELITE":
      return "rgba(224, 224, 224, 0.5)";
    default:
      return "rgba(255, 255, 255, 0.1)";
  }
};

const getTierGlow = (tier: string) => {
  switch (tier) {
    case "LEGEND":
      return "rgba(255, 215, 0, 0.2)";
    case "ELITE":
      return "rgba(224, 224, 224, 0.15)";
    default:
      return "rgba(0, 0, 0, 0.3)";
  }
};

const formatArchetype = (arch: string) => {
  return arch.replace(/_/g, " ").replace(/\w\S*/g, (w) => w.replace(/^\w/, (c) => c.toUpperCase()));
};

export const CoachCard: React.FC<CoachCardProps> = ({
  name,
  role,
  tier,
  archetype,
  playbookOffense,
  playbookDefense,
  experience,
}) => {
  return (
    <CardContainer tier={tier} whileHover={{ scale: 1.02 }} transition={{ duration: 0.2 }}>
      <TierBadge tier={tier}>{tier}</TierBadge>

      <div>
        <CoachName>{name}</CoachName>
        <CoachRole>{role}</CoachRole>
      </div>

      <ArchetypeSection>
        <Label>Archetype</Label>
        <Value>{formatArchetype(archetype)}</Value>
      </ArchetypeSection>

      <StatGrid>
        <ArchetypeSection>
          <Label>Experience</Label>
          <Value>{experience} Yrs</Value>
        </ArchetypeSection>

        <ArchetypeSection>
          <Label>Scheme</Label>
          <Value>{playbookOffense || playbookDefense || "Multiple"}</Value>
        </ArchetypeSection>
      </StatGrid>
    </CardContainer>
  );
};
