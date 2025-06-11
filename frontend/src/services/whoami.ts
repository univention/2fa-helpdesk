/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

// src/services/user.ts
import axios from "axios";

interface WhoAmI {
  success: boolean;
  twofa_admin: boolean;
}

let _whoami: Promise<WhoAmI> | null = null;

export async function fetchWhoAmI(): Promise<WhoAmI> {
  if (!_whoami) {
    _whoami = axios
      .get<WhoAmI>("/whoami")
      .then((r) => r.data)
      .catch((err) => {
        _whoami = null;
        throw err;
      });
  }

  return _whoami;
}
