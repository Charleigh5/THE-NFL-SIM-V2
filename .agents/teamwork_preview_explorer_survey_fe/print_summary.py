import json
from pathlib import Path

REPO_ROOT = Path(r"c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2")
with open(REPO_ROOT / ".agents" / "teamwork_preview_explorer_survey_fe" / "audit_summary.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== UNREACHABLE FILES (TOTAL: %d) ===" % len(data["unreachable_files"]))
for f in data["unreachable_files"]:
    print(f" - {f}")

print("\n=== PAGES AUDIT ===")
for p, pdata in data["pages"].items():
    print(f"Page: {p} | Reachable: {pdata['reachable']} | Imported by: {pdata['imported_by']}")

print("\n=== UNREACHABLE / ORPHANED COMPONENTS ===")
unmounted_comps = [c for c, cdata in data["components"].items() if not cdata["reachable"]]
print(f"Total unmounted components: {len(unmounted_comps)}")
for c in unmounted_comps:
    print(f" - {c} (Imported by: {data['components'][c]['imported_by']})")
