# SIAC - Sistema Inteligente de Asistencia Clínica

SIAC es un asistente clínico virtual desarrollado con FastAPI, OpenAI y arquitectura RAG (Retrieval-Augmented Generation).

El sistema permite responder preguntas médicas utilizando documentos clínicos almacenados en una base vectorial ChromaDB.

---

# Tecnologías utilizadas

- FastAPI
- OpenAI API
- LangChain
- ChromaDB
- Sentence Transformers
- Python
- Pydantic

---

# Arquitectura

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
OpenAI GPT-4o-mini
↓
Respuesta final

---

# Instalación

## 1. Clonar repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

---

## 2. Crear entorno virtual

```bash
python -m venv venv311
```

---

## 3. Activar entorno virtual

### Windows PowerShell

```bash
.\venv311\Scripts\Activate.ps1
```

---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Variables de entorno

Crear archivo `.env`

```env
OPENAI_API_KEY=TU_API_KEY
MODEL_NAME=gpt-4o-mini
```

---

# Crear base vectorial

```bash
python create_db.py
```

---

# Ejecutar API

```bash
python -m uvicorn app.main:app --reload --port 8001
```

---

# Endpoint principal

## POST `/ask`

### Ejemplo:

```bash
POST http://127.0.0.1:8001/ask
```

---

# Funcionalidades

- Arquitectura RAG
- Recuperación documental
- Embeddings semánticos
- Base vectorial ChromaDB
- Integración OpenAI
- Validaciones Pydantic
- Manejo de errores
- Configuración mediante `.env`

---

# Autor

Proyecto académico SIAC.
