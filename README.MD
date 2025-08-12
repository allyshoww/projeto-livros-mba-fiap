# API Pública de Consulta de Livros

## Visão Geral

Este projeto implementa um pipeline completo de dados — da extração por web scraping à disponibilização via API RESTful — para alimentar sistemas de recomendação de livros e cientistas de dados.

**Objetivo:**  
Extrair todos os livros de https://books.toscrape.com, armazenar localmente em CSV e disponibilizá-los de forma organizada e acessível via API pública.

## Arquitetura & Pipeline

1. **Extração**: Script automatizado de web scraping com Python
2. **Armazenamento**: Dados salvos em `data/books.csv`
3. **API**: FastAPI servindo os dados para consumo
4. **Deploy**: Pronto para deploy em plataformas cloud

## Estrutura do Projeto

```
Projeto Livros/
├── api/
│   └── main.py              # API FastAPI
├── scripts/
│   └── scrape_books.py      # Script de web scraping
├── data/
│   └── books.csv            # Dados extraídos (gerado após scraping)
├── docs/                    # Documentação adicional
├── tests/                   # Testes (opcional)
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

## Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd "Projeto Livros"
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute o web scraping
```bash
python scripts/scrape_books.py
```

### 4. Inicie a API
```bash
uvicorn api.main:app --reload
```

A API estará disponível em: http://localhost:8000

## Endpoints da API

### Health Check
- `GET /api/v1/health` - Verifica status da API

### Livros
- `GET /api/v1/books` - Lista livros com paginação
  - Parâmetros: `skip` (padrão: 0), `limit` (padrão: 20)
- `GET /api/v1/books/{book_id}` - Detalhes de um livro específico
- `GET /api/v1/books/search` - Busca livros por título e/ou categoria
  - Parâmetros: `title`, `category`

### Categorias
- `GET /api/v1/categories` - Lista todas as categorias disponíveis

## Documentação da API

Acesse a documentação interativa em:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Dados Extraídos

O script de scraping coleta as seguintes informações de cada livro:
- **title**: Título do livro
- **price**: Preço em libras (£)
- **rating**: Avaliação de 0 a 5 estrelas
- **availability**: Status de disponibilidade
- **category**: Categoria do livro
- **image_url**: URL da imagem da capa

## Tecnologias Utilizadas

- **Python 3.x**
- **FastAPI**: Framework web moderno e rápido
- **BeautifulSoup4**: Web scraping
- **Pandas**: Manipulação de dados
- **Requests**: Requisições HTTP
- **Uvicorn**: Servidor ASGI

## Deploy no Vercel

### Pré-requisitos
1. Conta no [Vercel](https://vercel.com)
2. [Vercel CLI](https://vercel.com/cli) instalado (opcional)
3. Git configurado

### Passos para Deploy

1. **Execute o scraping localmente** (dados são necessários para a API):
```bash
python scripts/scrape_books.py
```

2. **Remova o CSV do .gitignore temporariamente**:
```bash
# Comente a linha no .gitignore:
# data/books.csv
```

3. **Faça push para o GitHub**:
```bash
git add .
git commit -m "Deploy inicial"
git push origin main
```

4. **Deploy via Vercel Dashboard**:
- Acesse [vercel.com](https://vercel.com)
- Conecte seu repositório GitHub
- Clique em "Deploy"

**OU via CLI:**
```bash
npx vercel
```

### Arquivos de Deploy
- `vercel.json`: Configuração do Vercel
- `requirements.txt`: Lista as dependências

### URLs da Aplicação
- API: `https://seu-projeto.vercel.app`
- Docs: `https://seu-projeto.vercel.app/docs`

## Exemplo de Uso

```python
import requests

# Listar primeiros 10 livros
response = requests.get("http://localhost:8000/api/v1/books?limit=10")
books = response.json()

# Buscar livros por categoria
response = requests.get("http://localhost:8000/api/v1/books/search?category=Fiction")
fiction_books = response.json()

# Obter detalhes de um livro específico
response = requests.get("http://localhost:8000/api/v1/books/1")
book_details = response.json()
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.# projeto-livros-mba-fiap
