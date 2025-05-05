import { createRouter, createWebHistory } from "vue-router";
import AdminPage from "@/pages/AdminPage.vue";
import SelfServicePage from "@/pages/SelfServicePage.vue";
import SwaggerPage from "@/pages/SwaggerPage.vue";

const routes = [
  {
    path: "/admin",
    component: AdminPage,
    meta: {
      title: "Administrator: 2FA zurücksetzen",
    },
  },
  {
    path: "/self-service",
    component: SelfServicePage,
    meta: {
      title: "Self-Service: 2FA zurücksetzen",
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
router.beforeEach((to, from, next) => {
  // Set the page title based on the route's meta title
  document.title = (to.meta.title as string) || "Vite + Vue + TS";
  next();
});

export default router;
