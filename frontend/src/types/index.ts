/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2026 Univention GmbH
 */

export interface UserData {
    username: string;
    firstname: string;
    lastname: string;
    email: string;
  keycloak_internal_id: string;
  totp: string | null;
}

export interface getUsersResponseData {
  data: {
    users: UserData[];
    success: boolean;
    has_next: boolean;
    page: number;
    limit: number;
    detail: string;
  }
}
