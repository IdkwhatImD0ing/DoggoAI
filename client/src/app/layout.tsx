import type { Metadata } from "next";
import { Poppins } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import { cn } from "@/lib/utils";

const poppins = Poppins({
    subsets: ["latin"],
    weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
});
export const metadata: Metadata = {
    title: "DoggoAI",
    description: "DoggoAI - HackDavis 2024",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body
                className={cn(
                    poppins.className,
                    "bg-jas-blue flex min-h-[100vh] p-4",
                )}
            >
                <Navbar />
                <div className="ml-[8rem]">{children}</div>
            </body>
        </html>
    );
}
