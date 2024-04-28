import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import {
    ArrowRight,
    BookCopy,
    BookMarked,
    Bookmark,
    Box,
    CreditCard,
    Dog,
    Gift,
    Heart,
    Pencil,
    Play,
    Plus,
    Search,
    TreeDeciduous,
} from "lucide-react";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

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
        title: "Frogs on lilypads",
        author: "Dobby the elf, age 4",
        background: "bg-jas-pink",
        image: "/frog.png",
    },
    {
        id: 2,
        title: "Duck duck goose",
        author: "Severus Snape, age 5",
        background: "bg-jas-green",
        image: "/goose.png",
    },
    {
        id: 3,
        title: "Bread and butter",
        author: "Ron Weasly, age 3",
        background: "bg-jas-purple",
        image: "/bread.png",
    },
    {
        id: 4,
        title: "Cows in the field",
        author: "Harry Potter, age 6",
        background: "bg-jas-purple",
        image: "/cow.png",
    },
    {
        id: 5,
        title: "Riding horses",
        author: "Albus Dumbledore, age 7",
        background: "bg-jas-blue",
        image: "/horse.png",
    },
    {
        id: 6,
        title: "Bunnies in the barn",
        author: "Lily Potter, age 4",
        background: "bg-jas-pink",
        image: "/bunny.png",
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

                    <div className="grid grid-cols-3 gap-x-8 gap-y-12">
                        {VIDEOS.map((video, index) => (
                            <Dialog>
                                <DialogTrigger>
                                    <div className="relative rounded-xl border-2 border-gray-200 bg-white p-4">
                                        <div
                                            className={cn(
                                                "absolute -top-[8%] left-[50%] h-8 w-32 -translate-x-1/2 transform",
                                                index % 3 == 0
                                                    ? "bg-jas-pink/30"
                                                    : index % 3 == 1
                                                      ? "bg-jas-green/30"
                                                      : "bg-jas-blue/30",
                                            )}
                                        />
                                        <div
                                            className={cn(
                                                "w-74 flex-center relative h-40 max-h-40 rounded-xl",
                                                video.background,
                                            )}
                                        >
                                            <img
                                                src={video.image}
                                                className="absolute bottom-0 h-[90%]"
                                            />
                                        </div>

                                        <div className="text-center">
                                            <h4 className="mt-4 text-xl font-bold text-black">
                                                {video.title}
                                            </h4>
                                            <div className="flex-center mx-auto flex-row space-x-2">
                                                <p className="w-fit rounded-full px-2 py-1 text-sm font-medium leading-relaxed tracking-wide text-[#7b7b7b]">
                                                    {video.author}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </DialogTrigger>
                                <DialogContent>
                                    <DialogHeader>
                                        <DialogTitle className="mx-auto space-y-4 pt-8 text-center">
                                            <p className="text-3xl">
                                                Cultivating the farm
                                            </p>
                                            <div className="flex-center mx-auto gap-2">
                                                <p className="w-fit rounded-full bg-[#EAEAEA] px-2 py-1 text-sm font-medium leading-relaxed tracking-wide text-[#393939]">
                                                    farming
                                                </p>
                                                <p className="w-fit rounded-full bg-[#EAEAEA] px-2 py-1 text-sm font-medium leading-relaxed tracking-wide text-[#393939]">
                                                    cultivation
                                                </p>
                                            </div>

                                            <p className="text-base font-medium text-[#7b7b7b]">
                                                A story about resilience and
                                                inspiration as a person
                                                cultivates his own garden
                                            </p>
                                        </DialogTitle>
                                        <DialogDescription>
                                            <div className="border-jas-outline flex-between my-4 rounded-xl border-4 bg-white p-4">
                                                <div className="flex items-center space-x-2">
                                                    <img src="/dobby.png" />
                                                    <div>
                                                        <p className="font-semibold">
                                                            author
                                                        </p>
                                                        <p className="text-jas-gray text-xl font-bold">
                                                            Dobby the Elf
                                                        </p>
                                                    </div>
                                                </div>
                                                <div className="bg-jas-outline w-fit rounded-xl p-3">
                                                    <ArrowRight />
                                                </div>
                                            </div>

                                            <div>
                                                <img
                                                    src="/fish.png"
                                                    className="w-full"
                                                />
                                            </div>

                                            <div className="flex-between flex items-center px-8 py-4">
                                                <div className="rounded-full border-[3px] border-[#c2c2c2] p-3">
                                                    <Heart className="fill-black text-black" />
                                                </div>
                                                <div>
                                                    <Button className="bg-jas-blue hover:bg-jas-blue/80 h-full space-x-2 rounded-full px-12 py-3">
                                                        <Play className="fill-white" />
                                                        <p className="text-xl">
                                                            Play Story
                                                        </p>
                                                    </Button>
                                                </div>
                                                <div className="rounded-full border-[3px] border-[#c2c2c2] p-3">
                                                    <Bookmark className="fill-black text-black" />
                                                </div>
                                            </div>
                                        </DialogDescription>
                                    </DialogHeader>
                                </DialogContent>
                            </Dialog>
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
