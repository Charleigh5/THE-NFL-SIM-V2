import os
import sys
import re

sys.path.insert(0, os.path.abspath('backend'))

from app.core.app_factory import create_app
from fastapi.routing import APIRoute

app = create_app()

def extract_routes(app_obj):
    # Use OpenAPI schema generation to get 100% of routes reliably
    openapi_schema = app_obj.openapi()
    routes = []
    paths = openapi_schema.get("paths", {})
    for path, methods_dict in paths.items():
        for method in methods_dict:
            if method.lower() in ["get", "post", "put", "delete", "patch", "options", "head"]:
                routes.append((method.upper(), path))
    return routes

all_be_routes = extract_routes(app)
print(f"Total OpenAPI Endpoint Operations: {len(all_be_routes)}")
unique_paths = sorted(set(r[1] for r in all_be_routes))
print(f"Total Unique Endpoint Paths: {len(unique_paths)}")

print("\n--- Sample Registered Backend Routes ---")
for p in unique_paths[:30]:
    print(f"  {p}")

# Read all frontend services
fe_services_dir = os.path.abspath('frontend/src/services')
all_service_urls = []

for fname in sorted(os.listdir(fe_services_dir)):
    if fname.endswith('.ts'):
        fpath = os.path.join(fe_services_dir, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fl:
            content = fl.read()
        # Find raw /api/ strings
        raw_urls = re.findall(r'[\'"`](/api/[^\'"`\s\?]+)[\'"`\?]', content)
        for u in raw_urls:
            all_service_urls.append((fname, u))

print(f"\nTotal Frontend API URL invocations: {len(all_service_urls)}")

# Verify matches
unmatched = []
matched_count = 0
for fname, u in all_service_urls:
    # Convert JS template literals like /api/players/${playerId}/stats -> /api/players/{player_id}/stats
    norm_u = re.sub(r'\$\{[^}]+\}', r'[^/]+', u)
    pattern = '^' + norm_u + '$'
    
    is_match = False
    for be_path in unique_paths:
        be_norm = re.sub(r'\{[^}]+\}', r'[^/]+', be_path)
        be_pattern = '^' + be_norm + '$'
        if re.match(pattern, be_path) or re.match(be_pattern, u):
            is_match = True
            break
        # also check exact string match ignoring param name differences
        p1 = re.sub(r'\$\{[^}]+\}', '{X}', u)
        p2 = re.sub(r'\{[^}]+\}', '{X}', be_path)
        if p1 == p2:
            is_match = True
            break
    
    if is_match:
        matched_count += 1
    else:
        unmatched.append((fname, u))

print(f"\nMatched Frontend URLs: {matched_count} / {len(all_service_urls)}")
print(f"Unmatched URLs: {len(unmatched)}")
if unmatched:
    for fname, u in unmatched:
        print(f"  [{fname}] {u}")
