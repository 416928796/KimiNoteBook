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
      <pre class="message-content">{{ pair.content }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ElCheckbox, ElTag } from 'element-plus';
import type { QAPair } from '@/types';

const props = defineProps<{
  pair: QAPair;
  isSelected: boolean;
}>();

defineEmits<{
  (e: 'toggle', index: number): void;
}>();

const formattedDate = computed(() => {
  if (!props.pair.created_at) return '';
  return new Date(props.pair.created_at).toLocaleString('zh-CN');
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
</style>
