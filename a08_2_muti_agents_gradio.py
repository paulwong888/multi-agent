# gradio_app.py（独立Gradio前端）
import gradio as gr
import requests
import json
from a00_01_prompt import *

# 配置后端API地址
API_ENDPOINT = "http://localhost:8000/api/predict"

def create_interface():
    test_message = "基于以下信息, 预测比赛结果\n " + user_prompt_1
    
    with gr.Blocks(theme="soft") as demo:
        gr.Markdown("## 🏆 足球赛事预测 - Present By EachGame (独立界面)")
        with gr.Row():
            chatbot = gr.Chatbot(elem_id="chatbot", label="预测过程", height=600)
        with gr.Row():
            msg = gr.Textbox(
                value=test_message,
                placeholder="输入预测赛事，格式：预测 时间 联赛 主队 VS 客队",
                container=False,
                scale=7,
                max_lines=120
            )
            submit = gr.Button("分析", scale=1)
        
        def user(user_message, history):
            return "", history + [[user_message, None]]
        
        def bot(history):
            history[-1][1] = ""
            
            # 创建SSE连接
            session = requests.Session()
            response = session.post(
                API_ENDPOINT,
                json={
                    "message": history[-1][0],
                    "history": []
                },
                stream=True
            )
            
            # 处理流式响应
            buffer = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data:'):
                        data = json.loads(decoded_line[5:].strip())
                        buffer += data["content"]
                        history[-1][1] = buffer
                        yield history
            
            return history
            
        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        submit.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.queue(concurrency_count=5).launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )