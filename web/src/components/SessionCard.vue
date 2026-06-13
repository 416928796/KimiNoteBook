<template>
  <el-card
    class="session-card"
    shadow="hover"
    :body-style="{ padding: '20px' }"
    @click="$emit('click', session)"
  >
    <div class="card-content">
      <div class="card-header">
        <h3 class="title">{{ session.title || session.id }}</h3>
        <el-tag size="small" type="info">{{ session.message_count }} 条消息</el-tag>
      </div>
      <div class="card-meta">
        <span class="meta-item">
          <el-icon><Calendar /></el-icon>
          {{ formattedDate }}
        </span>
        <span class="meta-item session-id">
          <el-icon><Document /></el-icon>
          {{ session.id }}
        </span>
      </div>
    </div>
    <el-icon class="arrow-icon"><ArrowRight /></el-icon>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ElCard, ElTag, ElIcon } from 'element-plus';
import { Calendar, Document, ArrowRight } from '@element-plus/icons-vue';
import type { SessionSummary } from '@/types';

const props = defineProps<{
  session: SessionSummary;
}>();

defineEmits<{
  (e: 'click', session: SessionSummary): void;
}>();

const formattedDate = computed(() => {
  if (!props.session.created_at) return '未知时间';
  return new Date(props.session.created_at).toLocaleString('zh-CN');
});
</script>

<style scoped>
.session-card {
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  position: relative;
  overflow: hidden;
}

.session-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.session-card:hover .arrow-icon {
  transform: translateX(4px);
  color: var(--el-color-primary);
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.session-id {
  font-family: monospace;
}

.arrow-icon {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--el-text-color-placeholder);
  transition: transform 0.25s ease, color 0.25s ease;
}
</style>
