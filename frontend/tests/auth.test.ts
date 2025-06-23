/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as keycloakService from '@/services/keycloak'
import { logoutUser } from "@/utils/auth";

describe('logoutUser', () => {
  let logoutMock: any;
  beforeEach(() => {
    logoutMock = vi.spyOn(keycloakService, 'logout').mockImplementation(() => { })
    vi.stubGlobal('window', {
      __APP_CONFIG__: {}
    });
  });

  afterEach(() => {
    logoutMock.mockRestore();
    vi.unstubAllGlobals();
  })

  it('calls logoutUser with a redirectUri', () => {
    const mockRedirectUri = 'https://example.com/';

    (window as any).__APP_CONFIG__.VITE_POST_LOGOUT_REDIRECT_URI = mockRedirectUri;

    logoutUser()

    expect(logoutMock).toHaveBeenCalledWith({ redirectUri: mockRedirectUri })

    vi.unstubAllGlobals()
  })

  it('calls logoutUser without any opts when no redirectUri is given', () => {
    logoutUser()

    expect(logoutMock).toHaveBeenCalledWith({})
  })
})
