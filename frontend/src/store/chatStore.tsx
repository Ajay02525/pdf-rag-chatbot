"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import { v4 as uuid } from "uuid";
import { Attachment, ChatMessage, Conversation, MODEL_OPTIONS } from "@/types/chat";
import { loadConversations, saveConversations } from "@/lib/persistence";
import { deriveTitle } from "@/lib/utils";
import { streamChat } from "@/lib/streamClient";
import { uploadFile } from "@/lib/uploadClient";

interface ChatStoreValue {
  conversations: Conversation[];
  activeId: string | null;
  activeConversation: Conversation | null;
  isStreaming: boolean;
  createConversation: () => void;
  deleteConversation: (id: string) => void;
  selectConversation: (id: string) => void;
  setModelForActive: (modelId: string) => void;
  sendMessage: (text: string, attachments: Attachment[]) => Promise<void>;
  stopStreaming: () => void;
  renameConversation: (id: string, title: string) => void;
}

const ChatStoreContext = createContext<ChatStoreValue | null>(null);

function newConversation(): Conversation {
  const now = Date.now();
  return {
    id: uuid(),
    title: "New conversation",
    messages: [],
    modelId: MODEL_OPTIONS[0].id,
    createdAt: now,
    updatedAt: now,
  };
}

function initialState(): { conversations: Conversation[]; activeId: string } {
  const fresh = newConversation();
  return { conversations: [fresh], activeId: fresh.id };
}

