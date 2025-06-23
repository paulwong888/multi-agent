from openai import NOT_GIVEN, AsyncStream
from openai._base_client import make_request_options
from openai._utils import async_maybe_transform, required_args

from openai.types.chat import completion_create_params
from openai.resources.chat.completions.completions import AsyncCompletions, validate_response_format
from openai.types.chat import ChatCompletion, ChatCompletionChunk


class ExtAsyncCompletions(AsyncCompletions):
    @required_args(["messages", "model"], ["messages", "model", "stream"])
    async def create(
            self,
            messages = NOT_GIVEN,
            model = NOT_GIVEN,
            audio = NOT_GIVEN,
            frequency_penalty = NOT_GIVEN,
            function_call = NOT_GIVEN,
            functions = NOT_GIVEN,
            logit_bias = NOT_GIVEN,
            logprobs = NOT_GIVEN,
            max_completion_tokens = NOT_GIVEN,
            max_tokens = NOT_GIVEN,
            metadata = NOT_GIVEN,
            modalities = NOT_GIVEN,
            n = NOT_GIVEN,
            parallel_tool_calls = NOT_GIVEN,
            prediction = NOT_GIVEN,
            presence_penalty = NOT_GIVEN,
            reasoning_effort = NOT_GIVEN,
            response_format = NOT_GIVEN,
            seed = NOT_GIVEN,
            service_tier = NOT_GIVEN,
            stop = NOT_GIVEN,
            store = NOT_GIVEN,
            stream = NOT_GIVEN,
            stream_options = NOT_GIVEN,
            temperature = NOT_GIVEN,
            tool_choice = NOT_GIVEN,
            tools = NOT_GIVEN,
            top_logprobs = NOT_GIVEN,
            top_p = NOT_GIVEN,
            user = NOT_GIVEN,
            web_search_options = NOT_GIVEN,
            extra_headers = None,
            extra_query = None,
            extra_body = None,
            timeout = NOT_GIVEN,
    ):
        validate_response_format(response_format)
        return await self._post(
            "/chat/completions",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "audio": audio,
                    "frequency_penalty": frequency_penalty,
                    "function_call": function_call,
                    "functions": functions,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_completion_tokens": max_completion_tokens,
                    "max_tokens": max_tokens,
                    "metadata": metadata,
                    "modalities": modalities,
                    "n": n,
                    "parallel_tool_calls": parallel_tool_calls,
                    "prediction": prediction,
                    "presence_penalty": presence_penalty,
                    "reasoning_effort": reasoning_effort,
                    "response_format": response_format,
                    "seed": seed,
                    "service_tier": service_tier,
                    "stop": stop,
                    "store": store,
                    "stream": stream,
                    "stream_options": stream_options,
                    "temperature": temperature,
                    "tool_choice": tool_choice,
                    "tools": tools,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "user": user,
                    "web_search_options": web_search_options,
                    **extra_body,
                    "extra_body": extra_body
                },
                completion_create_params.CompletionCreateParamsStreaming
                if stream
                else completion_create_params.CompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCompletion,
            stream=stream or False,
            stream_cls=AsyncStream[ChatCompletionChunk],
        )


@property
def completions(self) -> ExtAsyncCompletions:
    return ExtAsyncCompletions(self._client)
