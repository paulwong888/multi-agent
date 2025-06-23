import time
from a00_constant import *
# from a01_muti_agents import get_participants
from a03_muti_agents import get_participants
# from a03_muti_agents import get_participants
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination

model_client = get_model_client_deepseek()

async def predict(message: str, chat_history):
    termination = TextMentionTermination("TERMINATE")
    group_chat_robin = RoundRobinGroupChat(
        get_participants(),
        termination_condition=termination
    )
    group_chat_selector = SelectorGroupChat(
        get_participants(),
        model_client=model_client,
        termination_condition=termination
    )
    
    print(f"=====> {message}")
    group_chat = group_chat_robin
    # group_chat = group_chat_selector
    stream = group_chat.run_stream(task=message)
    
    chat_history.append({"role": "assistant", "content": ""})  # 先添加空消息

    current_source = None
    i = 0
    async for chunk in stream:
        if hasattr(chunk, 'content'):
            if i == 0:
                current_source = chunk.source
                print(f"i == 0, role: {chunk.source}")
            elif chunk.source != current_source:
                print(f"role: {chunk.source}")
                chat_history.append({"role": "assistant", "content": "## " + chunk.source + "\n\n\n" +chunk.content})
                i += i
                current_source = chunk.source
                yield chat_history  # 持续生成中间结果
                continue

            chat_history[-1]['content'] += chunk.content  # 逐字填充最后一条消息
            time.sleep(0.05)  # 模拟流式延迟
            i = i + 1
            yield chat_history  # 持续生成中间结果