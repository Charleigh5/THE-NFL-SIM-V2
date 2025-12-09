#!/usr/bin/env python3
"""
NFL Sim Engine - Quick Start Runner
====================================

Simplified runner to execute the build automation with pre-authorized approvals.

Usage:
    python scripts/run_automation.py           # Run all batches
    python scripts/run_automation.py --batch 3 # Start from batch 3
    python scripts/run_automation.py --dry-run # Preview without changes
"""

import subprocess
import sys
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    automation_script = script_dir / "automate_build.py"

    if not automation_script.exists():
        print(f"Error: {automation_script} not found")
        sys.exit(1)

    # Build command with all arguments passed through
    cmd = [sys.executable, str(automation_script)] + sys.argv[1:]

    print("=" * 60)
    print("NFL SIM ENGINE - AUTOMATED BUILD")
    print("=" * 60)
    print(f"Running: {' '.join(cmd)}")
    print("=" * 60)
    print()

    # Run the automation script
    result = subprocess.run(cmd, cwd=script_dir.parent)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
