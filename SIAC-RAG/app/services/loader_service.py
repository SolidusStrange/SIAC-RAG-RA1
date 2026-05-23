import glob

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents():

    # Buscar automáticamente todos los PDFs
    pdf_files = glob.glob(
        "app/data/documentos/*.pdf"
    )

    all_documents = []

    # Cargar PDFs
    for pdf in pdf_files:

        print("Cargando PDF:", pdf)

        loader = PyPDFLoader(pdf)

        documents = loader.load()

        all_documents.extend(documents)

    # Dividir texto en chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(all_documents)

    print("Cantidad de chunks:", len(chunks))

    return chunks