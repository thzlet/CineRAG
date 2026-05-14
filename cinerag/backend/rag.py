from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

CHROMA_PATH = "../chroma_db"

PROMPT_TEMPLATE = """Você é o CineRAG, um agente especialista em cinema.
Use apenas o contexto abaixo para responder. Se não souber, diga que não encontrou nos documentos.

Contexto:
{context}

Pergunta: {question}

Resposta:"""

def load_rag_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

if __name__ == "__main__":
    chain = load_rag_chain()
    print("🎬 CineRAG pronto! Digite 'sair' para encerrar.\n")
    while True:
        question = input("Você: ")
        if question.lower() == "sair":
            break
        result = chain.invoke(question)
        print(f"\nCineRAG: {result}\n")