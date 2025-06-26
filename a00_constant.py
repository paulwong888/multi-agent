import os
from a01_openai_client import MyOpenAIChatCompletionClient
from dotenv import load_dotenv
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient

# env_openai_file_path = "/root/autodl-fs/paul/config/.env"
# env_deepseek_file_path = "/root/autodl-fs/paul/config/.env"
# env_openai_file_path = "/home/paul/config/.env-deepseek"
# env_deepseek_file_path = "/home/paul/config/.env-deepseek"
env_openai_file_path = "/home/coder/config/.env"
env_deepseek_file_path = env_openai_file_path

llm_model = "deepseek-chat"
# ali_llm_model = "qwq-plus"
# ali_llm_model = "qwen3-235b-a22b"
ali_llm_model = "qwq-32b"

model_info = {
    "name": "deepseek-chat", # 模型名称，可随意填写
    "parameters": {
        "max_tokens": 2048,  # 每次输出最大token数
                            # deepseek官方数据：1个英文字符 ≈ 0.3 个 token。1 个中文字符 ≈ 0.6 个 token。
        "temperature": 0.4,  # 模型随机性参数，数字越大，生成的结果随机性越大，一般为0.7，
                            # 如果希望AI提供更多的想法，可以调大该数字
        "top_p": 0.9,  # 模型随机性参数，接近 1 时：模型几乎会考虑所有可能的词，只有概率极低的词才会被排除，随机性也越强；
                    # 接近 0 时：只有概率非常高的极少数词会被考虑，这会使模型的输出变得非常保守和确定
    },
    "family": ModelFamily.GPT_4O,  # 必填字段，model属于的类别
    "functions": [],  # 非必填字段，如果模型支持函数调用，可以在这里定义函数信息
    "vision": False,  # 必填字段，模型是否支持图像输入
    "json_output": True,  # 必填字段，模型是否支持json格式输出
    "function_calling": True  # 必填字段，模型是否支持函数调用，如果模型需要使用工具函数，该字段为true
}
    

model_info_ali = {
    "name": "qwq-32b", # 模型名称，可随意填写
    # "name": "qwen-max-latest", # 模型名称，可随意填写
    # "name": "qwen3-235b-a22b", # 模型名称，可随意填写
    "parameters": {
        "max_tokens": 2048,  # 每次输出最大token数
                            # deepseek官方数据：1个英文字符 ≈ 0.3 个 token。1 个中文字符 ≈ 0.6 个 token。
        "temperature": 0.4,  # 模型随机性参数，数字越大，生成的结果随机性越大，一般为0.7，
                            # 如果希望AI提供更多的想法，可以调大该数字
        "top_p": 0.9,  # 模型随机性参数，接近 1 时：模型几乎会考虑所有可能的词，只有概率极低的词才会被排除，随机性也越强；
                    # 接近 0 时：只有概率非常高的极少数词会被考虑，这会使模型的输出变得非常保守和确定
        "enable_thinking": True,
        "extra_body": {
            "enable_search": True,
            "search_options": {
                "forced_search": True,
                "search_strategy": "pro" 
            }
        },
    },
    "family": ModelFamily.ANY,  # 必填字段，model属于的类别
    "functions": [],  # 非必填字段，如果模型支持函数调用，可以在这里定义函数信息
    "vision": False,  # 必填字段，模型是否支持图像输入
    "json_output": True,  # 必填字段，模型是否支持json格式输出
    "function_calling": True  # 必填字段，模型是否支持函数调用，如果模型需要使用工具函数，该字段为true
}

def get_config():
    load_dotenv(env_deepseek_file_path)
    # MySQL配置
    mysql_config = dict(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        pool_name="football_pool",  # 使用连接池
        pool_size=3,
    )

    # AutoGen配置
    config_list = [{
        "model": llm_model,
        # "model": "QwQ-32B",
        # "api_key": os.environ["OPENAI_API_KEY"],
        # "base_url": os.environ["OPENAI_BASE_URL"],
    }]

    llm_config = {
        "config_list": config_list,
        "temperature": 0.3,  # 降低随机性以获得更稳定的预测
        "timeout": 400,
        # "readtimeout": 400,
    }

    return mysql_config, llm_config

def get_code_execution_config(work_dir):
    # return {"work_dir": work_dir, "use_docker": False}
    return {
        "work_dir": work_dir,
        "use_docker": False,  # 若本地环境已配置Python，设为False
        "timeout": 60,
        "last_n_messages": 3,
        # "execute_at_receive": True,
        "language": "python"  # 显式指定语言为Python
    }

def get_model_client_deepseek():
    load_dotenv(env_deepseek_file_path)
    # return OpenAIChatCompletionClient(
    return MyOpenAIChatCompletionClient(
        model=llm_model,
        # model_info={
        #     "vision": False,
        #     "function_calling": False,
        #     "json_output": False,
        #     "family": ModelFamily.R1,
        #     "structured_output": True,
        # },
        model_info=model_info,
        # enable_internet=True
    )

def get_model_client_openai():
    load_dotenv(env_openai_file_path)
    return OpenAIChatCompletionClient(
        model="gpt-4o-mini"
    )

def get_model_client_ali():
    # return OpenAIChatCompletionClient(
    load_dotenv(env_deepseek_file_path)
    return MyOpenAIChatCompletionClient(
        model = ali_llm_model,
        api_key = os.getenv("ALI_OPENAI_API_KEY"),
        base_url = os.getenv("ALI_OPENAI_BASE_URL"),
        # model_info={
        #     "vision": False,
        #     "function_calling": False,
        #     "json_output": False,
        #     "family": ModelFamily.R1,
        #     "structured_output": True,
        # },
        model_info=model_info_ali,
        # enable_internet=True
    )


# 全局配置：定义终止符和缓存
termination_msg = lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE")

VLLM_COMPLETIONS_URL = "http://localhost:8080/v1"

SYSTEM_PROMPT = """
你是一名专业的足球分析师，请基于以下数据预测比赛结果：
        
主队: {features['home_team']}
客队: {features['away_team']}

实力对比:
- 主队实力评分: {features['strength_diff'] + features['home_advantage']:.2f}
- 客队实力评分: {features['strength_diff']:.2f}

近期状态:
- 主队最近5场: {features['home_form']*5}/5 胜利
- 客队最近5场: {features['away_form']*5}/5 胜利

历史交锋:
- 平均比分: {features['h2h_avg']['home_goals']:.1f} - {features['h2h_avg']['away_goals']:.1f}

伤病情况:
- 主队伤病球员: {features['home_injuries']}人
- 客队伤病球员: {features['away_injuries']}人
"""


if __name__ == "__main__":
    get_config()