import { PlayerCard } from "./PlayerCard";

// Note: We need to install @react-spring/web if not present, or use framer-motion.
// Since we installed framer-motion, let's use that instead for simplicity if possible,
// but use-gesture works best with react-spring.
// I'll assume react-spring/web is needed or I can use standard style transforms.
// Let's use a simple style transform for now to avoid extra deps if possible,
// OR just install @react-spring/web.
// Actually, let's use framer-motion's drag controls since we have it.

import { motion } from "framer-motion";

interface DraggableCardProps {
  name: string;
  position: string;
  rating: number;
  team: string;
  onClick?: () => void;
}

export const DraggableCard = (props: DraggableCardProps) => {
  return (
    <motion.div
      drag
      dragConstraints={{ left: 0, right: 0, top: 0, bottom: 0 }} // Free drag but snaps back (for demo)
      dragElastic={0.2}
      whileDrag={{ scale: 1.05, cursor: "grabbing", zIndex: 50 }}
      className="cursor-grab active:cursor-grabbing"
    >
      <PlayerCard {...props} />
    </motion.div>
  );
};
