from clerk_backend_api import authenticate_request, AuthenticateRequestOptions
from fastapi import HTTPException, Request
from starlette import status

from app.config_vars import CLERK_API_SECRET_KEY, CLERK_AUTHORIZED_PARTIES


async def authenticated_user(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        request_state = authenticate_request(
            request,
            AuthenticateRequestOptions(
                secret_key=CLERK_API_SECRET_KEY,
                authorized_parties=CLERK_AUTHORIZED_PARTIES,
            ),
        )
        if request_state.reason:
            raise credentials_exception
        username: str = request_state.payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    return username