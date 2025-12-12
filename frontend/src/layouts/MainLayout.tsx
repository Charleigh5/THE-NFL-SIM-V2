import { Outlet, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import Navigation from "../components/Navigation";
import FeedbackWidget from "../components/common/FeedbackWidget";
import { routeVariants } from "../styles/motion";
import "./MainLayout.css";

const MainLayout = () => {
  const location = useLocation();

  // Extract page name from pathname
  const currentPage = location.pathname.split("/").filter(Boolean).pop() || "Dashboard";

  return (
    <div className="main-layout">
      <Navigation />
      <main className="main-content" role="main">
        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={location.pathname}
            variants={routeVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            className="route-stage"
          >
            <Outlet />
          </motion.div>
        </AnimatePresence>
      </main>
      <FeedbackWidget currentPage={currentPage} />
    </div>
  );
};

export default MainLayout;
