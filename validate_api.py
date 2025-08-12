#!/usr/bin/env python3
"""
Script para validar se a API está funcionando corretamente no Vercel
"""
import urllib.request
import urllib.error
import sys

def test_api(base_url):
    """Testa todos os endpoints da API"""
    print(f"🔍 Testando API em: {base_url}")
    print("-" * 50)
    
    tests = [
        ("Health Check", f"{base_url}/api/v1/health"),
        ("Listar Livros", f"{base_url}/api/v1/books?limit=5"),
        ("Buscar por Título", f"{base_url}/api/v1/books/search?title=a"),
        ("Buscar por Categoria", f"{base_url}/api/v1/books/search?category=Fiction"),
        ("Livro Específico", f"{base_url}/api/v1/books/1"),
        ("Categorias", f"{base_url}/api/v1/categories"),
        ("Documentação", f"{base_url}/docs")
    ]
    
    results = []
    
    for name, url in tests:
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                status_code = response.getcode()
                status = "✅ OK" if status_code == 200 else f"❌ {status_code}"
                print(f"{name:<20} {status}")
                results.append(status_code == 200)
        except Exception as e:
            print(f"{name:<20} ❌ ERRO: {str(e)}")
            results.append(False)
    
    print("-" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 API funcionando perfeitamente!")
    else:
        print("⚠️  Alguns testes falharam. Verifique os logs.")
    
    return passed == total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python validate_api.py <URL_DA_API>")
        print("Exemplo: python validate_api.py https://seu-projeto.vercel.app")
        sys.exit(1)
    
    url = sys.argv[1].rstrip('/')
    success = test_api(url)
    sys.exit(0 if success else 1)