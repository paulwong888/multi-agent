import time
from a00_constant import *
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

model_client = get_model_client_deepseek()
ali_model_client = get_model_client_ali()

# ai_agent = AssistantAgent(
#     name="ai_agent",
#     description="搜索智能助手",
#     system_message="使用工具完成任务。",
#     tools=[web_search],
#     model_client=model_client,
#     model_client_stream=True,
# )

ai_agent = AssistantAgent(
    name="ai_agent",
    description="搜索智能助手",
    system_message="根据用户问题, 搜索网上内容。",
    model_client=ali_model_client,
    model_client_stream=True,
)

audit_agent = AssistantAgent(
    name="audit_agent",
    description="回答智能助手",
    system_message="你是一个回答智能助手, 结合用户的问题, 以及搜索智能助手搜索到的内容, 进行回答.发送 '任务完成，TERMINATE' 终止流程",
    model_client=model_client,
    model_client_stream=True,
)

async def web_search(query: str) -> str:
    """模拟或实际执行网络搜索"""
    # 此处可替换为真实搜索逻辑（如调用搜索引擎API）
    return "搜索到的内容：AutoGen 是一个多智能体框架..."

# 数据收集智能体
data_collector = AssistantAgent(
    name="data_collector",
    description="足球情报专员",
    system_message="你负责从数据库和API获取历史比赛数据、实时球员状态和天气信息。输出格式为JSON。",
    model_client=model_client,
    model_client_stream=True,
)

data_analyst = AssistantAgent(
    name="data_analyst",
    description="足球数据分析师",
    system_message="""
    你是一个专业的足球数据分析师，擅长处理历史战绩和统计数据。
    当收到比赛数据时，你需要：
    1. 计算双方最近3个月的交锋记录
    2. 分析主客场胜率差异
    3. 提供关键数据指标对比
    """,
    model_client=model_client,
    model_client_stream=True,
)

tactics_expert = AssistantAgent(
    name="tactics_expert",
    description="足球战术专家",
    system_message="""
    你是足球战术专家，擅长分析阵型和战术影响。
    需要分析：
    1. 双方常用阵型的克制关系
    2. 关键球员位置影响
    3. 主教练历史战术倾向
    """,
    model_client=model_client,
    model_client_stream=True,
)

injury_analyst = AssistantAgent(
    name="injury_analyst",
    description="运动医学专家",
    system_message="""
    你是运动医学专家，评估伤病影响：
    1. 计算伤病对关键位置的影响系数
    2. 分析替补深度
    3. 提供阵容调整建议
    """,
    model_client=model_client,
    model_client_stream=True,
)

weather_impact = AssistantAgent(
    name="weather_impact",
    description="气象专家",
    system_message="""
    你是气象专家，分析天气对比赛的影响：
    1. 雨天对传球成功率的影响
    2. 温度对球员体能消耗的影响
    3. 湿滑场地对不同阵型的影响
    """,
    model_client=model_client,
    model_client_stream=True,
)

predictor = AssistantAgent(
    name="predictor",
    description="足球预测大师",
    system_message="""
    你是足球预测大师，综合所有分析生成最终预测：
    1. 结合所有代理的分析结果
    2. 使用贝叶斯方法计算概率
    3. 输出胜平负概率和比分预测
    检查所有任务完成后发送 '任务完成，TERMINATE' 终止流程。
    """,
    model_client=model_client,
    model_client_stream=True,
)

def get_participants():
    # return [data_collector, data_analyst, tactics_expert, injury_analyst, weather_impact, predictor]
    return [ai_agent, audit_agent]

async def predict(message: str, chat_history):
    termination = TextMentionTermination("TERMINATE")
    group_chat = RoundRobinGroupChat(
        get_participants(),
        termination_condition=termination
    )
    
    print(f"=====> {message}")
    stream = group_chat.run_stream(task=message)
    
    chat_history.append({"role": "assistant", "content": ""})  # 先添加空消息

    async for chunk in stream:
        print(chunk)
        if hasattr(chunk, 'content'):
            chat_history[-1]['content'] += chunk.content  # 逐字填充最后一条消息
            # time.sleep(0.05)  # 模拟流式延迟
            yield chat_history  # 持续生成中间结果

if __name__ == "__main__":

    # message="""
    # 请分析以下比赛：
    # 曼联 vs 切尔西
    # 时间：2023-10-28 19:30
    # 地点：老特拉福德
    # 天气：有雨
    # """

    message="""
    请分析以下比赛：
    巴伦西亚 VS 赫塔费
    时间：2025-05-10 20:00
    地点：梅斯塔利亚
    天气：多云
    """

