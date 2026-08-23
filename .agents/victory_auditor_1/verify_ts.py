import re
import subprocess
import os

files = [
    r"docs\design_theory\nfl_simulation_blueprint\physics_engine.md",
    r"docs\design_theory\nfl_simulation_blueprint\dynasty_empire.md",
    r"docs\design_theory\nfl_simulation_blueprint\broadcast_director.md",
    r"docs\design_theory\nfl_simulation_blueprint\ui_design_system.md",
]

print("=== EXTRACTING TYPESCRIPT CODE BLOCKS ===")
ts_code = []
for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"```typescript\s*(.*?)\s*```"
    blocks = re.findall(pattern, content, re.DOTALL)
    print(f"{filepath}: {len(blocks)} TS blocks")
    for b in blocks:
        ts_code.append(b)

combined_ts = "\n\n// --- NEW BLOCK ---\n\n".join(ts_code)
out_file = r".agents\victory_auditor_1\combined_contracts.ts"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(combined_ts)

print(f"Wrote combined TS to {out_file}")
