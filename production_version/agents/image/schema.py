# Currently no complex input schema needed for Image Agent beyond AgentState
# But we adhere to the structure.
from pydantic import BaseModel

class ImageAgentInput(BaseModel):
    # This might be used if we ever change to strict structured output from this agent
    pass
