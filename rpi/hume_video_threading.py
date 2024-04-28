import cv2
import time
import asyncio
from dotenv import load_dotenv
import os
import base64
import websockets
import threading
import json
import queue

load_dotenv()


async def process_frame(frame, socket):
    print("Sending data")
    try:
        frame_base64 = base64.b64encode(cv2.imencode(".jpg", frame)[1]).decode()

        data = {"data": frame_base64, "models": {"face": {}}}

        await socket.send(json.dumps(data))

        result = await socket.recv()
        result = json.loads(result)
        print(result)
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

            return last_bbox, last_prob, last_emotions
        return {"x": 0, "y": 0, "w": 0, "h": 0}, 0.0, []
    except Exception as e:
        print("Error processing frame:", str(e))
        return {"x": 0, "y": 0, "w": 0, "h": 0}, 0.0, []


def update_data(frame_queue, lock, last_bbox, last_prob, last_emotions, loop, socket):
    while True:
        frame = frame_queue.get()  # Receive frame from the queue
        print("Frame received")

        if frame is None:  # We can use None as a signal to stop the process
            print("Stopping update process")
            break

        # Run the asynchronous frame processing function
        # Get current vent loop
        print("Processing frame")
        bbox, prob, emotions = asyncio.run_coroutine_threadsafe(
            process_frame(frame, socket), loop=loop
        ).result()
        print(f"bbox: {bbox}, prob: {prob}, emotions: {emotions}")

        # Update shared variables with the results
        with lock:
            if bbox:
                last_bbox["x"] = bbox["x"]
                last_bbox["y"] = bbox["y"]
                last_bbox["w"] = bbox["w"]
                last_bbox["h"] = bbox["h"]
            last_prob = prob
            last_emotions[:] = emotions

        print(
            f"Updated bbox: {last_bbox}, prob: {last_prob}, emotions: {last_emotions}"
        )


def capture_and_display(frame_queue, lock, last_bbox, last_prob, last_emotions):
    cap = cv2.VideoCapture(0)
    prev_time = 0
    interval = 0.5
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
                prev_time = time.time()
                if frame_queue.full():
                    frame_queue.get_nowait()  # Remove the oldest item
                frame_queue.put(frame)  # Add the new frame
                print("Frame added to queue")
                # Send frame to the queue

            # Display the frame with annotations
            with lock:
                if last_bbox:
                    x, y, w, h = (
                        int(last_bbox["x"]),
                        int(last_bbox["y"]),
                        int(last_bbox["w"]),
                        int(last_bbox["h"]),
                    )
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f"Prob: {last_prob:.2f}",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 0),
                        2,
                    )

                if last_emotions:
                    for i, emotion in enumerate(last_emotions):
                        text = f"{emotion['name']}: {emotion['score']:.2f}"
                        cv2.putText(
                            frame,
                            text,
                            (10, 30 * (i + 1)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (255, 255, 255),
                            2,
                        )
                # Save as frame.jpg
                cv2.imwrite("frame.jpg", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        frame_queue.put(None)  # Signal to the update_data process to stop
        cap.release()
        cv2.destroyAllWindows()


async def main():
    lock = threading.Lock()
    frame_queue = queue.Queue(
        maxsize=1
    )  # Limit the queue size to prevent excessive memory usage
    last_bbox = {
        "x": 0,
        "y": 0,
        "w": 0,
        "h": 0,
    }
    last_prob = 0.0
    last_emotions = []

    hume_server = (
        f"wss://api.hume.ai/v0/stream/models?api_key={os.getenv('HUME_API_KEY')}"
    )

    socket = await websockets.connect(hume_server)
    loop = asyncio.get_event_loop()

    update_process = threading.Thread(
        target=update_data,
        args=(frame_queue, lock, last_bbox, last_prob, last_emotions, loop, socket),
    )
    capture_process = threading.Thread(
        target=capture_and_display,
        args=(frame_queue, lock, last_bbox, last_prob, last_emotions),
    )

    update_process.start()
    capture_process.start()

    update_process.join()
    capture_process.join()


asyncio.run(main())
