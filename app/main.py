import logging
from typing import List, Annotated

from fastapi import FastAPI
from pydantic_settings import BaseSettings
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pydantic import Field, field_validator

from app.router import api_router

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    clerk_api_secret_key: str
    clerk_authorized_parties: str

    # override property to return list from comma separated string
    @property
    def clerk_authorized_parties(self) -> List[str]:
        return self.clerk_authorized_parties.split(",")



settings = Settings()
app = FastAPI(
    title="Clerk FastAPI example",
    description="Clerk FastAPI example",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.clerk_authorized_parties,
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


# If using uvicorn directly in the file
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
