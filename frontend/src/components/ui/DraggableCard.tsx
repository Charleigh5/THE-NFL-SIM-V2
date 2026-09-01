import { PlayerCard } from "./PlayerCard";
import { motion } from "framer-motion";
import { PlayerArchetype } from "../../types/archetypes";

interface DraggableCardProps {
  playerId?: number;
  name: string;
  position: string;
  rating: number;
  team: string;
  jerseyNumber?: number;
  speed?: number;
  strength?: number;
  agility?: number;
  acceleration?: number;
  awareness?: number;
  devTrait?: "NORMAL" | "STAR" | "SUPERSTAR" | "XFACTOR";
  morale?: string;
  className?: string;
  traits?: string[];
  archetype?: PlayerArchetype | string;
  onClick?: () => void;
  testId?: string;
}

export const DraggableCard = (props: DraggableCardProps) => {
  return (
    <motion.div
      drag
      dragConstraints={{ left: 0, right: 0, top: 0, bottom: 0 }}
      dragElastic={0.2}
      whileDrag={{ scale: 1.05, cursor: "grabbing", zIndex: 50 }}
      className="cursor-grab active:cursor-grabbing"
    >
      <PlayerCard {...props} testId={props.testId} />
    </motion.div>
  );
};

export default DraggableCard;
