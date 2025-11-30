export const Playbook = () => {
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-4xl font-bold text-white tracking-tight">Playbook</h1>
        <p className="text-cyan-400/80">Offensive Scheme: West Coast</p>
      </header>

      <div className="glass-panel p-6 rounded-xl border border-white/5 min-h-[600px] flex items-center justify-center relative">
        <span className="text-white/20 font-mono">TELESTRATOR_CANVAS_TARGET</span>

        <div className="absolute top-4 right-4 flex gap-2">
          <button className="p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors">
            ✏️ Draw
          </button>
          <button className="p-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-colors">
            🗑️ Clear
          </button>
        </div>
      </div>
    </div>
  );
};
