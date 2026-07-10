export interface PipelineHeader {
  session_id: string;
  provider: string;
  model: string;
  temperature: number;
  embedding_model: string;
  vector_database: string;
  started_at: string;
  completed_at: string;
  total_duration_ms: number;
  input_tokens: number | null;
  output_tokens: number | null;
  total_tokens: number | null;
  cost: number | null;
}

export interface PipelineChild {
  id: string;
  title: string;
  icon: string;
  status: string;
  fields: Record<string, any>;
}

export interface PipelineStep {
  id: string;
  title: string;
  icon: string;
  status: string;
  duration_ms: number;
  fields: Record<string, any>;
  children: PipelineChild[];
}

export interface ExecutionPipeline {
  header: PipelineHeader;
  steps: PipelineStep[];
}