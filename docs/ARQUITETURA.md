# Plano Arquitetural - API de Livros

## 1. Pipeline de Dados

### Fluxo Atual
```
[books.toscrape.com] → [Web Scraping] → [CSV Local] → [FastAPI] → [Consumidores]
```

### Detalhamento do Pipeline

#### 1.1 Ingestão
- **Fonte**: https://books.toscrape.com
- **Método**: Web scraping automatizado
- **Frequência**: Sob demanda
- **Dados coletados**: Título, preço, rating, disponibilidade, categoria, imagem

#### 1.2 Processamento
- **Limpeza**: Remoção de caracteres especiais (£, Â)
- **Transformação**: Conversão de ratings textuais para numéricos
- **Validação**: Verificação de URLs de imagem
- **Armazenamento**: CSV estruturado com encoding UTF-8

#### 1.3 API
- **Framework**: FastAPI
- **Endpoints**: 5 endpoints RESTful
- **Documentação**: Swagger automático
- **Formato**: JSON padronizado

#### 1.4 Consumo
- **Clientes**: Aplicações web, mobile, scripts Python
- **Formatos**: JSON via HTTP REST
- **Paginação**: Suporte nativo

## 2. Arquitetura para Escalabilidade Futura

### 2.1 Arquitetura Atual (MVP)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Scraper   │ -> │   CSV Storage   │ -> │   FastAPI       │
│   (Python)      │    │   (Local File)  │    │   (Vercel)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2.2 Arquitetura Escalável (Futuro)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Schedulers    │    │   Data Lake     │    │   API Gateway   │
│   (Airflow)     │ -> │   (S3/GCS)      │ -> │   (Kong/AWS)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         v                       v                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Scrapers  │    │   Databases     │    │   Microservices │
│   (Distributed) │    │   (PostgreSQL)  │    │   (Kubernetes)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 2.3 Componentes de Escalabilidade

#### Cache Layer
- **Redis**: Cache de consultas frequentes
- **CDN**: Cache de imagens de livros
- **TTL**: 1 hora para dados dinâmicos

#### Database Evolution
- **PostgreSQL**: Dados estruturados
- **Elasticsearch**: Busca textual avançada
- **MongoDB**: Dados não estruturados (reviews, metadata)

#### Monitoring & Observability
- **Prometheus**: Métricas de performance
- **Grafana**: Dashboards de monitoramento
- **ELK Stack**: Logs centralizados

## 3. Cenários de Uso para Cientistas de Dados/ML

### 3.1 Análise Exploratória
```python
# Exemplo de uso para análise
import requests
import pandas as pd

# Carregar todos os dados
books = requests.get("https://api-livros.vercel.app/api/v1/books?limit=1000").json()
df = pd.DataFrame(books)

# Análises possíveis
price_analysis = df.groupby('category')['price'].agg(['mean', 'std'])
rating_correlation = df[['price', 'rating']].corr()
```

### 3.2 Feature Engineering
- **Preço normalizado por categoria**
- **Score de popularidade** (rating × availability)
- **Categorização automática** via NLP
- **Sazonalidade de preços**

### 3.3 Casos de Uso ML
1. **Sistema de Recomendação**
   - Collaborative filtering
   - Content-based filtering
   - Hybrid approaches

2. **Análise de Sentimento**
   - Classificação de reviews
   - Predição de ratings

3. **Precificação Inteligente**
   - Predição de preços ótimos
   - Análise de elasticidade

4. **Detecção de Anomalias**
   - Preços fora do padrão
   - Livros com ratings suspeitos

## 4. Plano de Integração com Modelos de ML

### 4.1 Arquitetura ML Pipeline
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data API      │ -> │   ML Pipeline   │ -> │   Model API     │
│   (FastAPI)     │    │   (MLflow)      │    │   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         v                       v                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Raw Data      │    │   Trained       │    │   Predictions   │
│   (Books CSV)   │    │   Models        │    │   (JSON)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 4.2 Endpoints ML Propostos

#### 4.2.1 Sistema de Recomendação
```python
# Endpoint: POST /api/v1/ml/recommendations
{
  "user_preferences": {
    "categories": ["Fiction", "Mystery"],
    "price_range": [10, 50],
    "min_rating": 3
  },
  "limit": 10
}

# Response:
{
  "recommendations": [
    {
      "book_id": 123,
      "title": "The Great Mystery",
      "confidence_score": 0.95,
      "reason": "Similar to your liked books"
    }
  ]
}
```

#### 4.2.2 Predição de Preços
```python
# Endpoint: POST /api/v1/ml/price-prediction
{
  "title": "New Book Title",
  "category": "Fiction",
  "rating": 4.2
}

# Response:
{
  "predicted_price": 25.99,
  "confidence_interval": [22.50, 29.48],
  "model_version": "v1.2.0"
}
```

#### 4.2.3 Análise de Sentimento
```python
# Endpoint: POST /api/v1/ml/sentiment-analysis
{
  "text": "This book is absolutely amazing!"
}

# Response:
{
  "sentiment": "positive",
  "confidence": 0.92,
  "predicted_rating": 4.8
}
```

### 4.3 Infraestrutura ML

#### Model Serving
- **MLflow**: Versionamento e deploy de modelos
- **Docker**: Containerização de modelos
- **Kubernetes**: Orquestração e scaling

#### Training Pipeline
- **Apache Airflow**: Orquestração de treino
- **Jupyter Notebooks**: Experimentação
- **Git**: Versionamento de código ML

#### Monitoring ML
- **Model Drift Detection**: Monitoramento de performance
- **A/B Testing**: Comparação de modelos
- **Feature Store**: Centralização de features

### 4.4 Roadmap de Implementação

#### Fase 1 (MVP ML) - 3 meses
- [ ] Sistema básico de recomendação
- [ ] API de predição de preços
- [ ] Métricas básicas de modelo

#### Fase 2 (Produção) - 6 meses
- [ ] Pipeline automatizado de treino
- [ ] Monitoramento de drift
- [ ] A/B testing framework

#### Fase 3 (Avançado) - 12 meses
- [ ] Deep learning para NLP
- [ ] Real-time recommendations
- [ ] Multi-armed bandit optimization

## 5. Considerações Técnicas

### 5.1 Performance
- **Latência**: < 200ms para consultas simples
- **Throughput**: 1000 req/s com cache
- **Disponibilidade**: 99.9% uptime

### 5.2 Segurança
- **Rate Limiting**: Proteção contra abuse
- **API Keys**: Autenticação de clientes
- **HTTPS**: Criptografia em trânsito

### 5.3 Compliance
- **LGPD**: Proteção de dados pessoais
- **Rate Limiting**: Respeito aos termos do site
- **Caching**: Redução de carga no servidor origem

## 6. Métricas de Sucesso

### 6.1 Técnicas
- **API Response Time**: < 200ms
- **Error Rate**: < 1%
- **Data Freshness**: < 24h

### 6.2 Negócio
- **API Adoption**: Número de desenvolvedores usando
- **Query Diversity**: Variedade de consultas
- **ML Model Accuracy**: > 85% para recomendações

### 6.3 Escalabilidade
- **Concurrent Users**: Suporte a 10k usuários
- **Data Volume**: Suporte a 1M+ livros
- **Geographic Distribution**: Multi-region deployment
