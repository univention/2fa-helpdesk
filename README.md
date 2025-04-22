# 2FA Admin Backend

This container image provides an API and business logic to connect the 2FA Admin Frontend module to Keycloak.

build with:

    docker build -f docker/backend/Dockerfile .
    # --net=host is required if you use kubeproxy
    # see .env sample file for environment help
    # run helper_scripts/environment.sh to extract info from a deployment
    docker run --net=host --env-file env.<yourfile> backend

# API

## POST `/token/reset/user`

Resets tokens for a list of specified users.

### Request Body

JSON object based on the `ResetUsersRequest` model:

```json
{
  "usernames": ["user1", "user2", "user3"]
}
```

### Response

```json
{
  "success": <bool>
  "details": <str>,
  "resets_by_user": {
    "user1": <int>,
    "user2": <int>,
    "user3": <int>"
  }
}
```

## POST `/token/reset/own`

Resets tokens for yourself, taking the username form the sub-claim of the OIDC-Token.

### Request Body

```json
None
```

### Response

```json
{
    "success" : <bool>
    "details" : <str>
}
```

## POST `/list_users`

Query applies to email, firstName, lastName and primaryMail for now.

### Request Body

```json
{
    "query" : str
}
```

### Response
A List of Users:

```json
{
    "users" : [
        {
            "username": <str>
            "email": <str>
            "firstname": <str>
            "lastname": <str>
        },
        ...
    ]
}
```
