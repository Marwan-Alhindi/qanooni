// app/api/chat/route.ts
import { openai } from "@ai-sdk/openai";
import {
  jsonSchema,
  streamText,
  type CoreMessage,
  type CoreTool,
} from "ai";

//
// 1) Define the shapes you actually receive from the UI & backend
//
interface Fragment {
  text: string;
}

type IncomingMessage = {
  role: "system" | "user" | "assistant";
  content: string | Fragment[];
};

interface Law {
  title: string;
  content: string;
}

interface ToolEntry {
  // we know these come in as plain JSON objects
  parameters: Record<string, unknown>;
}

export const runtime = "edge";
export const maxDuration = 30;

export async function POST(req: Request) {
  //
  // 2) Strongly‐type the JSON body
  //
  const body = (await req.json()) as {
    messages?: IncomingMessage[];
    system?: string;
    tools?: Record<string, ToolEntry>;
  };

  const rawMessages = body.messages ?? [];
  const initialSystem = body.system ?? "";
  const tools = body.tools ?? {};

  //
  // 3) Turn IncomingMessage → CoreMessage
  //
  const messages: CoreMessage[] = rawMessages.map((m) => {
    const content =
      typeof m.content === "string"
        ? m.content
        : m.content.map((frag) => frag.text).join("");
    return { role: m.role, content };
  });

  //
  // 4) Pull the user’s last question
  //
  const question = messages[messages.length - 1]?.content ?? "";

  //
  // 5) Fetch extra context from your FastAPI backend
  //
  const ctxRes = await fetch("https://qanooni-rr8b.onrender.com/context", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!ctxRes.ok) {
    throw new Error("Context fetch failed: " + (await ctxRes.text()));
  }
  const { system: extraSystem = "", message: extraMsgRaw, laws } =
    (await ctxRes.json()) as {
      system?: string;
      message: IncomingMessage;
      laws: Law[];
    };

  //
  // 6) Convert that extra message into CoreMessage too
  //
  const extraContent =
    typeof extraMsgRaw.content === "string"
      ? extraMsgRaw.content
      : extraMsgRaw.content.map((f) => f.text).join("");
  const extraMsg: CoreMessage = {
    role: extraMsgRaw.role,
    content: extraContent,
  };

  //
  // 7) Build your system prompt, including the laws
  //
  const lawContext = laws.map((l) => `${l.title}: ${l.content}`).join("\n\n");
  const systemPrompt = [
    initialSystem,
    extraSystem,
    "السياق القانوني:",
    lawContext,
  ]
    .filter(Boolean)
    .join("\n\n");

  //
  // 8) Append the extra message
  //
  const augmentedMessages = [...messages, extraMsg];

  //
  // 9) Convert your incoming tools → CoreTool
  //
  const toolsForStream: Record<string, CoreTool> = Object.fromEntries(
    Object.entries(tools).map(([name, tool]) => [
      name,
      {
        parameters: jsonSchema(tool.parameters),
      },
    ])
  );

  //
  // 10) Finally stream!
  //
  const result = streamText({
    model: openai("gpt-4o"),
    system: systemPrompt,
    messages: augmentedMessages,
    tools: toolsForStream,
  });

  return result.toDataStreamResponse();
}