import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "./router";
import { createPinia } from "pinia";
import { loadCustomStyles } from "./utils/customStyles";
import keycloak from "./services/keycloak";

import "./base-styles.css";

loadCustomStyles();

const app = createApp(App);

app.use(createPinia());

keycloak
  .init({ onLoad: "login-required", checkLoginIframe: true })
  .then((authenticated) => {
    if (authenticated) {
  
      axios.defaults.headers.common["Authorization"] = `Bearer ${keycloak.token}`;
     
      app.use(router);
      app.mount("#app");
    } else {
      console.warn("Not authenticated");
      // Optionally, redirect to Keycloak login page or show a message
      // keycloak.login(); // Uncomment to redirect to login immediately
    }
  })
  .catch((error) => {
    console.error("Keycloak initialization failed:", error);
  });
