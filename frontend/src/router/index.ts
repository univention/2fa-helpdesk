import { createRouter, createWebHistory } from "vue-router";
import AdminPage from "@/pages/AdminPage.vue";
import SelfServicePage from "@/pages/SelfServicePage.vue";
import SwaggerPage from "@/pages/SwaggerPage.vue";
import keycloak from "../services/keycloak";

const routes = [
  {
    path: "/admin",
    component: AdminPage,
    meta: {
      title: "Administrator: 2FA zurücksetzen",
      requiresAuth: true,
    },
  },
  {
    path: "/self-service",
    component: SelfServicePage,
    meta: {
      title: "Self-Service: 2FA zurücksetzen",
      requiresAuth: true,
    },
  },
  {
    path: "/swagger",
    component: SwaggerPage,
    meta: {
      title: "API Documentation",
    },
  },
];

const router = createRouter({
  history: createWebHistory("/ui"),
  routes,
});

// Navigation guard to update document title
router.beforeEach((to, _from, next) => {
  document.title = (to.meta.title as string) || "Vite + Vue + TS";

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (keycloak.authenticated) {
      next();
    } else {
      const loginOptions = { redirectUri: window.location.href };
      keycloak.login(loginOptions);
    }
  } else {
    next();
  }
});

export default router;
