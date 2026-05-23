from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.services.loader_service import load_documents
import os

DB_DIRECTORY = "chroma"


def create_vector_db():

    documents = load_documents()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DB_DIRECTORY
    )

    vectordb.persist()

    return vectordb


def get_retriever():

    # Validar existencia de base vectorial
    if not os.path.exists(DB_DIRECTORY):

        raise Exception(
            "La base vectorial no existe. Ejecuta create_db.py"
        )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=DB_DIRECTORY,
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 5}
    )

    return retriever

