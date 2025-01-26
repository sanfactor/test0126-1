export interface Message {
  agent_id: string;
  content: string;
  timestamp: string;
  role: string;
}

export interface Vote {
  agent_id: string;
  choice: 'approve' | 'reject';
  reasoning: string;
  timestamp: string;
}

export interface Discussion {
  id: string;
  topic: string;
  status: string;
  messages: Message[];
  votes: Vote[];
  created_at: string;
  updated_at: string;
  conclusion: string | null;
}

export interface TopicRequest {
  topic: string;
}
