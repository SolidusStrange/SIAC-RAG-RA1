# SIAC - Sistema Inteligente de Asistencia Clínica

SIAC es un asistente clínico virtual académico desarrollado con **FastAPI** y arquitectura **RAG** (*Retrieval-Augmented Generation*).

El sistema permite responder preguntas relacionadas con documentos clínicos previamente cargados en una base vectorial **ChromaDB**. Para generar las respuestas, utiliza **GitHub Models** mediante el SDK compatible de OpenAI.

---

## Tecnologías utilizadas

- FastAPI
- GitHub Models
- OpenAI SDK
- LangChain
- ChromaDB
- Sentence Transformers
- Python
- Pydantic
- Uvicorn
- Python Dotenv

---

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
```

---

## Instalación

### 1. Clonar repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd SIAC-RAG
```

---

### 2. Crear entorno virtual

```bash
python -m venv venv311
```

---

### 3. Activar entorno virtual

En Windows PowerShell:

```powershell
.\venv311\Scripts\Activate.ps1
```

En caso de que PowerShell bloquee la activación del entorno virtual, ejecutar:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego activar nuevamente:

```powershell
.\venv311\Scripts\Activate.ps1
```

---

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo:

```env
GITHUB_TOKEN=TU_TOKEN_DE_GITHUB
GITHUB_BASE_URL=https://models.github.ai/inference
MODEL_NAME=openai/gpt-4.1-mini
```

También se puede usar otro modelo disponible en GitHub Models, por ejemplo:

```env
MODEL_NAME=openai/o4-mini
```

---

## Configuración del token de GitHub

Para utilizar GitHub Models, se necesita un token de GitHub con permisos para acceder a modelos.

### Opción recomendada: Fine-grained token

Crear un **Fine-grained personal access token** con los siguientes permisos mínimos:

```text
Account permissions:
  Models: Read-only
```

No es necesario entregar permisos de escritura ni permisos completos sobre repositorios.

---

## Seguridad del archivo `.env`

El archivo `.env` contiene credenciales privadas y **no debe subirse al repositorio**.

Agregar al archivo `.gitignore`:

```gitignore
.env
venv/
venv311/
__pycache__/
chroma_db/
```

---

## Configuración recomendada

El archivo `app/core/config.py` debe cargar explícitamente el archivo `.env` desde la raíz del proyecto.

Ejemplo:

```python
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH, override=True)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_BASE_URL = os.getenv(
    "GITHUB_BASE_URL",
    "https://models.github.ai/inference"
)
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openai/gpt-4.1-mini"
)
```

El uso de `override=True` permite asegurar que el proyecto utilice las variables definidas en el archivo `.env` del proyecto y no una variable antigua cargada en el sistema operativo.

---

## Servicio RAG

El servicio RAG recupera documentos relevantes desde ChromaDB, arma el contexto y envía la consulta a GitHub Models.

Ejemplo de estructura principal:

```python
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
```

---

## Prueba de conexión con GitHub Models

Antes de ejecutar la API completa, se recomienda probar que el token funciona correctamente.

Crear o ejecutar un archivo de prueba, por ejemplo:

```bash
python test_token_debug.py
```

El resultado esperado debe ser similar a:

```text
GitHub user status: 200
Models status: 200
```

Esto confirma que:

- El token de GitHub es válido.
- El token tiene acceso a GitHub Models.
- El modelo configurado responde correctamente.

---

## Crear base vectorial

Antes de consultar el sistema, se debe crear la base vectorial con los documentos clínicos.

Ejecutar:

```bash
python create_db.py
```

Este comando procesa los documentos disponibles y genera la base vectorial en ChromaDB.

---

## Ejecutar la API

Para levantar el servidor local con FastAPI:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

La API quedará disponible en:

```text
http://127.0.0.1:8001
```

---

## Acceso a Swagger UI

FastAPI genera automáticamente una interfaz Swagger para probar los endpoints.

Abrir en el navegador:

```text
http://127.0.0.1:8001/docs
```

Desde Swagger UI se puede probar el endpoint principal del sistema.

---

## Endpoint principal

### `POST /ask`

Permite enviar una pregunta al asistente clínico.

URL local:

```text
http://127.0.0.1:8001/ask
```

Ejemplo de body:

```json
{
  "question": "¿Cuál es la información clínica relevante del documento?"
}
```

Ejemplo de respuesta:

```json
{
  "answer": "Respuesta generada por el sistema en base a los documentos recuperados."
}
```

---

## Flujo de uso desde Swagger UI

1. Levantar la API:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

2. Abrir Swagger UI:

```text
http://127.0.0.1:8001/docs
```

3. Buscar el endpoint:

```text
POST /ask
```

4. Presionar **Try it out**.

5. Ingresar una pregunta en formato JSON:

```json
{
  "question": "¿Qué información aparece en los documentos clínicos?"
}
```

6. Presionar **Execute**.

7. Revisar la respuesta generada por el sistema.

---

## Archivos principales del proyecto

```text
SIAC-RAG/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── prompts.py
│   │
│   ├── services/
│   │   ├── rag_service.py
│   │   └── vector_service.py
│   │
│   └── main.py
│
├── create_db.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Funcionalidades

- Arquitectura RAG.
- Recuperación documental.
- Embeddings semánticos.
- Base vectorial con ChromaDB.
- Integración con GitHub Models.
- Uso del SDK de OpenAI compatible con GitHub Models.
- Validaciones con Pydantic.
- Manejo de errores.
- Configuración mediante variables de entorno.
- Pruebas mediante Swagger UI.
- Separación por servicios.
- Uso de documentos clínicos como fuente de contexto.

---

## Errores comunes

### Error: `ModuleNotFoundError: No module named 'dotenv'`

Solución:

```bash
pip install python-dotenv
```

---

### Error: `openai.AuthenticationError: Unauthorized`

Posibles causas:

- El token no tiene permisos para GitHub Models.
- El token fue copiado incorrectamente.
- El proyecto está leyendo un token antiguo desde las variables del sistema.
- El archivo `.env` no está siendo cargado correctamente.
- El modelo configurado no está disponible para la cuenta.

Soluciones recomendadas:

- Crear un nuevo token con permiso `Models: Read-only`.
- Revisar que el archivo `.env` tenga el token correcto.
- Usar `load_dotenv(ENV_PATH, override=True)`.
- Verificar que el modelo tenga el formato correcto:

```env
MODEL_NAME=openai/gpt-4.1-mini
```

---

### Error: el token funciona en un archivo, pero no en el proyecto

Revisar que `config.py` esté cargando el archivo `.env` desde la raíz del proyecto:

```python
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH, override=True)
```

---

## Consideraciones académicas

Este proyecto fue desarrollado como una implementación académica de un sistema RAG aplicado a documentos clínicos.

El sistema no entrega diagnósticos médicos propios, sino que genera respuestas en base al contenido documental recuperado desde la base vectorial.

---

## Autor

Proyecto académico SIAC.
