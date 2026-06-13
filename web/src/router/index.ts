import { createRouter, createWebHistory } from 'vue-router';
import SessionListView from '@/views/SessionListView.vue';
import SessionDetailView from '@/views/SessionDetailView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'SessionList',
      component: SessionListView,
      meta: { transition: 'fade' },
    },
    {
      path: '/sessions/:id',
      name: 'SessionDetail',
      component: SessionDetailView,
      props: true,
      meta: { transition: 'slide' },
    },
  ],
});

export default router;
