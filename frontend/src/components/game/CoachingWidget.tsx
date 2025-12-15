import { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { useSimulationStore } from "../../store/useSimulationStore";
import "./CoachingWidget.css";

interface Philosophy {
  run_pass_ratio: number;
  aggressiveness: number;
  tempo: number;
  fourth_down_aggression: number;
  clock_management_style: string;
}

export const CoachingWidget = ({ teamId }: { teamId: number }) => {
  const [philosophy, setPhilosophy] = useState<Philosophy | null>(null);
  const { gameState } = useSimulationStore();
  const activeStrategy = gameState.clockStrategy || "NORMAL";

  const aggressionBarRef = useRef<HTMLDivElement>(null);
  const tempoBarRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get(`/api/teams/${teamId}/coach/settings`);
        setPhilosophy(res.data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchData();
  }, [teamId]);

  useEffect(() => {
    if (philosophy) {
      if (aggressionBarRef.current) {
        aggressionBarRef.current.style.width = `${philosophy.aggressiveness}%`;
      }
      if (tempoBarRef.current) {
        tempoBarRef.current.style.width = `${philosophy.tempo}%`;
      }
    }
  }, [philosophy]);

  if (!philosophy) return null;

  return (
    <Card className="w-64 bg-black/60 backdrop-blur-md border-white/10" variant="glass">
      <CardHeader className="py-2 px-3 border-b border-white/5">
        <CardTitle className="text-xs font-bold uppercase tracking-widest text-cyan-400">
          Coach Strategy
        </CardTitle>
      </CardHeader>
      <CardContent className="p-3 space-y-3">
        <div className="space-y-1">
          <div className="flex justify-between text-xs text-gray-300">
            <span>Aggression</span>
            <span>{philosophy.aggressiveness}%</span>
          </div>
          <div className="coaching-widget-bar-outer">
            <div className="coaching-widget-bar-aggression" ref={aggressionBarRef} />
          </div>
        </div>

        <div className="space-y-1">
          <div className="flex justify-between text-xs text-gray-300">
            <span>Tempo</span>
            <span>{philosophy.tempo}%</span>
          </div>
          <div className="coaching-widget-bar-outer">
            <div className="coaching-widget-bar-tempo" ref={tempoBarRef} />
          </div>
        </div>

        <div className="flex justify-between text-[10px] text-gray-400 uppercase tracking-wider">
          <span>
            {philosophy.run_pass_ratio > 55
              ? "RUN HEAVY"
              : philosophy.run_pass_ratio < 45
                ? "PASS HEAVY"
                : "BALANCED"}
          </span>
          <span
            className={
              activeStrategy === "HURRY_UP" ? "text-yellow-400 animate-pulse font-bold" : ""
            }
          >
            {activeStrategy !== "NORMAL"
              ? activeStrategy.replace("_", " ")
              : philosophy.clock_management_style}
          </span>
        </div>
      </CardContent>
    </Card>
  );
};
