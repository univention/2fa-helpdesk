import { createRouter, createWebHistory } from 'vue-router';
import AdminPage from '@/pages/AdminPage.vue';
import SelfServicePage from '@/pages/SelfServicePage.vue';

const routes = [
  { path: '/admin', component: AdminPage },
  { path: '/self-service', component: SelfServicePage },
];

const router = createRouter({
  history: createWebHistory("/ui"),
  routes,
});

export default router;
