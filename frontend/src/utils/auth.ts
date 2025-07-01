/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

import { logout } from "@/services/keycloak";

export const logoutUser = () => {
  const cfg = window.__APP_CONFIG__;
  const opts: {redirectUri?: string} = {}

  if (cfg && 'VITE_POST_LOGOUT_REDIRECT_URI' in cfg) {
    opts.redirectUri = cfg.VITE_POST_LOGOUT_REDIRECT_URI;
  }

  logout(opts)
}
