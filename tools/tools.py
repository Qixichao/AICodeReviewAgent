import warnings

warnings.filterwarnings("ignore")

from langchain.tools import StructuredTool
from .search_db import search_components_from_db
from .read_file import read_from_file_raw
from .finish import finish

search_db_tool = StructuredTool.from_function(
    func=search_components_from_db,
    name="SearchComponentsFromDatabase",
    description="根据模块的名字查询所有与之相关的模块",
)

read_file_tool = StructuredTool.from_function(
    func=read_from_file_raw,
    name="ReadCodeReviewFromFile",
    description="从文档中读取代码编写规范",
)

finish_placeholder = StructuredTool.from_function(
    func=finish,
    name="FINISH",
    description="结束任务，返回最终结果"
)
