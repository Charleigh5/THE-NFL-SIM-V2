import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard";
import SeasonDashboard from "./pages/SeasonDashboard";
import OffseasonDashboard from "./pages/OffseasonDashboard";
import { FrontOffice } from "./pages/FrontOffice";
import { DepthChart } from "./pages/DepthChart";
import { DraftRoom } from "./pages/DraftRoom";
import TeamSelection from "./pages/TeamSelection";
import Settings from "./pages/Settings";
import ErrorBoundary from "./components/ErrorBoundary";
import "./App.css";

const NotFound = () => <div className="page-placeholder">404 Not Found</div>;

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="season" element={<SeasonDashboard />} />
            <Route path="offseason" element={<OffseasonDashboard />} />
            <Route path="offseason/draft" element={<DraftRoom />} />
            <Route path="empire/front-office" element={<FrontOffice />} />
            <Route path="empire/depth-chart" element={<DepthChart />} />
            <Route path="settings" element={<Settings />} />
            <Route path="team-selection" element={<TeamSelection />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
