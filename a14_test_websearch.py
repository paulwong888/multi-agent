import asyncio
from a00_constant import *
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

async def main() -> None:

    model_client = get_model_client_deepseek()
    # model_client = OpenAIChatCompletionClient(model="gpt-4o-2024-08-06")

    # web_surfer = MultimodalWebSurfer(
    #     name="web_surfer",
    #     model_client = model_client,
    # )
    web_surfer = MultimodalWebSurfer(
        "web_surfer", 
        model_client, 
        headless=True, 
        animate_actions=True
    )

    # await web_surfer.init(
    #     to_save_screenshots = True,
    # )

    termination = TextMentionTermination("exit")
    # Web surfer and user proxy take turns in a round-robin fashion.
    team = RoundRobinGroupChat([web_surfer], termination_condition=termination)

    while True:
        # Run the team and stream messages
        user_input = await asyncio.get_event_loop().run_in_executor(None, input, ">: ")
        # print(user_input)
        # response = await web_surfer.run(user_input)
        await Console(
            # team.run_stream(task="Find information about AutoGen and write a short summary.")
            team.run_stream(task=user_input)
        )
        print(response)

if __name__ == "__main__":
    asyncio.run(main())