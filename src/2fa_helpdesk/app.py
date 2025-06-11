# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH
from pydantic import BaseModel
from typing import Annotated, Any, Dict, List, Optional

import jwt
import os
import fastapi
from fastapi import FastAPI, HTTPException, Security, security, status
from fastapi.responses import JSONResponse
import pydantic
from pydantic_settings import BaseSettings

import adapters.keycloak
import adapters.udm
import logging

class ResetUsersRequest(BaseModel):
    user_ids: List[str]

class ListUserQuery(BaseModel):
    query: Optional[str] = pydantic.Field(
        "", description="Search for users matching this query",
    )

class ResetResponse(BaseModel):
    success: bool
    detail: str
    resets_by_user: Dict[str, int] = pydantic.Field(
        "", description="Map of usernames to reset counts",
    )

class WhoAmIResponse(BaseModel):
    token: dict
    success: bool
    twofa_admin: bool

class ListUserResponse(BaseModel):
    users: List[adapters.keycloak.User]
    success: bool
    detail: str
    total: int
    total_pages: int
    page: int
    limit: int

class Settings(BaseSettings):
    oidc_host: str
    oidc_realm: str
    well_known_url: pydantic.HttpUrl
    token_url: pydantic.HttpUrl
    authorization_url: pydantic.HttpUrl
    jwks_url: pydantic.HttpUrl
    client_id: str
    permitted_jwt_audiences: List[str] = ["account"]


# init logger #
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

#
# Constants
#

OIDC_DEFAULT_SCOPES = ["openid"]

#
# OIDC Settings
#

oidc_host = os.environ["OIDC_HOST"].rstrip("/")
oidc_realm = os.environ["OIDC_REALM"].rstrip("/")

settings = Settings(
    well_known_url=f"{oidc_host}/realms/{oidc_realm}/.well-known/openid-configuration",
    token_url=f"{oidc_host}/realms/{oidc_realm}/protocol/openid-connect/token",
    authorization_url=f"{oidc_host}/realms/{oidc_realm}/login-actions/authenticate",
    jwks_url=f"{oidc_host}/realms/{oidc_realm}/protocol/openid-connect/certs",
    client_id=os.environ["OIDC_CLIENT_ID"],
)
jwks_client = jwt.PyJWKClient(settings.jwks_url)  # Caches JWKS


#
# Dependencies
#


oauth2_scheme = security.OAuth2AuthorizationCodeBearer(
    authorizationUrl=str(settings.authorization_url),
    tokenUrl=str(settings.token_url),
)

def _not_2fa_admin_msg(user_token):
    return f"You ({user_token['username']}) are not a 2FA admin."

def user_token(
    token_str: Annotated[str, Security(oauth2_scheme)],
    required_scopes: security.SecurityScopes,
):

    LOG.debug(token_str)
    # Parse & validate token
    try:
        token = jwt.decode(
            token_str,
            jwks_client.get_signing_key_from_jwt(token_str).key,
            algorithms=["RS256"],
            audience=settings.permitted_jwt_audiences,
        )
    except (RuntimeError, jwt.exceptions.DecodeError) as e:
        #print("Token no validated. Using Fake Token", e)
        #return {"username" : "Administrator",
        # "2fa_user_groups": ["2fa_admin", "test"],
        # "is_fake_token": True }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    # Validate scopes (if required)
    for scope in required_scopes.scopes:
        if scope not in token["scope"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={
                    "WWW-Authenticate": f'Bearer scope="{required_scopes.scope_str}"',
                },
            )

    return token


#
# App
#
backend_app = FastAPI(
    docs_url="/",
    openapi_url="/openapi.json",
    swagger_ui_init_oauth={
        "appName": "2FA Helpdesk Admin Backend",
        "clientId": settings.client_id,
        "usePkceWithAuthorizationCodeGrant": True,
        "url": "openapi.json",
    },
)

# Create a "root" app
app = FastAPI()

# Mount the backend app under the /backend prefix
prefix = os.environ.get("PREFIX") or "/"
app.mount(prefix, backend_app)

def is_2fa_admin(user_token: dict) -> bool:
    '''Check if a given user is a 2FA-Admin'''

    groups = user_token["2fa_user_groups"]
    twofa_admin_groups = os.environ["TWOFA_ADMIN_GROUPS"].split(",")
    return any([g in twofa_admin_groups for g in groups ])


@backend_app.post(
    "/token/reset/own/",
    dependencies=[Security(user_token, scopes=OIDC_DEFAULT_SCOPES)],
    response_model=ResetResponse,
)
def reset_own_token(user_token: Annotated[Dict[Any, Any], Security(user_token)]):

    user_id = user_token["sub"]
    results_count = adapters.keycloak.reset_2fa_token(user_id)
    return ResetResponse(
        success=True,
        detail="",
        resets_by_user={user_id: results_count},
    )

@backend_app.post(
    "/token/reset/user/",
    dependencies=[Security(user_token, scopes=OIDC_DEFAULT_SCOPES)],
    response_model=ResetResponse,
)
def reset_user_tokens(
    user_token: Annotated[Dict[Any, Any], Security(user_token)],
    body: ResetUsersRequest,
):

    results = dict()
    success = False
    if is_2fa_admin(user_token):
        for user_id in body.user_ids:
            reset_count = adapters.keycloak.reset_2fa_token(user_id)
            results.update({ "user_id": reset_count})
        success = True
        detail = ""
    else:
        success = False
        detail = _not_2fa_admin_msg(user_token)

    return ResetResponse(
        users=results,
        success=success,
        detail=detail,
    )


@backend_app.post(
    "/list_users",
    dependencies=[Security(user_token, scopes=OIDC_DEFAULT_SCOPES)],
    response_model=ListUserResponse,
)
def list_users(
    user_token: Annotated[Dict[Any, Any], Security(user_token)],
    page: Optional[int] = fastapi.Query(0),
    limit: Optional[int] = fastapi.Query(20),
    body: ListUserQuery = None,
):

    success = False
    users = None

    if body:
        query = body.query
    else:
        query = ""

    if is_2fa_admin(user_token):
        users, total = adapters.keycloak.list_users(query, page, limit)
        success = True
        detail = ""
    else:
        users, total = 0, 0
        success = False
        detail = _not_2fa_admin_msg(user_token)

    return ListUserResponse(
        users=users,
        success=success,
        detail=detail,
        total=total,
        total_pages=int(total/limit)+1,
        page=page,
        limit=limit,
    )

@backend_app.get(
    "/whoami",
    dependencies=[Security(user_token, scopes=OIDC_DEFAULT_SCOPES)],
    response_model=WhoAmIResponse,
)
def whoami(
    user_token: Annotated[Dict[Any, Any], Security(user_token)],
):

    return WhoAmIResponse(
        token=user_token,
        success=True, # FIXME
        twofa_admin=is_2fa_admin(user_token),
    )

@backend_app.get("/backend/openapi.json", include_in_schema=False)
@backend_app.get("//backend/openapi.json", include_in_schema=False)
async def custom_openapi():
    return JSONResponse(backend_app.openapi())
