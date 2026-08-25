import os
import re

fe_services_dir = os.path.abspath('frontend/src/services')
be_api_dir = os.path.abspath('backend/app/api')

print("=== Frontend Services Endpoints ===")
for fname in sorted(os.listdir(fe_services_dir)):
    if fname.endswith('.ts'):
        fpath = os.path.join(fe_services_dir, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fl:
            content = fl.read()
        endpoints = re.findall(r'[\'"`](/api/[^\'"`\s]+)[\'"`]', content)
        print(f"\n{fname} ({len(endpoints)} endpoints):")
        for ep in sorted(set(endpoints)):
            print(f"  {ep}")

print("\n=== Backend Route Registration (api.py) ===")
api_py = os.path.join(be_api_dir, 'api.py')
with open(api_py, 'r', encoding='utf-8') as fl:
    lines = [l.strip() for l in fl.readlines() if 'include_router' in l]
for l in lines:
    print(f"  {l}")
