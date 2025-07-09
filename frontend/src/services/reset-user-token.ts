/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

import axiosInstance from "./axios";
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

  try {
    const url = "/token/reset/user/";

    await axiosInstance.post(
      url,
      { user_ids: [selectedUser.keycloak_internal_id] },
      {
        headers: {
          Accept: "application/json",
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
