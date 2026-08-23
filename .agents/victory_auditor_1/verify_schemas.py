import re
import sys
import pydantic

files = [
    r"docs\design_theory\nfl_simulation_blueprint\physics_engine.md",
    r"docs\design_theory\nfl_simulation_blueprint\dynasty_empire.md",
    r"docs\design_theory\nfl_simulation_blueprint\broadcast_director.md",
    r"docs\design_theory\nfl_simulation_blueprint\ui_design_system.md",
]

print("=== VERIFYING PYTHON CODE BLOCKS IN BLUEPRINTS ===")
total_tested = 0
for filepath in files:
    print(f"\nProcessing: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract python code blocks
    pattern = r"```python\s*(.*?)\s*```"
    blocks = re.findall(pattern, content, re.DOTALL)
    print(f"Found {len(blocks)} python code blocks.")
    for idx, block in enumerate(blocks, 1):
        total_tested += 1
        print(f"  Testing block {idx} ({len(block.splitlines())} lines)...")
        # Compile and exec the block in an isolated namespace
        ns = {}
        try:
            exec(block, ns)
            print(f"  [PASS] Block {idx} executed successfully.")
        except Exception as e:
            print(f"  [FAIL] Block {idx} raised an exception: {e}")
            sys.exit(1)

print(f"\n[ALL {total_tested} PYTHON BLOCKS COMPILED AND EXECUTED WITH ZERO ERRORS]")
