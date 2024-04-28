import { Pause, StopCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

const Page = () => {
    return (
        <div className="h-[calc(100vh-2rem)] max-h-[calc(100vh-2rem)] overflow-auto rounded-3xl bg-white p-12">
            <div className="space-y-2">
                <h1 className="text-5xl font-bold">Welcome back, Jasmine</h1>
                <h2 className="text-2xl font-semibold text-[#808080]">
                    You have 2 stories waiting for you!
                </h2>
            </div>

            <div className="flex flex-row space-x-12 pt-8">
                <div className="max-h-fit w-full space-y-4">
                    <div className="h-[600px] w-full rounded-xl bg-gray-200"></div>
                </div>

                <div className="w-[400px] min-w-[400px] space-y-4">
                    <div className="border-jas-outline max-h-[600px] w-full space-y-6 overflow-auto rounded-xl border-[6px] bg-white p-6">
                        <div className="text-3xl font-bold tracking-tight">
                            Live storytime
                        </div>

                        <div className="space-y-4">
                            <div className="bg-jas-card space-y-2 rounded-xl p-4">
                                <div className="flex items-center space-x-2">
                                    <img src="/doggo.png" />
                                    <p className="text-xl font-bold tracking-wide">
                                        Doggo
                                    </p>
                                </div>
                                <p className="text-lg text-[#3e3e3e]">
                                    Hey there! How was your day so far?
                                </p>
                            </div>
                            <div className="bg-jas-card space-y-2 rounded-xl p-4">
                                <div className="flex items-center space-x-2">
                                    <img src="/doggo.png" />
                                    <p className="text-xl font-bold tracking-wide">
                                        Doggo
                                    </p>
                                </div>
                                <p className="text-lg text-[#3e3e3e]">
                                    Hey there! How was your day so far?
                                </p>
                            </div>
                            <div className="bg-jas-card space-y-2 rounded-xl p-4">
                                <div className="flex items-center space-x-2">
                                    <img src="/doggo.png" />
                                    <p className="text-xl font-bold tracking-wide">
                                        Doggo
                                    </p>
                                </div>
                                <p className="text-lg text-[#3e3e3e]">
                                    Hey there! How was your day so far?
                                </p>
                            </div>
                            <div className="bg-jas-card space-y-2 rounded-xl p-4">
                                <div className="flex items-center space-x-2">
                                    <img src="/doggo.png" />
                                    <p className="text-xl font-bold tracking-wide">
                                        Doggo
                                    </p>
                                </div>
                                <p className="text-lg text-[#3e3e3e]">
                                    Hey there! How was your day so far?
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="flex-center space-x-4">
                        <Button className="space-x-2 rounded-full bg-gray-600 drop-shadow-lg hover:bg-gray-600/80">
                            <Pause />
                            <p className="text-xl">Pause</p>
                        </Button>
                        <Button className="bg-jas-blue hover:bg-jas-blue/80 space-x-2 rounded-full drop-shadow-lg">
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
