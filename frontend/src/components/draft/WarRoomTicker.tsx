import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./WarRoom.css";

interface TickerItem {
  id: string;
  type: "PICK" | "TRADE" | "RUMOR" | "NEWS";
  text: string;
  timestamp: string;
}

export const WarRoomTicker: React.FC = () => {
  const [items, setItems] = useState<TickerItem[]>([
    { id: "1", type: "NEWS", text: "Welcome to the 2025 NFL Draft War Room", timestamp: "Now" },
    {
      id: "2",
      type: "RUMOR",
      text: "Sources say Lions looking to trade down from #5",
      timestamp: "2m ago",
    },
    { id: "3", type: "PICK", text: "The Bears are on the clock", timestamp: "Now" },
  ]);

  // Simulate incoming news
  useEffect(() => {
    const interval = setInterval(() => {
      const newRumors = [
        "Vikings aggressive for a QB?",
        "Commanders listening to offers for #2",
        "Generational talent at DE sliding?",
        "Chiefs looking to move into top 10",
      ];
      const randomRumor = newRumors[Math.floor(Math.random() * newRumors.length)];

      const newItem: TickerItem = {
        id: Date.now().toString(),
        type: "RUMOR",
        text: randomRumor,
        timestamp: "Just now",
      };

      setItems((prev) => [newItem, ...prev].slice(0, 5)); // Keep last 5
    }, 8000); // New rumor every 8s

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="war-room-ticker">
      <div className="ticker-label">WAR ROOM LIVE</div>
      <div className="ticker-content">
        <AnimatePresence mode="popLayout">
          {items.map((item) => (
            <motion.div
              key={item.id}
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -20, opacity: 0 }}
              className={`ticker-item type-${item.type.toLowerCase()}`}
            >
              <span className="ticker-time">{item.timestamp}</span>
              <span className="ticker-text">{item.text}</span>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
};
