import mcp
import inspect
import pkgutil

def list_modules(package):
    if hasattr(package, "__path__"):
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            print(f"Module: {name}, is_pkg: {is_pkg}")

print("Top level mcp:")
print(dir(mcp))
list_modules(mcp)

try:
    from mcp import client
    print("\nmcp.client:")
    print(dir(client))
    list_modules(client)
except ImportError:
    print("\nNo mcp.client module")
