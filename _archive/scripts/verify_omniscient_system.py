import sys
import os
import unittest

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

# Import all verification functions
from backend.tests.test_genesis_omniscient import test_genesis_omniscient
from backend.tests.test_empire_omniscient import test_empire_omniscient
from backend.tests.test_hive_omniscient import test_hive_omniscient
from backend.tests.test_society_omniscient import test_society_omniscient
from backend.tests.test_core_omniscient import test_core_omniscient
from backend.tests.test_rpg_omniscient import test_rpg_omniscient

def verify_omniscient_system():
    print("==============================================")
    print("   CORTEX OMNISCIENT BUILD v5.0 - SYSTEM VERIFICATION")
    print("==============================================\n")

    try:
        print(">>> [1/6] VERIFYING GENESIS ENGINE (Bio/Neuro)...")
        test_genesis_omniscient()
        print(">>> GENESIS ENGINE: PASS\n")

        print(">>> [2/6] VERIFYING EMPIRE ENGINE (Financial/Owner)...")
        test_empire_omniscient()
        print(">>> EMPIRE ENGINE: PASS\n")

        print(">>> [3/6] VERIFYING HIVE ENGINE (Physics/Weather)...")
        test_hive_omniscient()
        print(">>> HIVE ENGINE: PASS\n")

        print(">>> [4/6] VERIFYING SOCIETY ENGINE (Social/Narrative)...")
        test_society_omniscient()
        print(">>> SOCIETY ENGINE: PASS\n")

        print(">>> [5/6] VERIFYING CORE ENGINE (Sim/AI)...")
        test_core_omniscient()
        print(">>> CORE ENGINE: PASS\n")

        print(">>> [6/6] VERIFYING RPG ENGINE (Progression/Training)...")
        test_rpg_omniscient()
        print(">>> RPG ENGINE: PASS\n")

        print("==============================================")
        print("   ALL SYSTEMS OPERATIONAL. READY FOR DEPLOYMENT.")
        print("==============================================")
        return True

    except Exception as e:
        print(f"\n!!! SYSTEM VERIFICATION FAILED !!!")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    verify_omniscient_system()
