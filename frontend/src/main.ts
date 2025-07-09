/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

import { createApp } from "vue";
import App from "./App.vue";
import axiosInstance from "./services/axios";
import router from "./router";
import { createPinia } from "pinia";
import { loadAllStyles } from "./utils/customStyles";

import { initKeycloak } from "./services/keycloak";

import "./base-styles.css";
import { loadConfig } from "./services/loadConfig";

loadAllStyles();

loadConfig()
  .then(() => {
    const cfg = window.__APP_CONFIG__!;
    axiosInstance.defaults.baseURL = cfg.VITE_API_URL;

    return initKeycloak({
      onLoad: "login-required",
      checkLoginIframe: true,
    });
  })
  .then((authenticated) => {
    if (!authenticated) {
      console.warn("Not authenticated");
      return;
    }

    const app = createApp(App);
    app.use(createPinia());
    app.use(router);
    app.mount("#app");
  })
  .catch((err) => {
    console.error("❌ Startup failed:", err);
  });
