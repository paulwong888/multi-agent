import time
from a00_constant import *
# from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console

_, llm_config = get_config()
# model_client = get_model_client_deepseek()
model_client = get_model_client_ali()

# 数据收集智能体
data_collector = AssistantAgent(
    name="DataCollector",
    system_message="你负责从数据库和API获取历史比赛数据、实时球员状态和天气信息。输出格式为CSV或JSON。",
    model_client=model_client,
    model_client_stream=True,
    # code_execution_config=get_code_execution_config("data")
)

# 特征工程智能体
feature_engineer = AssistantAgent(
    name="FeatureEngineer",
    system_message="你负责清洗数据、提取特征（如进攻效率、防守评分），并生成训练集。使用Pandas处理数据。",
    model_client=model_client,
    model_client_stream=True,
    # code_execution_config=get_code_execution_config("features")
)

# 模型预测智能体
model_predictor = AssistantAgent(
    name="ModelPredictor",
    system_message="你使用预训练的XGBoost模型预测比赛结果，输出概率和胜负预测。",
    model_client=model_client,
    model_client_stream=True,
    # code_execution_config=get_code_execution_config("models")
)

# 协调者智能体
coordinator = AssistantAgent(
    name="Coordinator",
    system_message="你负责协调任务流程，检查各环节输出是否完整，并触发下一步操作。 如果流程完成则输出 TERMINATE",
    model_client=model_client,
    model_client_stream=True,
)
def get_participants():
    return [data_collector, feature_engineer, model_predictor, coordinator]

async def predict(message: str, chat_history):
    termination = TextMentionTermination("TERMINATE")
    group_chat = RoundRobinGroupChat(
        [data_collector, feature_engineer, model_predictor, coordinator],
        termination_condition=termination
    )
    
    print(f"=====> {message}")
    stream = group_chat.run_stream(task=message)
    
    chat_history.append({"role": "assistant", "content": ""})  # 先添加空消息

    async for chunk in stream:
        if hasattr(chunk, 'content'):
            chat_history[-1]['content'] += chunk.content  # 逐字填充最后一条消息
            time.sleep(0.05)  # 模拟流式延迟
            yield chat_history  # 持续生成中间结果



if __name__ == "__main__":
    import asyncio

    message="""
    请分析以下比赛：
    曼联 vs 切尔西
    时间：2023-10-28 19:30
    地点：老特拉福德
    天气：有雨
    """

    message="""
    请分析以下比赛：
    巴伦西亚 VS 赫塔费
    时间：2025-05-10 20:00
    地点：梅斯塔利亚
    天气：多云
    需要历史数据、实时状态和模型预测。
    """

    """
    请分析以下比赛：
    2025-05-11 03:00
    勒阿弗尔 VS 马赛
    地点：奥莎尼体育场
    天气：晴
    需要历史数据、实时状态和模型预测。
    """
    # print_stream_message()
