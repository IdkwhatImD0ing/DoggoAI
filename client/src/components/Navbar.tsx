"use client";

import React from "react";
import { Home, Mic2, Cross } from "lucide-react";
import { useRouter, usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const LINKS = [
    {
        id: 1,
        icon: Home,
        link: "/app",
    },
    {
        id: 2,
        icon: Mic2,
        link: "/live",
    },
    {
        id: 3,
        icon: Cross,
        link: "/health",
    },
];

const Navbar = () => {
    const router = useRouter();
    const pathname = usePathname();

    return (
        <div className="min-h-full w-[100px] bg-gray-500 py-16">
            <div className="mx-auto space-y-4">
                {LINKS.map((item) => (
                    <div
                        key={item.id}
                        className={cn(
                            "flex-center mx-auto aspect-square w-16 cursor-pointer",
                            pathname.includes(item.link)
                                ? "bg-gray-800"
                                : "bg-gray-400",
                        )}
                        onClick={() => router.push(item.link)}
                    >
                        <item.icon className="text-white" />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Navbar;
