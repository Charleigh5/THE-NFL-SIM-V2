import { CoachingStyleType } from "../../types/training";
import { Dumbbell, Brain, Scale, Sword } from "lucide-react";

interface CoachingStylePickerProps {
  currentStyle: CoachingStyleType;
  onStyleSelect: (style: CoachingStyleType) => void;
}

const STYLES = [
  {
    type: CoachingStyleType.VOLUME,
    label: "High Volume",
    icon: Dumbbell,
    desc: "Max reps. High XP, High Fatigue.",
    color: "text-amber-400",
  },
  {
    type: CoachingStyleType.INTENSITY,
    label: "High Intensity",
    icon: Sword,
    desc: "Game speed. Max XP, High Injury Risk.",
    color: "text-red-500",
  },
  {
    type: CoachingStyleType.SMART,
    label: "Smart & Balanced",
    icon: Brain,
    desc: "Data-driven. Moderate gains, Low Risk.",
    color: "text-cyan-400",
  },
  {
    type: CoachingStyleType.OLD_SCHOOL,
    label: "Old School",
    icon: Scale,
    desc: "Grit & tough love. Boosts physicals, lowers morale.",
    color: "text-stone-400",
  },
];

export const CoachingStylePicker = ({ currentStyle, onStyleSelect }: CoachingStylePickerProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {STYLES.map((style) => {
        const Icon = style.icon;
        const isSelected = currentStyle === style.type;

        return (
          <div
            key={style.type}
            onClick={() => onStyleSelect(style.type)}
            className={`
              relative p-4 rounded-xl border cursor-pointer transition-all
              ${
                isSelected
                  ? "bg-white/10 border-white/40 ring-1 ring-white/20"
                  : "bg-black/20 border-white/5 hover:bg-white/5"
              }
            `}
          >
            <div className={`flex items-center gap-3 mb-2 ${style.color}`}>
              <Icon className="w-5 h-5" />
              <h3 className="font-bold text-sm tracking-wide">{style.label}</h3>
            </div>
            <p className="text-xs text-gray-400 leading-relaxed">{style.desc}</p>
          </div>
        );
      })}
    </div>
  );
};
