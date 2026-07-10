import { ExecutionPipeline } from "@/types/pipeline";

export interface Source {
  file: string;
  page: number;
}

export interface StreamCallbacks {
  onDelta: (text: string) => void;
  onSources?: (sources: Source[]) => void;
  onPipeline?: (pipeline: ExecutionPipeline) => void;
  onDone: () => void;
  onError: (error: Error) => void;
}

interface StreamChatArgs {
  messages: {
    role: "user" | "assistant" | "system";
    content: string;
  }[];
  modelId: string;
  signal: AbortSignal;
  sessionId?: string;
}

export async function streamChat(
  { messages, modelId, signal, sessionId }: StreamChatArgs,
  callbacks: StreamCallbacks
): Promise<void> {
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages,
        modelId,
        sessionId,
      }),
      signal,
    });

    if (!res.ok || !res.body) {
      throw new Error(`Request failed with status ${res.status}`);
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();

      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      const events = buffer.split("\n\n");
      buffer = events.pop() ?? "";

      for (const event of events) {
        const line = event.trim();

        if (!line.startsWith("data:")) continue;

        const payload = line.slice(5).trim();

        if (payload === "[DONE]") {
          callbacks.onDone();
          return;
        }

        try {
          const parsed = JSON.parse(payload);

          switch (parsed.type) {
            case "delta":
              callbacks.onDelta(parsed.delta);
              break;

            case "sources":
              console.log("Received sources:", parsed.sources);
              callbacks.onSources?.(parsed.sources ?? []);
              break;
            case "pipeline":
              console.log("Received pipeline:", parsed.pipeline);
              callbacks.onPipeline?.(parsed.pipeline);
              break;
            default:
              console.warn("Unknown SSE event:", parsed);
          }
        } catch (err) {
          console.warn("Unable to parse SSE event:", payload, err);
        }
      }
    }

    callbacks.onDone();
  } catch (err) {
    if (signal.aborted) {
      callbacks.onDone();
      return;
    }

    callbacks.onError(
      err instanceof Error
        ? err
        : new Error("Unknown streaming error")
    );
  }
}