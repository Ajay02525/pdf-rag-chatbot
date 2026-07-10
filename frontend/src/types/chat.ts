import { ExecutionPipeline } from "@/types/pipeline";

export type Role = "user" | "assistant" | "system";

export interface Attachment {
  id: string;
  name: string;
  type: string; // mime type
  size: number;
  url: string; // object URL (client-side) or data URL
  isImage: boolean;
  file: File;
}

export interface ChatMessage {
  id: string;
  role: Role;
  content: string;
  attachments?: Attachment[];
  createdAt: number;
  /** true while a message is still being streamed in */
  streaming?: boolean;
  /** set if generation failed */
  error?: string;
  /** sources for the message, if any */
  sources?: Source[];
  /** execution pipeline for the message, if any */
  pipeline?: ExecutionPipeline;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  modelId: string;
  createdAt: number;
  updatedAt: number;
}

export interface ModelOption {
  id: string;
  name: string;
  description: string;
}

export interface Source {
  file: string;
  page: number;
}


export const MODEL_OPTIONS: ModelOption[] = [
  {
    id: "mock-fast",
    name: " Fast",
    description: "Quick responses for UI testing",
  },
  {
    id: "mock-thoughtful",
    name: "Thoughtful",
    description: "Slower responses with longer output",
  },
];
