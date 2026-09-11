import React from "react";
import { HelpCircle, Clock, Split } from "lucide-react";

interface VoidYearsSliderProps {
  realYears: number;
  setRealYears: (years: number) => void;
  voidYears: number;
  setVoidYears: (years: number) => void;
  postJune1: boolean;
  setPostJune1: (val: boolean) => void;
  signingBonus: number;
}

export const VoidYearsSlider: React.FC<VoidYearsSliderProps> = ({
  realYears,
  setRealYears,
  voidYears,
  setVoidYears,
  postJune1,
  setPostJune1,
  signingBonus,
}) => {
  const maxVoidAllowed = Math.max(0, 5 - realYears);
  const prorationYears = Math.min(realYears + voidYears, 5);
  const annualProration = prorationYears > 0 ? Math.floor(signingBonus / prorationYears) : 0;
  const unamortizedAtVoid =
    voidYears > 0 ? annualProration * Math.max(0, prorationYears - realYears) : 0;

  const handleRealYearsChange = (val: number) => {
    setRealYears(val);
    if (val + voidYears > 5) {
      setVoidYears(Math.max(0, 5 - val));
    }
  };

  const handleVoidYearsChange = (val: number) => {
    const clamped = Math.min(val, maxVoidAllowed);
    setVoidYears(clamped);
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-4 text-slate-100">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4 text-cyan-400" />
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            CBA Article 13: Void Years & Proration
          </span>
        </div>
        <span className="text-xs text-slate-400">
          Max Proration: <strong className="text-cyan-400">5 Years</strong>
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Real Contract Length */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="text-slate-300 font-medium">Active Playing Years</span>
            <span className="font-bold text-cyan-400">{realYears} {realYears === 1 ? "Year" : "Years"}</span>
          </div>
          <input
            type="range"
            min={1}
            max={5}
            step={1}
            value={realYears}
            onChange={(e) => handleRealYearsChange(Number(e.target.value))}
            className="w-full accent-cyan-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
          />
          <div className="flex justify-between text-[10px] text-slate-500">
            <span>1 yr</span>
            <span>2 yr</span>
            <span>3 yr</span>
            <span>4 yr</span>
            <span>5 yr</span>
          </div>
        </div>

        {/* CBA Void Dummy Years */}
        <div className="space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="text-slate-300 font-medium flex items-center gap-1">
              Void Dummy Years
              <span title="Dummy years that automatically void to spread signing bonus proration over up to 5 seasons">
                <HelpCircle className="w-3 h-3 text-slate-500" />
              </span>
            </span>
            <span className="font-bold text-amber-400">
              {voidYears} {voidYears === 1 ? "Void Year" : "Void Years"}
            </span>
          </div>
          <input
            type="range"
            min={0}
            max={4}
            step={1}
            value={voidYears}
            onChange={(e) => handleVoidYearsChange(Number(e.target.value))}
            disabled={maxVoidAllowed === 0}
            className="w-full accent-amber-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg disabled:opacity-40"
          />
          <div className="flex justify-between text-[10px] text-slate-500">
            <span>0</span>
            <span>+1</span>
            <span>+2</span>
            <span>+3</span>
            <span>+4</span>
          </div>
        </div>
      </div>

      {/* Proration & Acceleration Stat Pill */}
      <div className="bg-slate-950/70 border border-slate-800/80 rounded-lg p-3 grid grid-cols-3 gap-2 text-center text-xs">
        <div>
          <span className="text-[10px] text-slate-400 block uppercase">Proration Window</span>
          <span className="font-bold text-cyan-300">{prorationYears} Years</span>
        </div>
        <div>
          <span className="text-[10px] text-slate-400 block uppercase">Annual Bonus Cap Hit</span>
          <span className="font-bold text-emerald-400">${(annualProration / 1_000_000).toFixed(2)}M/yr</span>
        </div>
        <div>
          <span className="text-[10px] text-slate-400 block uppercase">Dead Cap Acceleration</span>
          <span className={`font-bold ${unamortizedAtVoid > 0 ? "text-rose-400" : "text-slate-400"}`}>
            {unamortizedAtVoid > 0 ? `$${(unamortizedAtVoid / 1_000_000).toFixed(2)}M` : "$0.00M"}
          </span>
        </div>
      </div>

      {/* Post-June 1st Split Toggle */}
      {voidYears > 0 && (
        <div className="flex items-center justify-between bg-slate-800/40 rounded-lg px-3 py-2 border border-slate-700/50">
          <div className="flex items-center gap-2">
            <Split className="w-4 h-4 text-purple-400" />
            <div>
              <span className="text-xs font-semibold text-slate-200 block">Post-June 1st Designation</span>
              <span className="text-[10px] text-slate-400 block">
                Splits dead money acceleration 50/50 over 2 league years
              </span>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setPostJune1(!postJune1)}
            className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors focus:outline-none ${
              postJune1 ? "bg-cyan-500" : "bg-slate-700"
            }`}
          >
            <span
              className={`inline-block h-3.5 w-3.5 transform rounded-full bg-white transition-transform ${
                postJune1 ? "translate-x-4.5" : "translate-x-1"
              }`}
            />
          </button>
        </div>
      )}
    </div>
  );
};
