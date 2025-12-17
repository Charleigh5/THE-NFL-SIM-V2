import { motion } from "framer-motion";
import { Activity, Battery, Skull, Zap } from "lucide-react";
import "./MedicalCenter.css";

interface TreatmentModalProps {
  isOpen: boolean;
  partName: string;
  currentHealth: number;
  onClose: () => void;
  onConfirm: (treatment: string) => void;
}

export const TreatmentModal: React.FC<TreatmentModalProps> = ({
  isOpen,
  partName,
  currentHealth,
  onClose,
  onConfirm,
}) => {
  if (!isOpen) return null;

  const treatments = [
    {
      id: "REST",
      name: "Complete Rest",
      icon: <Battery size={24} className="text-green-400" />,
      desc: "Significant recovery. Player unavailable for practice/games.",
      risk: "Low",
      cost: "1 Week",
    },
    {
      id: "THERAPY",
      name: "Physical Therapy",
      icon: <Activity size={24} className="text-blue-400" />,
      desc: "Moderate recovery. Player limited in practice.",
      risk: "None",
      cost: "Daily",
    },
    {
      id: "INJECTION",
      name: "Pain Injection",
      icon: <Zap size={24} className="text-yellow-400" />,
      desc: "Immediate boost to play through pain. DOES NOT HEAL.",
      risk: "High (Aggravation)",
      cost: "Game Day",
    },
    {
      id: "SURGERY",
      name: "Surgery",
      icon: <Skull size={24} className="text-red-500" />,
      desc: "Full repair of damaged tissue.",
      risk: "Season Ending",
      cost: "Months",
    },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
      <motion.div
        className="bg-gray-900 border border-cyan-500/30 p-6 rounded-xl w-[90%] max-w-lg shadow-2xl"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
      >
        <div className="flex justify-between items-center mb-6 border-b border-gray-700 pb-4">
          <div>
            <h2 className="text-2xl font-bold text-white uppercase tracking-wider">
              {partName} Treatment
            </h2>
            <div className="text-sm text-cyan-400 mt-1">Current Condition: {currentHealth}%</div>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            ✕
          </button>
        </div>

        <div className="space-y-3">
          {treatments.map((t) => (
            <div
              key={t.id}
              onClick={() => onConfirm(t.id)}
              className="group flex items-center gap-4 p-4 rounded-lg border border-gray-700 bg-gray-800/50 hover:bg-gray-800 hover:border-cyan-500/50 cursor-pointer transition-all"
            >
              <div className="p-3 rounded-full bg-gray-900 group-hover:bg-black transition-colors">
                {t.icon}
              </div>
              <div className="flex-1">
                <div className="flex justify-between items-center mb-1">
                  <span className="font-bold text-lg text-gray-200">{t.name}</span>
                  <span className="text-xs font-mono px-2 py-1 rounded bg-gray-900 text-gray-400 border border-gray-700">
                    {t.cost}
                  </span>
                </div>
                <p className="text-sm text-gray-400 mb-2">{t.desc}</p>
                <div className="text-xs uppercase tracking-widest font-bold text-red-400/80">
                  Risk: {t.risk}
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};
