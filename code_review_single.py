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
from erniebot_agent.extensions.langchain.chat_models import ErnieBotChat
from typing import List, Optional, Dict, Any, Tuple, Union
from dotenv import load_dotenv, find_dotenv
from langchain.memory.chat_memory import BaseChatMemory
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate, ChatMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain.schema.output_parser import StrOutputParser
import erniebot


# 加载环境变量
_ = load_dotenv(find_dotenv())

class CodeReviewAgent:
    def __init__(
            self,
            llm: BaseChatModel = ErnieBotChat(
                aistudio_access_token="ecdaa00a52ce7eaea15d69bc91d9d8a23c538f04",
                api_type="aistudio",
                model="ernie-3.5"
            ),
            prompt: str = "",
            max_thought_steps: Optional[int] = 10,
    ):
        self.llm = llm
        self.max_thought_steps = max_thought_steps

        # OutputFixingParser： 如果输出格式不正确，尝试修复
        self.robust_parser = OutputFixingParser.from_llm(
            parser=self.output_parser,
            llm=ErnieBotChat(
                aistudio_access_token="ecdaa00a52ce7eaea15d69bc91d9d8a23c538f04",
                api_type="aistudio",
                model="ernie-3.5"
            )
        )
        self.main_prompt_file = prompt
        # self.__init_prompt_templates()
        # self.__init_chains()

    # def __init_prompt_templates(self):
    #     with open(self.main_prompt_file, 'r', encoding='utf-8') as f:
    #         self.prompt = ChatPromptTemplate.from_messages(
    #             [
    #                 MessagesPlaceholder(variable_name="chat_history"),
    #                 HumanMessagePromptTemplate.from_template(f.read()),
    #             ]
    #         ).partial(
    #             work_dir=self.work_dir,
    #             tools=render_text_description(self.tools),
    #             tool_names=','.join([tool.name for tool in self.tools]),
    #             format_instructions=self.output_parser.get_format_instructions(),
    #         )
    #
    # def __init_chains(self):
    #     # 主流程的chain
    #     self.main_chain = (self.prompt | self.llm | StrOutputParser())


#codeReviewAgent = CodeReviewAgent()

stream = False
erniebot.api_type = "aistudio"
erniebot.access_token = "ecdaa00a52ce7eaea15d69bc91d9d8a23c538f04"
session = [{"role": "user",
            "content": "你是一位优秀的Python软件工程师。"}, {
            "role": "assistant",
            "content": "你的任务是对下面的代码进行评审，审查其中的代码格式，变量命名，逻辑问题和安全等问题。"
           }]
code = f'''
from utils import postgre

def search_components_from_db(component) -> list:
    related_components = []
    dboperation = postgre.DBOperation()
    related_components = dboperation.get_component_list(component)
    return related_components
'''
session.append({"role": "user", "content": code})
response = erniebot.ChatCompletion.create(
        model="ernie-3.5",
        messages=session,
        top_p=0.95,
        stream=stream)

print(response.get_result())

session = [{"role": "user",
            "content": "你是一位优秀的Python测试工程师。"}, {
            "role": "assistant",
            "content": "你的任务是理解下面的代码，根据代码，制定测试用例，需要注意测试用例的边界。"
           }]

session.append({"role": "user", "content": code})
response = erniebot.ChatCompletion.create(
        model="ernie-3.5",
        messages=session,
        top_p=0.95,
        stream=stream)

print(response.get_result())