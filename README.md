# 2FA Admin Backend

This container image provides an API and business logic to connect the 2FA Admin Frontend module to Keycloak.

## Local Development and Testing with Docker Compose

The project includes a Docker Compose setup for local development and testing. All necessary images can be built locally from the `docker/` directory.

### Prerequisites

- Docker and Docker Compose installed
- Git repository cloned locally

### Setting up test-realm on keycloak version changes

The steps in this sections are only required to be executed whenever we change the keycloak version and the realm we've exported under `tests/data/export/realm-export-with-user.json` doesn't work well anymore.

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
    *  Add new mapper: `2fa Groups`
      *  Set "Claim Name": `2fa_user_groups`
6. Add client scope `twofa-default` to client `2fa-helpdesk`
7. Adjust "Authentication Flow":
    * Deactivate OTP for `direct grant`
    * Change `browser/Conditional OTP` to required.
8. Create user with username `test`
    * Add user to groups: 
      * `2fa-users`
      * `2FA Admins`
    * Create *non-temporary* password** `123qwe`

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
   tests/data/export/realm-export.json \
   > tests/data/export/realm-export-with-user.json
rm tests/data/export/realm-export.json
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
# (Re-)build and run the testrunner for testing tests/twofa
docker compose run -it --rm --build testrunner

# Alternatively: (Re-)build and run the testrunner for testing tests/twofa
docker compose run -it --rm --build testrunner pytest --vv tests/twofa

# Run tests from above without explicit building
docker compose run -it --rm testrunner
docker compose run -it --rm testrunner pytest --vv tests/twofa

```

In case you want to build and use an image named the same as the one specified in the compose file:
```shell
# Build the testrunner image
docker compose --profile testrunner up --build --no-start
docker compose --profile testrunner down --remove-orphans --volumes

# Run the integration tests
docker compose run -it --rm testrunner pytest -vv tests/twofa
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
# Load environment file
source .env.test.local
pytest -vv tests/twofa
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

### Environment Configuration

For integration testing, create a `.env.test` file with the necessary environment variables. You can use the provided `docker-env.sample` as a template:

```shell
cp docker-env.sample .env.test
# Edit .env.test with your specific configuration
```

### Accessing Services

When running the full stack:
- Keycloak Admin Console: [http://localhost:8080/admin]() (username: admin & password:admin)
- Backend API: Available internally to other services or access under [http://localhost:8081]()

### Rebuilding Images

To force rebuild all images:

```shell
docker compose --profile test-it build --no-cache
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
