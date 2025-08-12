import os
import subprocess
import pandas as pd
import requests
import sys
from typing import Optional

# --- Ajuste automático de paths relativos ---
# Diretório raiz do projeto (considerando que esse script está em tests/)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCRAPING_SCRIPT = os.path.join(BASE_PATH, "scripts", "scrape_books.py")
CSV_PATH = os.path.join(BASE_PATH, "data", "books.csv")
PROCFILE_PATH = os.path.join(BASE_PATH, "Procfile")
API_BASE_URL = "http://localhost:8000/api/v1"

# --- Funções de teste ---

def test_scrape_and_csv():
    print(f"[INFO] Executando o script de scraping: {SCRAPING_SCRIPT}")
    result = subprocess.run([sys.executable, SCRAPING_SCRIPT], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERRO] Script de scraping retornou erro:\n{result.stderr}")
        return False

    if not os.path.isfile(CSV_PATH):
        print(f"[ERRO] Arquivo CSV '{CSV_PATH}' não encontrado após scraping.")
        return False

    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        print(f"[ERRO] Falha ao ler CSV: {e}")
        return False

    if df.empty:
        print("[ERRO] Arquivo CSV está vazio.")
        return False

    # Colunas esperadas conforme enunciado
    required_columns = ["title", "price", "rating", "availability", "category", "image_url"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print("[ERRO] Colunas faltantes no CSV:", missing_cols)
        return False

    print(f"[OK] CSV gerado com sucesso. Total de livros: {len(df)}")
    return True


def test_api_endpoint(path: str, expected_status: int = 200, optional_check: Optional[callable] = None):
    url = API_BASE_URL + path
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != expected_status:
            print(f"[ERRO] {path}: Status {r.status_code} (esperado {expected_status})")
            return False
        if optional_check is not None and not optional_check(r):
            print(f"[ERRO] {path}: Checagem adicional falhou.")
            return False
        print(f"[OK] Endpoint {path} respondeu corretamente.")
        return True
    except requests.exceptions.ConnectionError:
        print(f"[ERRO] Endpoint {path} inacessível (Conexão recusada). Verifique se a API está rodando.")
        return False
    except Exception as e:
        print(f"[ERRO] Endpoint {path} falhou com exceção: {e}")
        return False


def test_api_endpoints():
    print("[INFO] Iniciando testes dos endpoints da API.")

    # health check deve retornar status "ok"
    if not test_api_endpoint("/health", optional_check=lambda r: r.json().get("status") == "ok"):
        return False

    # /books retorna lista não-vazia
    if not test_api_endpoint("/books", expected_status=200,
                             optional_check=lambda r: isinstance(r.json(), list) and len(r.json()) > 0):
        return False

    # /books/1 retorna livro com campo 'title'
    if not test_api_endpoint("/books/1", expected_status=200, optional_check=lambda r: "title" in r.json()):
        return False

    # /books/search recebe parâmetros opcionais corretamente (ajuste para aceitar opcionais na API)
    # Testa buscando titulo e categoria, esperando lista como resposta (mesmo vazia, é ok)
    if not test_api_endpoint("/books/search?title=a&category=Science", expected_status=200,
                             optional_check=lambda r: isinstance(r.json(), list)):
        return False

    # /categories retorna lista de categorias
    if not test_api_endpoint("/categories", expected_status=200,
                             optional_check=lambda r: "categories" in r.json() and isinstance(r.json()["categories"], list)):
        return False

    print("[OK] Todos os endpoints da API estão funcionando corretamente.")
    return True


def test_procfile():
    if not os.path.isfile(PROCFILE_PATH):
        print("[ERRO] Arquivo Procfile não encontrado.")
        return False
    with open(PROCFILE_PATH, "r", encoding="utf-8") as f:
        content = f.read().lower()
        # Procfile deve conter comando para rodar api.main:app via uvicorn
        if "uvicorn" in content and "api.main:app" in content:
            print("[OK] Procfile encontrado e formatado corretamente.")
            return True
        else:
            print("[ERRO] Conteúdo do Procfile não parece correto. Deve conter: uvicorn api.main:app")
            return False


# --- Main ---

def main():
    print("="*60)
    print("INÍCIO DOS TESTES DO PROJETO - TECH CHALLENGE (a partir do Item 2)")
    print("="*60)

    all_passed = True

    # Testar script de scraping + CSV
    if not test_scrape_and_csv():
        all_passed = False
    print("-"*60)

    # Testar endpoints da API (API deve estar rodando localmente por conta do usuário)
    print("[AVISO] Garanta que a API está rodando localmente em http://localhost:8000 antes de continuar.")
    proceed = input("Deseja continuar com os testes da API? (s/n): ").strip().lower()
    if proceed == "s":
        if not test_api_endpoints():
            all_passed = False
    else:
        print("[PULADO] Testes da API foram pulados.")
    print("-"*60)

    # Testar Procfile para deploy
    if not test_procfile():
        all_passed = False
    print("-"*60)

    # Relatar resultado final
    if all_passed:
        print("RESULTADO FINAL: TODOS OS TESTES PASSARAM COM SUCESSO! Parabéns!")
        sys.exit(0)
    else:
        print("RESULTADO FINAL: ALGUNS TESTES FALHARAM. Revise os erros acima antes da entrega.")
        sys.exit(1)


if __name__ == "__main__":
    main()
