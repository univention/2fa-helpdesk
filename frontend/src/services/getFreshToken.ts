import keycloak from "./keycloak";

export const getFreshToken = async () => {
  try {
    // If your token will expire in the next 30s, refresh it
    const refreshed = await keycloak.updateToken(30);
    if (refreshed) {
      console.log("🔄 Token was refreshed");
    }
    return keycloak.token;
  } catch (err) {
    console.error("Failed to refresh token:", err);
 
    keycloak.login();
    throw err;
  }
}