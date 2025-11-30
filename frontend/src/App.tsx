import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard";
import SeasonDashboard from "./pages/SeasonDashboard";
import OffseasonDashboard from "./pages/OffseasonDashboard";
import { FrontOffice } from "./pages/FrontOffice";
import ErrorBoundary from "./components/ErrorBoundary";
import "./App.css";

// Placeholder components for engine pages
const GenesisPage = () => (
  <div className="page-placeholder">🧬 Genesis Engine (Coming Soon)</div>
);
const EmpirePage = () => (
  <div className="page-placeholder">💰 Empire Engine (Coming Soon)</div>
);
const HivePage = () => (
  <div className="page-placeholder">🌦️ Hive Engine (Coming Soon)</div>
);
const SocietyPage = () => (
  <div className="page-placeholder">📰 Society Engine (Coming Soon)</div>
);
const CorePage = () => (
  <div className="page-placeholder">⚙️ Core Engine (Coming Soon)</div>
);
const RPGPage = () => (
  <div className="page-placeholder">📊 RPG Engine (Coming Soon)</div>
);
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
          <Route path="genesis" element={<GenesisPage />} />
          <Route path="empire" element={<EmpirePage />} />
          <Route path="empire/front-office" element={<FrontOffice />} />
          <Route path="hive" element={<HivePage />} />
          <Route path="society" element={<SocietyPage />} />
          <Route path="core" element={<CorePage />} />
          <Route path="rpg" element={<RPGPage />} />
          <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
