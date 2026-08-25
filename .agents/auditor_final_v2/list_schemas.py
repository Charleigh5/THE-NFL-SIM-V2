import os

be_schemas_dir = os.path.abspath('backend/app/schemas')
fe_types_dir = os.path.abspath('frontend/src/types')

print("=== Backend Schema Files ===")
for root, dirs, files in os.walk(be_schemas_dir):
    for f in files:
        if f.endswith('.py') and not f.startswith('__'):
            rel = os.path.relpath(os.path.join(root, f), be_schemas_dir)
            print(f"  backend/app/schemas/{rel}")

print("\n=== Frontend Type Files ===")
for root, dirs, files in os.walk(fe_types_dir):
    for f in files:
        if f.endswith(('.ts', '.d.ts')):
            rel = os.path.relpath(os.path.join(root, f), fe_types_dir)
            print(f"  frontend/src/types/{rel}")
