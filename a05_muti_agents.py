import time
from a00_constant import *
from typing import Dict
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
# from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
# from autogen_agentchat.conditions import TextMentionTermination

# model_client = get_model_client_deepseek()
ali_model_client = get_model_client_ali()
model_client = ali_model_client

result_text = """# 基于自身专业角度的预测输出要求
1. **胜负预测**
   - 给出三种结果（主胜/平局/客胜）概率分布与理由
   - 标注核心决定因素（不超过3个）

2. **比分建议**
   - 提供3个最可能比分与概率及对应理由

3. **让球预测**
   - 给出实时盘口值与所对应的（主胜/客胜）的概率分布与理由

3. **大小球预测**
   - 给出实时盘口值与所对应的大小球的概率分布与理由

# 分析限制条件
1. 仅使用提供数据，缺失字段标注"N/A"
2. 需区分统计显著差异与偶然波动
3. 避免主观臆断，保持数据驱动

请按[比分预测→概率分布→战术要点]的顺序输出分析结果，使用中文且保持专业简洁风格。"""

# ================== 角色定义 ==================
def define_agents() -> Dict[str, AssistantAgent]:
    """创建四个专业角色智能体"""
    return {
        "data_collector": AssistantAgent(
            name="data_collector",
            description="足球情报专员",
            system_message="""你只负责从数据库和API提取影响赛事结果的数据，不进行比赛预测, 要求
                1. 获取历史比赛数据
                2. 实时球员状态
                3. 主客队近期表现评估
                4. 主客队历史交锋评估
                5. 伤病因素
                6. 战意与身心压力因素
                7. 天气与环境信息
                9. 博彩盘口走势
                8. 舆情
                
                """,
            # system_message="你负责联网收集两队最新的情报",
            # model_client=model_client,
            model_client=ali_model_client,
            model_client_stream=True,
        ),
        "data_analyst": AssistantAgent(
            name="data_analyst",
            description="足球数据分析师",
            system_message=f"""
            # 角色指令
            你是一名专业的足球战术分析师，必需基于球情报专员提供的数据，并结合自身的专业，通过多维数据集对即将到来的比赛进行结果预测。请按以下框架分析数据并输出结构化结论：

            # 前置要求
            1. 分析足球情报专员提供的原始数据

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

            5. **伤病因素整合**
               - 球员伤病情况、疲劳情况

            6. **战意与压力因素**
               - 球队战意与压力情况

            6. **市场信号解读**
               - 初始赔率隐含的预期胜率计算
               - 异常赔率波动检测

            {result_text}
            """,
            model_client=model_client,
            model_client_stream=True,
        ),
        "ml_expert": AssistantAgent(
            name="ml_expert",
            description="机器学习足球预测专家",
            system_message=f"""你是一名通过机器学习算法进行足球预测的专家，具备深厚的计算机科学和数学背景，你需要：
                1. 基于足球情报专员提供的数据
                2. 利用高级数学模型和机器学习算法处理大量数据，以发现潜在的规律并做出预测

            {result_text}
            """,
            model_client=ali_model_client,
            model_client_stream=True,
        ),
        "match_analyst": AssistantAgent(
            name="match_analyst",
            description="赛事分析专家",
            system_message=f"""你是一名资深的赛事分析专家，你需要：
                    1. 基于足球情报专员提供的数据
                    2. 专注于分析具体比赛的战略层面，包括球队战术、教练风格、比赛节奏等
                    3. 外部条件：
                       - 考虑天气预报、场地状况（如草皮质量）等可能影响比赛的因素。
                       - 分析长途旅行对客队球员体力的影响。

            {result_text}
            """,
            model_client=ali_model_client,
            model_client_stream=True,
        ),
        "sports_psychologist": AssistantAgent(
            name="sports_psychologist",
            description="足球赛事心理学家",
            system_message=f"""你是一名足球赛事领域心理学家，你需要：
                        1. 基于足球情报专员提供的数据
                        2. 研究运动员的心理状态如何影响其表现，以及团队动力学对比赛结果的影响
                        3. 从心理韧性、团队凝聚力、动机与目标设定、专注力与注意力控制、赛后恢复等角度进行分析
                        4. 评估球队的心理状态，包括压力管理、士气高低及团队精神。
                        5. 关注关键时刻的心态稳定性，如点球大战或终场前的关键时刻。

            {result_text}
            """,
            model_client=ali_model_client,
            model_client_stream=True,
        ),
        "odds_analyst": AssistantAgent(
            name="odds_analyst",
            description="足球博彩分析师",
            system_message=f"""你是一名足球博彩分析师，你需要：
                            1. 基于足球情报专员提供的数据
                            2. 分析市场上的赔率变化，了解大众投注趋势，并据此调整自己的预测策略

            {result_text}
            """,
            model_client=ali_model_client,
            model_client_stream=True,
        ),
        "experienced_coach": AssistantAgent(
            name="experienced_coach",
            description="经验丰富教练",
            system_message=f"""你是一名经验丰富足球教练，你需要：
                                1. 基于足球情报专员提供的数据
                                2. 凭借自己在足球领域的实际经验和见解，能够提供对比赛的深刻理解，尤其是关于战术和技术细节方面
                                3. 评估球员的技术水平，包括传球准确性、控球能力、射门精度等基本技能。
                                4. 关注球员的耐力、速度、力量等体能因素，了解他们的身体状态是否能够满足高强度比赛的需求。
                                5. 研究即将对阵的对手的比赛风格、强弱点、常用战术等，为制定针对性的比赛策略提供依据。
                                6. 观察球队内部的关系，包括领导力、团队精神、球员间的默契程度等，良好的团队氛围有助于提高整体表现。

            {result_text}
            """,
            model_client=ali_model_client,
            model_client_stream=True,
        ),
        "injury_analyst": AssistantAgent(
            name="injury_analyst",
            description="伤病专家",
            system_message=f"""你是一名足球伤病专家，你需要：
                                    1. 基于足球情报专员提供的数据
                                    2. 跟踪受伤球员的康复过程，包括参与康复训练的程度、身体机能的恢复情况等
                                    3. 参考球员过往的伤病记录，分析其受伤频率、恢复速度及复发的可能性。
                                    4. 评估球员的身体素质和体能状态，判断是否有可能因为过度使用或其他原因导致再次受伤。
                                    5. 考虑球员的比赛出场时间、密集赛程对体力的影响，以及这可能对伤病风险带来的变化。
                                    6. 心理状态对伤病恢复的影响不容忽视。例如，压力、焦虑或缺乏自信可能会延长康复时间或增加再次受伤的风险。
                                    7. 天气、场地状况等外部因素也可能影响球员的健康和表现。比如，在湿滑的场地上比赛增加了扭伤的风险。
                {result_text}
                """,
            model_client=ali_model_client,
            model_client_stream=True,
        ),
    }

def build_flow():

    agents = define_agents()
    data_collector = agents["data_collector"]

    # 构建工作流图
    # DiGraphBuilder 是一个流畅的API，用于构建有向图
    builder = DiGraphBuilder()

    # 添加所有节点
    for agent in agents.items():
        builder.add_node(agent[1])

    # del agents["data_collector"]
    # del agents["summary_analyst"]

    # 添加从writer到两个编辑的边（并行展开）
    for agent in agents.items():
        if agent[0] != "data_collector":
            builder.add_edge(data_collector, agent[1])

    

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

if __name__ == "__main__":
    build_flow()