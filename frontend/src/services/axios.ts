/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

import axios, { AxiosHeaders } from "axios";
import { getToken, refreshToken } from "./keycloak";

const axiosInstance = axios.create({
  baseURL: ""
});

axiosInstance.interceptors.request.use(
    async (config) => {
        await refreshToken();

        const token = getToken();
        if (token) {
            (config.headers as AxiosHeaders).set("Authorization", `Bearer ${token}`);
        }
        return config;
    },
    (error) => {
        Promise.reject(new Error(error));
    }
)

export default axiosInstance;
