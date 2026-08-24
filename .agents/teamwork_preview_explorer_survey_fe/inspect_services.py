import re
import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
FRONTEND_SRC = REPO_ROOT / "frontend" / "src"

services_dir = FRONTEND_SRC / "services"
services_report = {}

for sf in sorted(services_dir.glob("*.ts")):
    with open(sf, "r", encoding="utf-8") as fh:
        code = fh.read()
    
    mock_hits = []
    for idx, line in enumerate(code.splitlines(), 1):
        low = line.lower()
        if any(w in low for w in ["mock", "dummy", "fake", "stub", "todo", "fixme", "hardcoded"]):
            mock_hits.append((idx, line.strip()))

    services_report[sf.name] = {
        "lines": len(code.splitlines()),
        "mock_hits": mock_hits
    }

for s_name, data in services_report.items():
    print(f"SERVICE: {s_name} ({data['lines']} lines) - Mock hits: {len(data['mock_hits'])}")
    for mh in data["mock_hits"]:
        print(f"  L{mh[0]}: {mh[1]}")
    print()
