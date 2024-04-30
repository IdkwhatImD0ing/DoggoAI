import cv2
import time
import asyncio
import os
import base64
import websockets
import threading
import json
import queue
import dotenv

dotenv.load_dotenv()


class HumeVideoFeed:
    def __init__(self, socket, loop, video_emotions, send_data, images):
        self.socket = socket
        self.send_data = send_data
        self.images = images
        self.loop = loop
        self.bbox = {"x": 0, "y": 0, "w": 0, "h": 0}
        self.prob = 0.0
        self.video_emotions = video_emotions
        self.count = 0

    def start_process(self):
        self.thread = threading.Thread(target=self.process_video)
        self.thread.start()

    def stop_process(self):
        self.thread.join()

    def process_video(self):
        cap = cv2.VideoCapture(0)
        prev_time = 0
        interval = 1
        if not cap.isOpened():
            print("Cannot open camera")
            return
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break

                if time.time() - prev_time > interval:
                    # Save the frame to an image
                    prev_time = time.time()

                    frame_base64 = base64.b64encode(
                        cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])[1]
                    ).decode()

                    asyncio.run_coroutine_threadsafe(
                        self.process_hume(frame_base64), self.loop
                    )

                    # NOTE: Debug Purposes
                    # Write bbox, prob, and emotions to the image
                    x, y, w, h = (
                        int(self.bbox["x"]),
                        int(self.bbox["y"]),
                        int(self.bbox["w"]),
                        int(self.bbox["h"]),
                    )
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    frame_base64 = base64.b64encode(
                        cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])[1]
                    ).decode()

                    # Convert frame to base64 image, and also send to server
                    data = {
                        "event": "video",
                        "data": frame_base64,
                    }
                    self.images[0] = frame_base64
                    # print("HumeVideoFeed - Sent to server:", self.count)
                    self.count += 1
                    asyncio.run_coroutine_threadsafe(self.send_video(data), self.loop)

        except Exception as e:
            print("Error - HumeVideoFeed:", str(e))

    async def send_video(self, data):
        try:
            await self.send_data(json.dumps(data))
            print("HumeVideoFeed - Sent to server:", self.count)
            self.count += 1
        except Exception as e:
            print("Error - HumeVideoFeed:", str(e))

    async def process_hume(self, frame_base64):
        try:

            data = {"data": frame_base64, "models": {"face": {}}}
            await self.socket.send(json.dumps(data))
            result = await self.socket.recv()
            result = json.loads(result)
            predictions = result.get("face", {}).get("predictions", [])

            if predictions:
                prediction = predictions[0]
                last_bbox = prediction["bbox"]
                last_prob = prediction["prob"]
                last_emotions = sorted(
                    prediction["emotions"],
                    key=lambda e: e["score"],
                    reverse=True,
                )[:3]

                pretty_emotions = []
                for i, emotion in enumerate(last_emotions):

                    pretty_emotions.append(
                        {"emotion": emotion["name"], "score": emotion["score"]}
                    )

                self.bbox = last_bbox
                self.prob = last_prob
                self.video_emotions[0] = pretty_emotions[0]
                self.video_emotions[1] = pretty_emotions[1]
                self.video_emotions[2] = pretty_emotions[2]

                await self.send_data(
                    json.dumps(
                        {
                            "event": "video_emotions",
                            "emotions": pretty_emotions,
                        }
                    )
                )

        except Exception as e:
            print("Error - HumeVideoFeed:", str(e))


# async def main():
#     hume_server = (
#         f"wss://api.hume.ai/v0/stream/models?api_key={os.getenv('HUME_API_KEY')}"
#     )
#     socket = await websockets.connect(hume_server)
#     loop = asyncio.get_event_loop()

#     hf = HumeVideoFeed(socket, loop)
#     hf.start_process()

#     while True:
#         await asyncio.sleep(1)


# if __name__ == "__main__":
#     asyncio.run(main())
