/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

// src/services/user.ts
import axiosInstance from "./axios";

interface WhoAmI {
  success: boolean;
  twofa_admin: boolean;
}

let _whoami: Promise<WhoAmI> | null = null;

export async function fetchWhoAmI(): Promise<WhoAmI> {
  if (!_whoami) {
    _whoami = axiosInstance
      .get<WhoAmI>("/whoami")
      .then((r) => r.data)
      .catch((err) => {
        throw err;
      });
  }

  return _whoami;
}
