import { describe, it, expect, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import MessageItem from '../MessageItem.vue';
import { useSessionsStore } from '@/stores/sessions';
import type { QAPair } from '@/types';

describe('MessageItem', () => {
  const pair: QAPair = {
    index: 0,
    role: 'assistant',
    content: '# Section\n\nHello **world**',
    created_at: '2026-01-01T00:00:00',
  };

  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('renders raw markdown in source mode', () => {
    const store = useSessionsStore();
    store.setRenderMode('source');
    const wrapper = mount(MessageItem, {
      props: { pair, isSelected: false },
    });
    const pre = wrapper.find('pre.message-content');
    expect(pre.exists()).toBe(true);
    expect(pre.text()).toContain('# Section');
    expect(pre.text()).toContain('**world**');
  });

  it('renders parsed markdown in rendered mode', () => {
    const store = useSessionsStore();
    store.setRenderMode('rendered');
    const wrapper = mount(MessageItem, {
      props: { pair, isSelected: false },
    });
    const rendered = wrapper.find('.rendered-message');
    expect(rendered.exists()).toBe(true);
    expect(rendered.html()).toContain('<h1>Section</h1>');
    expect(rendered.html()).toContain('<strong>world</strong>');
  });

  it('toggles display mode when store renderMode changes', async () => {
    const store = useSessionsStore();
    store.setRenderMode('source');
    const wrapper = mount(MessageItem, {
      props: { pair, isSelected: false },
    });
    expect(wrapper.find('pre.message-content').exists()).toBe(true);
    expect(wrapper.find('.rendered-message').exists()).toBe(false);

    store.setRenderMode('rendered');
    await wrapper.vm.$nextTick();
    expect(wrapper.find('pre.message-content').exists()).toBe(false);
    expect(wrapper.find('.rendered-message').exists()).toBe(true);
  });
});
