import os
import sys

# Ensure backend is in path
current_dir = os.getcwd()
if current_dir.endswith("backend"):
    sys.path.append(current_dir)
elif current_dir.endswith("THE NFL SIM"):
    sys.path.append(os.path.join(current_dir, "backend"))

try:
    print("Import successful!")
except Exception as e:
    print(f"Import failed: {e}")
