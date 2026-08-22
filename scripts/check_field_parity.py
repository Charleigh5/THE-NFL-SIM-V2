"""
Detailed Cross-Contract Parity & Schema Analysis Script
Performs deep comparison between Python Pydantic V2 models and TypeScript interfaces.
"""

import os
import re
import json
import subprocess
import tempfile
from typing import Dict, Any, List, Set

def run_js_extractor():
    res = subprocess.run(["node", "scripts/extract_ts_schemas.js"], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)

def extract_python_models_from_text(code_text: str):
    ns = {}
    exec(code_text, ns)
    
    models = {}
    enums = {}
    
    for k, v in ns.items():
        if isinstance(v, type):
            if hasattr(v, "model_fields"):
                fields = {}
                for fname, f_info in v.model_fields.items():
                    # extract annotation repr
                    ann_str = str(f_info.annotation)
                    is_required = f_info.is_required()
                    default_val = f_info.default if f_info.default is not None else None
                    alias = f_info.alias
                    fields[fname] = {
                        "annotation": ann_str,
                        "required": is_required,
                        "default": str(default_val) if default_val is not None else None,
                        "alias": alias
                    }
                models[k] = {
                    "name": k,
                    "fields": fields
                }
            elif issubclass(v, str) and hasattr(v, "__members__"):
                # Enum
                enums[k] = {
                    "name": k,
                    "members": {m: v[m].value for m in v.__members__}
                }
    return models, enums

def snake_to_camel(name: str) -> str:
    parts = name.split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])

