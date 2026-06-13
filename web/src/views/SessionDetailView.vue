<template>
  <div class="session-detail-view">
    <div class="detail-header">
      <el-button circle :icon="ArrowLeft" @click="goBack" />
      <div class="detail-title">
        <h2>{{ store.currentSession?.title || sessionId }}</h2>
        <p v-if="store.currentSession?.created_at" class="detail-meta">
          {{ formattedDate }} · {{ store.currentSession?.message_count || 0 }} 条消息
        </p>
      </div>
      <div class="detail-actions">
        <el-button
          type="primary"
          :icon="Download"
          :disabled="selectedIndices.length === 0"
          @click="showExport = true"
        >
          导出 Markdown
        </el-button>
      </div>
    </div>

    <div class="selection-bar">
      <el-checkbox
        :model-value="isAllSelected"
        :indeterminate="isIndeterminate"
        @change="toggleAll"
      >
        全选
      </el-checkbox>
      <span class="selection-count">已选 {{ selectedIndices.length }} 条</span>
    </div>

    <el-skeleton v-if="store.loading" :rows="10" animated />

    <el-empty v-else-if="store.error" :description="store.error" />

    <transition-group
      v-else
      name="message-list"
      tag="div"
      class="message-list"
      appear
    >
      <MessageItem
        v-for="pair in store.currentSession?.qa_pairs"
        :key="pair.index"
        :pair="pair"
        :is-selected="selectedIndices.includes(pair.index)"
        @toggle="toggleSelection"
      />
    </transition-group>

    <ExportDialog
      v-if="store.currentSession"
      v-model:visible="showExport"
      :session-id="sessionId"
      :session-title="store.currentSession.title"
      :pairs="store.currentSession.qa_pairs"
      :selected-indices="selectedIndices"
    />

    <RenderToggle />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { ElButton, ElCheckbox, ElSkeleton, ElEmpty } from 'element-plus';
import { ArrowLeft, Download } from '@element-plus/icons-vue';
import { useSessionsStore } from '@/stores/sessions';
import MessageItem from '@/components/MessageItem.vue';
import ExportDialog from '@/components/ExportDialog.vue';
import RenderToggle from '@/components/RenderToggle.vue';

const props = defineProps<{
  id: string;
}>();

const router = useRouter();
const store = useSessionsStore();
const sessionId = computed(() => props.id);

const selectedIndices = ref<number[]>([]);
const showExport = ref(false);

const formattedDate = computed(() => {
  const date = store.currentSession?.created_at;
  if (!date) return '';
  return new Date(date).toLocaleString('zh-CN');
});

const isAllSelected = computed(() => {
  const pairs = store.currentSession?.qa_pairs || [];
  return pairs.length > 0 && selectedIndices.value.length === pairs.length;
});

const isIndeterminate = computed(() => {
  const pairs = store.currentSession?.qa_pairs || [];
  return selectedIndices.value.length > 0 && selectedIndices.value.length < pairs.length;
});

onMounted(() => {
  store.fetchSession(sessionId.value);
});

watch(
  () => props.id,
  (newId) => {
    selectedIndices.value = [];
    store.fetchSession(newId);
  }
);

function goBack() {
  router.push({ name: 'SessionList' });
}

function toggleSelection(index: number) {
  const idx = selectedIndices.value.indexOf(index);
  if (idx === -1) {
    selectedIndices.value.push(index);
  } else {
    selectedIndices.value.splice(idx, 1);
  }
}

function toggleAll() {
  const pairs = store.currentSession?.qa_pairs || [];
  if (isAllSelected.value) {
    selectedIndices.value = [];
  } else {
    selectedIndices.value = pairs.map((p: { index: number }) => p.index);
  }
}
</script>

<style scoped>
.session-detail-view {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
  min-height: 100vh;
  background: var(--el-bg-color-page);
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.detail-title {
  flex: 1;
}

.detail-title h2 {
  margin: 0 0 4px;
  font-size: 24px;
  font-weight: 600;
}

.detail-meta {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

.selection-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  margin-bottom: 16px;
  background: var(--el-bg-color);
  border-radius: 8px;
  border: 1px solid var(--el-border-color-lighter);
}

.selection-count {
  margin-left: auto;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

.message-list {
  padding-bottom: 40px;
}

.message-list-enter-active,
.message-list-leave-active {
  transition: all 0.3s ease;
}

.message-list-enter-from,
.message-list-leave-to {
  opacity: 0;
  transform: translateY(16px);
}

.message-list-move {
  transition: transform 0.3s ease;
}
</style>
