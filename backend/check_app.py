import sys
import os
sys.path.append(os.getcwd())

try:
    from app.main import app
    print("Successfully imported app")
except Exception as e:
    print(f"Failed to import app: {e}")
    import traceback
    traceback.print_exc()
