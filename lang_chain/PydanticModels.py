from pydantic import BaseModel, Field

# Define the Pydantic model that will be used to parse the output
class AnswerInfo(BaseModel):
    title: str = Field(description="Title of the answer")
    text: int = Field(description="Helpful Answer")