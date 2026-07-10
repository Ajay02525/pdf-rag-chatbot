"use client";

import { useRef, useState } from "react";
import { ArrowUp, Paperclip, Square, X, FileText } from "lucide-react";
import { v4 as uuid } from "uuid";
import { Attachment } from "@/types/chat";
import { useChatStore } from "@/store/chatStore";
import { formatBytes } from "@/lib/utils";
import Image from "next/image";

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export default function Composer() {
  const { sendMessage, isStreaming, stopStreaming } = useChatStore();
  const [text, setText] = useState("");
  const [attachments, setAttachments] = useState<Attachment[]>([]);
  const [fileError, setFileError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
    }
  };

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList) return;
    setFileError(null);
    const newAttachments: Attachment[] = [];

    for (const file of Array.from(fileList)) {
      if (file.size > MAX_FILE_SIZE) {
        setFileError(`"${file.name}" is over the 10MB limit and was skipped.`);
        continue;
      }
      newAttachments.push({
        id: uuid(),
        name: file.name,
        type: file.type,
        size: file.size,
        url: URL.createObjectURL(file),
        isImage: file.type.startsWith("image/"),
        file,

      });
    }

    setAttachments((prev) => [...prev, ...newAttachments]);
  };

  const removeAttachment = (id: string) => {
    setAttachments((prev) => {
      const target = prev.find((a) => a.id === id);
      if (target) URL.revokeObjectURL(target.url);
      return prev.filter((a) => a.id !== id);
    });
  };

  const handleSubmit = async () => {
    if (isStreaming) return;
    if (!text.trim() && attachments.length === 0) return;

    const toSend = attachments;
    setText("");
    setAttachments([]);
    setFileError(null);
    if (textareaRef.current) textareaRef.current.style.height = "auto";

    await sendMessage(text, toSend);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="border-t border-[var(--border)] bg-[var(--bg)] px-4 py-4">
      <div className="mx-auto max-w-3xl">
        {fileError && (
          <p className="mb-2 text-xs text-[var(--error-text)]">{fileError}</p>
        )}

        {attachments.length > 0 && (
          <div className="mb-2 flex flex-wrap gap-2">
            {attachments.map((att) => (
              <div
                key={att.id}
                className="group relative flex items-center gap-2 rounded-lg border border-[var(--border)] bg-[var(--surface)] px-2.5 py-1.5"
              >
                {att.isImage ? (
                  <div className="relative h-8 w-8 overflow-hidden rounded">
                    <Image src={att.url} alt={att.name} fill className="object-cover" unoptimized />
                  </div>
                ) : (
                  <FileText size={16} className="text-[var(--muted)]" />
                )}
                <div className="leading-tight">
                  <div className="max-w-[140px] truncate text-xs font-medium text-[var(--text)]">
                    {att.name}
                  </div>
                  <div className="text-[10px] text-[var(--muted)]">{formatBytes(att.size)}</div>
                </div>
                <button
                  onClick={() => removeAttachment(att.id)}
                  className="ml-1 rounded-full p-0.5 text-[var(--muted)] hover:bg-[var(--hover)] hover:text-[var(--text)]"
                  aria-label={`Remove ${att.name}`}
                >
                  <X size={13} />
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="flex items-end gap-2 rounded-2xl border border-[var(--border)] bg-[var(--surface)] px-3 py-2 shadow-sm">
          <input
            ref={fileInputRef}
            type="file"
            multiple
            className="hidden"
            onChange={(e) => handleFiles(e.target.files)}
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="mb-1 shrink-0 rounded-lg p-2 text-[var(--muted)] transition-colors hover:bg-[var(--hover)] hover:text-[var(--text)]"
            aria-label="Attach file"
          >
            <Paperclip size={18} />
          </button>

          <textarea
            ref={textareaRef}
            value={text}
            onChange={handleTextChange}
            onKeyDown={handleKeyDown}
            placeholder="Message the assistant..."
            rows={1}
            className="flex-1 resize-none bg-transparent py-1.5 text-sm text-[var(--text)] placeholder:text-[var(--muted)] focus:outline-none"
          />

          {isStreaming ? (
            <button
              onClick={stopStreaming}
              className="mb-1 shrink-0 rounded-lg bg-[var(--text)] p-2 text-[var(--bg)] transition-opacity hover:opacity-80"
              aria-label="Stop generating"
            >
              <Square size={16} fill="currentColor" />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={!text.trim() && attachments.length === 0}
              className="mb-1 shrink-0 rounded-lg bg-[var(--accent)] p-2 text-white transition-opacity disabled:opacity-30"
              aria-label="Send message"
            >
              <ArrowUp size={16} />
            </button>
          )}
        </div>

        <p className="mt-2 text-center text-[11px] text-[var(--muted)]">
          Frontend created in Next.js with Typescript + TailwindCSS 
        </p>
        <p className=" text-center text-[11px] text-[var(--muted)]">
          By Ajay Patel  
        </p>
      </div>
    </div>
  );
}
