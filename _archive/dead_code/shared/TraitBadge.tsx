import { motion } from "framer-motion";
import "./TraitBadge.css";

interface TraitBadgeProps {
  name: string;
  tier: "GOLD" | "SILVER" | "BRONZE" | "COMMON";
  description?: string;
  iconUrl?: string;
}

export const TraitBadge = ({ name, tier, description, iconUrl }: TraitBadgeProps) => {
  const tierStyles: Record<string, string> = {
    GOLD: "badge-gold",
    SILVER: "badge-silver",
    BRONZE: "badge-bronze",
    COMMON: "badge-common",
  };

  return (
    <motion.div
      className={`trait-badge ${tierStyles[tier]}`}
      whileHover={{ scale: 1.1 }}
      title={description || name}
    >
      {iconUrl ? (
        <img src={iconUrl} alt={name} className="badge-icon" />
      ) : (
        <span className="badge-initial">{name.charAt(0)}</span>
      )}
      <span className="badge-name">{name}</span>
    </motion.div>
  );
};
