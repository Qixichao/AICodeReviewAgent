import json
import re
from typing import List

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from models.factory import ChatModelFactory


class Person(BaseModel):
    """Information about a person."""

    name: str = Field(..., description="The name of the person")
    height_in_meters: float = Field(
        ..., description="The height of the person expressed in meters."
    )


class People(BaseModel):
    """Identifying information about all people in a text."""

    people: List[Person]

# Custom parser
def extract_json(message: AIMessage) -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between ```json and ``` tags.

    Parameters:
        text (str): The text containing the JSON content.

    Returns:
        list: A list of extracted JSON strings.
    """
    text = message.content
    print("-------------------{}".format(text))
    # Define the regular expression pattern to match JSON blocks
    pattern = r"```json(.*?)```"

    # Find all non-overlapping matches of the pattern in the string
    matches = re.findall(pattern, text, re.DOTALL)

    # Return the list of matched JSON strings, stripping any leading or trailing whitespace
    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f"Failed to parse: {message}")

llm = ChatModelFactory.get_model("qwen")

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user query. Output your answer as JSON that  "
            "matches the given schema: ```json\n{schema}\n```. "
            "Make sure to wrap the answer in ```json and ``` tags",
        ),
        ("human", "{query}"),
    ]
).partial(schema=People.schema())

query = "Anna is 23 years old and she is 6 feet tall"

chain = prompt | llm | extract_json

print(chain.invoke({"query": query}))
