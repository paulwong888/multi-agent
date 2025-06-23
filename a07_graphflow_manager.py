import time
from a00_constant import get_model_client_ali

from a03_muti_agents import build_flow
# from a05_muti_agents import build_flow

# model_client = get_model_client_ali()

# def build_flow():
#     # 构建工作流图
#     # DiGraphBuilder 是一个流畅的API，用于构建有向图
#     builder = DiGraphBuilder()

#     # 添加所有节点
#     builder.add_node(data_collector) \
#            .add_node(data_analyst) \
#            .add_node(tactics_expert) \
#            .add_node(injury_analyst) \
#            .add_node(weather_impact) \
#            .add_node(predictor)

#     # 添加从writer到两个编辑的边（并行展开）
#     builder.add_edge(data_collector, data_analyst)  \
#            .add_edge(data_collector, tactics_expert)  \
#            .add_edge(data_collector, injury_analyst)  \
#            .add_edge(data_collector, weather_impact)  \

#     # 添加从两个编辑到终审编辑的边（合并节点）
#     # editor_grammar完成后，结果传递给final_reviewer
#     # editor_style完成后，结果也传递给final_reviewer
#     builder.add_edge(data_analyst, predictor)  \
#            .add_edge(tactics_expert, predictor)  \
#            .add_edge(injury_analyst, predictor)  \
#            .add_edge(weather_impact, predictor)  \

#     # 构建并验证图
#     graph = builder.build()

#     # 创建GraphFlow实例
#     # participants参数指定参与工作流的所有代理
#     # graph参数指定工作流的执行图
#     flow = GraphFlow(
#         participants=builder.get_participants(),  # 自动获取图中的所有参与者
#         graph=graph,  # 指定执行图
#     )
#     return flow

async def predict(message: str, chat_history):
    flow = build_flow()
    # group_chat = group_chat_selector
    stream = flow.run_stream(task=message)
    
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