<template>
  <el-dialog
    v-model="visible"
    title="导出 Markdown"
    width="700px"
    :close-on-click-modal="false"
    destroy-on-close
  >
    <div class="export-preview">
      <el-input
        v-model="filename"
        placeholder="文件名"
        class="filename-input"
      >
        <template #append>.md</template>
      </el-input>
      <el-scrollbar max-height="400px">
        <pre class="preview-content">{{ previewContent }}</pre>
      </el-scrollbar>
    </div>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleExport">
        下载 Markdown
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { ElDialog, ElInput, ElButton, ElScrollbar } from 'element-plus';
import type { QAPair } from '@/types';
import { buildMarkdownPreview, downloadMarkdown } from '@/utils/markdown';
import { exportSession } from '@/api/sessions';

const props = defineProps<{
  sessionId: string;
  sessionTitle: string;
  pairs: QAPair[];
  selectedIndices: number[];
}>();

const visible = defineModel<boolean>('visible', { default: false });

const loading = ref(false);
const filename = ref('');

const selectedPairs = computed(() => {
  return props.selectedIndices
    .map((idx) => props.pairs.find((p) => p.index === idx))
    .filter(Boolean) as QAPair[];
});

const previewContent = computed(() => {
  return buildMarkdownPreview(selectedPairs.value);
});

watch(
  () => visible.value,
  (val) => {
    if (val) {
      filename.value = props.sessionTitle || props.sessionId;
    }
  }
);

async function handleExport() {
  if (selectedPairs.value.length === 0) return;
  loading.value = true;
  try {
    const blob = await exportSession(props.sessionId, {
      selected_indices: props.selectedIndices,
    });
    const text = await blob.text();
    downloadMarkdown(filename.value || props.sessionId, text);
    visible.value = false;
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.export-preview {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.filename-input {
  width: 100%;
}

.preview-content {
  margin: 0;
  padding: 16px;
  background: var(--el-fill-color-light);
  border-radius: 8px;
  font-family: var(--el-font-family);
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
