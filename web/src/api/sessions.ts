import axios from 'axios';
import type { SessionSummary, SessionDetail, ExportRequest } from '@/types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || '请求失败';
    return Promise.reject(new Error(message));
  }
);

export async function listSessions(): Promise<SessionSummary[]> {
  const response = await api.get<SessionSummary[]>('/sessions');
  return response.data;
}

export async function getSession(id: string): Promise<SessionDetail> {
  const response = await api.get<SessionDetail>(`/sessions/${id}`);
  return response.data;
}

export async function exportSession(
  id: string,
  request: ExportRequest
): Promise<Blob> {
  const response = await api.post(`/sessions/${id}/export`, request, {
    responseType: 'blob',
  });
  return response.data;
}

export default api;
