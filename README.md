# 2FA Helpdesk

This project provides:
* 2fa backend: This handles all communication related to keycloak
* 2fa frontend: This provides a self-service and an admin page and allows to reset OTP tokens

## Local Development and Testing with Docker Compose

The project includes a Docker Compose setup for local development and testing. 
All necessary images can be built locally from the `docker/` directory.

### Prerequisites

- Docker and Docker Compose installed
- Git repository cloned locally

### Setting up test-realm on keycloak version changes

For all types of integration tests we need a keycloak realm which has a specific setup.
The realm's export is part of this repository and is loaded by keycloak in the docker compose environment.

This section describes how to (re-)create the realm if necessary.
The steps in this sections are only required to be executed whenever we change the keycloak version and the realm we've exported under `tests/integration/data/export/realm-export-with-user.json` doesn't work well anymore.

#### Start keycloak setup container

Start the keycloak setup container:
```shell
docker compose up -d keycloak-setup
docker compose exec -it keycloak-setup bash
```

Start keycloak within the setup container:
```shell
export PATH=/opt/keycloak/bin:$PATH
kc.sh start-dev
```

#### Configure keycloak via UI

1. Login as `admin` (pw: `admin`)  under `localhost:8080`
2. Create realm: `test-realm`
3. Create client: `2fa-helpdesk`
    - Activate `Direct Access Grants`
    - Set "Valid redirect URIs": `*`
    - Set "Valid post logout redirect URIs": `*`
    - Set "Web origins": `*`
4. Create groups:
    * `2fa-users`
    * `2FA Admins`
5. Create "Client Scope": `twofa-default`
    * Create and add new mapper: `2fa Groups`
      * Set "Claim Name": `2fa_user_groups`
      * Turn off the "Full group path" option
6. Add client scope `twofa-default` to client `2fa-helpdesk`
7. Adjust "Authentication Flow":
    * Deactivate OTP for `direct grant`
    * Change `browser/Conditional OTP` to required.
8. Create user with username `test`
    * Add user to groups:
      * `2fa-users`
      * `2FA Admins`
    * Create *non-temporary* password: `123qwe`

#### Export keycloak realm

Stop keycloak the keycloak setup container and export the realm (by Ctrl+C).
Then export the realms to JSON:

```shell
kc.sh export --file=/opt/keycloak/data/export/realm-export.json --optimized
```

Exit and shutdown the container:

```shell
docker compose down --timeout 0 keycloak-setup
```

Remove the admin user from the export to avoid failures on import:

```shell
jq '.[].users |= map(select(.realmRoles | index("admin") | not))' \
   tests/integration/data/export/realm-export.json \
   > tests/integration/data/export/realm-export-with-user.json
rm tests/integration/data/export/realm-export.json
```

### Building and Running Services

The Docker Compose configuration supports different profiles for different use cases:

#### Setup Integration Testing

To run the complete 2FA helpdesk stack with all services:

```shell
# Build all images and start the integration test environment
docker compose --profile test-it up --build

# This will start:
# - Keycloak server (localhost:8080)
# - 2FA Helpdesk Backend API (localhost:8081)
```

#### Running Integration Tests with Docker Compose

```shell
# (Re-)build and run the testrunner for testing tests/integration/api-2fa
docker compose run -it --rm --build testrunner

# Alternatively: (Re-)build and run the testrunner for testing tests/integration/api-2fa
docker compose run -it --rm --build testrunner pytest -vv tests/integration/api-2fa

# Run tests from above without explicit building
docker compose run -it --rm testrunner
docker compose run -it --rm testrunner pytest -vv tests/integration/api-2fa

```

In case you want to build and use images named the same as the one specified in the compose file:

```shell
# Build the testrunner image
docker compose --profile test-it up --build --no-start
docker compose --profile test-it down --remove-orphans --volumes

# Run the integration tests
docker compose run -it --rm testrunner pytest -vv tests/integration/api-2fa
```

#### Running Integration Tests locally

Prerequisites:

* Python 3.13

First load the pipenv environment:

```shell
cd docker/testrunner
pipenv sync
pipenv shell
cd -
```

The execute the tests:

```shell
pytest -vv tests/integration/api-2fa
```

#### Setup E2E Testing

To run the complete 2FA helpdesk stack with all services, to build all images and to start the e2e test environment for testing headless via docker compose:

```shell
docker compose --profile test-e2e-service up --build

# This will start:
# - Keycloak server (keycloak:8080, localhost:8080)
# - 2FA Helpdesk Backend API (api:8080, localhost:8081)
# - 2FA Helpdesk Frontend (keycloak:80)
```

