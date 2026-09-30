import logging
import time
import uuid

logger = logging.getLogger("api.access")

class LoggingMiddleware:
    """Pure ASGI logging middleware providing sub-millisecond dispatch and header injection."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        if "state" not in scope:
            scope["state"] = {}
        scope["state"]["request_id"] = request_id

        start_time = time.time()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.append((b"x-request-id", request_id.encode("latin1")))
                process_time = (time.time() - start_time) * 1000
                headers.append((b"x-process-time-ms", str(round(process_time, 2)).encode("latin1")))
                message["headers"] = headers
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"Request failed",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "process_time_ms": round(process_time, 2),
                }
            )
            raise e
