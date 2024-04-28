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
    def __init__(self, socket, loop, video_emotions, server_socket):
        self.socket = socket
        self.server_socket = server_socket
        self.loop = loop
        self.bbox = {"x": 0, "y": 0, "w": 0, "h": 0}
        self.prob = 0.0
        self.video_emotions = video_emotions

    def start_process(self):
        self.thread = threading.Thread(target=self.process_video)
        self.thread.start()

    def stop_process(self):
        self.thread.join()
        self.thread2.join()

    def process_video(self):
        cap = cv2.VideoCapture(0)
        prev_time = 0
        interval = 1
        if not cap.isOpened():
            print("Cannot open camera")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            if time.time() - prev_time > interval:
                prev_time = time.time()
                asyncio.run_coroutine_threadsafe(self.process_hume(frame), self.loop)

            # NOTE: Debug Purposes
            # Write bbox, prob, and emotions to the image
            x, y, w, h = (
                int(self.bbox["x"]),
                int(self.bbox["y"]),
                int(self.bbox["w"]),
                int(self.bbox["h"]),
            )
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"Prob: {self.prob:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2,
            )
            for i, emotion in enumerate(self.video_emotions):
                if emotion:
                    text = f"{emotion['emotion']}: {emotion['score']:.2f}"
                    cv2.putText(
                        frame,
                        text,
                        (10, 30 * (i + 1)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (255, 255, 255),
                        2,
                    )

            # Convert frame to base64 image, and also send to server
            frame_base64 = base64.b64encode(cv2.imencode(".jpg", frame)[1]).decode()
            data = {
                "event": "video",
                "data": frame_base64,
            }
            asyncio.run_coroutine_threadsafe(
                self.server_socket.send(json.dumps(data)), self.loop
            )

    async def process_hume(self, frame):
        try:
            frame_base64 = base64.b64encode(cv2.imencode(".jpg", frame)[1]).decode()
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

                await self.server_socket.send(
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
