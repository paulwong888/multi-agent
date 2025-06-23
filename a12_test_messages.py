import asyncio
from dataclasses import dataclass
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler
from autogen_core import SingleThreadedAgentRuntime

@dataclass
class MyTextMessage:
    content: str


class MyWorkerAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("MyWorkerAgent")
        
    @message_handler
    async def handle_my_message(self, message: MyTextMessage, ctx: MessageContext) -> MyTextMessage:
        print(f"{self.id.key} 收到来自 {ctx.sender} 的消息: {message.content}\n")
        return MyTextMessage(content="OK, Got it!")
    
class MyManagerAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("MyManagerAgent")
        self.worker_agent_id = AgentId('my_worker_agent', 'worker')

    @message_handler
    async def handle_my_message(self, message: MyTextMessage, ctx: MessageContext) -> None:
        print(f"{self.id.key} 收到消息: {message.content}\n")
        print(f"{self.id.key} 发送消息给 {self.worker_agent_id}...\n")
        response = await self.send_message(message, self.worker_agent_id)
        print(f"{self.id.key} 收到来自 {self.worker_agent_id} 的消息: {response.content}\n")


async def main():

    #创建runtime，并注册agent类型
    runtime = SingleThreadedAgentRuntime()
    await MyManagerAgent.register(runtime, "my_manager_agent", lambda: MyManagerAgent())
    await MyWorkerAgent.register(runtime, "my_worker_agent", lambda: MyWorkerAgent())

    #启动runtime，发送消息，关闭runtime
    runtime.start() 

    #创建agent_id，发送消息
    agent_id = AgentId("my_manager_agent", "manager")
    await runtime.send_message(MyTextMessage(content="Hello World!"), recipient=agent_id)

    #关闭runtime
    await runtime.stop_when_idle()

if __name__ =="__main__":
    asyncio.run(main())