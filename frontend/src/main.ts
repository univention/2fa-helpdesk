import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "./router";
import { createPinia } from "pinia";
import { loadCustomStyles } from "./utils/customStyles";
import keycloak from "./services/keycloak";

import "./base-styles.css";

loadCustomStyles();

;(window as any).__ENV = Object.fromEntries(
  Object.entries(import.meta.env).filter(([k]) => k.startsWith("VITE_"))
)
console.log((window as any).__ENV)
const app = createApp(App);

app.use(createPinia());

keycloak
  .init({ onLoad: "login-required", checkLoginIframe: true })
  .then((authenticated: boolean) => {
    if (authenticated) {
  
      axios.defaults.headers.common["Authorization"] = `Bearer ${keycloak.token}`;
     
      app.use(router);
      app.mount("#app");
    } else {
      console.warn("Not authenticated");
    }
  })
  // eslint-disable-next-line
  // @ts-ignore 
  .catch((error) => { 
    console.error("Keycloak initialization failed:", error);
  });
