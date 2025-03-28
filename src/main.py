from fastapi import FastAPI, HTTPException, Query
from typing import List
import requests
from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakGetError
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

# Configuration - adjust as needed
KEYCLOAK_URL = "http://localhost:8080/"
REALM_NAME = "master"
USERNAME = "admin"
PASSWORD = "admin"
TARGET_ROLE = "2fa"

UDM_USER = "Administrator"
UDM_PASSWORD = "univention"

UDM_HOST =  ""
UDM_URL = f"https://${UDM_HOST}/univention/udm"
REQUIRED_GROUP = "2fa-admins"

VERIFY_SSL = False

security = HTTPBasic()

# Request body model
class Reset2FARequest(BaseModel):
    username: str

# Request model
class GroupToRoleRequest(BaseModel):
    group_name: str

def is_functional_admin(username):

    try:
        guardian = Guardian()
        user_roles = guardian.get_roles_of_user(username)

        for role in user_roles:
            if role.get("name") == "Functional Admin":
                return True

        return False

    except GuardianError as e:
        print(f"Guardian error occurred: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def verify_user_in_group(credentials: HTTPBasicCredentials = Depends(security)):
    """FastAPI dependency that checks if user is part of a UDM group."""

    auth = HTTPBasicAuth(credentials.username, credentials.password)

    user_url = f"{UDM_URL}/users/user"

    try:

        resp = requests.get(user_url, auth=auth,
                                params={"filter": f"username={credentials.username}"}, verify=VERIFY_SSL)

        if not resp.ok or not resp.json().get("items"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid UDM credentials")

        user_info = resp.json()["items"][0]
        user_dn = user_info["dn"]

        group_url = f"{UDM_URL}/groups"
        group_resp = requests.get(group_url, auth=auth,
                                  params={"filter": f"name={REQUIRED_GROUP}"}, verify=VERIFY_SSL)
        if not group_resp.ok or not group_resp.json().get("items"):
            raise HTTPException(status_code=403, detail=f"Required group '{REQUIRED_GROUP}' not found")

        group_members = group_resp.json()["items"][0].get("users", [])

        if user_dn not in group_members:
            raise HTTPException(status_code=403, detail="User is not authorized")

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to UDM: {str(e)}")

def get_kc_admin():
    try:
        kc_admin = KeycloakAdmin(
            server_url=KEYCLOAK_URL,
            username=USERNAME,
            password=PASSWORD,
            realm_name=REALM_NAME,
            client_id="admin-cli",
            verify=True  # Set to False if using self-signed certs
        )
        return kc_admin
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keycloak connection error: {str(e)}")


@app.get("/2fa-groups")
def get_2fa_groups():
    kc = get_kc_admin()

    try:
        groups = kc.get_role_groups(name=TARGET_ROLE)
    except KeycloakGetError as e:
        raise HTTPException(status_code=404, detail=f"Error fetching groups for role '{TARGET_ROLE}': {str(e)}")

    return {"role": TARGET_ROLE, "groups": groups}

def _get_users_in_groups(group_names):

    auth = HTTPBasicAuth(UDM_USER, UDM_PASSWORD)

    #verify_ssl = True

    users = set()

    for group_name in group_names:

        group_url = f"{UDM_URL}/groups"
        params = {"filter": f"name={group_name}"}
        resp = requests.get(group_url, auth=auth, params=params, verify=verify_ssl)
        if not resp.ok:
            raise HTTPException(status_code=resp.status_code, detail=f"Failed to get group '{group_name}'")

        group_data = resp.json()
        if not group_data.get("items"):
            print(f"Group '{group_name}' not found - TODO ??")

        group = group_data["items"][0]
        group_members = group.get("users", [])

        for user_dn in group_members:
            user_resp = requests.get(f"{UDM_URL}/users/user/{user_dn}", auth=auth, verify=verify_ssl)
            if user_resp.ok:
                user_data = user_resp.json()
                users.append(user_data)
            else:
                print("User DN not found??")
                continue

    return user_objects

@app.get("/get-users")
def get_group_users(groups: List[str] = Query(..., description="List of group names")):

    users = get_users_in_groups(groups)
    return {"groups": groups, "users": users}

@app.post("/group-add")
def add_user_to_group(data: GroupAddRequest, auth: HTTPBasicAuth = Depends(get_udm_auth)):

    user_resp = requests.get(
        f"{UDM_URL}/users/user",
        auth=auth,
        params={"filter": f"username={data.username}"},
        verify=VERIFY_SSL
    )
    if not user_resp.ok or not user_resp.json().get("items"):
        raise HTTPException(status_code=404, detail=f"User '{data.username}' not found")

    user_dn = user_resp.json()["items"][0]["dn"]

    group_resp = requests.get(
        f"{UDM_URL}/groups",
        auth=auth,
        params={"filter": f"name={data.group}"},
        verify=VERIFY_SSL
    )
    if not group_resp.ok or not group_resp.json().get("items"):
        raise HTTPException(status_code=404, detail=f"Group '{data.group}' not found")

    group = group_resp.json()["items"][0]
    group_dn = group["dn"]
    group_users = group.get("users", [])

    if user_dn in group_users:
        return {"detail": f"User '{data.username}' already in group '{data.group}'"}

    group_users.append(user_dn)

    patch_resp = requests.patch(
        f"{UDM_URL}/groups/{group_dn}",
        auth=auth,
        json={"users": group_users},
        verify=VERIFY_SSL
    )
    if not patch_resp.ok:
        raise HTTPException(status_code=500, detail=f"Failed to update group: {patch_resp.text}")

    return {"detail": f"User '{data.username}' added to group '{data.group}'"}

@app.post("/reset-2fa")
def reset_user_2fa(data: Reset2FARequest):
    kc = get_kc_admin()

    try:
        # Get user ID
        user_id = kc.get_user_id(data.username)
        if not user_id:
            raise HTTPException(status_code=404, detail=f"User '{data.username}' not found")

        # Get all credentials for the user
        credentials = kc.get_credentials(user_id)

        # Filter and delete OTP credentials
        removed = 0
        for cred in credentials:
            if cred.get("type") == "otp":
                kc.delete_credential(user_id=user_id, credential_id=cred["id"])
                removed += 1

        return {"username": data.username, "otp_removed": removed}

    except KeycloakGetError as e:
        raise HTTPException(status_code=500, detail=f"Keycloak error: {str(e)}")

@app.post("/add-group-to-2fa-role")
def add_group_to_2fa_role(data: GroupToRoleRequest):
    kc = get_kc_admin()

    try:
        # Step 1: Find the group
        groups = kc.get_groups()
        group = next((g for g in groups if g["name"] == data.group_name), None)
        if not group:
            raise HTTPException(status_code=404, detail=f"Group '{data.group_name}' not found")
        group_id = group["id"]

        # Step 2: Get the 2fa role object
        role = kc.get_realm_role("2fa")

        # Step 3: Add the role to the group
        kc.assign_group_realm_roles(group_id=group_id, roles=[role])

        return {
            "group": data.group_name,
            "role_assigned": "2fa",
            "status": "success"
        }

    except KeycloakGetError as e:
        raise HTTPException(status_code=500, detail=f"Keycloak error: {str(e)}")
