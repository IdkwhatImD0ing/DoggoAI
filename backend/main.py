from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
from socket_manager import ConnectionManager

app = FastAPI()

origins = ["*"]

manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: Optional[str] = None):
    if client_id is None:
        client_id = websocket.query_params.get("client_id")

    if client_id is None:
        await websocket.close(code=4001)
        return
    # save this client into server memory
    await manager.connect(websocket, client_id)  
    try:
        while True:
            data = await websocket.receive_json()
            event = data["event"]
            print(f"Event: {event}")
            if event == "user":
                message = {event: "display_user_message", "transcript": data["transcript"], "audio_emotions": data["audio_emotions"]}
                await manager.broadcast(message)
            elif event == "assistant":
                message = {event: "display_assistant_message", "content": data["content"]}
                await manager.broadcast(message)
            elif event == "video_emotions":
                message = {event: "display_video_emotions", "emotions": data["emotions"]}
                await manager.broadcast(message)
            elif event == "video":
                message = {event: "display_video", "data": data["data"]}
                await manager.broadcast(message)
    except WebSocketDisconnect:
        print("Disconnecting...")
        await manager.disconnect(client_id)


if __name__ == "__main__":
    # uvicorn main:app --reload
    # ws://localhost:8000/ws?client_id=123
    uvicorn.run(app, host="127.0.0.1", port=8000)