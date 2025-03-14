import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.config_vars import CLERK_AUTHORIZED_PARTIES
from app.router import api_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Clerk FastAPI example",
    description="Clerk FastAPI example",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CLERK_AUTHORIZED_PARTIES.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.exception_handler(Exception)
async def http_exception_handler(request, exc):
    message = str(exc)
    logger.error(f"request: {request.url}, body {request.body}, exception: {message}")
    error_response = {
        "detail": ["Server error"],  # this will make it compliant with standard FastAPI error definition
    }
    return JSONResponse(error_response, status_code=exc.status_code if hasattr(exc, 'status_code') else 500)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# If using uvicorn directly in the file
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
