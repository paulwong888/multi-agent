from autogen_ext.models.openai import OpenAIChatCompletionClient

class MyOpenAIChatCompletionClient(OpenAIChatCompletionClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_stream(
        self,
        messages,
        *,
        tools = [],
        json_output = None,
        extra_create_args = {},
        cancellation_token = None,
        max_consecutive_empty_chunk_tolerance: int = 0,
    ):
        print(f"MyOpenAIChatCompletionClient ----> create_stream")
        extra_body = {
            "extra_body": {
                "enable_thinking": True,
                "enable_search": True, # 开启联网搜索的参数
                "search_options": {
                    "forced_search": True, # 强制联网搜索的参数
                    "search_strategy": "pro" # 模型将搜索10条互联网信息
                }}
            }
        # extra_body = {
        #         "enable_thinking": True,
        #         "enable_search": True,  # 开启联网搜索的参数
        #         "search_options": {
        #             "forced_search": True,  # 强制联网搜索的参数
        #             "search_strategy": "pro"  # 模型将搜索10条互联网信息
        #         }
        # }
        # extra_body = {
        #     "web_search_options": {
        #         "forced_search": True,  # 强制联网搜索的参数
        #         "search_strategy": "pro"  # 模型将搜索10条互联网信息
        #     }
        # }
        # extra_body = {
        #     "extra_body": {
        #         "enable_internet": True
        #     }
        # }
        return super().create_stream(
            messages, 
            tools=tools, 
            json_output=json_output, 
            extra_create_args=extra_body,
            cancellation_token=cancellation_token, 
            max_consecutive_empty_chunk_tolerance=max_consecutive_empty_chunk_tolerance
        )