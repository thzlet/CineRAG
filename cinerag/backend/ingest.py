import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

DOCS_PATH = "../docs"
CHROMA_PATH = "../chroma_db"

def load_documents():
    docs = []
    for filename in os.listdir(DOCS_PATH):
        filepath = os.path.join(DOCS_PATH, filename)
        if filename.endswith(".txt"):
            loader = TextLoader(filepath, encoding="utf-8")
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
        else:
            continue
        docs.extend(loader.load())
        print(f"✅ Carregado: {filename}")
    return docs

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"📄 Total de chunks: {len(chunks)}")
    return chunks

def save_to_chroma(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"✅ Salvo no ChromaDB em: {CHROMA_PATH}")

if __name__ == "__main__":
    print("🎬 Iniciando ingestão...")
    docs = load_documents()
    chunks = split_documents(docs)
    save_to_chroma(chunks)
    print("🎉 Ingestão completa!")