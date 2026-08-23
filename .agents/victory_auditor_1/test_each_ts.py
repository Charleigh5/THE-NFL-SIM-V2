import re
import subprocess
import os

files = [
    r"docs\design_theory\nfl_simulation_blueprint\physics_engine.md",
    r"docs\design_theory\nfl_simulation_blueprint\dynasty_empire.md",
    r"docs\design_theory\nfl_simulation_blueprint\broadcast_director.md",
    r"docs\design_theory\nfl_simulation_blueprint\ui_design_system.md",
]

print("=== CHECKING TYPESCRIPT COMPILATION PER BLOCK ===")
tsc_path = os.path.join(os.getcwd(), "frontend", "node_modules", "typescript", "bin", "tsc")
if not os.path.exists(tsc_path):
    print("tsc not found directly at", tsc_path)

block_idx = 0
for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"```typescript\s*(.*?)\s*```"
    blocks = re.findall(pattern, content, re.DOTALL)
    for i, b in enumerate(blocks, 1):
        block_idx += 1
        tmp_ts = os.path.join(r".agents\victory_auditor_1", f"block_{block_idx}.ts")
        with open(tmp_ts, "w", encoding="utf-8") as tf:
            tf.write(b)
        
        # Test compile with node tsc if available
        if os.path.exists(tsc_path):
            cmd = ["node", tsc_path, "--noEmit", "--skipLibCheck", "--target", "es2022", "--lib", "es2022,dom", tmp_ts]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"[{os.path.basename(filepath)} Block {i}]: PASS (TypeScript clean)")
            else:
                print(f"[{os.path.basename(filepath)} Block {i}]: FAIL\n{res.stdout}\n{res.stderr}")
        else:
            print(f"[{os.path.basename(filepath)} Block {i}]: Extracted {len(b.splitlines())} lines.")

