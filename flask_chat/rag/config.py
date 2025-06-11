# flask_chat/rag/config.py
 
import os
 
# Base dir do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
 
# Caminho para a pasta de documentos
DOCS_PATH = os.path.join(BASE_DIR, 'docs')
FACTS_FILE = os.path.join(DOCS_PATH, 'facts.txt')
FAKES_FILE = os.path.join(DOCS_PATH, 'fakes.txt')
 
# Caminho do índice FAISS salvo em disco
FAISS_INDEX_PATH = os.path.join(DOCS_PATH, 'faiss_index')
 
# Parâmetros do RAG
TOP_K = 5
SCORE_THRESHOLD = 0.5  # ajustar conforme o modelo e teste
 
# Chave de API (se necessário) — usar dotenv no .flaskenv
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "sua-chave-aqui")  # ou None se não for usar agora
 
# Modelo RAG (se for fazer swap fácil entre vários)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"