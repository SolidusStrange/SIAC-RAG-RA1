from pydantic import BaseModel


class AnswerResponse(BaseModel):
    response: str
    