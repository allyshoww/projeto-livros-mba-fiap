from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import pandas as pd
import os

app = FastAPI(
    title="API Pública de Consulta de Livros",
    description="API para consulta de livros extraídos de books.toscrape.com",
    version="1.0.0"
)

# Configuração para permitir acesso CORS de qualquer origem (para testes e frontends externos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Em produção, restrinja para domínios confiáveis
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define o caminho absoluto para o CSV, assumindo estrutura padrão do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "books.csv")

def load_data():
    """
    Lê o CSV com os dados dos livros. Adiciona coluna 'id' baseada no índice.
    Retorna DataFrame ou None em caso de erro.
    """
    try:
        df = pd.read_csv(DATA_PATH)
        df["id"] = df.index + 1
        return df
    except Exception:
        return None

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    """
    Endpoint para verificar o status da API e conexão com dados.
    """
    df = load_data()
    if df is None:
        return {"status": "error", "message": "Erro ao carregar os dados."}
    return {"status": "ok", "message": "API funcionando normalmente."}

@app.get("/api/v1/books", tags=["Books"])
def list_books(skip: int = 0, limit: int = 20):
    """
    Lista livros com paginação.
    - skip: número de registros para pular (default 0)
    - limit: quantidade máxima de livros na resposta (default 20)
    """
    df = load_data()
    if df is None:
        raise HTTPException(status_code=500, detail="Erro ao carregar os dados.")
    books = df.iloc[skip: skip+limit].to_dict(orient="records")
    return books

@app.get("/api/v1/books/search", tags=["Books"])
def search_books(
    title: Optional[str] = Query(default=None, description="Título parcial ou completo do livro"),
    category: Optional[str] = Query(default=None, description="Categoria do livro")
):
    """
    Busca livros por título e/ou categoria.
    Ambos os parâmetros são opcionais e a busca é case insensitive.
    """
    df = load_data()
    if df is None:
        raise HTTPException(status_code=500, detail="Erro ao carregar os dados.")
    filtered = df
    if title:
        filtered = filtered[filtered["title"].str.contains(title, case=False, na=False)]
    if category:
        filtered = filtered[filtered["category"].str.contains(category, case=False, na=False)]
    return filtered.to_dict(orient="records")

@app.get("/api/v1/books/{book_id}", tags=["Books"])
def get_book(book_id: int):
    """
    Detalhes completos de um livro pelo seu ID.
    """
    df = load_data()
    if df is None:
        raise HTTPException(status_code=500, detail="Erro ao carregar os dados.")
    book = df.loc[df["id"] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return book.iloc[0].to_dict()


@app.get("/api/v1/categories", tags=["Categories"])
def list_categories():
    """
    Retorna todas as categorias únicas disponíveis.
    """
    df = load_data()
    if df is None:
        raise HTTPException(status_code=500, detail="Erro ao carregar os dados.")
    categories = df["category"].dropna().unique().tolist()
    return {"categories": categories}