In the scenario above `keycloak` and `frontend` share the same network (similar to a sidecar container in k8s).
The reason is, that otherwise keycloak won't make the login page available and raise a "Web Crypto API is not available" error in the browser. 
That's a security feature, which enforces that pure http requests for login are only supported from localhost.
Thus the e2e tests wouldn't run properly.
(see also https://github.com/keycloak/keycloak/issues/36804)

To run the complete 2FA helpdesk stack with all services, to build all images and start the e2e test environment for testing directly via pytest:

```shell

docker compose --profile test-e2e-local up --build

# This will start:
# - Keycloak server (keycloak:8080, localhost:8080)
# - 2FA Helpdesk Backend API (api:8080, localhost:8081)
# - 2FA Helpdesk Frontend (frontend:80, localhost:3000)
```
This allows also to test in headed mode which is helpful during development.

#### Running E2E Tests with Docker Compose

Ensure all services are started with the profile `test-e2e-service` (see [section on E2E setup](#setup-e2e-testing)).

```shell
# (Re-)build and run the testrunner for testing tests/integration/api-2fa
docker compose run -it --rm --build testrunner

# Alternatively: (Re-)build and run the testrunner for testing tests/integration/api-2fa
docker compose run -it --rm --build testrunner pytest -vv tests/integration/e2e

# Run tests from above without explicit building
docker compose run -it --rm testrunner
docker compose run -it --rm testrunner pytest -vv tests/integration/e2e

```

In case you want to build and use an image named the same as the one specified in the compose file:
```shell
# Build the testrunner image
docker compose --profile test-e2e up --build --no-start
docker compose --profile test-e2e down --remove-orphans --volumes

# Run the integration tests
docker compose run -it --rm testrunner pytest -vv tests/integration/e2e
```

#### Running E2E Tests locally

Prerequisites:

* Python 3.13

First load the pipenv environment:

```shell
cd docker/testrunner
pipenv sync
pipenv shell
cd -
```

The execute the tests:

```shell
pytest -vv tests/integration/e2e
```

#### Running Helm Chart Tests

```shell
# Run the test suite
docker compose run -it --rm test-chart

# Deal with trouble via pdb
docker compose run -it --rm test-chart tests/chart --pdb

# Have a shell
docker compose run -it --rm test-chart bash
pytest tests/chart
```

### Accessing Services

When running the full stack (either with profile `test-it` or `test-e2e-services`):
- Keycloak Admin Console: [http://localhost:8080/admin]() (username: admin & password:admin)
- Backend API: Available internally to other services or access under [http://localhost:8081]()

When running the full stack (with profile `test-e2e-local`):
- Keycloak Admin Console: [http://localhost:8080/admin]() (username: admin & password:admin)
- Backend API: Available internally to other services or access under [http://localhost:8081]()
- Frontend: Access under:
  - Self-Service: http://localhost:3000/univention/2fa/self-service
  - Admin Page: http://localhost:3000/univention/2fa/admin
  - User credentials: User `test` with password `123qwe`

### Rebuilding Images

To force rebuild all images:

```shell
docker compose --profile test-e2e build --no-cache
```

To rebuild a specific service:

```shell
docker compose build --no-cache api
```

# API
## reset_own_token_token_reset_own__post

<a id="opIdreset_own_token_token_reset_own__post"></a>

> Code samples

`POST /token/reset/own/`

*Reset Own Token*

> Example responses

> 200 Response

```json
{
  "users": [
    {
      "keycloak_internal_id": "string",
      "username": "string",
      "email": "string",
      "firstname": "string",
      "lastname": "string"
    }
  ],
  "succes": true,
  "detail": "string"
}
```

<h3 id="reset_own_token_token_reset_own__post-responses">Responses</h3>

| Status | Meaning                                                 | Description         | Schema                                      |
| ------ | ------------------------------------------------------- | ------------------- | ------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | [ListUserResponse](#schemalistuserresponse) |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2AuthorizationCodeBearer ( Scopes: openid ), OAuth2AuthorizationCodeBearer
</aside>

## reset_user_tokens_token_reset_user__post

<a id="opIdreset_user_tokens_token_reset_user__post"></a>

> Code samples

`POST /token/reset/user/`

*Reset User Tokens*

> Body parameter

```json
{
  "user_ids": [
    "string"
  ]
}
```

<h3 id="reset_user_tokens_token_reset_user__post-parameters">Parameters</h3>

| Name | In   | Type                                          | Required | Description |
| ---- | ---- | --------------------------------------------- | -------- | ----------- |
| body | body | [ResetUsersRequest](#schemaresetusersrequest) | true     | none        |

> Example responses

> 200 Response

```json
{
  "success": true,
  "detail": "string",
  "resets_by_user": ""
}
```

<h3 id="reset_user_tokens_token_reset_user__post-responses">Responses</h3>

| Status | Meaning                                                                  | Description         | Schema                                            |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [ResetResponse](#schemaresetresponse)             |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2AuthorizationCodeBearer ( Scopes: openid ), OAuth2AuthorizationCodeBearer
</aside>

## list_users_list_users_post

<a id="opIdlist_users_list_users_post"></a>

> Code samples

`POST /list_users`

*List Users*

> Body parameter

```json
{
  "query": ""
}
```

<h3 id="list_users_list_users_post-parameters">Parameters</h3>

| Name | In   | Type                                  | Required | Description |
| ---- | ---- | ------------------------------------- | -------- | ----------- |
| body | body | [ListUserQuery](#schemalistuserquery) | false    | none        |

> Example responses

> 200 Response

```json
{
  "users": [
    {
      "keycloak_internal_id": "string",
      "username": "string",
      "email": "string",
      "firstname": "string",
      "lastname": "string"
    }
  ],
  "succes": true,
  "detail": "string"
}
```

<h3 id="list_users_list_users_post-responses">Responses</h3>

| Status | Meaning                                                                  | Description         | Schema                                            |
| ------ | ------------------------------------------------------------------------ | ------------------- | ------------------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)                  | Successful Response | [ListUserResponse](#schemalistuserresponse)       |
| 422    | [Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3) | Validation Error    | [HTTPValidationError](#schemahttpvalidationerror) |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2AuthorizationCodeBearer ( Scopes: openid ), OAuth2AuthorizationCodeBearer
</aside>

## whoami_whoami_get

<a id="opIdwhoami_whoami_get"></a>

> Code samples

`GET /whoami`

*Whoami*

> Example responses

> 200 Response

```json
{
  "token": {},
  "success": true,
  "twofa_admin": true
}
```

<h3 id="whoami_whoami_get-responses">Responses</h3>

| Status | Meaning                                                 | Description         | Schema                                  |
| ------ | ------------------------------------------------------- | ------------------- | --------------------------------------- |
| 200    | [OK](https://tools.ietf.org/html/rfc7231#section-6.3.1) | Successful Response | [WhoAmIResponse](#schemawhoamiresponse) |

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2AuthorizationCodeBearer ( Scopes: openid ), OAuth2AuthorizationCodeBearer
</aside>

# Schemas

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

| Name   | Type                                        | Required | Restrictions | Description |
| ------ | ------------------------------------------- | -------- | ------------ | ----------- |
| detail | [[ValidationError](#schemavalidationerror)] | false    | none         | none        |

<h2 id="tocS_ListUserQuery">ListUserQuery</h2>
<!-- backwards compatibility -->
<a id="schemalistuserquery"></a>
<a id="schema_ListUserQuery"></a>
<a id="tocSlistuserquery"></a>
<a id="tocslistuserquery"></a>

```json
{
  "query": ""
}

```

ListUserQuery

### Properties

| Name  | Type | Required | Restrictions | Description                          |
| ----- | ---- | -------- | ------------ | ------------------------------------ |
| query | any  | false    | none         | Search for users matching this query |

anyOf

| Name          | Type   | Required | Restrictions | Description |
| ------------- | ------ | -------- | ------------ | ----------- |
| » *anonymous* | string | false    | none         | none        |

or

| Name          | Type | Required | Restrictions | Description |
| ------------- | ---- | -------- | ------------ | ----------- |
| » *anonymous* | null | false    | none         | none        |

<h2 id="tocS_ListUserResponse">ListUserResponse</h2>
<!-- backwards compatibility -->
<a id="schemalistuserresponse"></a>
<a id="schema_ListUserResponse"></a>
<a id="tocSlistuserresponse"></a>
<a id="tocslistuserresponse"></a>

```json
{
  "users": [
    {
      "keycloak_internal_id": "string",
      "username": "string",
      "email": "string",
      "firstname": "string",
      "lastname": "string"
    }
  ],
  "succes": true,
  "detail": "string"
}

```

ListUserResponse

### Properties

| Name   | Type                  | Required | Restrictions | Description |
| ------ | --------------------- | -------- | ------------ | ----------- |
| users  | [[User](#schemauser)] | true     | none         | none        |
| succes | boolean               | true     | none         | none        |
| detail | string                | true     | none         | none        |

<h2 id="tocS_ResetResponse">ResetResponse</h2>
<!-- backwards compatibility -->
<a id="schemaresetresponse"></a>
<a id="schema_ResetResponse"></a>
<a id="tocSresetresponse"></a>
<a id="tocsresetresponse"></a>

```json
{
  "success": true,
  "detail": "string",
  "resets_by_user": ""
}

```

ResetResponse

### Properties

| Name                       | Type    | Required | Restrictions | Description                      |
| -------------------------- | ------- | -------- | ------------ | -------------------------------- |
| success                    | boolean | true     | none         | none                             |
| detail                     | string  | true     | none         | none                             |
| resets_by_user             | object  | false    | none         | Map of usernames to reset counts |
| » **additionalProperties** | integer | false    | none         | none                             |

<h2 id="tocS_ResetUsersRequest">ResetUsersRequest</h2>
<!-- backwards compatibility -->
<a id="schemaresetusersrequest"></a>
<a id="schema_ResetUsersRequest"></a>
<a id="tocSresetusersrequest"></a>
<a id="tocsresetusersrequest"></a>

```json
{
  "user_ids": [
    "string"
  ]
}

```

ResetUsersRequest

### Properties

| Name     | Type     | Required | Restrictions | Description |
| -------- | -------- | -------- | ------------ | ----------- |
| user_ids | [string] | true     | none         | none        |

<h2 id="tocS_User">User</h2>
<!-- backwards compatibility -->
<a id="schemauser"></a>
<a id="schema_User"></a>
<a id="tocSuser"></a>
<a id="tocsuser"></a>

```json
{
  "keycloak_internal_id": "string",
  "username": "string",
  "email": "string",
  "firstname": "string",
  "lastname": "string"
}

```

User

### Properties

| Name                 | Type   | Required | Restrictions | Description |
| -------------------- | ------ | -------- | ------------ | ----------- |
| keycloak_internal_id | string | true     | none         | none        |
| username             | string | true     | none         | none        |
| email                | any    | false    | none         | none        |

anyOf

| Name          | Type   | Required | Restrictions | Description |
| ------------- | ------ | -------- | ------------ | ----------- |
| » *anonymous* | string | false    | none         | none        |

or

| Name          | Type | Required | Restrictions | Description |
| ------------- | ---- | -------- | ------------ | ----------- |
| » *anonymous* | null | false    | none         | none        |

continued

| Name      | Type | Required | Restrictions | Description |
| --------- | ---- | -------- | ------------ | ----------- |
| firstname | any  | false    | none         | none        |

anyOf

| Name          | Type   | Required | Restrictions | Description |
| ------------- | ------ | -------- | ------------ | ----------- |
| » *anonymous* | string | false    | none         | none        |

or

| Name          | Type | Required | Restrictions | Description |
| ------------- | ---- | -------- | ------------ | ----------- |
| » *anonymous* | null | false    | none         | none        |

continued

| Name     | Type | Required | Restrictions | Description |
| -------- | ---- | -------- | ------------ | ----------- |
| lastname | any  | false    | none         | none        |

anyOf

| Name          | Type   | Required | Restrictions | Description |
| ------------- | ------ | -------- | ------------ | ----------- |
| » *anonymous* | string | false    | none         | none        |

or

| Name          | Type | Required | Restrictions | Description |
| ------------- | ---- | -------- | ------------ | ----------- |
| » *anonymous* | null | false    | none         | none        |

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

| Name | Type    | Required | Restrictions | Description |
| ---- | ------- | -------- | ------------ | ----------- |
| loc  | [anyOf] | true     | none         | none        |

anyOf

| Name          | Type   | Required | Restrictions | Description |
| ------------- | ------ | -------- | ------------ | ----------- |
| » *anonymous* | string | false    | none         | none        |

or

| Name          | Type    | Required | Restrictions | Description |
| ------------- | ------- | -------- | ------------ | ----------- |
| » *anonymous* | integer | false    | none         | none        |

continued

| Name | Type   | Required | Restrictions | Description |
| ---- | ------ | -------- | ------------ | ----------- |
| msg  | string | true     | none         | none        |
| type | string | true     | none         | none        |

<h2 id="tocS_WhoAmIResponse">WhoAmIResponse</h2>
<!-- backwards compatibility -->
<a id="schemawhoamiresponse"></a>
<a id="schema_WhoAmIResponse"></a>
<a id="tocSwhoamiresponse"></a>
<a id="tocswhoamiresponse"></a>

```json
{
  "token": {},
  "success": true,
  "twofa_admin": true
}

```

WhoAmIResponse

### Properties

| Name        | Type    | Required | Restrictions | Description |
| ----------- | ------- | -------- | ------------ | ----------- |
| token       | object  | true     | none         | none        |
| success     | boolean | true     | none         | none        |
| twofa_admin | boolean | true     | none         | none        |
