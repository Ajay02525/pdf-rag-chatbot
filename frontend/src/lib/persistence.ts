import { Conversation } from "@/types/chat";

const STORAGE_KEY = "ai-chat-ui:conversations";

export function loadConversations(): Conversation[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed;
  } catch {
    return [];
  }
}

export function saveConversations(conversations: Conversation[]): void {
  if (typeof window === "undefined") return;
  try {
    // Strip attachment object URLs before persisting — they don't survive
    // a page reload anyway, and we don't want to bloat localStorage.
    const safe = conversations.map((c) => ({
      ...c,
      messages: c.messages.map((m) => ({
        ...m,
        attachments: m.attachments?.map((a) => ({ ...a, url: "" })),
      })),
    }));
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(safe));
  } catch {
    // localStorage may be full or unavailable (e.g. private browsing) — fail silently
  }
}
