// import { NextRequest } from "next/server";

// /**
//  * ============================================================================
//  * MOCK CHAT ENDPOINT — REPLACE THIS TO CONNECT A REAL BACKEND
//  * ============================================================================
//  *
//  * This route currently fakes a streaming AI response so the UI is fully
//  * functional without any API keys. It streams back a Server-Sent-Events-style
//  * stream of plain text chunks, which `src/lib/streamClient.ts` consumes.
//  *
//  * To connect a real backend (Claude, OpenAI, or your own server):
//  *
//  * 1. Keep the same request shape coming in: { messages, modelId }
//  *    where messages = [{ role: "user" | "assistant", content: string }, ...]
//  *
//  * 2. Keep returning a `text/event-stream` Response with chunks shaped like:
//  *      data: {"delta": "some text"}\n\n
//  *    ...followed by a final:
//  *      data: [DONE]\n\n
//  *
//  *    This keeps `streamClient.ts` working unchanged. Example with the
//  *    Anthropic SDK:
//  *
//  *      const stream = await anthropic.messages.stream({
//  *        model: "claude-sonnet-4-6",
//  *        max_tokens: 1024,
//  *        messages,
//  *      });
//  *      for await (const event of stream) {
//  *        if (event.type === "content_block_delta") {
//  *          send({ delta: event.delta.text });
//  *        }
//  *      }
//  *
//  *    Or with OpenAI's SDK, map `chunk.choices[0].delta.content` the same way.
//  *
//  * 3. Add your API key to `.env.local` (never commit real keys) and read it
//  *    with `process.env.YOUR_KEY_NAME` server-side only.
//  * ============================================================================
//  */

// export const runtime = "nodejs";

// interface IncomingMessage {
//   role: "user" | "assistant" | "system";
//   content: string;
// }

// function buildMockReply(messages: IncomingMessage[], modelId: string): string {
//   const lastUser = [...messages].reverse().find((m) => m.role === "user");
//   const prompt = lastUser?.content?.trim() || "";

//   const intro = modelId === "mock-thoughtful"
//     ? "Let me think through this carefully before answering.\n\n"
//     : "";

//   if (!prompt) {
//     return intro + "I didn't receive any text to respond to. Try typing a message below.";
//   }

//   // A few canned behaviors so the mock feels alive without a real model.
//   if (/```|code|function|component|bug/i.test(prompt)) {
//     return (
//       intro +
//       `Here's a small example responding to "${prompt.slice(0, 60)}":\n\n` +
//       "```javascript\n" +
//       "function greet(name) {\n" +
//       "  return `Hello, ${name}! This is a mock response.`;\n" +
//       "}\n\n" +
//       "console.log(greet(\"world\"));\n" +
//       "```\n\n" +
//       "This is placeholder output from the mock API route at `src/app/api/chat/route.ts`. " +
//       "Swap in a real model call there and responses like this will come from the actual backend instead."
//     );
//   }

//   if (/^(hi|hey|hello|yo)\b/i.test(prompt)) {
//     return intro + "Hey there! This is a mock streaming response so you can see the chat UI in action — connect a real backend in `src/app/api/chat/route.ts` whenever you're ready.";
//   }

//   return (
//     intro +
//     `You said: "${prompt}"\n\n` +
//     "This response is being streamed token-by-token from a mock endpoint so you can test the interface end-to-end — typing indicators, markdown rendering, code blocks, and message history all work the same way they will once a real model is wired in.\n\n" +
//     "A few things worth trying right now:\n\n" +
//     "- Start a new conversation from the sidebar\n" +
//     "- Attach an image or file using the paperclip icon\n" +
//     "- Switch models using the selector at the top\n" +
//     "- Ask for some code to see syntax highlighting"
//   );
// }

// export async function POST(req: NextRequest) {
//   const body = await req.json();
//   const messages: IncomingMessage[] = body.messages ?? [];
//   const modelId: string = body.modelId ?? "mock-fast";

//   const fullText = buildMockReply(messages, modelId);
//   const words = fullText.split(/(\s+)/); // keep whitespace tokens so spacing is preserved

//   const delayMs = modelId === "mock-thoughtful" ? 55 : 18;

//   const encoder = new TextEncoder();

//   const stream = new ReadableStream({
//     async start(controller) {
//       const send = (payload: object) => {
//         controller.enqueue(encoder.encode(`data: ${JSON.stringify(payload)}\n\n`));
//       };

//       // Optional thinking delay for the "thoughtful" mock model
//       if (modelId === "mock-thoughtful") {
//         await new Promise((r) => setTimeout(r, 600));
//       }

//       for (const word of words) {
//         // Allow the client to abort mid-stream (e.g. user clicked Stop)
//         if (req.signal.aborted) {
//           controller.close();
//           return;
//         }
//         send({ delta: word });
//         await new Promise((r) => setTimeout(r, delayMs));
//       }

//       controller.enqueue(encoder.encode("data: [DONE]\n\n"));
//       controller.close();
//     },
//     cancel() {
//       // client disconnected; nothing else to clean up in the mock
//     },
//   });

//   return new Response(stream, {
//     headers: {
//       "Content-Type": "text/event-stream",
//       "Cache-Control": "no-cache",
//       Connection: "keep-alive",
//     },
//   });
// }
import { NextRequest } from "next/server";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  const body = await req.json();

  // Find the latest user message
  const lastUserMessage =
    [...(body.messages ?? [])]
      .reverse()
      .find((m) => m.role === "user");

  const backendBody = {
    session_id: body.sessionId ?? crypto.randomUUID(),
    question: lastUserMessage?.content ?? "",
  };

  console.log("Sending to backend:", backendBody);
  const baseUrl = process.env.NEXT_PUBLIC_API_URL!;
  const response = await fetch(`${baseUrl}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(backendBody),
    signal: req.signal,
  });


  console.log("Received from backend:", response.status, response.statusText,response);

  if (!response.ok) {
    return new Response(await response.text(), {
      status: response.status,
    });
  }

  return new Response(response.body, {
    status: response.status,
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}