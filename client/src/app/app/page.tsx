import { HoverBorderGradient } from "@/components/ui/hover-border-gradient";
import { Sparkles } from "lucide-react";

const Page = () => {
    return (
        <div className="w-full overflow-auto px-16 pt-10">
            <div className="space-y-2">
                <h1 className="text-5xl font-bold">Welcome back, Jasmine</h1>
                <h2 className="text-2xl font-semibold text-gray-400">
                    You have 2 stories waiting for you!
                </h2>
            </div>

            <div className="flex flex-row space-x-16 pt-8">
                {/* Contains all elements */}
                <div className="w-full">
                    {/* Contains non-statistical */}
                    <div className="flex-between h-full rounded-lg border-4 border-dashed border-gray-400 bg-gray-400 bg-clip-padding p-6">
                        <div className="flex h-full flex-col justify-between pt-4">
                            <h3 className="text-4xl font-bold">
                                Create a new story!
                            </h3>

                            <HoverBorderGradient
                                className="flex-center w-60 space-x-2 py-4 text-2xl "
                                duration={0.1}
                            >
                                <Sparkles /> <p>make magic</p>
                            </HoverBorderGradient>
                        </div>
                        <img src="/bear.svg" />
                    </div>
                </div>

                <div className="w-[400px]">{/*Contains statistical */}</div>
            </div>
        </div>
    );
};

export default Page;
