import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI MultiPDF ChatBot",
  description: "A Claude/ChatGPT-style chat interface ready to connect to any backend.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <head>
        {/* Runs before paint to avoid a flash of the wrong theme. */}
        <script
          dangerouslySetInnerHTML={{
            __html: `try {
              var t = window.localStorage.getItem("ai-chat-ui:theme");
              if (t === "dark") document.documentElement.classList.add("dark");
            } catch (e) {}`,
          }}
        />
      </head>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
