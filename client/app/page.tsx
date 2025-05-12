// import { Assistant } from "./assistant";

// export default function Home() {
//   return <Assistant />;
// }

// app/page.tsx
import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col">
      {/* Hero */}
      <section className="flex-1 flex flex-col items-center justify-center px-4 text-center">
        <h1 className="text-5xl font-bold mb-4">مساعد القانون الذكي</h1>
        <p className="text-lg text-gray-700 max-w-xl mb-8">
          احصل على إجابات قانونية فورية ودقيقة مبنية على نصوص القوانين المحلية. 
          وفر وقتك وجهدك في البحث وفهم حقوقك والتزاماتك.
        </p>
        <div className="flex space-x-4" dir="rtl">
          <Link
            href="/auth/register"
            className="
              inline-block
              px-8 py-3
              bg-green-600 text-white
              rounded-lg shadow
              hover:bg-green-700
              transition
              whitespace-nowrap
              min-w-max
            "
          >
            إنشاء حساب
          </Link>

          <Link
            href="/auth/login"
            className="
              inline-block
              px-8 py-3
              border border-green-600
              text-green-600
              rounded-lg
              hover:bg-green-50
              transition
              whitespace-nowrap
              min-w-max
            "
          >
            تسجيل الدخول
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="bg-white py-16 px-4">
        <h2 className="text-3xl font-semibold text-center mb-10">لماذا تختارنا؟</h2>
        <div className="max-w-4xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-xl font-medium mb-2">بحث مبني على قانون</h3>
            <p className="text-gray-600">
              نعرض لك المواد القانونية ذات الصلة بسؤالك بشكل فوري ودقيق.
            </p>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-xl font-medium mb-2">إجابات فورية</h3>
            <p className="text-gray-600">
              لا حاجة للانتظار أو الترجمة؛ تحصل على الإجابة باللغة العربية مباشرة.
            </p>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-xl font-medium mb-2">واجهة سهلة الاستخدام</h3>
            <p className="text-gray-600">
              صُممت الواجهة لتكون بسيطة وواضحة، مناسبة للجميع دون تعقيد.
            </p>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-xl font-medium mb-2">محدثة دائماً</h3>
            <p className="text-gray-600">
              نحرص على تضمين أحدث التعديلات في القوانين لتبقى معلوماتك دقيقة.
            </p>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-xl font-medium mb-2">دعم وتوجيه</h3>
            <p className="text-gray-600">
              إذا احتجت لمزيد من التوضيح، يمكنك الرجوع إلى المصادر أو التواصل معنا.
            </p>
          </div>
          <div className="p-6 bg-gray-50 rounded-lg shadow">
            <h3 className="text-xl font-medium mb-2">آمن وسري</h3>
            <p className="text-gray-600">
              نضمن سرية استفساراتك وعدم مشاركة أي بيانات شخصية.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-100 py-6 text-center text-sm text-gray-500">
        <p>© 2025 مساعد القانون الذكي. جميع الحقوق محفوظة.</p>
      </footer>
    </main>
  )
}