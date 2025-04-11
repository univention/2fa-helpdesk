# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import json
from base64 import b64decode
from binascii import Error
from univention.admin.rest.client import UDM
# from udm_rest_client.udm import UDM


class UDMCredentialError(Exception):
    pass


def udm_module(
    uri: str,
    udm_module: str = "users/user",
    token: str | None = None,
    username: str | None = None,
    password: str | None = None,
):
    if token:
        try:
            payload = json.loads(b64decode(token.split[1] + "==="))
            username = payload["uid"]
        except (json.JSONDecodeError, Error, KeyError):
            raise UDMCredentialError("Invalid bearer token")
        udm = UDM.bearer(uri, token)
    elif username and password:
        username = username
        udm = UDM.http(uri, username, password)
    else:
        raise UDMCredentialError("Insufficient authentication data")
    module = udm.get(udm_module)
    return module
