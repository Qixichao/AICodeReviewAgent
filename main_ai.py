from typing import Union
from langchain.output_parsers import OutputFixingParser
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from pydantic.v1 import BaseModel, Field
from langchain.agents import AgentExecutor, create_react_agent, AgentOutputParser
from tools import *
from utils.call_back_handlers import ColoredPrintHandler
from utils.print_response import THOUGHT_COLOR
from erniebot_agent.extensions.langchain.chat_models import ErnieBotChat
from agents.agent import AIAgent

def launch_agent(agent: AIAgent):
    human_icon = "\U0001F468"
    ai_icon = "\U0001F916"
    chat_history = ChatMessageHistory()

    while True:
        task = input(f"{ai_icon}：有什么可以帮您？\n{human_icon}：")
        if task.strip().lower() == "quit":
            break
        reply = agent.run(task, chat_history, verbose=True)
        print(f"{ai_icon}：{reply}\n")


def main():

    # 语言模型
    llm = ErnieBotChat(
        aistudio_access_token="",
        api_type="aistudio",
        model="ernie-3.5"
    )

    # 自定义工具集
    tools = [
        search_db_tool,
        finish_placeholder,
    ]

    # 定义智能体
    agent = AIAgent(
        llm=llm,
        tools=tools,
        main_prompt_file="./prompts/main_prompt.txt",
        max_thought_steps=10,
    )

    # 运行智能体
    launch_agent(agent)


if __name__ == "__main__":
    main()