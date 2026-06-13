export interface QAPair {
  index: number;
  role: 'user' | 'assistant' | string;
  content: string;
  created_at?: string;
}

export interface SessionSummary {
  id: string;
  title: string;
  created_at?: string;
  updated_at?: string;
  message_count: number;
  source?: 'kimi-code' | 'kimi-legacy' | string;
}

export interface SessionDetail extends SessionSummary {
  qa_pairs: QAPair[];
}

export interface ExportRequest {
  selected_indices: number[];
}
