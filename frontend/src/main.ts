import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "./router";
import { createPinia } from "pinia";
import { loadCustomStyles } from "./utils/customStyles";

import {
  initKeycloak,
  //  getToken
} from "./services/keycloak";

import "./base-styles.css";
import { loadConfig } from "./services/loadConfig";

loadCustomStyles();

loadConfig()
  .then(() => {
    const cfg = window.__APP_CONFIG__!;
    axios.defaults.baseURL = cfg.VITE_API_URL;

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
    //  axios.defaults.headers.common["Authorization"] = `Bearer ${getToken()}`;
    axios.defaults.headers.common["Authorization"] = `Bearer test`;

    const app = createApp(App);
    app.use(createPinia());
    app.use(router);
    app.mount("#app");
  })
  .catch((err) => {
    console.error("❌ Startup failed:", err);
  });