export function ChatStoreProvider({ children }: { children: React.ReactNode }) {
  const [{ conversations, activeId }, setState] = useState<{
    conversations: Conversation[];
    activeId: string | null;
  }>(initialState);
  const [isStreaming, setIsStreaming] = useState(false);
  const [hydrated, setHydrated] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const setConversations = useCallback(
    (updater: Conversation[] | ((prev: Conversation[]) => Conversation[])) => {
      setState((prev) => ({
        ...prev,
        conversations:
          typeof updater === "function" ? updater(prev.conversations) : updater,
      }));
    },
    []
  );

  const setActiveId = useCallback((id: string | null) => {
    setState((prev) => ({ ...prev, activeId: id }));
  }, []);

  // Hydrate from localStorage on mount (client only). This intentionally
  // runs once on mount; the resulting setState call replaces the
  // placeholder conversation created above with any saved data.
  useEffect(() => {
    const loaded = loadConversations();
    if (loaded.length > 0) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- one-time hydration from localStorage, which is only readable client-side after mount
      setState({ conversations: loaded, activeId: loaded[0].id });
    }
    setHydrated(true);
  }, []);

  // Persist whenever conversations change (after initial hydration)
  useEffect(() => {
    if (!hydrated) return;
    saveConversations(conversations);
  }, [conversations, hydrated]);

  const activeConversation = conversations.find((c) => c.id === activeId) ?? null;

  const updateConversation = useCallback(
    (id: string, updater: (c: Conversation) => Conversation) => {
      setConversations((prev) =>
        prev.map((c) => (c.id === id ? updater(c) : c))
      );
    },
    [setConversations]
  );

  const createConversation = useCallback(() => {
    const fresh = newConversation();
    setConversations((prev) => [fresh, ...prev]);
    setActiveId(fresh.id);
  }, [setConversations, setActiveId]);

  const deleteConversation = useCallback(
    (id: string) => {
      setConversations((prev) => {
        const next = prev.filter((c) => c.id !== id);
        if (id === activeId) {
          setActiveId(next[0]?.id ?? null);
        }
        return next;
      });
    },
    [activeId, setConversations, setActiveId]
  );

  const selectConversation = useCallback((id: string) => {
    setActiveId(id);
  }, [setActiveId]);

  const renameConversation = useCallback(
    (id: string, title: string) => {
      updateConversation(id, (c) => ({ ...c, title }));
    },
    [updateConversation]
  );

  const setModelForActive = useCallback(
    (modelId: string) => {
      if (!activeId) return;
      updateConversation(activeId, (c) => ({ ...c, modelId }));
    },
    [activeId, updateConversation]
  );

  const stopStreaming = useCallback(() => {
    abortRef.current?.abort();
  }, []);

  const sendMessage = useCallback(
    async (text: string, attachments: Attachment[]) => {
      if (!activeId) return;
      const trimmed = text.trim();
      if (!trimmed && attachments.length === 0) return;

      const userMessage: ChatMessage = {
        id: uuid(),
        role: "user",
        content: trimmed,
        attachments,
        createdAt: Date.now(),
      };

      const assistantId = uuid();
      const assistantMessage: ChatMessage = {
        id: assistantId,
        role: "assistant",
        content: "",
        createdAt: Date.now(),
        streaming: true,
        sources: [],
      };

      let isFirstMessage = false;

      updateConversation(activeId, (c) => {
        isFirstMessage = c.messages.length === 0;
        return {
          ...c,
          title: isFirstMessage ? deriveTitle(trimmed) : c.title,
          messages: [...c.messages, userMessage, assistantMessage],
          updatedAt: Date.now(),
        };
      });

      setIsStreaming(true);
      const controller = new AbortController();
      abortRef.current = controller;

      // Build message history for the API call (exclude the empty streaming placeholder)
      const conv = conversations.find((c) => c.id === activeId);
      const history = [
        ...(conv?.messages ?? []),
        userMessage,
      ].map((m) => ({ role: m.role, content: m.content }));

      const modelId = conv?.modelId ?? MODEL_OPTIONS[0].id;
      if (attachments.length) {
          for (const attachment of attachments) {
              await uploadFile(attachment.file);
          }

      }
      await streamChat(
        { messages: history, modelId, signal: controller.signal, sessionId: activeId },
        {
          onDelta: (delta) => {
            updateConversation(activeId, (c) => ({
              ...c,
              messages: c.messages.map((m) =>
                m.id === assistantId ? { ...m, content: m.content + delta } : m
              ),
            }));
          },
          onPipeline: (pipeline) => {
            updateConversation(activeId, (c) => ({
              ...c,
              messages: c.messages.map((m) =>
                m.id === assistantId
                  ? {
                      ...m,
                      pipeline,
                    }
                  : m
              ),
            }));
          },
          onSources: (sources) => {
            updateConversation(activeId, (c) => ({
              ...c,
              messages: c.messages.map((m) =>
                m.id === assistantId
                  ? {
                      ...m,
                      sources,
                    }
                  : m
              ),
            }));
          },
          onDone: () => {
            updateConversation(activeId, (c) => ({
              ...c,
              messages: c.messages.map((m) =>
                m.id === assistantId ? { ...m, streaming: false } : m
              ),
              updatedAt: Date.now(),
            }));
            setIsStreaming(false);
            abortRef.current = null;
          },
          onError: (err) => {
            updateConversation(activeId, (c) => ({
              ...c,
              messages: c.messages.map((m) =>
                m.id === assistantId
                  ? {
                      ...m,
                      streaming: false,
                      error: err.message || "Something went wrong while generating a response.",
                    }
                  : m
              ),
            }));
            setIsStreaming(false);
            abortRef.current = null;
          },
        }
      );
    },
    [activeId, conversations, updateConversation]
  );

  const value: ChatStoreValue = {
    conversations,
    activeId,
    activeConversation,
    isStreaming,
    createConversation,
    deleteConversation,
    selectConversation,
    setModelForActive,
    sendMessage,
    stopStreaming,
    renameConversation,
  };

  return (
    <ChatStoreContext.Provider value={value}>
      {children}
    </ChatStoreContext.Provider>
  );
}

export function useChatStore(): ChatStoreValue {
  const ctx = useContext(ChatStoreContext);
  if (!ctx) {
    throw new Error("useChatStore must be used within a ChatStoreProvider");
  }
  return ctx;
}
