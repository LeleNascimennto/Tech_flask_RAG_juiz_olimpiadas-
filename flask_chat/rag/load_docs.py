import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def gerar_faiss(docs, caminho_index="flask_chat/rag/index_faiss"):
    if not os.path.exists(caminho_index):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        db = FAISS.from_documents(docs, embeddings)
        db.save_local(caminho_index)
    else:
        print(f"FAISS index já existe em {caminho_index}")

def carregar_documentos(diretorio="docs"):
    loader = DirectoryLoader(diretorio)
    documentos = loader.load()
    return documentos

def dividir_documentos(documentos):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(documentos)

def gerar_faiss(docs, caminho_index="flask_chat/rag/index_faiss"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(caminho_index)
