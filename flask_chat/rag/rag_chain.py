import os
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Carregar o banco FAISS
def carregar_base(caminho_index="flask_chat/rag/index_faiss"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    return FAISS.load_local(caminho_index, embeddings, allow_dangerous_deserialization=True)

# Função principal de resposta via RAG
def responder_rag(pergunta):
    db = carregar_base()
    docs = db.similarity_search(pergunta, k=3)

    modelo = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=api_key)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
Você é um assistente especializado em responder perguntas com base no seguinte contexto:

{context}

Pergunta: {question}
Resposta precisa, clara e direta:
"""
    )

    chain = load_qa_chain(llm=modelo, chain_type="stuff", prompt=prompt, verbose=False)
    resposta = chain.run(input_documents=docs, question=pergunta)
    return resposta
