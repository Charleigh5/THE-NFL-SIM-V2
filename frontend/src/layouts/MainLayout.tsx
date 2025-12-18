import { Outlet, useLocation } from "react-router-dom";
import Navigation from "../components/Navigation";
import FeedbackWidget from "../components/common/FeedbackWidget";
import GlobalNotificationLayer from "../components/ui/GlobalNotificationLayer";
import "./MainLayout.css";

const MainLayout = () => {
  const location = useLocation();

  // Extract page name from pathname
  const currentPage = location.pathname.split("/").filter(Boolean).pop() || "Dashboard";

  return (
    <div className="main-layout">
      <Navigation />
      <GlobalNotificationLayer />
      <main className="main-content">
        <Outlet />
      </main>
      <FeedbackWidget currentPage={currentPage} />
    </div>
  );
};

export default MainLayout;
