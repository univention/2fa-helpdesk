/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2025 Univention GmbH
 */

import { createRouter, createWebHistory } from "vue-router";
import AdminPage from "@/pages/AdminPage.vue";
import SelfServicePage from "@/pages/SelfServicePage.vue";
import SwaggerPage from "@/pages/SwaggerPage.vue";
import { fetchWhoAmI } from "../services/whoami";
import { isAuthenticated, login } from "@/services/keycloak";

const routes = [
  {
    path: "/admin",
    component: AdminPage,
    meta: {
      title: "Administrator: 2FA zurücksetzen",
      requiresAuth: true,
      adminOnly: true,
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
router.beforeEach(async (to, _from, next) => {
  document.title = (to.meta.title as string) || "2FA Reset";

  if (to.meta.requiresAuth) {
    if (!isAuthenticated()) {
      return login({ redirectUri: window.location.href });
    }

    let info;
    try {
      info = await fetchWhoAmI();
      console.log("Fetched whoami:", info);
    } catch (err) {
      console.error("Could not fetch whoami:", err);
      return next(false);
    }

    if (to.meta.adminOnly && !info.twofa_admin) {
      return next("/self-service");
    }

    return next();
  }

  return next();
});

export default router;
