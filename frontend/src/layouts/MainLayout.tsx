import { useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Navigation from "../components/Navigation";
import FeedbackWidget from "../components/common/FeedbackWidget";
import SoundtrackPlayer from "../components/audio/SoundtrackPlayer";
import { PageTransition } from "../components/transitions/PageTransition";
import TraitNotification from "../components/ui/TraitNotification";

const MainLayout = () => {
  const location = useLocation();
  const [activeNotification, setActiveNotification] = useState<{
    traitName: string;
    playerName: string;
    type?: "UNLOCK" | "UPGRADE" | "LOST";
  } | null>(null);

  // Extract page name from pathname
  const currentPage = location.pathname.split("/").filter(Boolean).pop() || "Dashboard";

  return (
    <div className="min-h-screen bg-broadcast-black text-white selection:bg-brand selection:text-white">
      <Navigation />

      {/* Main Content Area - Shifted for fixed nav */}
      <main className="md:ml-64 relative min-h-screen overflow-x-hidden" role="main">
        {/* Broadcast Background Elements */}
        <div className="fixed inset-0 pointer-events-none z-0">
          {/* Omni-present stadium lights glow */}
          <div className="absolute top-[-20%] left-[20%] w-[500px] h-[500px] bg-brand/20 blur-[120px] rounded-full mix-blend-screen" />
          <div className="absolute bottom-[-20%] right-[10%] w-[600px] h-[600px] bg-blue-900/10 blur-[100px] rounded-full mix-blend-screen" />
        </div>

        <div className="relative z-10 p-8">
          <PageTransition>
            <Outlet />
          </PageTransition>
        </div>
      </main>

      {activeNotification && (
        <TraitNotification
          traitName={activeNotification.traitName}
          playerName={activeNotification.playerName}
          type={activeNotification.type}
          onDismiss={() => setActiveNotification(null)}
        />
      )}

      <FeedbackWidget currentPage={currentPage} />
      <SoundtrackPlayer />
    </div>
  );
};

export default MainLayout;
