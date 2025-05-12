// import { openai } from "@ai-sdk/openai";
// import { jsonSchema, streamText } from "ai";

// export const runtime = "edge";
// export const maxDuration = 30;

// export async function POST(req: Request) {
//   const { messages, system, tools } = await req.json();

//   const result = streamText({
//     model: openai("gpt-4o"),
//     messages,
//     // forward system prompt and tools from the frontend
//     system,
//     tools: Object.fromEntries(
//       Object.entries<{ parameters: unknown }>(tools).map(([name, tool]) => [
//         name,
//         {
//           parameters: jsonSchema(tool.parameters!),
//         },
//       ]),
//     ),
//   });

//   return result.toDataStreamResponse();
// }


// // app/api/chat/route.ts
// import { openai } from "@ai-sdk/openai";
// import { jsonSchema, streamText } from "ai";

// export const runtime = "edge";
// export const maxDuration = 30;

// export async function POST(req: Request) {
//   // 1) pull off the UI’s payload
//   const { messages, system, tools } = await req.json();

//   // 2) fetch your new context API
//   const ctxRes = await fetch("http://localhost:8000/context");
//   if (!ctxRes.ok) {
//     throw new Error("Failed to load extra context: " + await ctxRes.text());
//   }
//   const { system: extraSystem, message: extraMsg } = await ctxRes.json();

//   // 3) inject into the existing streams
//   const augmentedSystem = system + "\n\n" + extraSystem;
//   const augmentedMessages = [...messages, extraMsg];
//   console.log(augmentedSystem)
//   console.log(augmentedMessages)

//   // 4) hand off to your original streamText call
//   const result = streamText({
//     model: openai("gpt-4o"),
//     messages: augmentedMessages,
//     system: augmentedSystem,
//     tools: Object.fromEntries(
//       Object.entries<{ parameters: unknown }>(tools).map(([name, tool]) => [
//         name,
//         {
//           parameters: jsonSchema(tool.parameters!),
//         },
//       ])
//     ),
//   });

//   return result.toDataStreamResponse();
// }


// app/api/chat/route.ts
import { openai } from "@ai-sdk/openai";
import { jsonSchema, streamText } from "ai";

export const runtime = "edge";
export const maxDuration = 30;

export async function POST(req: Request) {
  // 1) Get UI payload (messages, system, tools)
  const {
    messages: rawMessages = [],
    system: initialSystem = "",
    tools = {},
  } = await req.json();

  // 2) Flatten each message.content → string
  const messages = rawMessages.map((m: any) => {
    if (typeof m.content === "string") {
      return { role: m.role, content: m.content };
    } else if (Array.isArray(m.content)) {
      return {
        role: m.role,
        content: m.content.map((c: any) => c.text).join(""),
      };
    }
    return { role: m.role, content: "" };
  });

  // 3) Extract the user’s last question
  const last = messages[messages.length - 1] || { content: "" };
  const question = last.content;

  // 4) Fetch context from FastAPI
  const ctxRes = await fetch("http://localhost:8000/context", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!ctxRes.ok) {
    throw new Error("Context fetch failed: " + await ctxRes.text());
  }
  const { system: extraSystem, message: extraMsg, laws } = await ctxRes.json();
  console.log(extraMsg)
  // 5) Build the full system prompt (Arabic) including the retrieved laws
  const lawContext = laws
    .map((l: any) => `${l.title}: ${l.content}`)
    .join("\n\n");
  const system = [
    initialSystem,
    extraSystem,
    "السياق القانوني:",
    lawContext,
  ]
    .filter(Boolean)
    .join("\n\n");

  console.log(lawContext)
  console.log('----------------------------')
  console.log()
  // console.log(laws)
  // 6) Append the extra message
  const augmentedMessages = [...messages, extraMsg];
  console.log(augmentedMessages)
  // 7) Stream via openai from the frontend
  const result = streamText({
    model: openai("gpt-4o"),
    system,
    messages: augmentedMessages,
    tools: Object.fromEntries(
      Object.entries<{ parameters: unknown }>(tools).map(([name, tool]) => [
        name,
        { parameters: jsonSchema(tool.parameters!) },
      ])
    ),
  });

  return result.toDataStreamResponse();
}