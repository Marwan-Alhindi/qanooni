import * as React from "react"
// import { Github, MessagesSquare } from "lucide-react"
import Link from "next/link"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar"
// import { ThreadList } from "./assistant-ui/thread-list"

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <Link
                href="https://bind.link/@qanoni"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2"
              >
                <div className="w-10 h-10 rounded-lg overflow-hidden">
                  <img
                    src="/Qanoni_Logo.png"
                    alt="Qanooni Logo"
                    className="w-full h-full object-cover"
                  />
                </div>
                <span className="font-semibold">قانوني - Qanooni</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent className="ml-4 mt-4 space-y-2">
        {/* Active item */}
        <Link
          href="/assistant"
          className="
            block text-center
            px-4 py-2
            bg-green-600 text-white
            rounded-lg
            hover:bg-green-700
            transition
            mr-4
          "
        >
          العمل
        </Link>
        <div className="border-b border-gray-200" />

        {/* Disabled “coming soon” items */}
        {[
          "التجارة",
          "الشركات",
          "المنافسة وعدم الاحتكار",
          "حماية المستهلك",
          "الشركات التأمينية",
          "الضريبة والرسوم",
          "الإفلاس",
          "الجرائم المعلوماتية",
          "مكافحة الفساد",
          "مكافحة غسل الأموال وتمويل الإرهاب",
          "التحكيم التجاري",
          "الاستثمار الأجنبي",
          "حماية الحقوق الفكرية",
          "المرور",
          "البيئة",
          "النظام البلدي",
        ].map((label) => (
          <React.Fragment key={label}>
            <div
              className="
                relative flex justify-center items-center
                px-4 py-2
                rounded-lg
                bg-gray-100
                text-gray-400
                opacity-75
                cursor-not-allowed
                mr-4
              "
            >
              {label}
              <span
                className="
                  absolute top-0 right-0
                  text-xs font-semibold
                  bg-yellow-300 text-yellow-900
                  px-1.5 py-0.5
                  rounded-bl
                "
              >
                قريباً
              </span>
            </div>
            <div className="border-b border-gray-200" />
          </React.Fragment>
        ))}
      </SidebarContent>

      <SidebarRail />

      <SidebarFooter>
        <SidebarMenu>
          {/* footer items… */}
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}