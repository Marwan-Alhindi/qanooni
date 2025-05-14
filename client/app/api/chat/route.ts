// app/api/chat/route.ts
import { openai } from "@ai-sdk/openai";
import {
  jsonSchema,
  streamText,
  type CoreMessage,
  type CoreTool,
} from "ai";

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
  url?: string;
}
interface ToolEntry {
  parameters: Record<string, unknown>;
}

export const runtime = "edge";
export const maxDuration = 30;

export async function POST(req: Request) {
  const body = (await req.json()) as {
    messages?: IncomingMessage[];
    system?: string;
    tools?: Record<string, ToolEntry>;
  };

  const rawMessages = body.messages ?? [];
  // const initialSystem = body.system ?? "";
  const tools = body.tools ?? {};

  const messages: CoreMessage[] = rawMessages.map((m) => {
    const content =
      typeof m.content === "string"
        ? m.content
        : m.content.map((frag) => frag.text).join("");
    return { role: m.role, content };
  });

  const question = messages[messages.length - 1]?.content ?? "";

  // RAG
  const ctxRes = await fetch("https://qanooni-1.onrender.com/context", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!ctxRes.ok) {
    throw new Error("Context fetch failed: " + (await ctxRes.text()));
  }


  const {message: extraMsgRaw, laws } =
    (await ctxRes.json()) as {
      system?: string;
      message: IncomingMessage;
      laws: Law[];
    };

  const extraContent =
    typeof extraMsgRaw.content === "string"
      ? extraMsgRaw.content
      : extraMsgRaw.content.map((f) => f.text).join("");
  const extraMsg: CoreMessage = {
    role: extraMsgRaw.role,
    content: extraContent,
  };

  const augmentedMessages = [...messages, extraMsg];

  // Finetuned
  const fineRes = await fetch("https://qanooni-1.onrender.com/finetuned", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  

  const fineJSON = await fineRes.json();
  const finetunedAnswer = fineJSON.answer ?? "❌ لم يتم توليد رد مخصص.";

  const lawContext = laws.map((l) => `${l.title}: ${l.content}`).join("\n\n");
  const systemPrompt = [
    "أنت مساعد قانوني، ويجب أن ترد على السؤال بالترتيب التالي:",
    "1. **ابدأ برد مختصر**:\nقم بإعطاء إجابة مباشرة وواضحة مستخلصة من فهمك للسياق القانوني.",
    "2. **ثم قدم الرد التفصيلي بناءً على القانون**:\nاشرح بشكل مفصل اعتمادًا على المعلومات التي قرأتها في السياق دون إعادة كتابة السياق نفسه.",
    "3. 🔗 **أخيراً، أضف المراجع التي استندت إليها فقط كرابط لكل مادة ذات صلة.**",
    "🔍 مثال كامل لتوضيح التنسيق المطلوب:",
    "إذا العميل سأل: ما مدة الإشعار قبل إنهاء عقد العمل؟",
    "\nالرد:",
    "هذا هو الرد المختصر لسؤالك،\nشهرين/شهر (حسب الاتفاق) قبل إنهاء عقد العمل غير محدد المدة.",
    "\nوالرد بالتفصيل بناء على قانون العمل:\n" +
      "مدة الإشعار قبل إنهاء عقد العمل تختلف بين البلدان ويمكن أن تعتمد على نوع العقد وفترة الخدمة. إليك بعض الإرشادات العامة الشائعة في الكثير من الأنظمة:\n\n" +
      "العقود المحددة المدة: ينتهي العقد بانتهاء مدته المحددة، لذا قد لا يتطلب إشعارًا مسبقًا. ومع ذلك، إذا تم إنهاؤه قبل انتهاء المدة، فقد تحتوي العقود على شروط للإشعار.\n\n" +
      "العقود غير المحددة المدة:\n- خلال فترة التجربة: تكون مدة الإشعار عادة أقصر، مثل أسبوع إلى أسبوعين.\n- بعد فترة التجربة: تتراوح مدة الإشعار من شهر إلى ثلاثة أشهر، حسب سنوات الخدمة ولوائح العمل المحلية.\n\n" +
      "القوانين المحلية: تختلف من بلد لآخر. من المهم الرجوع إلى قانون العمل المحلي للحصول على المدة الدقيقة والمتطلبات الإضافية.\n\n" +
      "اتفاقيات العمل الجماعية: قد تحتوي على شروط خاصة تختلف عن القانون العام.\n\n" +
      "العقد الفردي: يمكن أن يتضمن شروطًا تتعلق بمدة الإشعار، طالما أنها لا تقل عن الحدود الدنيا التي يحددها القانون.\n\n" +
      "دائمًا يُفضل مراجعة عقد العمل الخاص بك والقوانين المحلية للتأكد من التفاصيل الدقيقة والامتثال الكامل.",
    "\nوإليك المراجع:\n- https://nezams.com/نظام-العمل/#subject-5",
    "\n✅ الآن طبق هذا التنسيق على السؤال التالي:",
    "السياق القانوني:\n" + lawContext,
    "المراجع:\n" + laws.map((l) => `- ${l.url}`).join("\n"),
  ]
    .filter(Boolean)
    .join("\n\n");
  
  // 3️⃣ Stream final output
  const toolsForStream: Record<string, CoreTool> = Object.fromEntries(
    Object.entries(tools).map(([name, tool]) => [
      name,
      {
        parameters: jsonSchema(tool.parameters),
      },
    ])
  );

  const result = streamText({
    model: openai("gpt-4o"),
    system: systemPrompt,
    messages: augmentedMessages,
    tools: toolsForStream,
  });

  const ragStream = result.toDataStreamResponse();

  // 🧠 Attach metadata headers if needed
  ragStream.headers.set("X-Finetuned-Answer", encodeURIComponent(finetunedAnswer));
  ragStream.headers.set("X-References", encodeURIComponent(JSON.stringify(laws.map((l) => l.url))));

  return ragStream;
}