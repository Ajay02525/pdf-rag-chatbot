"use client";

import { useState } from "react";
import { PanelLeftClose, PanelLeftOpen, Plus, Trash2, MessageSquare } from "lucide-react";
import { useChatStore } from "@/store/chatStore";
import { cn } from "@/lib/utils";

export default function Sidebar() {
  const {
    conversations,
    activeId,
    createConversation,
    deleteConversation,
    selectConversation,
  } = useChatStore();
  const [collapsed, setCollapsed] = useState(false);

  if (collapsed) {
    return (
      <div className="flex h-full w-14 flex-col items-center gap-3 border-r border-[var(--border)] bg-[var(--surface)] py-3">
        <button
          onClick={() => setCollapsed(false)}
          className="rounded-lg p-2 text-[var(--muted)] transition-colors hover:bg-[var(--hover)] hover:text-[var(--text)]"
          aria-label="Expand sidebar"
        >
          <PanelLeftOpen size={18} />
        </button>
        <button
          onClick={createConversation}
          className="rounded-lg p-2 text-[var(--muted)] transition-colors hover:bg-[var(--hover)] hover:text-[var(--text)]"
          aria-label="New conversation"
        >
          <Plus size={18} />
        </button>
      </div>
    );
  }

  return (
    <div className="flex h-full w-64 flex-col border-r border-[var(--border)] bg-[var(--surface)]">
      <div className="flex items-center justify-between gap-2 px-3 py-3">
        <button
          onClick={createConversation}
          className="flex flex-1 items-center gap-2 rounded-lg border border-[var(--border)] px-3 py-2 text-sm font-medium text-[var(--text)] transition-colors hover:bg-[var(--hover)]"
        >
          <Plus size={16} />
          New chat
        </button>
        <button
          onClick={() => setCollapsed(true)}
          className="rounded-lg p-2 text-[var(--muted)] transition-colors hover:bg-[var(--hover)] hover:text-[var(--text)]"
          aria-label="Collapse sidebar"
        >
          <PanelLeftClose size={18} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-2 pb-2">
        {conversations.length === 0 && (
          <p className="px-3 py-6 text-center text-sm text-[var(--muted)]">
            No conversations yet
          </p>
        )}
        <ul className="flex flex-col gap-0.5">
          {conversations.map((c) => (
            <li key={c.id}>
              <button
                onClick={() => selectConversation(c.id)}
                className={cn(
                  "group flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-sm transition-colors",
                  c.id === activeId
                    ? "bg-[var(--active)] text-[var(--text)]"
                    : "text-[var(--muted)] hover:bg-[var(--hover)] hover:text-[var(--text)]"
                )}
              >
                <MessageSquare size={15} className="shrink-0 opacity-60" />
                <span className="flex-1 truncate">{c.title}</span>
                <span
                  role="button"
                  tabIndex={-1}
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteConversation(c.id);
                  }}
                  className="shrink-0 rounded p-1 opacity-0 transition-opacity hover:bg-[var(--border)] group-hover:opacity-100"
                  aria-label="Delete conversation"
                >
                  <Trash2 size={13} />
                </span>
              </button>
            </li>
          ))}
        </ul>
      </div>

      <div className="border-t border-[var(--border)] px-3 py-3 text-xs text-[var(--muted)]">
        Connected to Python FastAPI backend
      </div>
    </div>
  );
}
