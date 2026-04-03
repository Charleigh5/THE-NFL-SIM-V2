import re

with open(".github/workflows/ci.yml", "r") as f:
    content = f.read()

content = content.replace("NODE_VERSION: \"20\"", "NODE_VERSION: \"24\"")

with open(".github/workflows/ci.yml", "w") as f:
    f.write(content)

with open(".github/workflows/e2e-tests.yml", "r") as f:
    content = f.read()

content = content.replace("node-version: 20", "node-version: 24")

with open(".github/workflows/e2e-tests.yml", "w") as f:
    f.write(content)
