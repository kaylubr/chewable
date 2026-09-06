from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_session
from core.services.oauth import (
    STATE_COOKIE_NAME,
    STATE_MAX_AGE_SECONDS,
    OAuthError,
    UnknownProviderError,
    authorize_url,
    error_redirect,
    is_valid_state,
    login_with_oauth_code,
    new_state_token,
    next_from_state,
    success_redirect,
    validate_next_path,
)

router = APIRouter(prefix="/auth", tags=["oauth"])


def _set_state_cookie(response: RedirectResponse, state: str) -> None:
    response.set_cookie(
        STATE_COOKIE_NAME,
        state,
        max_age=STATE_MAX_AGE_SECONDS,
        httponly=True,
        samesite="lax",
        secure=False,
    )


@router.get("/{provider}/authorize")
async def oauth_authorize(
    provider: str,
    next: str | None = Query(default=None),
) -> RedirectResponse:
    try:
        state = new_state_token(next_path=validate_next_path(next))
        url = authorize_url(provider, state)
    except UnknownProviderError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown provider") from None
    response = RedirectResponse(url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    _set_state_cookie(response, state)
    return response


@router.get("/{provider}/callback")
async def oauth_callback(
    provider: str,
    request: Request,
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> RedirectResponse:
    cookie_state = request.cookies.get(STATE_COOKIE_NAME)
    if error is not None:
        return RedirectResponse(error_redirect(error), status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    if code is None or state is None or cookie_state is None:
        return RedirectResponse(
            error_redirect("invalid_request"), status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
    if state != cookie_state or not is_valid_state(state):
        return RedirectResponse(
            error_redirect("state_mismatch"), status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )

    try:
        user = await login_with_oauth_code(session, provider, code)
    except UnknownProviderError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown provider") from None
    except OAuthError:
        return RedirectResponse(
            error_redirect("provider_error"), status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )

    redirect = RedirectResponse(
        success_redirect(user, next_from_state(state)),
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
    redirect.delete_cookie(STATE_COOKIE_NAME)
    return redirect
