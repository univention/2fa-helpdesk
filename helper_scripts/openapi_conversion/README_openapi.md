<!-- Generator: Widdershins v4.0.1 -->

<h1 id="fastapi">FastAPI v0.1.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

# Authentication

- oAuth2 authentication. 

    - Flow: authorizationCode
    - Authorization URL = [https://id.ys-opendesk.test.rancher.falkenstein-2.potaris.de/realms/master/login-actions/authenticate](https://id.ys-opendesk.test.rancher.falkenstein-2.potaris.de/realms/master/login-actions/authenticate)
    - Token URL = [https://id.ys-opendesk.test.rancher.falkenstein-2.potaris.de/realms/master/protocol/openid-connect/token](https://id.ys-opendesk.test.rancher.falkenstein-2.potaris.de/realms/master/protocol/openid-connect/token)

|Scope|Scope Description|
|---|---|

<h1 id="fastapi-default">Default</h1>

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

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ListUserResponse](#schemalistuserresponse)|

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

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[ResetUsersRequest](#schemaresetusersrequest)|true|none|

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

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ResetResponse](#schemaresetresponse)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

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

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[ListUserQuery](#schemalistuserquery)|false|none|

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

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[ListUserResponse](#schemalistuserresponse)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

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

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[WhoAmIResponse](#schemawhoamiresponse)|

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

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

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

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|query|any|false|none|Search for users matching this query|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

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

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|users|[[User](#schemauser)]|true|none|none|
|succes|boolean|true|none|none|
|detail|string|true|none|none|

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

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|success|boolean|true|none|none|
|detail|string|true|none|none|
|resets_by_user|object|false|none|Map of usernames to reset counts|
|» **additionalProperties**|integer|false|none|none|

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

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|user_ids|[string]|true|none|none|

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

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|keycloak_internal_id|string|true|none|none|
|username|string|true|none|none|
|email|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|firstname|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|lastname|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|null|false|none|none|

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

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[anyOf]|true|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|msg|string|true|none|none|
|type|string|true|none|none|

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

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|token|object|true|none|none|
|success|boolean|true|none|none|
|twofa_admin|boolean|true|none|none|
