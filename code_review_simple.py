# 加载环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
from models.factory import ChatModelFactory
from tools import *
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from agents.agent import AIAgent
import gradio as gr

# def launch_agent(agent: AIAgent):
#     human_icon = "\U0001F468"
#     ai_icon = "\U0001F916"
#     chat_history = ChatMessageHistory()
#
#
#     while True:
#         # task = input(f"{ai_icon}：有什么可以帮您？\n{human_icon}：")
#         # if task.strip().lower() == "quit":
#         #     break
#
#         task =
#         reply = agent.run(task, chat_history, verbose=True)
#         print(f"{ai_icon}：{reply}\n")

def greet(code):
    # 语言模型
    llm = ChatModelFactory.get_model("qwen")
    chat_history = ChatMessageHistory()

    # 自定义工具集
    tools = [
        search_db_tool,
        read_file_tool,
        finish_placeholder
    ]

    # 定义智能体
    agent = AIAgent(
        llm=llm,
        tools=tools,
        work_dir="./docs/代码编写规范.docx",
        main_prompt_file="./prompts/codereview.txt",
        max_thought_steps=5,
    )
    task = code
    reply = agent.run(task, chat_history, verbose=True)
    print("-------------------------------------"+reply+"--------------------------------------------")
    return reply


def main():

    # 语言模型
    # llm = ChatModelFactory.get_model("qwen")
    #
    # # 自定义工具集
    # tools = [
    #     search_db_tool,
    #     read_file_tool,
    #     finish_placeholder
    # ]
    #
    # # 定义智能体
    # agent = AIAgent(
    #     llm=llm,
    #     tools=tools,
    #     work_dir="./docs/代码编写规范.docx",
    #     main_prompt_file="./prompts/codereview.txt",
    #     max_thought_steps=5,
    # )

    demo = gr.Interface(fn=greet, inputs="textbox", outputs="textbox")
    demo.launch(share=True)
    # 运行智能体
    # launch_agent(agent)


if __name__ == "__main__":
    main()
