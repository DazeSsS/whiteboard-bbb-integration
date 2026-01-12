from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class BearerTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.token = None

        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split()[1]
                request.state.token = token
            except Exception:
                pass

        response = await call_next(request)
        return response
