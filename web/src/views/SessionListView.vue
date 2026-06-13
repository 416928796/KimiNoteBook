<template>
  <div class="session-list-view">
    <div class="page-header">
      <h1 class="page-title">
        <el-icon size="32" color="var(--el-color-primary)"><ChatLineRound /></el-icon>
        Kimi 会话浏览器
      </h1>
      <p class="page-subtitle">浏览本地 Kimi Code CLI 会话，导出精彩对话</p>
    </div>

    <div class="toolbar">
      <el-input
        v-model="store.searchQuery"
        placeholder="搜索会话标题或 ID"
        clearable
        class="search-input"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      <el-button type="primary" :icon="Refresh" :loading="store.loading" @click="store.fetchSessions">
        刷新
      </el-button>
    </div>

    <el-skeleton v-if="store.loading" :rows="6" animated />

    <el-empty v-else-if="store.error" :description="store.error">
      <el-button type="primary" @click="store.fetchSessions">重试</el-button>
    </el-empty>

    <el-empty
      v-else-if="store.filteredSessions.length === 0"
      description="暂无会话"
    />

    <transition-group
      v-else
      name="card-list"
      tag="div"
      class="session-grid"
      appear
    >
      <SessionCard
        v-for="session in store.filteredSessions"
        :key="session.id"
        :session="session"
        @click="goToDetail"
      />
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElSkeleton, ElEmpty, ElInput, ElButton, ElIcon } from 'element-plus';
import { ChatLineRound, Search, Refresh } from '@element-plus/icons-vue';
import { useSessionsStore } from '@/stores/sessions';
import SessionCard from '@/components/SessionCard.vue';
import type { SessionSummary } from '@/types';

const store = useSessionsStore();
const router = useRouter();

onMounted(() => {
  store.fetchSessions();
});

function goToDetail(session: SessionSummary) {
  router.push({ name: 'SessionDetail', params: { id: session.id } });
}
</script>

<style scoped>
.session-list-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin: 0 0 12px;
  font-size: 32px;
  font-weight: 700;
  color: var(--el-text-color-primary);
}

.page-subtitle {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 16px;
}

.toolbar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.search-input {
  flex: 1;
  max-width: 480px;
}

.session-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 20px;
}

.card-list-enter-active,
.card-list-leave-active {
  transition: all 0.35s ease;
}

.card-list-enter-from,
.card-list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.card-list-move {
  transition: transform 0.35s ease;
}
</style>
