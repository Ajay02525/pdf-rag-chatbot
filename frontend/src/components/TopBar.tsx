"use client";

import { useState, useRef, useEffect } from "react";
import { ChevronDown, Check, Sun, Moon } from "lucide-react";
import { MODEL_OPTIONS } from "@/types/chat";
import { useChatStore } from "@/store/chatStore";
import { cn } from "@/lib/utils";

export default function TopBar({
  theme,
  onToggleTheme,
}: {
  theme: "light" | "dark";
  onToggleTheme: () => void;
}) {
  const { activeConversation, setModelForActive } = useChatStore();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const currentModel =
    MODEL_OPTIONS.find((m) => m.id === activeConversation?.modelId) ?? MODEL_OPTIONS[0];

  return (
    <div className="flex h-14 items-center justify-between border-b border-[var(--border)] bg-[var(--bg)] px-4">
      <div className="relative" ref={ref}>
        <button
          onClick={() => setOpen((o) => !o)}
          className="flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-sm font-medium text-[var(--text)] transition-colors hover:bg-[var(--hover)]"
        >
          {currentModel.name}
          <ChevronDown size={14} className="text-[var(--muted)]" />
        </button>

        {open && (
          <div className="absolute left-0 top-full z-20 mt-1 w-64 rounded-xl border border-[var(--border)] bg-[var(--surface)] p-1.5 shadow-lg">
            {MODEL_OPTIONS.map((model) => (
              <button
                key={model.id}
                onClick={() => {
                  setModelForActive(model.id);
                  setOpen(false);
                }}
                className="flex w-full items-start gap-2 rounded-lg px-2.5 py-2 text-left transition-colors hover:bg-[var(--hover)]"
              >
                <div className="flex-1">
                  <div className="text-sm font-medium text-[var(--text)]">{model.name}</div>
                  <div className="text-xs text-[var(--muted)]">{model.description}</div>
                </div>
                {model.id === currentModel.id && (
                  <Check size={15} className="mt-0.5 shrink-0 text-[var(--accent)]" />
                )}
              </button>
            ))}
          </div>
        )}
      </div>

      <button
        onClick={onToggleTheme}
        className={cn(
          "rounded-lg p-2 text-[var(--muted)] transition-colors hover:bg-[var(--hover)] hover:text-[var(--text)]"
        )}
        aria-label="Toggle theme"
      >
        {theme === "light" ? <Moon size={17} /> : <Sun size={17} />}
      </button>
    </div>
  );
}
