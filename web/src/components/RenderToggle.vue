<template>
  <div class="render-toggle">
    <el-tooltip
      :content="tooltipText"
      placement="left"
    >
      <el-switch
        :model-value="isRendered"
        inline-prompt
        active-text="渲染"
        inactive-text="源码"
        @update:model-value="toggle"
      />
    </el-tooltip>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { ElSwitch, ElTooltip } from 'element-plus';
import { useSessionsStore, type RenderMode } from '@/stores/sessions';

const store = useSessionsStore();

const isRendered = computed(() => store.renderMode === 'rendered');
const tooltipText = computed(() =>
  isRendered.value ? '当前为渲染模式，点击切换源码' : '当前为源码模式，点击切换渲染'
);

function toggle(value: boolean | string | number) {
  const mode: RenderMode = value ? 'rendered' : 'source';
  store.setRenderMode(mode);
}
</script>

<style scoped>
.render-toggle {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 100;
  padding: 10px 14px;
  background: var(--el-bg-color);
  border-radius: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--el-border-color-lighter);
}
</style>
