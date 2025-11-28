import { DraggableCard } from "../components/ui/DraggableCard";

// BASELINE VERSION: Mock Data for Visual Regression Testing
export const FrontOffice_Baseline = () => {
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-4xl font-bold text-white tracking-tight">
          Front Office
        </h1>
        <p className="text-cyan-400/80">Cap Space: $12.4M</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-panel p-6 rounded-xl border border-white/5 min-h-[500px]">
          <h2 className="text-xl font-bold text-white mb-4">Active Roster</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            <DraggableCard
              name="C. Weir"
              position="QB"
              rating={99}
              team="EMP"
            />
            <DraggableCard name="J. Doe" position="WR" rating={88} team="EMP" />
            <DraggableCard
              name="A. Smith"
              position="RB"
              rating={92}
              team="EMP"
            />
            <DraggableCard
              name="B. Jones"
              position="LB"
              rating={85}
              team="GEN"
            />
            <DraggableCard
              name="T. Wilson"
              position="TE"
              rating={89}
              team="GEN"
            />
          </div>
        </div>
        <div className="glass-panel p-6 rounded-xl border border-white/5 min-h-[500px] flex items-center justify-center">
          <span className="text-white/20 font-mono">TRANSACTION_LOG</span>
        </div>
      </div>
    </div>
  );
};
