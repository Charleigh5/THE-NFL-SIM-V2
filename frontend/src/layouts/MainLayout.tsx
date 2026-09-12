import { useState } from "react";
import { MotionConfig } from "framer-motion";
import { Outlet, useLocation } from "react-router-dom";
import Navigation from "../components/Navigation";
import FeedbackWidget from "../components/common/FeedbackWidget";
import SoundtrackPlayer from "../components/audio/SoundtrackPlayer";
import { PageTransition } from "../components/transitions/PageTransition";
import TraitNotification from "../components/ui/TraitNotification";
import { DynamicWeatherFXOverlay } from "../components/weather/DynamicWeatherFXOverlay";
import { ThreeStadiumBackdrop } from "../components/weather/ThreeStadiumBackdrop";
import { WeatherControlHUD } from "../components/weather/WeatherControlHUD";
import { getSpatialRoutePolicy } from "../components/spatial/spatialSceneManifest";

const MainLayout = () => {
  const location = useLocation();
  const [activeNotification, setActiveNotification] = useState<{
    traitName: string;
    playerName: string;
    type?: "UNLOCK" | "UPGRADE" | "LOST";
  } | null>(null);

  // Extract page name from pathname
  const currentPage = location.pathname.split("/").filter(Boolean).pop() || "Dashboard";
  const scenePolicy = getSpatialRoutePolicy(location.pathname);

  return (
    <MotionConfig reducedMotion="user">
    <div className="min-h-screen bg-broadcast-black text-white selection:bg-brand selection:text-white">
      {/* Global environmental layers are route-governed so indoor spatial scenes do not stack canvases/effects. */}
      {scenePolicy.globalStadiumBackdrop && <ThreeStadiumBackdrop />}
      {scenePolicy.weatherFx && <DynamicWeatherFXOverlay />}

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

      {/* Indoor scene routes can suppress the global environmental console. */}
      {scenePolicy.weatherHud && <WeatherControlHUD />}

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
    </MotionConfig>
  );
};

export default MainLayout;
