
from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.config import API_KEY

async def api_key_middleware(request: Request, call_next):
    if API_KEY and request.url.path.startswith('/api/'):
        key = request.headers.get('x-api-key') or request.query_params.get('api_key')
        if key != API_KEY:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
    response = await call_next(request)
    return response
