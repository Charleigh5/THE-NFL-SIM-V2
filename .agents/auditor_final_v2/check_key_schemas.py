import os

def check_file(path, label):
    print(f"=== {label}: {path} ===")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f, 1):
                if any(k in line for k in ['class ', 'interface ', 'type ', 'neck_health', 'ceiling_grade', 'floor_grade', 'notes']):
                    print(f"  {idx}: {line.rstrip()}")
    else:
        print("  FILE NOT FOUND!")

# Medical
check_file('backend/app/schemas/deep_dive.py', 'Backend Deep Dive / Medical')
check_file('frontend/src/types/medical.ts', 'Frontend Medical')

# Scouting
check_file('backend/app/schemas/scouting.py', 'Backend Scouting')
check_file('frontend/src/types/api/scouting.ts', 'Frontend Scouting')

# Coach
check_file('backend/app/schemas/coach.py', 'Backend Coach')

# Trade
check_file('backend/app/schemas/trade.py', 'Backend Trade')
check_file('frontend/src/types/trade.ts', 'Frontend Trade')
