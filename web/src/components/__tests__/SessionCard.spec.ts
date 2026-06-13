import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import SessionCard from '../SessionCard.vue';
import type { SessionSummary } from '@/types';

describe('SessionCard', () => {
  const session: SessionSummary = {
    id: 'session_001',
    title: 'Test Session',
    created_at: '2026-01-01T00:00:00',
    message_count: 4,
  };

  it('renders session title and message count', () => {
    const wrapper = mount(SessionCard, {
      props: { session },
    });
    expect(wrapper.text()).toContain('Test Session');
    expect(wrapper.text()).toContain('4 条消息');
  });

  it('emits click event when clicked', async () => {
    const wrapper = mount(SessionCard, {
      props: { session },
    });
    await wrapper.find('.session-card').trigger('click');
    expect(wrapper.emitted('click')).toBeTruthy();
    expect(wrapper.emitted('click')![0]).toEqual([session]);
  });
});
