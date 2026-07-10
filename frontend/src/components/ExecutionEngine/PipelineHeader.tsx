import { PipelineHeader as Header } from "@/types/pipeline";

interface Props {
  header: Header;
}

export default function PipelineHeader({ header }: Props) {
  return (
    <div className="grid grid-cols-2 gap-4 p-4 text-sm border-b bg-[var(--assistant-bg)] border-[var(--border)]">

      <div>
        <div className="text-[var(--muted)]">Provider</div>
        <div>{header.provider}</div>
      </div>

      <div>
        <div className="text-[var(--muted)]">Model</div>
        <div>{header.model}</div>
      </div>

      <div>
        <div className="text-[var(--muted)]">Embedding</div>
        <div>{header.embedding_model}</div>
      </div>

      <div>
        <div className="text-[var(--muted)]">Vector DB</div>
        <div>{header.vector_database}</div>
      </div>

      <div>
        <div className="text-[var(--muted)]">Temperature</div>
        <div>{header.temperature}</div>
      </div>

      <div>
        <div className="text-[var(--muted)]">Execution Time</div>
        <div>{header.total_duration_ms.toFixed(2)} ms</div>
      </div>

    </div>
  );
}