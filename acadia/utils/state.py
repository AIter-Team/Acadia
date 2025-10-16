from enum import Enum
from typing_extensions import TypedDict, Literal, List, Annotated

from pydantic import BaseModel, Field

from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage

class Intent(Enum):
    START_OR_CONTINUE_LEARNING = "start_or_continue_learning"
    EXPLAIN_CONCEPT = "explain_concept"
    ANSWER_ASSESSMENT = "answer_assessment"
    REQUEST_ASSESSMENT = "request_assessment"
    GENERAL_CHAT = "general_chat"

class IntentClassification(TypedDict):
    intent: Intent

# @dataclass
# class Module:
#     name: str
#     status: Literal["in_progress", "assessment", "finished"]
#     score: float

class MainState(BaseModel):
    current_task: Literal["learning", "explaining", "assessing", "evaluating", "idle"]
    messages: Annotated[List[AnyMessage], add_messages]
    intent: str