/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as keycloakService from '@/services/keycloak'
import { logoutUser } from "@/utils/auth";
import { fetchWhoAmI } from "@/services/whoami.ts"
import axiosInstance from "@/services/axios";
import { AxiosHeaders } from "axios";

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

describe('refreshToken', () => {
  let refreshTokenMock: any;
  let getTokenMock: any;
  let axiosGetMock: any;
  let token = Math.random().toString(36).slice(2);


  beforeEach(() => {
    refreshTokenMock = vi.spyOn(keycloakService, 'refreshToken').mockImplementation(() => { token = Math.random().toString(36).slice(2); })
    getTokenMock = vi.spyOn(keycloakService, 'getToken').mockImplementation(() => { return token })
    axiosGetMock = vi.spyOn(axiosInstance, 'get').mockImplementation(() => {
      axiosInstance.interceptors.request.forEach((interceptor) => {
        let config = {}
        config.headers = new AxiosHeaders()
        interceptor.fulfilled(config)
      })
      return Promise.resolve({ data: { success: true, twofa_admin: false } })
    })
    vi.stubGlobal('window', {
      __APP_CONFIG__: {}
    });
  });

  afterEach(() => {
    refreshTokenMock.mockRestore();
    getTokenMock.mockRestore();
    axiosGetMock.mockRestore();
    vi.unstubAllGlobals();
  })

  it('make axios request', () => {
    let initToken = token
    return fetchWhoAmI().then((data) => {
      expect(axiosGetMock).toHaveBeenCalledTimes(1)
      expect(getTokenMock).toHaveBeenCalledTimes(1)
      expect(refreshTokenMock).toHaveBeenCalledTimes(1)
      expect(initToken).not.toBe(token)
      expect(data.success).toBe(true)
      expect(data.twofa_admin).toBe(false)
    })
  })
})
