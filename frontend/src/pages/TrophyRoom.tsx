import { TrophyCaseScene } from "../components/trophy/TrophyCaseScene";
import { LogoTimeline } from "../components/history/LogoTimeline";
import { useTheme } from "../context/useTheme";
import { motion } from "framer-motion";
import "./TrophyRoom.css";

const TrophyRoom = () => {
  const { activeTeam } = useTheme();

  return (
    <div className="trophy-room">
      {/* 3D Scene Layer */}
      <div className="canvas-container">
        <TrophyCaseScene />
      </div>

      {/* UI Overlay Layer */}
      <div className="ui-layer trophy-room__ui-layer">
        <motion.header
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="trophy-room__header"
        >
          <h1 className="trophy-room__title">Hall of Champions</h1>
          <h2 className="trophy-room__subtitle">{activeTeam?.name || "Franchise"} Trophy Case</h2>
        </motion.header>

        <div className="trophy-room__footer w-full max-w-5xl mx-auto z-20">
          <LogoTimeline />
        </div>
      </div>
    </div>
  );
};

export default TrophyRoom;
