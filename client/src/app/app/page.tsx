import { HoverEffect } from "@/components/ui/card-hover-effect";
import { HoverBorderGradient } from "@/components/ui/hover-border-gradient";
import { BookMarked, Sparkles } from "lucide-react";
import { Progress } from "@/components/ui/progress";

const STORIES = [
    {
        id: 1,
        title: "Cows in the field",
        tags: ["animals", "grazing"],
        background: "bg-jas-pink",
        link: "k3v.in",
    },
    {
        id: 2,
        title: "Riding horses",
        tags: ["animals", "grazing"],
        background: "bg-jas-green",
        link: "k3v.in",
    },
    {
        id: 3,
        title: "Pigs in the barn",
        tags: ["animals", "grazing"],
        background: "bg-jas-teal",
        link: "k3v.in",
    },
];

const EMOTIONS = [
    {
        emotion: "joy",
        value: 86,
    },
    {
        emotion: "concentration",
        value: 76,
    },
    {
        emotion: "confusion",
        value: 12,
    },
];

const Page = () => {
    return (
        <div className="h-[calc(100vh-2rem)] max-h-[calc(100vh-2rem)] w-full overflow-auto rounded-3xl bg-white p-12">
            <div className="space-y-2">
                <h1 className="text-5xl font-bold">Welcome back, Jasmine</h1>
                <h2 className="text-2xl font-semibold text-[#808080]">
                    You have 2 stories waiting for you!
                </h2>
            </div>

            <div className="flex flex-row space-x-12 pt-8">
                {/* Contains all elements */}
                <div className="max-h-fit w-full space-y-4">
                    {/* Contains non-statistical */}
                    <div className="flex-between rounded-lg border-[6px] border-dashed border-[#D6D6D6] bg-[#F3F5F7] bg-clip-padding px-12">
                        <div className="my-8 flex h-full flex-col justify-between space-y-8">
                            <h3 className="text-4xl font-bold">
                                Create a story!
                            </h3>

                            <HoverBorderGradient
                                className="flex-center bg-jas-blue w-48 space-x-2 py-4 text-xl"
                                duration={0.1}
                            >
                                <Sparkles />{" "}
                                <p className="font-medium">Make magic</p>
                            </HoverBorderGradient>
                        </div>
                        <img src="/dog.svg" className="max-h-40" />
                    </div>

                    <div className="border-jas-outline space-y-2 rounded-xl border-[6px] bg-white p-6">
                        <h4 className="px-2 text-2xl font-bold">
                            Your Stories
                        </h4>
                        <HoverEffect items={STORIES} className="py-0" />
                    </div>

                    <div className="space-y-2 rounded-xl bg-gray-100 p-6">
                        <h4 className="px-2 text-2xl font-bold">Your Words</h4>
                        <HoverEffect items={STORIES} className="py-0" />
                    </div>
                </div>

                <div className="w-[400px] min-w-[400px] space-y-4">
                    <div className="border-jas-outline w-full space-y-3 rounded-xl border-[6px] bg-white p-6">
                        <div className="bg-jas-outline text-jas-gray flex-center w-fit space-x-1 rounded-full px-3 py-2 font-medium">
                            <BookMarked className="h-4 w-4" />
                            <p>Learning style</p>
                        </div>

                        <div>
                            <p className="text-jas-gray text-xl font-semibold">
                                You are a
                            </p>
                            <p className="text-3xl font-bold tracking-tight">
                                whimsical learner
                            </p>
                        </div>
                        <div>
                            <p className="text-[#7B7B7B]">
                                You are creative and love to expand on details
                                in the stories through unique twists and turns!
                            </p>
                        </div>
                        <div className="bg-jas-pink h-48 rounded-xl"></div>
                    </div>

                    <div className="border-jas-outline w-full space-y-6 rounded-xl border-[6px] bg-white p-6">
                        <div className="text-3xl font-bold tracking-tight">
                            Emotional Health
                        </div>

                        <div className="space-y-12">
                            <div className="space-y-4">
                                <p className="text-lg font-semibold">
                                    Distribution
                                </p>
                                <div className="space-y-2">
                                    {EMOTIONS.map((item, index) => (
                                        <div className="space-y-1">
                                            <div className="flex-between w-full">
                                                <p className="text-sm font-semibold">
                                                    {item.emotion}
                                                </p>
                                                <p className="text-sm font-semibold opacity-40">
                                                    {item.value}%
                                                </p>
                                            </div>
                                            <Progress
                                                value={item.value}
                                                className="h-6 bg-[#E5E5E5]"
                                                //@ts-expect-error trust me bro
                                                jasBackground={
                                                    index == 0
                                                        ? "bg-jas-pink"
                                                        : index == 1
                                                          ? "bg-jas-green"
                                                          : "bg-jas-teal"
                                                }
                                            />
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className="space-y-4">
                                <p className="text-lg font-semibold">
                                    Attention
                                </p>

                                <div className="flex-center h-[350px] rounded-xl">
                                    <img src="/chart2.png" className="pr-4" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Page;
