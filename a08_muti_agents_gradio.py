import json, requests
import gradio as gr
from a00_01_prompt import *
from openai.resources.chat.chat import AsyncChat
from core import completions
from autogen_ext.models.openai._openai_client import create_kwargs

from a06_group_manager import predict
# from a07_graphflow_manager import predict

[create_kwargs.add(x) for x in ("extra_body",)]


AsyncChat.completions = completions

def create_gradio_app():
    # 统一测试消息格式（修复重复赋值问题）
    # 预测 2025 05-01 03:00 欧冠 巴萨 VS 国际米兰

    # test_message = user_prompt_5
    # test_message = "基于以下信息, 预测比赛结果\n " + user_prompt_4
    # test_message = "基于以下信息, 预测比赛结果\n " + user_prompt_3
    # test_message = "基于以下信息, 预测比赛结果\n " + user_prompt_2
    test_message = "预测 05-24 22:00 谢菲联 VS 桑德兰 比赛结果"
    # test_message = "基于以下信息, 预测比赛结果\n " + user_prompt_0
    
    # test_message = """
    # 预测 2025/5/10 22:00 狼队 vs 布莱顿 比赛结果
    # """.strip()

    with gr.Blocks(theme="soft") as demo:
        # 使用更专业的组件布局
        gr.Markdown("## 🏆 足球赛事预测 - Present By EachGpame")
        with gr.Row():
            chatbot = gr.Chatbot(elem_id="chatbot", label="预测过程", type="messages", height=600)
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
                return user_message, history + [{"role": "user", "content": user_message}]
        
        # 使用更现代的交互模式
        # user_message = msg.value
        msg.submit(user, [msg, chatbot], [msg, chatbot]).then(predict, [msg, chatbot], chatbot)
        submit.click(user, [msg, chatbot], [msg, chatbot]).then(predict, [msg, chatbot], chatbot)
        # clear.click(lambda: [], None, chatbot)
        # submit.click(
        #     predict, 
        #     inputs=msg,
        #     outputs=chatbot,
        #     queue=True
        # )
        # msg.submit(
        #     predict, 
        #     inputs=msg, 
        #     outputs=chatbot,
        #     queue=True
        # )
    return demo

def main():
    app = create_gradio_app()
    # 优化服务器配置
    app.queue(
        max_size=20,
        default_concurrency_limit=10
    ).launch(
        server_name="0.0.0.0",
        server_port=6006,
        share=False
    )

    """
    需提供两队数据
    1. 两队近5场赛事胜负/得失球/控球率数据 
    2. 伤病与停赛名单 
    3. 历史交锋记录 
    4. 主客场表现差异 
    5. 战术阵型变化 
    6. 天气与场地状况。

    如:
    预测2024年5月12日英超第37轮曼城vs阿森纳：
    1. 主队德布劳内复出后场均关键传球提升40% 
    2. 客队赖斯累计黄牌停赛 
    3. 近3次交锋场均产生4.3球 
    4. 曼城本赛季主场胜率91% 
    5. 比赛当日曼彻斯特预报有中雨。
    请给出战术克制关系分析和加布里埃尔vs哈兰德的头球争顶成功率预测。
    """

if __name__ == "__main__":
     main()