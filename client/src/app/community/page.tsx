import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import {
    BookCopy,
    BookMarked,
    Box,
    CreditCard,
    Dog,
    Gift,
    Pencil,
    Plus,
    Search,
    TreeDeciduous,
} from "lucide-react";

const TOPICS = [
    {
        id: 1,
        icon: BookCopy,
        title: "all",
    },
    {
        id: 2,
        icon: Dog,
        title: "animals",
    },
    {
        id: 3,
        icon: TreeDeciduous,
        title: "places",
    },
    {
        id: 4,
        icon: Pencil,
        title: "things",
    },
];

const GIFTS = [
    {
        title: "Send a gift",
        description: "send a surprise gift to a random hospital patient!",
        background: "bg-jas-pink",
        icon: Gift,
    },
    {
        title: "Donate care package",
        description: "fund a gift for a stranger!",
        background: "bg-jas-purple",
        icon: Box,
    },
    {
        title: "Write a card",
        description: "Send a get well card to a hospital patient!",
        background: "bg-jas-green",
        icon: CreditCard,
    },
];

const VIDEOS = [
    {
        id: 1,
        title: "Cultivating the farm",
        tags: ["farming"],
    },
    {
        id: 2,
        title: "Cultivating the farm",
        tags: ["farming"],
    },
    {
        id: 3,
        title: "Cultivating the farm",
        tags: ["farming"],
    },
    {
        id: 4,
        title: "Cultivating the farm",
        tags: ["farming", "farming"],
    },
    {
        id: 5,
        title: "Cultivating the farm",
        tags: ["farming", "farming"],
    },
    {
        id: 6,
        title: "Cultivating the farm",
        tags: ["farming"],
    },
];

const Page = () => {
    return (
        <div className="h-[calc(100vh-2rem)] max-h-[calc(100vh-2rem)] overflow-auto rounded-3xl bg-white p-12">
            <div className="space-y-2">
                <h1 className="text-5xl font-bold">Find a story</h1>
            </div>

            <div className="flex flex-row space-x-12 pt-8">
                <div className="max-h-fit w-full space-y-12">
                    <div className="space-y-8">
                        <div className="relative">
                            <Search className="absolute left-4 top-1/2 w-5 -translate-y-1/2 transform" />
                            <Input
                                className="border-jas-outline h-12 rounded-full border-4 bg-white pl-10"
                                placeholder="search"
                            />
                        </div>

                        <div className="border-jas-outline space-y-4 rounded-xl border-4 bg-white p-6">
                            <p className="text-2xl font-bold">Select a topic</p>
                            <div className="flex flex-row space-x-4 overflow-auto">
                                {TOPICS.map((topic) => (
                                    <div
                                        className="flex-center hover:bg-jas-card hover:border-jas-blue group h-40 w-32 min-w-32 cursor-pointer flex-col space-y-2 rounded-xl hover:border-4"
                                        key={topic.id}
                                    >
                                        <div className="flex-center group-hover:bg-jas-blue h-24 w-24 rounded-xl bg-[#3F3F3F]">
                                            <topic.icon className="h-12 w-12 text-white group-hover:text-white" />
                                        </div>
                                        <p className="text-xl font-semibold">
                                            {topic.title}
                                        </p>
                                    </div>
                                ))}
                                <div className="flex-center group group h-40 w-32 min-w-32 cursor-pointer flex-col space-y-2 rounded-xl">
                                    <div className="flex-center group-hover:bg-jas-gray/10 h-24 w-24 rounded-xl border-[6px] border-dotted border-[#868686] bg-clip-padding">
                                        <Plus className="h-12 w-12 text-[#868686]" />
                                    </div>
                                    <p className="text-xl font-semibold">
                                        See more...
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="grid grid-cols-3 gap-x-8 gap-y-8">
                        {VIDEOS.map((video) => (
                            <div className="relative rounded-xl border-2 border-gray-200 bg-white p-4">
                                <div className="absolute -top-[8%] left-[50%] h-8 w-32 -translate-x-1/2 transform bg-gray-300" />
                                <div className="w-74 flex-center h-40 max-h-40 bg-gray-200">
                                    video
                                </div>

                                <div className="space-y-2 text-center">
                                    <h4 className="mt-4 text-xl font-bold text-black">
                                        {video.title}
                                    </h4>
                                    <div className="flex-center mx-auto flex-row space-x-2">
                                        {video.tags.map((tag) => (
                                            <p className="w-fit rounded-full bg-gray-200 px-2 py-1 text-sm font-medium leading-relaxed tracking-wide text-zinc-800">
                                                {tag}
                                            </p>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="w-[450px] min-w-[450px] space-y-4">
                    <div className="border-jas-outline max-w-[85%] space-y-6 rounded-xl border-4 bg-white p-6">
                        <div className="space-y-3">
                            <div className="bg-jas-outline text-jas-gray flex-center w-fit space-x-2 rounded-full px-3 py-2 font-semibold">
                                <BookMarked className="h-4 w-4" />
                                <p>Learning style</p>
                            </div>
                            <div className="space-y-3">
                                <p className="text-3xl font-bold">
                                    Your story tokens
                                </p>
                                <p className="text-[#7b7b7b]">
                                    Story tokens are used to measure the impact
                                    of your stories in your communities!
                                </p>
                            </div>
                        </div>

                        <div className="border-jas-outline space-y-2 rounded-xl border-[3px] bg-white p-4">
                            <div className="flex items-center space-x-1 text-4xl font-bold">
                                <img src="/token.svg" />
                                <p>562 tokens</p>
                            </div>
                            <p className="leading-snug text-[#7b7b7b]">
                                24 stories made. 251 people impacted
                            </p>
                        </div>
                    </div>

                    <div className="border-jas-outline max-w-[85%] space-y-6 rounded-xl border-4 bg-white p-6">
                        <div className="space-y-3">
                            <div className="bg-jas-outline text-jas-gray flex-center w-fit space-x-2 rounded-full px-3 py-2 font-semibold">
                                <BookMarked className="h-4 w-4" />
                                <p>Social Impact</p>
                            </div>
                            <div className="space-y-3">
                                <p className="text-3xl font-bold">
                                    Send Kindness
                                </p>
                                <p className="text-[#7b7b7b]">
                                    Use your tokens to propel change and create
                                    a random act of kindness!
                                </p>
                            </div>
                        </div>

                        <div className="flex flex-col space-y-4">
                            {GIFTS.map((item) => (
                                <div className="border-jas-outline flex flex-row items-center space-x-4 rounded-xl border-[3px] bg-white p-4">
                                    <div
                                        className={cn(
                                            "flex-center h-20 w-20 min-w-20 rounded-xl bg-gray-400 text-white",
                                            item.background,
                                        )}
                                    >
                                        <item.icon className="h-10 w-10" />
                                    </div>
                                    <div className="space-y-1 text-sm">
                                        <p className="text-2xl font-bold">
                                            {item.title}
                                        </p>
                                        <p className="leading-snug text-[#7b7b7b]">
                                            {item.description}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Page;
