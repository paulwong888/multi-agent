import gradio as gr
import random
import time


def chat_not_stream():
    with gr.Blocks() as demo:
        # 聊天机器人组件（使用消息格式）
        chatbot = gr.Chatbot(type="messages")
        
        # 用户输入文本框（带中文提示）
        msg = gr.Textbox(placeholder="请输入您的消息...")
        
        # 清空按钮（中文本）
        clear = gr.ClearButton([msg, chatbot], value="清空聊天")

        def respond(message, chat_history):
            """处理用户输入并生成机器人响应"""
            # 随机选择中文回复
            bot_messages = [
                "您好，今天感觉怎么样？",
                "真是个美好的晴天！",
                "要不要一起讨论人工智能？",
                "我刚刚学习了新的知识",
                "您最近在读什么书吗？"
            ]
            bot_message = random.choice(bot_messages)
            
            # 添加用户消息到聊天记录
            chat_history.append({"role": "user", "content": message})
            
            # 添加AI回复到聊天记录
            chat_history.append({"role": "assistant", "content": bot_message})
            
            # 模拟响应延迟
            time.sleep(1.5)
            
            return "", chat_history  # 清空输入框并更新聊天记录

        # 绑定提交事件：用户按回车时触发
        msg.submit(
            fn=respond,
            inputs=[msg, chatbot],  #msg：用户输入文本框的内容（用户发送的消息）
                                    #chatbot：当前聊天记录（包含历史消息的列表）

            outputs=[msg, chatbot]  #在 Gradio 中，outputs=[msg, chatbot] 指定了函数执行后需要更新的界面组件。这里表示：
                                    # msg：清空用户输入文本框（设为空字符串 ""）
                                    # chatbot：更新聊天机器人显示内容（传入新的 chat_history 列表）    
        )
        demo.launch(server_name="0.0.0.0") 

def chat_with_stream():
    with gr.Blocks(theme="soft") as demo:
        chatbot = gr.Chatbot(height=400, type="messages")
        with gr.Row():
            msg = gr.Textbox(scale=7)
            submit = gr.Button("Send", scale=1)
        clear = gr.Button("Clear History")
        stop = gr.Button("Stop Generation")

        def user(user_message, history):
            return "", history + [{"role": "user", "content": user_message}]

        def bot(history):
            bot_message = random.choice(["*Hello*! How can I help?", 
                                    "**Interesting**! Tell me more...",
                                    "I'm thinking... 🤔"])
            history.append({"role": "assistant", "content": ""})  # 先添加空消息
            for character in bot_message:
                history[-1]['content'] += character  # 逐字填充最后一条消息
                time.sleep(0.05)  # 模拟流式延迟
                yield history  # 持续生成中间结果

        def stop_gen():
            raise gr.Stop()

        msg.submit(user, [msg, chatbot], [msg, chatbot]).then(bot, chatbot, chatbot)
        submit.click(user, [msg, chatbot], [msg, chatbot]).then(bot, chatbot, chatbot)
        clear.click(lambda: [], None, chatbot)
        stop.click(stop_gen)

    demo.queue().launch(server_name="0.0.0.0")

if __name__ == "__main__":
    # chat_not_stream()
    chat_with_stream()