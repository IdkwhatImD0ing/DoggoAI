import { Input } from "@/components/ui/input";
import {
    BookCopy,
    Dog,
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
    {
        id: 5,
        icon: Pencil,
        title: "things",
    },
];

const GIFTS = [
    {
        title: "Send a gift",
        description: "send a surprise gift to a random hospital patient!",
    },
    {
        title: "Donate care package",
        description: "fund a gift for a stranger!",
    },
    {
        title: "Write a card",
        description: "Send a get well card to a hospital patient!",
    },
];

const Page = () => {
    return (
        <div className="w-full overflow-auto pl-16 pr-8 pt-10">
            <div className="space-y-2">
                <h1 className="text-5xl font-bold">
                    Find your favorite stories!
                </h1>
            </div>

            <div className="flex flex-row space-x-12 pt-8">
                <div className="max-h-fit w-full space-y-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 w-5 -translate-y-1/2 transform" />
                        <Input
                            className="h-12 rounded-full bg-gray-200 pl-10"
                            placeholder="search"
                        />
                    </div>

                    <div className="space-y-4 rounded-xl bg-gray-200 p-6">
                        <p className="text-2xl font-bold">Select a topic</p>

                        <div className="flex flex-row space-x-4 overflow-auto">
                            {TOPICS.map((topic) => (
                                <div
                                    className="flex-center group h-40 w-32 min-w-32 flex-col space-y-2 rounded-xl bg-gray-300 hover:bg-gray-400"
                                    key={topic.id}
                                >
                                    <div className="flex-center h-24 w-24 rounded-xl bg-gray-400 group-hover:bg-gray-900">
                                        <topic.icon className="h-12 w-12 group-hover:text-white" />
                                    </div>
                                    <p className="text-xl font-bold">
                                        {topic.title}
                                    </p>
                                </div>
                            ))}
                            <div className="flex-center group h-40 w-32 min-w-32 flex-col space-y-2 rounded-xl bg-gray-300 hover:bg-gray-400">
                                <div className="flex-center h-24 w-24 rounded-xl border-4 border-dotted">
                                    <Plus className="h-12 w-12 group-hover:text-white" />
                                </div>
                                <p className="text-xl font-bold">See more...</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="w-[450px] min-w-[450px] space-y-4">
                    <div className="max-w-[85%] space-y-6 rounded-xl bg-gray-100 p-6">
                        <div className="space-y-3">
                            <div className="w-fit rounded-full bg-gray-200 px-3 py-1">
                                Your impact
                            </div>
                            <div className="space-y-3">
                                <p className="text-3xl font-bold">
                                    Your story tokens
                                </p>
                                <p>
                                    Story tokens are used to measure the impact
                                    of your stories in your communities!
                                </p>
                            </div>
                        </div>

                        <div className="space-y-2 rounded-xl bg-white p-4">
                            <p className="text-4xl font-bold">562 tokens</p>
                            <p>24 stories made. 251 people impacted</p>
                        </div>
                    </div>

                    <div className="max-w-[85%] space-y-6 rounded-xl bg-gray-100 p-6">
                        <div className="space-y-2">
                            <div className="w-fit rounded-full bg-gray-200 px-3 py-1">
                                Social impact
                            </div>
                            <div className="space-y-1">
                                <p className="text-3xl font-bold">
                                    Send Kindness
                                </p>
                                <p>
                                    Use your tokens to propel change and create
                                    a random act of kindness!
                                </p>
                            </div>
                        </div>

                        <div className="flex flex-col space-y-4">
                            {GIFTS.map((item) => (
                                <div className="flex flex-row space-x-4 rounded-xl bg-white p-4">
                                    <div className="h-20 w-20 min-w-20 rounded-xl bg-gray-400">
                                        <img className="object-cover" />
                                    </div>
                                    <div className="space-y-1">
                                        <p className="text-2xl font-bold">
                                            {item.title}
                                        </p>
                                        <p className="leading-snug">
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
