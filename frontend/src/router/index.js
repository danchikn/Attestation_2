import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/Login.vue';
import AdminView from '../views/Admin.vue';
import store from '../store';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView,
    meta: { requiresAuth: true, adminOnly: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const token = store.state.token;

  if (to.meta.requiresAuth) {
    if (!token) {
      return next('/');
    }

    try {
      if (!store.state.user) {
        await store.dispatch('fetchUser');
      }

      if (to.meta.adminOnly && store.state.user?.role !== 'admin') {
        alert('Доступ запрещён');
        return next('/');
      }

      next();
    } catch (err) {
      console.error('Auth error:', err);
      store.dispatch('logout');
      next('/');
    }
  } else {
    next();
  }
});

export default router;
