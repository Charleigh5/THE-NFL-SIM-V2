try:
    import websockets
    print("websockets installed")
except ImportError:
    print("websockets NOT installed")

try:
    import httpx
    print("httpx installed")
except ImportError:
    print("httpx NOT installed")
