# Guia de Deploy no Vercel - API de Livros

## Pré-requisitos

1. **Conta no Vercel**: Crie em [vercel.com](https://vercel.com)
2. **Repositório no GitHub**: Seu código deve estar no GitHub
3. **Git**: Certifique-se que está instalado e configurado

## Passo a Passo

### 1. Prepare os Dados
Execute o scraping para gerar o arquivo CSV:
```bash
python scripts/scrape_books.py
```

### 2. Inclua o CSV no Git
Edite o `.gitignore` e comente a linha:
```bash
# data/books.csv
```

### 3. Push para o GitHub
```bash
git add .
git commit -m "Deploy inicial no Vercel"
git push origin main
```

### 4. Deploy via Vercel Dashboard

1. Acesse [vercel.com](https://vercel.com)
2. Faça login com sua conta GitHub
3. Clique em "New Project"
4. Selecione seu repositório
5. Clique em "Deploy"

### 5. Deploy via CLI (Alternativo)

Instale a CLI do Vercel:
```bash
npm i -g vercel
```

Execute o deploy:
```bash
vercel
```

## Arquivos Necessários

- `vercel.json` ✓ - Configuração do Vercel
- `requirements.txt` ✓ - Dependências Python

## URLs da Sua API

Após o deploy, sua API estará disponível em:
- **Base**: `https://seu-projeto.vercel.app`
- **Documentação**: `https://seu-projeto.vercel.app/docs`
- **Health Check**: `https://seu-projeto.vercel.app/api/v1/health`

## Testando a API

```bash
# Teste básico
curl https://seu-projeto.vercel.app/api/v1/health

# Listar livros
curl https://seu-projeto.vercel.app/api/v1/books?limit=5
```

## Comandos Úteis

```bash
# Ver logs (via CLI)
vercel logs

# Listar deployments
vercel ls

# Remover projeto
vercel remove
```

## Configurações Avançadas

### Variáveis de Ambiente
No dashboard do Vercel:
1. Vá em Settings > Environment Variables
2. Adicione suas variáveis se necessário

### Domínio Customizado
1. Vá em Settings > Domains
2. Adicione seu domínio personalizado

## Solução de Problemas

### Build falha
- Verifique se `requirements.txt` está correto
- Confirme que `vercel.json` está na raiz do projeto

### CSV não encontrado
- Certifique-se que `data/books.csv` foi commitado
- Execute o scraping localmente antes do deploy

### Timeout na API
- Vercel tem limite de 10s para funções serverless
- Considere otimizar queries grandes

## Atualizações

Para atualizar a aplicação:
```bash
git add .
git commit -m "Atualização da API"
git push origin main
```

O Vercel fará deploy automático a cada push!

## Importante

⚠️ **Lembre-se**: 
- Após o deploy, volte a descomentar `data/books.csv` no `.gitignore`
- Vercel faz deploy automático a cada push no GitHub
- Funções serverless têm limite de tempo de execução
