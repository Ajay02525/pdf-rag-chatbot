"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { AlertCircle, FileText, User, Sparkles } from "lucide-react";
import { ChatMessage } from "@/types/chat";
import CodeBlock from "@/components/CodeBlock";
import ExecutionPipeline from "@/components/ExecutionEngine/ExecutionPipeline";
import { formatBytes } from "@/lib/utils";
import Image from "next/image";

export default function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div className={`rounded-lg mb-5 flex gap-3 px-4 py-5 ${isUser ? "" : "bg-[var(--assistant-bg)]"}`}>
      <div
        className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full ${
          isUser ? "bg-[var(--accent)]" : "bg-[var(--surface)] border border-[var(--border)]"
        }`}
      >
        {isUser ? (
          <User size={14} className="text-white" />
        ) : (
          <Sparkles size={14} className="text-[var(--accent)]" />
        )}
      </div>

      <div className="min-w-0 flex-1">
        {message.attachments && message.attachments.length > 0 && (
          <div className="mb-2 flex flex-wrap gap-2">
            {message.attachments.map((att) =>
              att.isImage ? (
                <div
                  key={att.id}
                  className="relative h-28 w-28 overflow-hidden rounded-lg border border-[var(--border)]"
                >
                  <Image
                    src={att.url}
                    alt={att.name}
                    fill
                    className="object-cover"
                    unoptimized
                  />
                </div>
              ) : (
                <div
                  key={att.id}
                  className="flex items-center gap-2 rounded-lg border border-[var(--border)] bg-[var(--surface)] px-3 py-2"
                >
                  <FileText size={16} className="text-[var(--muted)]" />
                  <div className="leading-tight">
                    <div className="text-xs font-medium text-[var(--text)]">{att.name}</div>
                    <div className="text-[11px] text-[var(--muted)]">{formatBytes(att.size)}</div>
                  </div>
                </div>
              )
            )}
          </div>
        )}

        {message.content && (
          <div className="prose-chat">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                code({ className, children, ...props }) {
                  const isBlock = /language-/.test(className || "");
                  if (isBlock) {
                    return <CodeBlock className={className}>{children}</CodeBlock>;
                  }
                  return (
                    <code
                      className="rounded bg-[var(--inline-code-bg)] px-1.5 py-0.5 text-[0.85em]"
                      {...props}
                    >
                      {children}
                    </code>
                  );
                },
                a({ children, ...props }) {
                  return (
                    <a
                      {...props}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-[var(--accent)] underline underline-offset-2"
                    >
                      {children}
                    </a>
                  );
                },
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
        {message.sources?.length ? (
            <div className="mt-4 border-t pt-3">
              <p className="text-xs font-semibold text-muted-foreground mb-2">
                Sources
              </p>

              {message.sources.map((source, index) => (
                <div key={index} className="text-sm">
                  📄 {source.file} (Page {source.page})
                </div>
              ))}
            </div>
          ) : null}
          {message.pipeline && (
              <ExecutionPipeline
                  pipeline={message.pipeline}
              />
          )}
        {message.streaming && !message.content && (
          <div className="flex gap-1 py-1">
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[var(--muted)] [animation-delay:-0.3s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[var(--muted)] [animation-delay:-0.15s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-[var(--muted)]" />
          </div>
        )}

        {message.error && (
          <div className="mt-2 flex items-center gap-2 rounded-lg border border-[var(--error-border)] bg-[var(--error-bg)] px-3 py-2 text-sm text-[var(--error-text)]">
            <AlertCircle size={15} className="shrink-0" />
            {message.error}
          </div>
        )}
      </div>
    </div>
  );
}
