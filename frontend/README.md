# AI Chat UI

A Claude/ChatGPT-style chat interface built with Next.js (App Router), TypeScript, and Tailwind CSS. Fully functional out of the box with a mock streaming backend — swap in a real AI API by editing a single file.

## Features

- Streaming responses, rendered token-by-token as they arrive
- Multiple conversations with a sidebar (create, switch, delete, auto-titled from the first message)
- File and image upload, attached to messages with previews
- Markdown rendering with GitHub-flavored markdown (tables, lists, etc.)
- Syntax-highlighted code blocks with a one-click copy button
- Model switcher (currently lists two mock models; replace with real ones)
- Light and dark theme, persisted across sessions
- Conversations persisted to localStorage (survives page reloads)
- Stop-generation button to cancel an in-progress response
- Responsive layout with a collapsible sidebar

## Getting started

Requires Node.js 18.18 or later.

```bash
npm install
npm run dev
```

Open http://localhost:3000. The first load may take a few seconds while Next.js compiles the page — this is normal in dev mode.

## Project structure

```
src/
  app/
    api/chat/route.ts     <- the mock backend. Replace this to connect a real AI API.
    layout.tsx             <- root layout, sets up theme-flash prevention
    page.tsx                <- main page, wires sidebar + chat panel together
    globals.css             <- design tokens (colors, spacing) for light/dark themes
  components/
    Sidebar.tsx              <- conversation list
    TopBar.tsx               <- model switcher + theme toggle
    MessageList.tsx          <- scrollable message history
    MessageBubble.tsx        <- single message, renders markdown + attachments
    CodeBlock.tsx             <- syntax-highlighted code block with copy button
    Composer.tsx               <- text input, file upload, send/stop button
  lib/
    streamClient.ts            <- consumes the SSE stream from /api/chat
    persistence.ts              <- localStorage read/write for conversations
    utils.ts                     <- small helpers (formatting, etc.)
  store/
    chatStore.tsx                <- React context holding all chat state
  types/
    chat.ts                       <- shared TypeScript types + the model list
```

## Connecting a real backend

Everything in the UI is already wired up to call `POST /api/chat` and stream
the response. To use a real model, open **`src/app/api/chat/route.ts`** —
it has detailed comments at the top explaining exactly what to change.

In short:

1. Keep accepting the same request body: `{ messages, modelId }`.
2. Replace `buildMockReply(...)` with a real call to your AI provider
   (Anthropic, OpenAI, or your own backend).
3. As you receive tokens from the provider's stream, write them out in the
   same format the client already expects:
   ```
   data: {"delta": "next chunk of text"}\n\n
   ```
   ...followed by `data: [DONE]\n\n` when finished.
4. Add any API key to `.env.local` (copy `.env.example` to get started) and
   read it server-side with `process.env.YOUR_KEY_NAME` — never expose it
   to the client.

No other file needs to change. The streaming client, message store, and UI
components are all protocol-based, not provider-specific.

To add or rename models, edit `MODEL_OPTIONS` in `src/types/chat.ts`.

## Notes

- Conversations are stored in the browser's localStorage, not a database —
  there's no multi-device sync or server-side history yet. If you need
  that, you'll want to add a real backend with persistence (e.g. Postgres)
  and replace `src/lib/persistence.ts` with API calls.
- There's no authentication. Add it at the Next.js middleware level or in
  front of `/api/chat` if you need it.
- File/image attachments are currently held in-browser only (as object
  URLs) and are not sent to the mock backend. When you connect a real
  model that supports file or image input, you'll need to base64-encode
  attachments and include them in the request body sent to `/api/chat`.
