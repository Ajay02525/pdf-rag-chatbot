"use client";

import { useState } from "react";
import { ChatStoreProvider, useChatStore } from "@/store/chatStore";
import Sidebar from "@/components/Sidebar";
import TopBar from "@/components/TopBar";
import MessageList from "@/components/MessageList";
import Composer from "@/components/Composer";

function getInitialTheme(): "light" | "dark" {
  if (typeof document === "undefined") return "light";
  return document.documentElement.classList.contains("dark") ? "dark" : "light";
}

function ChatLayout() {
  const { activeConversation } = useChatStore();
  const [theme, setTheme] = useState<"light" | "dark">(getInitialTheme);

  const toggleTheme = () => {
    const next = theme === "light" ? "dark" : "light";
    setTheme(next);
    document.documentElement.classList.toggle("dark", next === "dark");
    window.localStorage.setItem("ai-chat-ui:theme", next);
  };

  return (
    <div className="flex h-screen w-full overflow-hidden bg-[var(--bg)]">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar theme={theme} onToggleTheme={toggleTheme} />
        <MessageList conversation={activeConversation} />
        <Composer />
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <ChatStoreProvider>
      <ChatLayout />
    </ChatStoreProvider>
  );
}
