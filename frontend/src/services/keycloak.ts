/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

// src/services/keycloak.ts
import Keycloak from "keycloak-js";

type KeycloakInstance = InstanceType<typeof Keycloak>;
type KCConfig = ConstructorParameters<typeof Keycloak>[0];
type KCInitOptions = Parameters<KeycloakInstance["init"]>[0];
type KCLoginOpts = Parameters<KeycloakInstance["login"]>[0];
type KCLogoutOpts = Parameters<KeycloakInstance["logout"]>[0];

let keycloak: KeycloakInstance;

export function initKeycloak(options: KCInitOptions): Promise<boolean> {
  const cfg = window.__APP_CONFIG__;
  if (!cfg) {
    throw new Error("Missing window.__APP_CONFIG__");
  }

  const kcConfig: KCConfig = {
    url: cfg.VITE_KEYCLOAK_URL,
    realm: cfg.VITE_KEYCLOAK_REALM,
    clientId: cfg.VITE_KEYCLOAK_CLIENT_ID,
  };

  // only now do we instantiate
  keycloak = new Keycloak(kcConfig);
  return keycloak.init(options);
}

export function getToken(): string | undefined {
  return keycloak?.token;
}

export async function refreshToken(): Promise<void> {
  try {
      // Refresh token if lifetime is <= 5 seconds
      const refreshed = await keycloak?.updateToken(5);
      console.log(refreshed ? 'Token was refreshed' : 'Token is still valid');
  } catch (error) {
      console.error('Failed to refresh the token:', error);
      throw error;
  }
}


export function isAuthenticated(): boolean {
  return keycloak?.authenticated === true;
}

export function login(opts?: KCLoginOpts): void {
  if (!keycloak) {
    throw new Error("Keycloak not initialized");
  }
  keycloak.login(opts);
}

export function logout(opts?: KCLogoutOpts): void {
  if (!keycloak) {
    throw new Error("Keycloak not initialized");
  }
  keycloak.logout(opts);
}
