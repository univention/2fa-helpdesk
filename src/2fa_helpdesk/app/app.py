# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from typing import Annotated, Any, Dict, List, Optional

import jwt
from fastapi import FastAPI, HTTPException, Security, security, status
from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    authorization_url: HttpUrl
    token_url: HttpUrl
    jwks_url: HttpUrl
    client_id: str
    permitted_jwt_audiences: List[str] = ["account"]


settings = Settings(
    authorization_url="https://id.jahlers-opendesk.univention.dev/realms/opendesk/login-actions/authenticate",
    token_url="https://id.jahlers-opendesk.univention.dev/realms/opendesk/protocol/openid-connect/token",
    jwks_url="https://id.jahlers-opendesk.univention.dev/realms/opendesk/protocol/openid-connect/certs",
    client_id="admin-cli",
)
jwks_client = jwt.PyJWKClient(settings.jwks_url)  # Caches JWKS


#
# Dependencies
#
oauth2_scheme = security.OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.authorization_url,
    tokenUrl=settings.token_url,
    # scopes={ # Populate UI for scope selection checkboxes
    #     f"example:{resource}:{action}": f"{action.title()} {resource}"
    #     for resource in ["note"]
    #     for action in ["create", "read", "update", "delete"]
    # },
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
    except Exception as e:
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
        "appName": "ExampleApp",
        "clientId": settings.client_id,
        "usePkceWithAuthorizationCodeGrant": True,
    },
)


@app.get(
    "/token/reset/own",
    dependencies=[Security(user_token, scopes=["openid"])],
)
def reset_own_token(user_token: Annotated[Dict[Any, Any], Security(user_token)]):
    return {
        "success": True,
        "details": "Hello World!",
    }


@app.post(
    "/token/reset/user",
    dependencies=[Security(user_token, scopes=["openid"])],
)
def reset_user_tokens(user_token: Annotated[Dict[Any, Any], Security(user_token)]):
    return {
        "success": True,
        "details": "Hello World!",
    }


@app.post(
    "list_users",
    dependencies=[Security(user_token, scopes=["openid"])],
)
def list_users(user_token: Annotated[Dict[Any, Any], Security(user_token)]):
    return {
        "success": True,
        "details": "Hello World!",
    }
