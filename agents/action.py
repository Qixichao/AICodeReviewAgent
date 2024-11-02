from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Action(BaseModel):
    """结构化定义工具的属性"""
    name: str = Field(description="工具或指令名称")
    args: Optional[Dict[str, Any]] = Field(description="工具或指令参数，由参数名称和参数值组成")
