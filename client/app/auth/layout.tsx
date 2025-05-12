// app/auth/layout.tsx
export const metadata = { title: 'التوثيق' }

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        {children}
      </div>
    </main>
  )
}