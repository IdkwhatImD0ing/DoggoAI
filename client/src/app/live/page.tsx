"use client";

import { Pause, StopCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import Websocket from "ws";
import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";
import { Progress } from "@/components/ui/progress";

const wss = new WebSocket("wss://58b7a26b7325.ngrok.app/ws?client_id=12345");
const clients: Record<string, Object> = {};

interface Emotion {
    emotion: string;
    score: number;
}

// received via the display_user_message event
interface user_message {
    transcript: string;
    audio_emotions: Emotion[];
}

// received via the display_assistant_message event
interface assistant_message {
    content: string;
}

// received via the display_video_message event
interface video_emotions {
    emotions: Emotion[];
}

// received via the display_video event
interface video {
    data: string; // base64
}

interface Message
    extends user_message,
        assistant_message,
        video_emotions,
        video {}

interface ChatBubble {
    role: "user" | "assistant";
    message: string;
}

const Page = () => {
    const [connected, setConnected] = useState(false);
    const [videoImage, setVideoImage] = useState<string | undefined>();
    const [conversation, setConversation] = useState<ChatBubble[]>([]);
    const [emotions, setEmotions] = useState<Emotion[]>();

    const ref = useRef<HTMLDivElement>(null);
    useEffect(() => {
        const scrollIntoViewInterval = () => {
            if (ref.current) {
                ref.current.scrollIntoView({
                    behavior: "smooth",
                    block: "end",
                    inline: "nearest",
                });
            }
        };

        scrollIntoViewInterval();

        return () => scrollIntoViewInterval();
    }, [conversation]);

    useEffect(() => {
        wss.onopen = () => {
            console.log("WebSocket connection established");
            setConnected(true);

            wss.onmessage = (event: MessageEvent) => {
                console.log("Received message");
                const message = JSON.parse(event.data) as Message;
                console.log(message);

                if (message["data"]) {
                    console.log("Got video image");
                    setVideoImage(message["data"]);
                } else if (message["transcript"]) {
                    console.log("Got user message");
                    setConversation((prev) => [
                        ...prev,
                        { role: "user", message: message["transcript"] },
                    ]);
                } else if (message["content"]) {
                    console.log("Got assistant message");
                    setConversation((prev) => [
                        ...prev,
                        { role: "assistant", message: message["content"] },
                    ]);
                } else if (message["emotions"]) {
                    console.log("Got video emotions");
                    setEmotions(message["emotions"]);
                } else {
                    console.warn("Received unknown message");
                }
            };

            wss.onclose = () => {
                console.log("Closing websocket");
                setConnected(false);
            };
        };
    }, []);

    return (
        <div className="h-[calc(100vh-2rem)] max-h-[calc(100vh-2rem)] overflow-hidden rounded-3xl bg-white p-12">
            <div className="space-y-2">
                <div className="flex flex-row items-center space-x-4">
                    <h1 className="text-5xl font-bold">
                        Welcome back, Jasmine
                    </h1>
                    <div
                        className={cn(
                            "rounded-full p-3",
                            connected ? "bg-green-500" : "bg-red-500",
                        )}
                    />
                </div>
                <h2 className="text-2xl font-semibold text-[#808080]">
                    You have 2 stories waiting for you!
                </h2>
            </div>

            <div className="flex flex-row space-x-12 pt-8">
                <div className="max-h-fit w-full space-y-4">
                    <div className="h-[550px] w-full rounded-xl bg-gray-200/40">
                        {videoImage ? (
                            <img
                                src={`data:image/[extension];base64,${videoImage}`}
                                className="h-full w-full object-contain"
                                datatype="base64"
                            />
                        ) : null}
                    </div>

                    <div className="grid grid-cols-2 gap-x-4">
                        <div className="space-y-1 rounded-xl border-4 border-jas-outline p-4">
                            <div className="flex-between w-full">
                                <p className="text-sm font-semibold">
                                    {emotions
                                        ? emotions[0]?.emotion
                                        : "emotion 1"}
                                </p>
                                <p className="text-sm font-semibold opacity-40">
                                    {emotions
                                        ? (emotions[0]?.score * 100).toFixed(0)
                                        : "x"}
                                    %
                                </p>
                            </div>
                            <Progress
                                value={emotions ? emotions[0].score * 100 : 25}
                                className="h-6 bg-[#E5E5E5]"
                                //@ts-expect-error trust me bro
                                jasBackground={"bg-jas-pink"}
                            />
                        </div>
                        <div className="space-y-1 rounded-xl border-4 border-jas-outline p-4">
                            <div className="flex-between w-full">
                                <p className="text-sm font-semibold">
                                    {emotions
                                        ? emotions[1]?.emotion
                                        : "emotion 2"}
                                </p>
                                <p className="text-sm font-semibold opacity-40">
                                    {emotions
                                        ? (emotions[1]?.score * 100).toFixed(0)
                                        : "x"}
                                    %
                                </p>
                            </div>
                            <Progress
                                value={emotions ? emotions[1].score * 100 : 25}
                                className="h-6 bg-[#E5E5E5]"
                                //@ts-expect-error trust me bro
                                jasBackground={"bg-jas-purple"}
                            />
                        </div>
                    </div>
                </div>

                <div className="w-[400px] min-w-[400px] space-y-4">
                    <div className="max-h-[600px] w-full space-y-6 overflow-auto rounded-xl border-[6px] border-jas-outline bg-white p-6">
                        <div className="text-3xl font-bold tracking-tight">
                            Live storytime
                        </div>

                        <div className="h-[475px] min-h-[475px]">
                            <div className="space-y-4 pb-4" ref={ref}>
                                {conversation.map((item) => (
                                    <div className="space-y-2 rounded-xl bg-jas-card p-4">
                                        <div className="flex items-center space-x-2">
                                            {item.role === "user" ? (
                                                <>
                                                    <img src="/dobby.png" />
                                                    <p className="text-xl font-bold tracking-wide">
                                                        User
                                                    </p>
                                                </>
                                            ) : (
                                                <>
                                                    <img src="/doggo.png" />
                                                    <p className="text-xl font-bold tracking-wide">
                                                        Doggo
                                                    </p>
                                                </>
                                            )}
                                        </div>
                                        <p className="text-lg text-[#3e3e3e]">
                                            {item.message}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="flex-center space-x-4">
                        <Button className="space-x-2 rounded-full bg-gray-600 drop-shadow-lg hover:bg-gray-600/80">
                            <Pause />
                            <p className="text-xl">Pause</p>
                        </Button>
                        <Button className="space-x-2 rounded-full bg-jas-blue drop-shadow-lg hover:bg-jas-blue/80">
                            <StopCircle />
                            <p className="text-xl">End Session</p>
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Page;
