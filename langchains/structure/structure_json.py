from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import Annotated, TypedDict
from models.factory import ChatModelFactory
from typing import Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# TypedDict
class Joke(TypedDict):
    """Joke to tell user."""

    setup: Annotated[str, ..., "The setup of the joke"]

    # Alternatively, we could have specified setup as:

    # setup: str                    # no default, no description
    # setup: Annotated[str, ...]    # no default, no description
    # setup: Annotated[str, "foo"]  # default, no description

    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]

json_schema = {
    "title": "joke",
    "description": "Joke to tell user.",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "The setup of the joke",
        },
        "punchline": {
            "type": "string",
            "description": "The punchline to the joke",
        },
        "rating": {
            "type": "integer",
            "description": "How funny the joke is, from 1 to 10",
            "default": None,
        },
    },
    "required": ["setup", "punchline"],
}

llm = ChatModelFactory.get_model("qwen")
structured_llm = llm.with_structured_output(Joke)

for chunk in structured_llm.stream("Tell me a joke about cats"):
    print(chunk)


# prompt_template = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant"),
#     ("user", "Tell me a joke about {topic}")
# ])
#
# print(prompt_template.invoke({"topic": "cats"}))