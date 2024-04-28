"use client";

import { cn } from "@/utils/cn";
import { AnimatePresence, motion } from "framer-motion";
import Link from "next/link";
import { useState } from "react";

export const HoverEffect = ({
    items,
    className,
}: {
    items: {
        title: string;
        tags: string[];
        link: string;
        id: number;
    }[];
    className?: string;
}) => {
    let [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

    return (
        <div className={cn("flex flex-row overflow-scroll py-10", className)}>
            {items.map((item, idx) => (
                <Link
                    href={item?.link}
                    key={item?.id}
                    className="group relative block h-full w-full min-w-[220px] p-2"
                    onMouseEnter={() => setHoveredIndex(idx)}
                    onMouseLeave={() => setHoveredIndex(null)}
                >
                    <AnimatePresence>
                        {hoveredIndex === idx && (
                            <motion.span
                                className="absolute inset-0 block h-full w-full rounded-3xl bg-blue-200  dark:bg-slate-800/[0.8]"
                                layoutId="hoverBackground"
                                initial={{ opacity: 0 }}
                                animate={{
                                    opacity: 1,
                                    transition: { duration: 0.15 },
                                }}
                                exit={{
                                    opacity: 0,
                                    transition: { duration: 0.15, delay: 0.2 },
                                }}
                            />
                        )}
                    </AnimatePresence>
                    <Card className="flex-center border-2 border-gray-300 text-center">
                        <img
                            src="/bear.svg"
                            className="h-36 w-full bg-gray-400"
                        />
                        <CardTitle>{item.title}</CardTitle>
                        <div className="flex-center flex-row space-x-2 pt-2">
                            {item.tags.map((tag) => (
                                <CardTag>{tag}</CardTag>
                            ))}
                        </div>
                    </Card>
                </Link>
            ))}
        </div>
    );
};

export const Card = ({
    className,
    children,
}: {
    className?: string;
    children: React.ReactNode;
}) => {
    return (
        <div
            className={cn(
                "relative z-20 h-full w-full overflow-hidden rounded-xl border border-transparent bg-white",
                className,
            )}
        >
            <div className="relative z-50 w-full p-2">
                <div className="">{children}</div>
            </div>
        </div>
    );
};
export const CardTitle = ({
    className,
    children,
}: {
    className?: string;
    children: React.ReactNode;
}) => {
    return (
        <h4 className={cn("mt-4 text-xl font-bold text-black", className)}>
            {children}
        </h4>
    );
};
export const CardTag = ({
    className,
    children,
}: {
    className?: string;
    children: React.ReactNode;
}) => {
    return (
        <p
            className={cn(
                "rounded-xl bg-gray-200 px-2 py-1 text-sm font-medium leading-relaxed tracking-wide text-zinc-800",
                className,
            )}
        >
            {children}
        </p>
    );
};
