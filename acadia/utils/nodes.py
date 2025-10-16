from typing_extensions import Literal

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.stores import BaseStore
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState
from langgraph.types import Command

from acadia.prompts.routing import ROUTING_PROMPT
from .state import MainState, IntentClassification

def routing(state: MainState, config: RunnableConfig) -> str:
    """Use LLM to classify user intent, then route accordingly"""

    message = state['messages'][-1].content

    llm = ChatOpenAI(model="gpt-4o-mini")

    structured_llm = llm.with_structured_output(IntentClassification)

    classification_prompt = ROUTING_PROMPT.format(current_task=state["current_task"])

    result = structured_llm.invoke([SystemMessage(classification_prompt)] + [HumanMessage(message)])

    if result['intent'] == "start_or_continue_learning":
        goto = "learning"

    elif result['intent'] == "explain_content":
        goto = "explainer"

    elif result['intent'] == "request_assessment":
        goto = "assessor"

    elif result['intent'] == "answer_assessment":
        goto = "assessor"
    else:
        goto = ""

    return Command(
        update=result,
        goto=goto
    )