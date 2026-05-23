from fastapi import APIRouter

from app.services.rag_service import ask_question

from app.models.question_model import QuestionRequest
from app.models.response_model import AnswerResponse

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):

    # Validar pregunta vacía
    if not request.question.strip():

        return AnswerResponse(
            response="La pregunta no puede estar vacía."
        )

    response = ask_question(request.question)

    return AnswerResponse(
        response=response
    )
