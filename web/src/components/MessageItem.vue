<template>
  <div
    class="message-item"
    :class="[`role-${pair.role}`, { selected: isSelected }]"
    @click="$emit('toggle', pair.index)"
  >
    <div class="message-header">
      <el-checkbox
        :model-value="isSelected"
        @click.stop
        @change="$emit('toggle', pair.index)"
      />
      <el-tag
        :type="pair.role === 'user' ? 'primary' : 'success'"
        size="small"
        effect="light"
        class="role-tag"
      >
        {{ pair.role === 'user' ? '用户' : pair.role === 'assistant' ? '模型' : pair.role }}
      </el-tag>
      <span v-if="pair.created_at" class="message-time">
        {{ formattedDate }}
      </span>
    </div>
    <div class="message-body">
      <pre v-if="renderMode === 'source'" class="message-content">{{ pair.content }}</pre>
      <div
        v-else
        class="message-content rendered-message"
        v-html="renderedContent"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ElCheckbox, ElTag } from 'element-plus';
import DOMPurify from 'dompurify';
import { marked } from 'marked';
import { useSessionsStore } from '@/stores/sessions';
import type { QAPair } from '@/types';

const props = defineProps<{
  pair: QAPair;
  isSelected: boolean;
}>();

defineEmits<{
  (e: 'toggle', index: number): void;
}>();

const store = useSessionsStore();
const renderMode = computed(() => store.renderMode);

const formattedDate = computed(() => {
  if (!props.pair.created_at) return '';
  return new Date(props.pair.created_at).toLocaleString('zh-CN');
});

const renderedContent = computed(() => {
  const raw = marked.parse(props.pair.content, { async: false }) as string;
  return DOMPurify.sanitize(raw);
});
</script>

<style scoped>
.message-item {
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  background: var(--el-bg-color);
  transition: all 0.2s ease;
  cursor: pointer;
}

.message-item:hover {
  border-color: var(--el-color-primary-light-5);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.message-item.selected {
  border-color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
}

.message-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.role-tag {
  font-weight: 600;
}

.message-time {
  margin-left: auto;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.message-body {
  overflow-x: auto;
}

.message-content {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: var(--el-font-family);
  font-size: 14px;
  line-height: 1.7;
  color: var(--el-text-color-primary);
}

.rendered-message {
  white-space: normal;
}

.rendered-message :deep(pre) {
  background: var(--el-fill-color-light);
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
}

.rendered-message :deep(code) {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  background: var(--el-fill-color-light);
  padding: 2px 6px;
  border-radius: 4px;
}

.rendered-message :deep(pre code) {
  padding: 0;
  background: transparent;
}

.rendered-message :deep(blockquote) {
  margin: 0 0 12px;
  padding-left: 12px;
  border-left: 4px solid var(--el-border-color);
  color: var(--el-text-color-secondary);
}

.rendered-message :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}

.rendered-message :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 12px;
}

.rendered-message :deep(th),
.rendered-message :deep(td) {
  border: 1px solid var(--el-border-color-lighter);
  padding: 8px 12px;
}

.rendered-message :deep(th) {
  background: var(--el-fill-color-light);
}
</style>
