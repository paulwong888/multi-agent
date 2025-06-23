import time
from a00_constant import *
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
# from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
# from autogen_agentchat.conditions import TextMentionTermination

# model_client = get_model_client_deepseek()
ali_model_client = get_model_client_ali()
model_client = ali_model_client

# 数据收集智能体
data_collector = AssistantAgent(
    name="data_collector",
    description="足球情报专员",
    system_message="你负责从数据库和API获取历史比赛数据、实时球员状态、天气信息和舆情。输出格式为JSON。",
    # system_message="你负责联网收集两队最新的情报",
    # model_client=model_client,
    model_client=ali_model_client,
    model_client_stream=True,
)

data_analyst = AssistantAgent(
    name="data_analyst",
    description="足球数据分析师",
    system_message="""
# 角色指令
你是一名专业的足球战术分析师，需要基于多维数据集对即将到来的比赛进行结果预测。请按以下框架分析数据并输出结构化结论：

# 数据分析框架
1. **实力对比分析**
   - 排名差异：主队[排名] vs 客队[排名]
   - 教练风格：比较[主队教练]与[客队教练]的战术体系
   - 年龄结构：分析两队平均年龄对比赛节奏的影响

2. **近期表现评估**
   - 进攻效率：对比场均进球/射正/关键传球数据
   - 防守稳定性：比较失球率/抢断/解围数据
   - 控场能力：解析控球率与传球成功率差异

3. **历史交锋模式**
   - 往绩胜负关系分析
   - 最近交锋结果对心理影响评估

4. **环境因素整合**
   - 天气条件对战术执行的影响
   - 阵型匹配度分析

5. **市场信号解读**
   - 初始赔率隐含的预期胜率计算
   - 异常赔率波动检测

# 预测输出要求
1. **胜负预测**
   - 给出三种结果概率分布（主胜/平局/客胜）
   - 标注核心决定因素（不超过3个）

2. **比分建议**
   - 提供3个最可能比分与概率及对应理由

3. **关键观察点**
   - 指出可能影响比赛的关键战术对位
   - 预警潜在风险因素（如主队防守漏洞）


# 分析限制条件
1. 仅使用提供数据，缺失字段标注"N/A"
2. 需区分统计显著差异与偶然波动
3. 避免主观臆断，保持数据驱动

请按[比分预测→概率分布→战术要点]的顺序输出分析结果，使用中文且保持专业简洁风格。
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
    4. 输出让球和大小球预测
    检查所有任务完成后发送 '任务完成，TERMINATE' 终止流程。
    """,
    model_client=model_client,
    model_client_stream=True,
)

def get_participants():
    return [data_collector, data_analyst, tactics_expert, injury_analyst, weather_impact, predictor]
    # return [data_analyst, tactics_expert, injury_analyst, weather_impact, predictor]

def build_flow():
    # 构建工作流图
    # DiGraphBuilder 是一个流畅的API，用于构建有向图
    builder = DiGraphBuilder()

    # 添加所有节点
    builder.add_node(data_collector) \
           .add_node(data_analyst) \
           .add_node(tactics_expert) \
           .add_node(injury_analyst) \
           .add_node(weather_impact) \
           .add_node(predictor)

    # 添加从writer到两个编辑的边（并行展开）
    builder.add_edge(data_collector, data_analyst)  \
           .add_edge(data_collector, tactics_expert)  \
           .add_edge(data_collector, injury_analyst)  \
           .add_edge(data_collector, weather_impact)  \

    # 添加从两个编辑到终审编辑的边（合并节点）
    # editor_grammar完成后，结果传递给final_reviewer
    # editor_style完成后，结果也传递给final_reviewer
    builder.add_edge(data_analyst, predictor)  \
           .add_edge(tactics_expert, predictor)  \
           .add_edge(injury_analyst, predictor)  \
           .add_edge(weather_impact, predictor)  \

    # 构建并验证图
    graph = builder.build()

    # 创建GraphFlow实例
    # participants参数指定参与工作流的所有代理
    # graph参数指定工作流的执行图
    flow = GraphFlow(
        participants=builder.get_participants(),  # 自动获取图中的所有参与者
        graph=graph,  # 指定执行图
    )
    return flow


# async def predict(message: str, chat_history):
#     termination = TextMentionTermination("TERMINATE")
#     # group_chat = RoundRobinGroupChat(
#     #     get_participants(),
#     #     termination_condition=termination
#     # )
#     group_chat = SelectorGroupChat(
#         get_participants(),
#         termination_condition=termination
#     )
    
#     print(f"=====> {message}")
#     stream = group_chat.run_stream(task=message)
    
#     chat_history.append({"role": "assistant", "content": ""})  # 先添加空消息

#     async for chunk in stream:
#         print(chunk)
#         if hasattr(chunk, 'content'):
#             chat_history[-1]['content'] += chunk.content  # 逐字填充最后一条消息
#             # time.sleep(0.05)  # 模拟流式延迟
#             yield chat_history  # 持续生成中间结果

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

