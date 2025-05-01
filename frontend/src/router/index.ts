import { createRouter, createWebHistory } from 'vue-router';
import AdminPage from '@/pages/AdminPage.vue';
import SelfServicePage from '@/pages/SelfServicePage.vue';
import SwaggerPage from '@/pages/SwaggerPage.vue';

const routes = [
  { path: '/admin', component: AdminPage },
  { path: '/self-service', component: SelfServicePage },
  {path: "/swagger", component: SwaggerPage},
];

const router = createRouter({
  history: createWebHistory("/ui"),
  routes,
});

export default router;
