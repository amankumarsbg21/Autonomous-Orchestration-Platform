export interface ChatRequest {
  message: string;
  thread_id: string;
}

export interface ChatResponse {
  response: string;
  thread_id: string;
  error?: string;
}

export interface UIConversationMessage {
  sender: 'user' | 'agent';
  text: string;
  timestamp: Date;
}