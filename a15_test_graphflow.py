from a00_constant import get_model_client_deepseek, get_model_client_ali
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_ext.models.openai import OpenAIChatCompletionClient

# client = get_model_client_deepseek()
client = get_model_client_ali()

# 创建写作代理
writer = AssistantAgent(
    name="writer",  # 代理名称
    model_client=client,  # 使用的模型客户端
    system_message="你是一名专业的写作者，请根据用户的要求，起草一个关于指定主题的简短文案。"
)

# 创建语法编辑代理
editor_grammar = AssistantAgent(
    name="editor_grammar",
    model_client=client,
    system_message="你是一名语法专家，负责检查文本的语法错误，并提供修正建议。只关注语法方面，不要改变内容和风格。"
)

# 创建风格编辑代理
editor_style = AssistantAgent(
    name="editor_style",
    model_client=client,
    system_message="你是一名文体风格专家，负责优化文本的表达方式、词语选择和整体风格。不要关注语法问题，专注于让文本更加生动有力。"
)

# 创建终审编辑代理
final_reviewer = AssistantAgent(
    name="final_reviewer",
    model_client=client,
    system_message="你是终审编辑，负责将语法编辑和风格编辑的结果整合，制作最终版本。综合考虑语法正确性和表达效果。"
)

# 构建工作流图
# DiGraphBuilder 是一个流畅的API，用于构建有向图
builder = DiGraphBuilder()

# 添加所有节点
builder.add_node(writer).add_node(editor_grammar).add_node(editor_style).add_node(final_reviewer)

# 添加从writer到两个编辑的边（并行展开）
builder.add_edge(writer, editor_grammar)  # writer完成后，editor_grammar开始工作
builder.add_edge(writer, editor_style)  # writer完成后，editor_style也开始工作

# 添加从两个编辑到终审编辑的边（合并节点）
builder.add_edge(editor_grammar, final_reviewer)  # editor_grammar完成后，结果传递给final_reviewer
builder.add_edge(editor_style, final_reviewer)  # editor_style完成后，结果也传递给final_reviewer

# 构建并验证图
graph = builder.build()

# 创建GraphFlow实例
# participants参数指定参与工作流的所有代理
# graph参数指定工作流的执行图
flow = GraphFlow(
    participants=builder.get_participants(),  # 自动获取图中的所有参与者
    graph=graph,  # 指定执行图
)

# 异步运行工作流
import asyncio

async def main():
    # 运行工作流并获取流式输出
    # run_stream方法会返回一个可以异步迭代的事件流
    stream = flow.run_stream(task="请写一段关于人工智能发展历史的短文。")

    # 显示每个步骤的输出
    async for event in stream:
        # 检查event是否是TaskResult对象（最终结果）
        if hasattr(event, 'source'):
            # 如果是消息对象，直接打印source和content
            print(f"========== {event.source} ==========")
            print(event.content)
            print("\n")
        else:
            # 如果是TaskResult对象，打印结果信息
            print("========== 任务完成 ==========")
            print(f"停止原因: {event.stop_reason}")
            print(f"消息数量: {len(event.messages)}")
            print("\n")

# 在脚本中运行时，使用asyncio.run()执行主函数
if __name__ == "__main__":
    asyncio.run(main())