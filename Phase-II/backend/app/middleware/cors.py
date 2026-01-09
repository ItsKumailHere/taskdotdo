"""
Custom middleware for the TaskDo backend
"""
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging


logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add timing information to requests
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"{request.method} {request.url.path} - {process_time:.3f}s")
        
        return response


class CORSMiddleware:
    """
    Basic CORS middleware
    Note: In production, use Starlette's CORSMiddleware instead
    """
    def __init__(self, app, allow_origins=None):
        self.app = app
        self.allow_origins = allow_origins or ["*"]
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        
        # Add CORS headers
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # Check if CORS headers are already set
                headers = message.get("headers", [])
                
                # Add CORS headers if not present
                cors_headers = [
                    (b"access-control-allow-origin", b"*"),
                    (b"access-control-allow-credentials", b"true"),
                    (b"access-control-allow-headers", b"*"),
                    (b"access-control-allow-methods", b"*"),
                ]
                
                # Add CORS headers to the response
                for header_name, header_value in cors_headers:
                    if not any(h[0] == header_name for h in headers):
                        headers.append((header_name, header_value))
                
                message["headers"] = headers
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)