/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

export interface AppConfig {
  VITE_KEYCLOAK_URL: string;
  VITE_API_URL: string;
  VITE_KEYCLOAK_REALM: string;
  VITE_KEYCLOAK_CLIENT_ID: string;
}

declare global {
  interface Window {
    __APP_CONFIG__?: AppConfig;
  }
}

export function loadConfig(): Promise<void> {
  return fetch("config.json", { cache: "no-cache" })
    .then((res) => {
      if (!res.ok) throw new Error("Could not load config.json");
      return res.json();
    })
    .then((json: AppConfig) => {
      window.__APP_CONFIG__ = json;
    });
}
