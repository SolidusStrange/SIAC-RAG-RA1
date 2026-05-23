from openai import OpenAI

from app.core.prompts import SYSTEM_PROMPT
from app.services.vector_service import get_retriever
from app.core.config import (
    GITHUB_TOKEN,
    GITHUB_BASE_URL,
    MODEL_NAME
)

client = OpenAI(
    api_key=GITHUB_TOKEN,
    base_url=GITHUB_BASE_URL,
    default_headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
)


def ask_question(question):
    try:
        print("Pregunta recibida:", question)

        retriever = get_retriever()
        docs = retriever.invoke(question)

        if not docs:
            return "No se encontró información relevante en los documentos."

        context = "\n".join([doc.page_content for doc in docs])

        final_prompt = f"""
Contexto:
{context}

Pregunta:
{question}
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        print("ERROR GENERAL:", repr(e))
        return "Ocurrió un error procesando la consulta."