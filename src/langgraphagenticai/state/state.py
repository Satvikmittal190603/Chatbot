from pydantic import BaseModel
from typing_extensions import TypedDict,List
from typing import Annotated
from langgraph.graph.message import add_messages


from typing import Optional, Any

class state(TypedDict):
    """
    Repreent the structure of the state used in graph
    """

    messages: Annotated[List, add_messages]
    frequency: Optional[str]
    news_data: Optional[List[Any]]
    summary: Optional[str]
    filename: Optional[str]