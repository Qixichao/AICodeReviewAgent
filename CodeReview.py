from typing import Union
from langchain.output_parsers import OutputFixingParser
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from pydantic.v1 import BaseModel, Field
from langchain.agents import AgentExecutor, create_react_agent, AgentOutputParser
from langchain_openai import ChatOpenAI
from Tools import *
from Tools.PythonTool import ExcelAnalyser

from dotenv import load_dotenv, find_dotenv

from Utils.CallbackHandlers import ColoredPrintHandler
from Utils.PrintUtils import THOUGHT_COLOR

# 加载环境变量
_ = load_dotenv(find_dotenv())

class CodeReviewAgent:
    class AgentActionWrapper(BaseModel):
        tool: str = Field(..., title="The name of the Tool to execute.")
        tool_input: Union[str, dict] = Field(..., title="The input to pass in to the Tool.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

