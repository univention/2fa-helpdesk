/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

import axios from "axios";

/**
 * Reset own user token (self-service) via POST /token/reset/own/
 */
export async function resetSelfServiceToken(): Promise<void> {
  await axios.post("/token/reset/own/", {
    headers: {
      Accept: "application/json",
    },
  });
}
