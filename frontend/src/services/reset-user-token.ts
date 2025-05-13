import axios from "axios";
// import { getFreshToken } from "./getFreshToken";
import type { UserData } from "../types";

let isResetting = false;

export async function resetUserToken(
  selectedUser: UserData,
  callBackFn: () => void,
  successMessage?: string,
  errorMessage?: string
): Promise<void> {
  if (isResetting || !selectedUser) {
    return;
  }

  isResetting = true;
  console.log("Resetting token for user:", selectedUser);

  try {
    const token = "test" //await getFreshToken();
    const url =
      `${import.meta.env.VITE_API_URL || "/backend"}` +
      `/token/reset/user/`;

    await axios.post(
      url,
      { user_ids: [selectedUser.keycloak_internal_id] },
      {
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    console.log("Token reset successful");
    alert(successMessage ?? "Token wurde erfolgreich zurückgesetzt.");
  } catch (err) {
    console.error("Error resetting token:", err);
    alert(
      errorMessage ??
        "Fehler beim Zurücksetzen des Tokens. Bitte versuchen Sie es erneut."
    );
  } finally {
    isResetting = false;
    callBackFn();
  }
}
