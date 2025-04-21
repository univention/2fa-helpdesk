# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH
from pydantic import BaseModel
from typing import List, Dict, Any, Annotated


from typing import Annotated, Any, Dict, List, Optional

import jwt
import os
from fastapi import FastAPI, HTTPException, Security, security, status
import pydantic
from pydantic_settings import BaseSettings

import os



import adapters.keycloak
import adapters.udm

class ResetUsersRequest(BaseModel):
    usernames: List[str]

class ListUserQuery(BaseModel):
    query: str

class Settings(BaseSettings):
    oidc_host: str
    oidc_realm: str
    well_known_url: pydantic.HttpUrl
    token_url: pydantic.HttpUrl
    authorization_url: pydantic.HttpUrl
    jwks_url: pydantic.HttpUrl
    client_id: str
    permitted_jwt_audiences: List[str] = ["account"]


oidc_host = os.environ["OIDC_HOST"].rstrip("/")
oidc_realm = os.environ["OIDC_REALM"].rstrip("/")

settings = Settings(
    well_known_url=f"{oidc_host}/realms/{oidc_realm}/.well-known/openid-configuration",
    token_url=f"{oidc_host}/realms/{oidc_realm}/protocol/openid-connect/token",
    authorization_url=f"{oidc_host}/realms/{oidc_realm}/login-actions/authenticate",
    jwks_url=f"{oidc_host}/realms/{oidc_realm}/protocol/openid-connect/certs",
    client_id=os.environ["OIDC_CLIENT_ID"]
)
jwks_client = jwt.PyJWKClient(settings.jwks_url)  # Caches JWKS


#
# Dependencies
#


oauth2_scheme = security.OAuth2AuthorizationCodeBearer(
    authorizationUrl=str(settings.authorization_url),
    tokenUrl=str(settings.token_url),
)


def user_token(
    token_str: Annotated[str, Security(oauth2_scheme)],
    required_scopes: security.SecurityScopes,
):

    # Parse & validate token
    try:
        token = jwt.decode(
            token_str,
            jwks_client.get_signing_key_from_jwt(token_str).key,
            algorithms=["RS256"],
            audience=settings.permitted_jwt_audiences,
        )
    except RuntimeError as e:
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
                    "WWW-Authenticate": f'Bearer scope="{required_scopes.scope_str}"'
                },
            )

    return token


#
# App
#
app = FastAPI(
    docs_url="/",
    swagger_ui_init_oauth={
        "appName": "2FA Helpdesk Admin Backend",
        "clientId": settings.client_id,
        "usePkceWithAuthorizationCodeGrant": True,
    },
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Custom Swagger UI",
        oauth2_redirect_url="/docs/oauth2-redirect",
    )

@app.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return HTMLResponse("""
    <html>
    <body>
      <script>
        'use strict';
        window.opener.postMessage(
          {
            type: 'authorization_response',
            response: {
              type: 'code',
              code: new URL(window.location).searchParams.get('code'),
              state: new URL(window.location).searchParams.get('state')
            }
          },
          window.location.origin
        );
        window.close();
      </script>
    </body>
    </html>
    """)

@app.post(
    "/token/reset/own",
    dependencies=[Security(user_token, scopes=["openid"])],
)
def reset_own_token(user_token: Annotated[Dict[Any, Any], Security(user_token)]):

    adapters.keycloak.two_fa.reset_token(user_token.username)
    return {
        "success": True,
        "details": "",
    }

@app.post(
    "/token/reset/user",
    dependencies=[Security(user_token, scopes=["openid"])],
)
def reset_user_tokens(
    user_token: Annotated[Dict[Any, Any], Security(user_token)],
    body: ResetUsersRequest
):

    results = dict()
    success = False
    if adapters.udm.is_2fa_admin(user_token.username):
        for username in body.usernames:
            reset_count = adapters.keycloak.reset_token(username)
            results.update({ "username": reset_count})
        success = True
        details = ""
    else:
        success = False
        details = f"You ({user_token.username}) are not a 2FA admin."

    return {
        "success": success,
        "details": details,
        "resets_by_user": results
    }


@app.post(
    "/list_users",
    dependencies=[Security(user_token, scopes=["openid"])]
)
def list_users(
    user_token: Annotated[Dict[Any, Any], Security(user_token)],
    body: ListUserQuery
):

    success = False
    users = None
    if adapters.udm.is_2fa_admin(user_token.username):
        users = adapters.udm.list_users(body.query)
        success = True
        details = ""
    else:
        success = False
        details = f"You ({user_token.username}) are not a 2FA admin."

    return {
        "users": users,
        "success": success,
        "details": details,
    }