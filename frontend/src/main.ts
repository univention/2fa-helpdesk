import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import { loadCustomStyles } from "./utils/customStyles";
import keycloak from "./services/keycloak";

import "./base-styles.css";

loadCustomStyles();

const app = createApp(App);

app.use(createPinia());

keycloak
  .init({ onLoad: "login-required", checkLoginIframe: false })
  .then((authenticated) => {
    if (authenticated) {
      console.log("Authenticated");
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
