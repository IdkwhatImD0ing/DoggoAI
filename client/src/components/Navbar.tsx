"use client";

import React from "react";
import { Home, HeartHandshake, Mic2 } from "lucide-react";
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
        icon: HeartHandshake,
        link: "/community",
    },
    {
        id: 3,
        icon: Mic2,
        link: "/live",
    },
];

const Navbar = () => {
    const router = useRouter();
    const pathname = usePathname();

    return (
        <div className="fixed max-h-[calc(100vh-2rem)] min-h-[calc(100vh-2rem)] w-[100px] rounded-3xl bg-white p-4 py-6">
            <div className="mx-auto space-y-3">
                {LINKS.map((item) => (
                    <div
                        key={item.id}
                        className={cn(
                            "flex-center mx-auto aspect-square w-16 cursor-pointer rounded-full",
                            pathname.includes(item.link)
                                ? "bg-jas-blue"
                                : "bg-[#E9F4F7]",
                        )}
                        onClick={() => router.push(item.link)}
                    >
                        <item.icon
                            className={cn(
                                "h-7 w-7 stroke-[3]",
                                pathname.includes(item.link)
                                    ? "text-white"
                                    : "text-jas-gray",
                            )}
                        />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Navbar;
