import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { SessionSummary, SessionDetail } from '@/types';
import { listSessions, getSession } from '@/api/sessions';

export const useSessionsStore = defineStore('sessions', () => {
  const sessions = ref<SessionSummary[]>([]);
  const currentSession = ref<SessionDetail | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const searchQuery = ref('');

  const filteredSessions = computed(() => {
    const query = searchQuery.value.trim().toLowerCase();
    if (!query) return sessions.value;
    return sessions.value.filter(
      (s) =>
        s.title.toLowerCase().includes(query) ||
        s.id.toLowerCase().includes(query)
    );
  });

  async function fetchSessions() {
    loading.value = true;
    error.value = null;
    try {
      sessions.value = await listSessions();
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载会话失败';
      sessions.value = [];
    } finally {
      loading.value = false;
    }
  }

  async function fetchSession(id: string) {
    loading.value = true;
    error.value = null;
    try {
      currentSession.value = await getSession(id);
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载会话详情失败';
      currentSession.value = null;
    } finally {
      loading.value = false;
    }
  }

  function clearCurrentSession() {
    currentSession.value = null;
  }

  return {
    sessions,
    currentSession,
    loading,
    error,
    searchQuery,
    filteredSessions,
    fetchSessions,
    fetchSession,
    clearCurrentSession,
  };
});
