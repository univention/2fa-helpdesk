import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import { initCustomStyles } from "./utils/customStyles";

import "./base-styles.css";

// Initialize custom styles
await initCustomStyles();

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount("#app");
