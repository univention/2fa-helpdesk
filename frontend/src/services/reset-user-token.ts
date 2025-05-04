import { DefaultApi } from "../api";
import { Configuration } from "../api/runtime";
import type { UserData } from "../types";

let isResetting = false;

export const resetUserToken = (
  selectedUser: UserData,
  callBackFn: () => void
) => {
  if (isResetting || !selectedUser) {
    return;
  }

  isResetting = true;
  console.log("Resetting token for user:", selectedUser);

  const config = new Configuration({
    basePath: `${import.meta.env.VITE_API_URL || "/backend"}`,
    accessToken: () => `Bearer ${import.meta.env.VITE_API_TOKEN || ""}`,
  });
  const apiClient = new DefaultApi(config);

  apiClient
    .resetUserTokensTokenResetUserPost({
      resetUsersRequest: {
        userIds: [selectedUser.keycloak_internal_id],
      },
    })
    .then((result) => {
      console.log("Token reset successful:", result);
      alert("Token wurde erfolgreich zurückgesetzt.");
    })
    .catch((error) => {
      console.error("Error resetting token:", error);
      alert(
        "Fehler beim Zurücksetzen des Tokens. Bitte versuchen Sie es erneut."
      );
    })
    .finally(() => {
      isResetting = false;
      callBackFn();
    });
};
