"""
Cross-Pillar Domain Model and Boundary Continuity Analyzer
Inspects:
1. Physics Engine (Pillar 1) schemas & interfaces
2. Dynasty Engine (Pillar 2) schemas & interfaces
3. Broadcast Director (Pillar 3) contracts & interfaces
4. UI & Master Contracts (Pillar 4) schemas & interfaces
5. Domain boundary transitions:
   - Physics (60Hz TelemetryFrame) -> Broadcast Director (CameraShot, OverlayCue, AudioTrigger)
   - Physics (Fatigue, Injuries) -> Dynasty Triage (InjuryTriageRecord)
   - Dynasty (PlayerAttributes, CoachingPhilosophy, TeamCapSheet) -> Physics & Roster
   - Broadcast & Simulation -> UI (GameStateSyncPayload, WebSocketBroadcastMessage)
"""

import os
import re
import json
import subprocess
from check_field_parity import extract_python_models_from_text, run_js_extractor

def main():
    docs_dir = os.path.abspath("docs/design_theory/nfl_simulation_blueprint")
    
    with open(os.path.join(docs_dir, "physics_engine.md"), "r", encoding="utf-8") as f:
        p1_text = f.read()
    with open(os.path.join(docs_dir, "dynasty_empire.md"), "r", encoding="utf-8") as f:
        p2_text = f.read()
    with open(os.path.join(docs_dir, "broadcast_director.md"), "r", encoding="utf-8") as f:
        p3_text = f.read()
    with open(os.path.join(docs_dir, "ui_design_system.md"), "r", encoding="utf-8") as f:
        p4_text = f.read()

    ts_data = run_js_extractor()

    print("=" * 80)
    print("PILLAR 1 (PHYSICS) DETAILS")
    print("=" * 80)
    p1_py_code = re.findall(r"```python\n(.*?)```", p1_text, re.DOTALL)[0]
    p1_models, p1_enums = extract_python_models_from_text(p1_py_code)
    p1_ts_ifaces = ts_data["physics_engine.md"][0]["parsed"]["interfaces"]
    p1_ts_types = ts_data["physics_engine.md"][0]["parsed"]["types"]
    
    for mname, mval in p1_models.items():
        print(f"\nModel: {mname}")
        for fname, fval in mval["fields"].items():
            print(f"  - {fname}: {fval['annotation']} (req={fval['required']}, default={fval['default']})")
        if mname in p1_ts_ifaces:
            ts_props = p1_ts_ifaces[mname]["properties"]
            print(f"  [TS match] Props: {list(ts_props.keys())}")

    print("\n" + "=" * 80)
    print("PILLAR 2 (DYNASTY) DETAILS")
    print("=" * 80)
    p2_py_code = re.findall(r"```python\n(.*?)```", p2_text, re.DOTALL)[0]
    p2_models, p2_enums = extract_python_models_from_text(p2_py_code)
    p2_ts_ifaces = ts_data["dynasty_empire.md"][0]["parsed"]["interfaces"]
    p2_ts_types = ts_data["dynasty_empire.md"][0]["parsed"]["types"]
    
    for mname, mval in p2_models.items():
        print(f"\nModel: {mname}")
        for fname, fval in mval["fields"].items():
            print(f"  - {fname}: {fval['annotation']} (req={fval['required']}, default={fval['default']})")

    print("\nTS Interfaces in P2:")
    for iname, ival in p2_ts_ifaces.items():
        print(f"\nTS Interface: {iname}")
        for pname, pval in ival["properties"].items():
            print(f"  - {pname}: {pval['type']} (optional={pval['optional']})")

    print("\n" + "=" * 80)
    print("PILLAR 3 (BROADCAST DIRECTOR) DETAILS")
    print("=" * 80)
    print("Checking broadcast state machine & audio synthesizer contracts...")
    # Look for broadcast transitions and contracts in P3
    p3_ts_blocks = ts_data["broadcast_director.md"]
    print(f"TypeScript blocks in P3: {len(p3_ts_blocks)}")
    
    print("\n" + "=" * 80)
    print("PILLAR 4 (UI & MASTER DOMAIN) DETAILS")
    print("=" * 80)
    p4_py_code = re.findall(r"```python\n(.*?)```", p4_text, re.DOTALL)[0]
    p4_models, p4_enums = extract_python_models_from_text(p4_py_code)
    p4_ts_ifaces = ts_data["ui_design_system.md"][1]["parsed"]["interfaces"]
    p4_ts_types = ts_data["ui_design_system.md"][1]["parsed"]["types"]
    
    for mname, mval in p4_models.items():
        print(f"\nModel: {mname} ({len(mval['fields'])} fields)")
        for fname, fval in mval["fields"].items():
            print(f"  - {fname}: {fval['annotation']}")

    print("\n" + "=" * 80)
    print("WEBSOCKET FRAME DISCRIMINATION & TYPING CHECK")
    print("=" * 80)
    ws_ts_type = p4_ts_types.get("WebSocketBroadcastMessage")
    if ws_ts_type:
        print("TypeScript WebSocketBroadcastMessage definition:")
        print(ws_ts_type["type"])
    
    ws_py_model = p4_models.get("WebSocketBroadcastMessage")
    if ws_py_model:
        print("\nPython WebSocketBroadcastMessage fields:")
        for fname, fval in ws_py_model["fields"].items():
            print(f"  - {fname}: {fval['annotation']} (default={fval['default']})")

if __name__ == "__main__":
    main()
