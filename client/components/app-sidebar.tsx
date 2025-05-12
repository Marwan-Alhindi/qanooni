import * as React from "react"
import { Github, MessagesSquare } from "lucide-react"
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
import { ThreadList } from "./assistant-ui/thread-list"

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
                    {/* Logo (must live in /public/Qanoni_Logo.png) */}
                    <div className="w-10 h-10 rounded-lg overflow-hidden">
                      <img
                        src="/Qanoni_Logo.png"
                        alt="Qanooni Logo"
                        className="w-full h-full object-cover"
                      />
                    </div>

                    {/* Label */}
                    <span className="font-semibold">قانوني - Qanooni</span>
                  </Link>
              </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent className="ml-4 mt-4">
          <p className="flex justify-center">العمل</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">التجارة</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">الشركات</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">المنافسة وعدم الاحتكار</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">حماية المستهلك</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">الشركات التأمينية</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">الضريبة والرسوم</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">الإفلاس</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">الجرائم المعلوماتية</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">مكافحة الفساد</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">مكافحة غسل الأموال وتمويل الإرهاب</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">التحكيم التجاري</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">الاستثمار الأجنبي</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">حماية الحقوق الفكرية</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">المرور</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">البيئة</p>
          <div className="border-b border-gray-200"></div>

          <p className="flex justify-center">النظام البلدي</p>
          <div className="border-b border-gray-200"></div>
      </SidebarContent>
      
      <SidebarRail />
      <SidebarFooter>
        <SidebarMenu>
         
          {/* <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <Link href="https://github.com/assistant-ui/assistant-ui" target="_blank">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                  <Github className="size-4" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-semibold">GitHub</span>
                  <span className="">View Source</span>
                </div>
              </Link>
            </SidebarMenuButton>
            
          </SidebarMenuItem> */}
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
