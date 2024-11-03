# 加载环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
from models.factory import ChatModelFactory
from tools import *
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from agents.agent import AIAgent
import gradio as gr

def greet(code):
    # 语言模型
    llm = ChatModelFactory.get_model("qwen")
    chat_history = ChatMessageHistory()

    # 自定义工具集
    tools = [
        search_db_tool,
        file_find_tool,
        read_file_tool,
        finish_placeholder
    ]

    # 定义智能体
    agent = AIAgent(
        llm=llm,
        tools=tools,
        work_dir="./docs",
        main_prompt_file="./prompts/codereview.txt",
        max_thought_steps=5,
    )
    task = code
    reply = agent.run(task, chat_history, verbose=True)
    return reply

def main():
    demo = gr.Interface(fn=greet, inputs="textbox", outputs="textbox")
    demo.launch(share=True)


if __name__ == "__main__":
    main()
