from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import gradio as gr
from openai.resources.chat.chat import AsyncChat
from core import completions
from autogen_ext.models.openai._openai_client import create_kwargs

from a08_muti_agents_gradio import create_gradio_app
from fastapi.middleware.cors import CORSMiddleware
import json

# from a06_group_manager import predict
from a07_graphflow_manager import predict

# [create_kwargs.add(x) for x in ("extra_body",)]


# AsyncChat.completions = completions
app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载Gradio应用到FastAPI
gradio_app = create_gradio_app()
app = gr.mount_gradio_app(app, gradio_app, path="/gradio")

# API端点
@app.post("/api/predict")
async def prediction_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")
    chat_history = data.get("history", [])

    async def event_stream():
        full_history = chat_history.copy()
        full_history.append({"role": "user", "content": message})
        
        async for updated_history in predict(message, full_history):
            last_msg = updated_history[-1]
            if last_msg["role"] == "assistant":
                yield f"data: {json.dumps(last_msg)}\n\n"
                
    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6006)