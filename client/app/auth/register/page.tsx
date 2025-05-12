'use client'
import Link from 'next/link'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from "../../../lib/supabaseClient";
export default function RegisterPage() {
  const [email, setEmail]       = useState('')
  const [password, setPassword]   = useState('')
  const [error, setError]       = useState<string|null>(null)
  const router = useRouter()

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const { error } = await supabase.auth.signUp({ email, password })
    if (error) setError(error.message)
    else router.push('/auth/login')
  }

  return (
    <form onSubmit={onSubmit} className="bg-white p-6 rounded shadow space-y-4">
      <h2 className="text-2xl font-bold text-center">إنشاء حساب</h2>
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
      <button type="submit" className="w-full bg-green-600 text-white py-2 rounded">
        تسجيل
      </button>
      <p className="text-center text-sm">
        لديك حساب؟{' '}
        <Link href="/auth/login" className="text-blue-600 underline">
          تسجيل الدخول
        </Link>
      </p>
    </form>
  )
}