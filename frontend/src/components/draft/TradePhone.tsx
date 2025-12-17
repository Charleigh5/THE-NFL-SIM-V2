import React from "react";
import { motion } from "framer-motion";
import { Phone, PhoneIncoming } from "lucide-react";
import "./WarRoom.css";

interface TradePhoneProps {
  onAnswer: () => void;
  hasOffer: boolean;
}

export const TradePhone: React.FC<TradePhoneProps> = ({ onAnswer, hasOffer }) => {
  return (
    <div className={`trade-phone-container ${hasOffer ? "ringing" : ""}`}>
      <motion.button
        className="trade-phone-btn"
        onClick={onAnswer}
        animate={
          hasOffer
            ? {
                rotate: [0, -5, 5, -5, 5, 0],
                scale: [1, 1.1, 1, 1.1, 1],
                boxShadow: ["0 0 0px #ff0000", "0 0 20px #ff0000", "0 0 0px #ff0000"],
              }
            : {}
        }
        transition={{
          duration: 0.5,
          repeat: hasOffer ? Infinity : 0,
          repeatDelay: 1,
        }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        {hasOffer ? <PhoneIncoming size={32} color="#fff" /> : <Phone size={32} color="#888" />}
      </motion.button>

      {hasOffer && <div className="phone-notification-badge">!</div>}

      <div className="phone-label">GM HOTLINE</div>
    </div>
  );
};
