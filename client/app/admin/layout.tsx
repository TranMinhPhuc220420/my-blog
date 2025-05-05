// app/admin/layout.tsx

import { ReactNode } from "react";
import AdminSidebar from "@/components/layout/AdminSidebar";
import "@/styles/admin.css"; // nếu có css riêng

export default function AdminLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen bg-gray-100">
      <AdminSidebar />
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
