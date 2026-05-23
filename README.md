# SIAC - Sistema Inteligente de Asistencia Clínica

SIAC es un asistente clínico virtual académico desarrollado con FastAPI y arquitectura RAG (*Retrieval-Augmented Generation*).

El sistema permite responder preguntas relacionadas con documentos clínicos previamente cargados en una base vectorial ChromaDB. Para generar las respuestas, utiliza GitHub Models mediante el SDK compatible de OpenAI.

> Este proyecto tiene fines académicos y no reemplaza el diagnóstico, tratamiento ni evaluación de un profesional de la salud.

## Tecnologías utilizadas

- FastAPI
- GitHub Models
- OpenAI SDK
- LangChain
- ChromaDB
- Sentence Transformers
- Python
- Pydantic

## Arquitectura general

```text
Usuario
↓
FastAPI
↓
RAG Service
↓
Retriever
↓
ChromaDB
↓
Documentos PDF
↓
GitHub Models
↓
Respuesta final
