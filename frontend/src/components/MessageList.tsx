"use client";

import { useEffect, useRef } from "react";
import { Sparkles } from "lucide-react";
import { Conversation } from "@/types/chat";
import MessageBubble from "@/components/MessageBubble";

export default function MessageList({ conversation }: { conversation: Conversation | null }) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const messageCount = conversation?.messages.length ?? 0;
  const lastMessageContent = conversation?.messages.at(-1)?.content ?? "";

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messageCount, lastMessageContent]);

  if (!conversation || conversation.messages.length === 0) {
    return (
      <div className="flex h-full flex-1 flex-col items-center justify-center gap-3 px-6 text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-full border border-[var(--border)] bg-[var(--surface)]">
          <Sparkles size={20} className="text-[var(--accent)]" />
        </div>
        <h2 className="text-lg font-medium text-[var(--text)]">What can I help with?</h2>
        <p className="max-w-sm text-sm text-[var(--muted)]">
          Upload Digital PDFS(max 10MB), ask questions, and get answers with context, source citation and execution pipeline.
          Type a message below to start a conversation. 
          
        </p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="mx-auto max-w-3xl">
        {conversation.messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
      </div>
      <div ref={bottomRef} />
    </div>
  );
}
