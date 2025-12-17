import { useState } from "react";
import { BodyMap } from "../components/medical/BodyMap";
import { TreatmentModal } from "../components/medical/TreatmentModal";
import "../components/medical/MedicalCenter.css";

export const MedicalCenter = () => {
  const [selectedPart, setSelectedPart] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);

  // Mock Data
  const [healthData, setHealthData] = useState({
    head: 95,
    torso: 88,
    rightArm: 75, // Injured
    leftArm: 98,
    rightLeg: 92,
    leftLeg: 85,
  });

  const handlePartSelect = (part: string) => {
    setSelectedPart(part);
    setShowModal(true);
  };

  const handleTreatment = (treatment: string) => {
    console.log(`Applied ${treatment} to ${selectedPart}`);
    // Simulate healing
    if (selectedPart) {
      setHealthData((prev) => ({
        ...prev,
        [selectedPart]: Math.min(100, (prev[selectedPart as keyof typeof prev] || 0) + 10),
      }));
    }
    setShowModal(false);
  };

  return (
    <div className="space-y-6 medical-center-container">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tight">Medical Center</h1>
          <p className="text-cyan-400/80">Active Roster Health: 89%</p>
        </div>
        <div className="text-right">
          <span className="text-xs text-gray-500 uppercase tracking-widest">Team Doctor</span>
          <div className="text-xl font-bold text-white">Dr. Chao</div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left: Body Visualizer */}
        <div className="glass-panel p-8 rounded-xl border border-white/5 flex flex-col items-center justify-center bg-gradient-to-b from-gray-900/50 to-black/50 body-map-container">
          <div className="mb-4 text-sm text-gray-400 uppercase tracking-widest">
            Select Zone to Treat
          </div>
          <BodyMap healthData={healthData} onPartSelect={handlePartSelect} />
        </div>

        {/* Right: Injury Report / Status */}
        <div className="glass-panel p-6 rounded-xl border border-white/5">
          <h3 className="text-xl font-bold text-white mb-4 border-b border-white/10 pb-2">
            Injury Report
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-red-900/20 border border-red-500/30 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-red-900/50 flex items-center justify-center font-bold text-red-400">
                  QB
                </div>
                <div>
                  <div className="font-bold text-white">J. Burrow</div>
                  <div className="text-xs text-red-300">Right Arm - Elbow Sprain</div>
                </div>
              </div>
              <div className="text-right">
                <div className="font-mono text-xl text-yellow-400">75%</div>
                <div className="text-[10px] text-gray-400">WEAR LEVEL</div>
              </div>
            </div>

            <div className="flex items-center justify-between p-3 bg-yellow-900/10 border border-yellow-500/20 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-yellow-900/40 flex items-center justify-center font-bold text-yellow-400">
                  RB
                </div>
                <div>
                  <div className="font-bold text-white">J. Mixon</div>
                  <div className="text-xs text-yellow-300">Left Leg - Hamstring Tightness</div>
                </div>
              </div>
              <div className="text-right">
                <div className="font-mono text-xl text-yellow-400">85%</div>
                <div className="text-[10px] text-gray-400">WEAR LEVEL</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <TreatmentModal
        isOpen={showModal}
        partName={selectedPart || ""}
        currentHealth={selectedPart ? healthData[selectedPart as keyof typeof healthData] : 0}
        onClose={() => setShowModal(false)}
        onConfirm={handleTreatment}
      />
    </div>
  );
};