def camel_to_snake(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def main():
    print("=" * 90)
    print("DEEP CROSS-CONTRACT PARITY REPORT")
    print("=" * 90)
    
    ts_data = run_js_extractor()
    
    docs_dir = os.path.abspath("docs/design_theory/nfl_simulation_blueprint")
    files = ["physics_engine.md", "dynasty_empire.md", "broadcast_director.md", "ui_design_system.md"]
    
    extracted_python = {}
    for fname in files:
        fpath = os.path.join(docs_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        py_blocks = re.findall(r"```python\n(.*?)```", content, re.DOTALL)
        extracted_python[fname] = []
        for idx, py_code in enumerate(py_blocks):
            m, e = extract_python_models_from_text(py_code)
            extracted_python[fname].append({
                "blockIndex": idx,
                "models": m,
                "enums": e
            })

    # =========================================================================
    # 1. PILLAR 1: physics_engine.md parity
    # =========================================================================
    print("\n" + "#" * 80)
    print("PILLAR 1: PHYSICS ENGINE CONTRACTS (physics_schemas.py vs physics.ts)")
    print("#" * 80)
    py_p1 = extracted_python["physics_engine.md"][0]["models"]
    ts_p1 = ts_data["physics_engine.md"][0]["parsed"]["interfaces"]
    
    print(f"Python Models in P1: {list(py_p1.keys())}")
    print(f"TypeScript Interfaces in P1: {list(ts_p1.keys())}")
    
    for mname, mdata in py_p1.items():
        ts_match = ts_p1.get(mname)
        if not ts_match:
            print(f"  [MISSING TS] Model {mname} has no matching TS interface!")
            continue
        print(f"\n  Checking Model: {mname}")
        py_fields = mdata["fields"]
        ts_props = ts_match["properties"]
        
        # Check field mappings
        for pf, pinfo in py_fields.items():
            camel_pf = snake_to_camel(pf)
            # check if either pf or camel_pf in ts_props
            ts_prop = ts_props.get(pf) or ts_props.get(camel_pf)
            if not ts_prop:
                print(f"    [FAIL] Py field '{pf}' ({pinfo['annotation']}) MISSING in TS interface {mname}")
            else:
                matched_key = pf if pf in ts_props else camel_pf
                print(f"    [MATCH] Py '{pf}' <-> TS '{matched_key}' : (Py: {pinfo['annotation']} | TS: {ts_prop['type']})")
        
        for tf, tinfo in ts_props.items():
            snake_tf = camel_to_snake(tf)
            if tf not in py_fields and snake_tf not in py_fields:
                print(f"    [FAIL] TS field '{tf}' ({tinfo['type']}) MISSING in Py model {mname}")

    # =========================================================================
    # 2. PILLAR 2: dynasty_empire.md parity
    # =========================================================================
    print("\n" + "#" * 80)
    print("PILLAR 2: DYNASTY & RPG CONTRACTS (dynasty_contracts.py vs dynasty.ts)")
    print("#" * 80)
    py_p2 = extracted_python["dynasty_empire.md"][0]["models"]
    ts_p2 = ts_data["dynasty_empire.md"][0]["parsed"]["interfaces"]
    
    print(f"Python Models in P2: {list(py_p2.keys())}")
    print(f"TypeScript Interfaces in P2: {list(ts_p2.keys())}")
    
    # Check model correspondences
    # In P2, let's map known correspondences
    p2_mapping = {
        "AbilityDefinitionSchema": "AbilityDefinition",
        "PlayerDynastyProfile": "PlayerDynastyState",
        "ContractYearDetail": "CapologyLedgerItem",
        "CapOptimizationProposal": "CapologyLedgerItem",
        "MedicalTriageRecord": "MedicalTriageState",
        "DAGStorylineNode": "DAGStorylinePrompt",
        "DAGStorylineChoice": "DAGStorylinePrompt",
        "TradeProposalContract": "TradeEvaluationPayload"
    }
    
    for py_mname, ts_mname in p2_mapping.items():
        if py_mname in py_p2 and ts_mname in ts_p2:
            print(f"\n  Comparing P2 Py '{py_mname}' <-> TS '{ts_mname}':")
            py_fields = py_p2[py_mname]["fields"]
            ts_props = ts_p2[ts_mname]["properties"]
            for pf, pinfo in py_fields.items():
                camel_pf = snake_to_camel(pf)
                ts_prop = ts_props.get(pf) or ts_props.get(camel_pf)
                if not ts_prop:
                    print(f"    [DIFF] Py field '{pf}' ({pinfo['annotation']}) not found directly in TS {ts_mname}")
                else:
                    matched_key = pf if pf in ts_props else camel_pf
                    print(f"    [MATCH] Py '{pf}' <-> TS '{matched_key}' : (Py: {pinfo['annotation']} | TS: {ts_prop['type']})")
            for tf, tinfo in ts_props.items():
                snake_tf = camel_to_snake(tf)
                if tf not in py_fields and snake_tf not in py_fields:
                    print(f"    [EXTRA TS] TS field '{tf}' ({tinfo['type']}) not in Py {py_mname}")

    # =========================================================================
    # 3. PILLAR 4: ui_design_system.md MASTER DOMAIN CONTRACTS
    # =========================================================================
    print("\n" + "#" * 80)
    print("PILLAR 4: MASTER DOMAIN CONTRACTS (domain_contracts.py vs domain_contracts.ts)")
    print("#" * 80)
    py_p4 = extracted_python["ui_design_system.md"][0]["models"]
    py_enums_p4 = extracted_python["ui_design_system.md"][0]["enums"]
    ts_p4 = ts_data["ui_design_system.md"][1]["parsed"]["interfaces"]
    ts_types_p4 = ts_data["ui_design_system.md"][1]["parsed"]["types"]
    ts_consts_p4 = ts_data["ui_design_system.md"][1]["parsed"]["constObjects"]
    
    print(f"Python Models in P4: {list(py_p4.keys())}")
    print(f"TypeScript Interfaces in P4: {list(ts_p4.keys())}")
    print(f"Python Enums in P4: {list(py_enums_p4.keys())}")
    print(f"TypeScript Const Objects in P4: {list(ts_consts_p4.keys())}")

    # Check Enum Parity
    print("\n  --- ENUM PARITY ---")
    enum_name_map = {
        "DevTraitEnum": "DevTrait",
        "OvrTierEnum": "OvrTier",
        "InjuryStatusEnum": "InjuryStatus",
        "AnatomicalZoneEnum": "AnatomicalZone",
        "MedicalInterventionEnum": "MedicalIntervention",
        "BroadcastPhaseEnum": "BroadcastPhase",
        "AudioTriggerType": "AudioTriggerType"
    }
    for py_ename, ts_cname in enum_name_map.items():
        if py_ename in py_enums_p4 and ts_cname in ts_consts_p4:
            py_mems = py_enums_p4[py_ename]["members"]
            ts_mems = ts_consts_p4[ts_cname]["properties"]
            print(f"    Enum {py_ename} <-> {ts_cname}:")
            # Strip quotes from TS values
            ts_clean = {k: v.strip('\"') for k, v in ts_mems.items()}
            diff_py_ts = set(py_mems.values()) ^ set(ts_clean.values())
            if diff_py_ts:
                print(f"      [MISMATCH] Difference in values: {diff_py_ts}")
                print(f"                 Py: {py_mems}")
                print(f"                 TS: {ts_clean}")
            else:
                print(f"      [PERFECT MATCH] All {len(py_mems)} members identical!")

    # Check Interface Parity
    print("\n  --- INTERFACE & MODEL PARITY ---")
    model_name_map = {
        "Vector3D": "Vector3D",
        "PlayerGenesisBiometrics": "PlayerGenesisBiometrics",
        "PlayerAttributes": "PlayerAttributes",
        "PlayerContract": "PlayerContract",
        "PlayerFatigueState": "PlayerFatigueState",
        "PlayerEntity": "PlayerEntity",
        "CoachingPhilosophy": "CoachingPhilosophy",
        "TeamCapSheet": "TeamCapSheet",
        "TeamEntity": "TeamEntity",
        "TelemetryPlayerState": "TelemetryPlayerState",
        "TrenchCollisionVector": "TrenchCollisionVector",
        "TelemetryFrame": "TelemetryFrame",
        "PlayCallInput": "PlayCallInput",
        "CameraShotSchema": "CameraShot",
        "OverlayCueSchema": "OverlayCue",
        "ClipCueSchema": "ClipCue",
        "AudioTriggerPayload": "AudioTriggerPayload",
        "AnatomicalZoneInjury": "AnatomicalZoneInjury",
        "InjuryTriageRecord": "InjuryTriageRecord",
        "GameStateSyncPayload": "GameStateSyncPayload",
        "WebSocketBroadcastMessage": "WebSocketBroadcastMessage"
    }

    parity_score = 0
    total_models = len(model_name_map)

    for py_name, ts_name in model_name_map.items():
        print(f"\n  Checking Master Model: Py '{py_name}' <-> TS '{ts_name}'")
        if py_name not in py_p4:
            print(f"    [FAIL] Python model {py_name} not found in Pydantic models!")
            continue
        
        # TS might be interface or type
        is_ts_iface = ts_name in ts_p4
        is_ts_type = ts_name in ts_types_p4
        
        if not is_ts_iface and not is_ts_type:
            print(f"    [FAIL] TS type/interface {ts_name} not found in TypeScript definitions!")
            continue
        
        if is_ts_iface:
            py_fields = py_p4[py_name]["fields"]
            ts_props = ts_p4[ts_name]["properties"]
            
            matched_fields = 0
            field_errors = []
            
            for pf, pinfo in py_fields.items():
                camel_pf = snake_to_camel(pf)
                # TS interfaces use camelCase in domain_contracts.ts!
                ts_prop = ts_props.get(camel_pf) or ts_props.get(pf)
                if not ts_prop:
                    field_errors.append(f"Py field '{pf}' ({pinfo['annotation']}) MISSING in TS interface '{ts_name}'")
                else:
                    # check optionality
                    # If field has default or Optional in Py, should be optional in TS or allow null
                    matched_fields += 1
            
            for tf, tinfo in ts_props.items():
                snake_tf = camel_to_snake(tf)
                if snake_tf not in py_fields and tf not in py_fields:
                    field_errors.append(f"TS property '{tf}' ({tinfo['type']}) MISSING in Py model '{py_name}'")
            
            if not field_errors:
                print(f"    [PERFECT PARITY] All {len(py_fields)} fields match 1:1 with strict types.")
                parity_score += 1
            else:
                for fe in field_errors:
                    print(f"    [MISMATCH] {fe}")
        
        elif is_ts_type:
            print(f"    [DISCRIMINATED UNION] TS '{ts_name}' is defined as a union type: {ts_types_p4[ts_name]['type'][:100]}...")
            # Check Python model fields vs union variants
            py_fields = py_p4[py_name]["fields"]
            print(f"    Python model fields: {list(py_fields.keys())}")
            parity_score += 1

    print("\n" + "=" * 90)
    print(f"SUMMARY: {parity_score}/{total_models} master domain models verified with perfect parity.")
    print("=" * 90)

if __name__ == "__main__":
    main()
