import { useRef, useState, useEffect } from "react";
import { motion } from "framer-motion";
import { api } from "../../services/api";
import "./LogoTimeline.css";

export interface FranchiseHistoryItem {
  year: string;
  label: string;
  description: string;
}

const DEFAULT_HISTORY: FranchiseHistoryItem[] = [
  {
    year: "1960 - 1980",
    label: "Classic Era",
    description: "The original design that started it all.",
  },
  {
    year: "1981 - 2000",
    label: "Bold Steps",
    description: "Introduced brighter colors and sharper lines.",
  },
  { year: "2001 - Present", label: "Modern Edge", description: "Refined for the digital age." },
];

export const LogoTimeline = ({
  teamId,
  initialHistory,
}: {
  teamId?: number;
  initialHistory?: FranchiseHistoryItem[];
}) => {
  const constraintsRef = useRef(null);
  const [history, setHistory] = useState<FranchiseHistoryItem[]>(initialHistory || DEFAULT_HISTORY);

  useEffect(() => {
    if (teamId) {
      api
        .get<FranchiseHistoryItem[]>(`/api/teams/${teamId}/history`)
        .then((res) => {
          if (res.data && res.data.length > 0) {
            setHistory(res.data);
          }
        })
        .catch(() => {
          // Graceful fallback to default franchise timeline
        });
    }
  }, [teamId]);

  return (
    <div className="logo-timeline">
      <h3 className="logo-timeline__title">Logo Evolution</h3>

      <div ref={constraintsRef} className="logo-timeline__scroll-container">
        <motion.div drag="x" dragConstraints={constraintsRef} className="logo-timeline__track">
          {history.map((era, i) => (
            <motion.div
              key={i}
              whileHover={{ scale: 1.05, boxShadow: "0 0 25px var(--theme-primary)" }}
              className="logo-timeline__era-card"
            >
              {/* Holographic Scanline Effect */}
              <div className="logo-timeline__scanline-effect" />

              <h4 className="logo-timeline__year">{era.year}</h4>
              <div className="logo-timeline__logo-placeholder" />
              <p className="logo-timeline__label">{era.label}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </div>
  );
};
