'use client'
import Link from 'next/link'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabaseClient'

export default function LoginPage() {
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [error, setError]       = useState<string|null>(null)
  const router = useRouter()

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) setError(error.message)
    else router.push('/assistant')
  }

  return (
    <form onSubmit={onSubmit} className="bg-white p-6 rounded shadow space-y-4">
      <h2 className="text-2xl font-bold text-center">تسجيل الدخول</h2>
      {error && <p className="text-red-600">{error}</p>}
      <input
        type="email"
        placeholder="البريد الإلكتروني"
        className="w-full border px-3 py-2 rounded"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="كلمة المرور"
        className="w-full border px-3 py-2 rounded"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
      />
      <button
        type="submit"
        className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded transition"
      >
        دخول
      </button>
      <p className="text-center text-sm">
        لا تملك حساب؟{' '}
        <Link
          href="/auth/register"
          className="text-green-600 hover:text-green-700 underline transition"
        >
          إنشاء حساب
        </Link>
      </p>
    </form>
  )
}