"use client"
// components/layout/AdminSidebar.tsx

import '@/styles/globals.css'

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function AdminSidebar() {
  const pathname = usePathname();

  const links = [
    { href: "/admin", label: "Dashboard" },
    { href: "/admin/posts", label: "Bài viết" },
    { href: "/admin/users", label: "Người dùng" },
  ];

  return (
    <aside className="w-64 bg-white border-r">
      <div className="p-4 text-xl font-bold">Admin Panel</div>
      <nav className="flex flex-col p-2">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={`p-2 rounded hover:bg-gray-100 ${
              pathname === link.href ? "bg-gray-200 font-medium" : ""
            }`}
          >
            {link.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
