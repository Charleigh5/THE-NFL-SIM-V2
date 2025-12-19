import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";
import { seasonApi } from "../services/season";
import { PrimeCard } from "../components/ui/PrimeCard";
import { Badge } from "../components/ui/Badge";
import { motion } from "framer-motion";
import {
  Activity,
  Calendar,
  ChevronRight,
  Play
} from "lucide-react";
import type { Season } from "../types/season";

const Dashboard = () => {
  const [currentSeason, setCurrentSeason] = useState<Season | null>(null);
  const [loadingSeason, setLoadingSeason] = useState(true);

  const { data: health } = useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      const response = await api.get("/api/system/health");
      return response.data;
    },
  });

  useEffect(() => {
    const fetchSeason = async () => {
      try {
        const season = await seasonApi.getCurrentSeason();
        setCurrentSeason(season);
      } catch {
        console.log("No active season found");
      } finally {
        setLoadingSeason(false);
      }
    };
    fetchSeason();
  }, []);

  const handleStartSeason = async () => {
    try {
      const year = currentSeason ? currentSeason.year + 1 : 2025;
      await seasonApi.initSeason(year);
      const season = await seasonApi.getCurrentSeason();
      setCurrentSeason(season);
      window.location.reload();
    } catch (e) {
      console.error("Failed to start season", e);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  return (
    <div className="min-h-screen p-8 text-white font-body selection:bg-brand selection:text-white overflow-hidden">

      {/* Header Section */}
      <motion.div
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        className="flex justify-between items-end mb-12 border-b-2 border-white/10 pb-6"
      >
        <div>
          <div className="flex items-center gap-3 mb-2">
            <div className="h-1 w-12 bg-brand" />
            <span className="text-brand font-bold tracking-widest uppercase text-sm">Live Broadcast</span>
          </div>
          <h1 className="font-header text-8xl uppercase italic tracking-tighter leading-none">
            Mission <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-500">Control</span>
          </h1>
        </div>

        <div className="flex flex-col items-end gap-2">
           <div className="flex items-center gap-4">
              <div className="flex flex-col items-end">
                <span className="text-xs text-gray-400 uppercase tracking-wider">System Status</span>
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${health?.status === 'healthy' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                  <span className="font-header text-xl">{health?.status === 'healthy' ? 'ONLINE' : 'OFFLINE'}</span>
                </div>
              </div>
              <div className="h-12 w-[1px] bg-white/20" />
              <div className="flex flex-col items-end">
                 <span className="text-xs text-gray-400 uppercase tracking-wider">Season</span>
                 <span className="font-header text-3xl text-brand">{currentSeason?.year || '2025'}</span>
              </div>
           </div>
        </div>
      </motion.div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="grid grid-cols-1 md:grid-cols-12 gap-8"
      >
        {/* Main Featured Card - 8 Cols */}
        <div className="md:col-span-8 flex flex-col gap-8">
           <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Link to="/season">
                <PrimeCard
                  title="Current Week"
                  icon={<Calendar size={28} />}
                  className="h-64 group cursor-pointer"
                  variant="default"
                >
                   <div className="flex flex-col justify-end h-full relative z-10">
                      <div className="text-6xl font-header mb-2 relative">
                         WEEK {currentSeason?.current_week || 1}
                         <span className="absolute -top-4 -right-4 text-brand/20 text-9xl -z-10">
                           {currentSeason?.current_week || 1}
                         </span>
                      </div>
                      <div className="flex items-center gap-2 text-brand group-hover:text-white transition-colors">
                        <span className="uppercase tracking-widest text-sm font-bold">View Matchups</span>
                        <ChevronRight className="group-hover:translate-x-2 transition-transform" />
                      </div>
                   </div>
                </PrimeCard>
              </Link>

              <Link to="/empire/front-office">
                <PrimeCard
                  title="Roster Health"
                  icon={<Activity size={28} />}
                  className="h-64 cursor-pointer"
                  variant="danger"
                  delay={0.1}
                >
                  <div className="flex items-center justify-between h-full">
                     <div className="text-center w-full">
                        <div className="text-5xl font-header mb-1">53/53</div>
                        <div className="text-xs uppercase tracking-widest text-white/60">Active Roster</div>
                     </div>
                     <div className="h-full w-[1px] bg-white/10" />
                     <div className="text-center w-full">
                        <div className="text-5xl font-header mb-1 text-red-500">2</div>
                        <div className="text-xs uppercase tracking-widest text-white/60">Injured</div>
                     </div>
                  </div>
                </PrimeCard>
              </Link>
           </div>

           {/* Action Bar */}
           <div className="grid grid-cols-4 gap-4">
              {[
                { label: "Depth Chart", path: "/empire/depth-chart", icon: "📋" },
                { label: "Trade Center", path: "/empire/trade-center", icon: "🔄" },
                { label: "Draft Room", path: "/offseason/draft", icon: "🏆" },
                { label: "Training", path: "/training", icon: "🏋️" },
              ].map((action, idx) => (
                <Link key={action.path} to={action.path}>
                   <PrimeCard
                      className="h-32 flex items-center justify-center hover:border-brand/50 transition-colors"
                      variant="glass"
                      delay={0.2 + (idx * 0.05)}
                   >
                      <div className="text-center">
                         <div className="text-3xl mb-2">{action.icon}</div>
                         <div className="font-header text-xl uppercase tracking-wide">{action.label}</div>
                      </div>
                   </PrimeCard>
                </Link>
              ))}
           </div>
        </div>

        {/* Side Panel - 4 Cols */}
        <div className="md:col-span-4 flex flex-col gap-6">
           {/* Season Control */}
           <PrimeCard title="Season Control" icon={<Play size={24} />} variant="default" delay={0.4}>
              <div className="space-y-4">
                 <div className="p-4 bg-black/40 border border-white/5 rounded">
                    <div className="flex justify-between items-center mb-2">
                       <span className="text-sm text-gray-400 uppercase">Phase</span>
                       <Badge variant="success">{currentSeason?.status || 'PRE_SEASON'}</Badge>
                    </div>
                    <div className="w-full bg-white/10 h-1 rounded-full overflow-hidden">
                       <div className="bg-brand h-full w-1/3" />
                    </div>
                 </div>

                 {!loadingSeason && (
                    <button
                      onClick={handleStartSeason}
                      className="w-full py-4 bg-brand hover:bg-red-600 text-white font-header text-xl uppercase tracking-widest skew-x-[-6deg] transition-all hover:scale-[1.02] shadow-[0_0_20px_rgba(239,68,68,0.4)]"
                    >
                       <span className="block skew-x-[6deg]">
                         {currentSeason ? "Simulate Week" : "Start Season"}
                       </span>
                    </button>
                 )}
              </div>
           </PrimeCard>

           {/* Quick Stats / Ticker */}
           <div className="flex-1 overflow-hidden relative">
              <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-broadcast-black z-10" />
              <div className="space-y-2 opacity-60">
                 {[1,2,3,4,5].map((i) => (
                    <div key={i} className="flex justify-between items-center py-2 border-b border-white/5 font-mono text-xs">
                       <span className="text-brand">NYG @ DAL</span>
                       <span>FINAL: 24 - 17</span>
                    </div>
                 ))}
              </div>
           </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
