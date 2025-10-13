# 📚 Documentação da API - QA Test Automation Dashboard

## 📋 Visão Geral

A API REST do QA Test Automation Dashboard fornece endpoints para gerenciamento de testes automatizados, métricas de qualidade e monitoramento do sistema. Desenvolvida com Flask e SQLite, oferece uma interface completa para automação de testes QA.

## 🔧 Configuração Base

### URL Base
```
http://localhost:5000/api
```

### Headers Padrão
```http
Content-Type: application/json
Accept: application/json
```

### Autenticação
Atualmente, a API não requer autenticação. Em produção, recomenda-se implementar autenticação JWT ou OAuth2.

## 📊 Endpoints de Métricas

### GET /api/metricas
Retorna métricas gerais do dashboard.

**Resposta:**
```json
{
  "taxaSucesso": 95.5,
  "tempoMedio": "2.3s",
  "cobertura": 87.2,
  "bugsEncontrados": 12,
  "tendencias": {
    "datas": ["01/12", "02/12", "03/12"],
    "sucesso": [94.5, 95.2, 95.8],
    "tempo": [2.1, 2.3, 2.2]
  },
  "distribuicao": {
    "tipos": ["web", "api", "performance"],
    "quantidades": [45, 32, 18]
  },
  "performance": {
    "testes": ["Login", "Navegação", "Formulários"],
    "tempos": [1200, 800, 1500]
  },
  "timestamp": "2024-12-07T10:30:00Z"
}
```

### GET /api/metricas/detalhadas
Retorna métricas detalhadas com mais informações.

**Resposta:**
```json
{
  "execucoes_por_status": {
    "sucesso": 45,
    "falha": 3,
    "executando": 2
  },
  "execucoes_por_ambiente": {
    "desenvolvimento": 35,
    "homologacao": 12,
    "producao": 3
  },
  "tempo_por_tipo": {
    "web": 2.1,
    "api": 1.8,
    "performance": 4.5
  },
  "timestamp": "2024-12-07T10:30:00Z"
}
```

## 🧪 Endpoints de Execuções

### GET /api/execucoes
Lista execuções de testes recentes.

**Parâmetros de Query:**
- `limite` (opcional): Número máximo de execuções (padrão: 10)
- `tipo` (opcional): Filtrar por tipo de teste
- `status` (opcional): Filtrar por status

**Exemplo:**
```http
GET /api/execucoes?limite=20&tipo=web&status=sucesso
```

**Resposta:**
```json
[
  {
    "id": 1,
    "tipo": "web",
    "status": "sucesso",
    "duracao": 180,
    "ambiente": "desenvolvimento",
    "observacoes": "Execução de testes web completos",
    "data_criacao": "2024-12-07T10:00:00Z",
    "data_atualizacao": "2024-12-07T10:03:00Z",
    "total_testes": 15,
    "testes_passaram": 15,
    "testes_falharam": 0
  }
]
```

### GET /api/execucoes/{id}
Obtém detalhes de uma execução específica.

**Resposta:**
```json
{
  "id": 1,
  "tipo": "web",
  "status": "sucesso",
  "duracao": 180,
  "ambiente": "desenvolvimento",
  "observacoes": "Execução de testes web completos",
  "data_criacao": "2024-12-07T10:00:00Z",
  "data_atualizacao": "2024-12-07T10:03:00Z",
  "total_testes": 15,
  "testes_passaram": 15,
  "testes_falharam": 0
}
```

### GET /api/execucoes/{id}/resultados
Obtém resultados detalhados de uma execução.

**Resposta:**
```json
{
  "execucao": {
    "id": 1,
    "tipo": "web",
    "status": "sucesso",
    "duracao": 180,
    "ambiente": "desenvolvimento"
  },
  "resultados": [
    {
      "id": 1,
      "execucao_id": 1,
      "nome_teste": "Teste Login - 1",
      "status": "passou",
      "tempo_execucao": 2.5,
      "mensagem_erro": null,
      "data_execucao": "2024-12-07T10:00:30Z"
    }
  ]
}
```

### POST /api/executar-testes
Executa uma nova suite de testes.

**Body:**
```json
{
  "tipo": "web",
  "ambiente": "desenvolvimento"
}
```

**Resposta:**
```json
{
  "mensagem": "Execução de testes iniciada",
  "execucao_id": 123,
  "status": "executando"
}
```

## 🖥️ Endpoints do Sistema

### GET /api/sistema
Retorna métricas atuais do sistema.

**Resposta:**
```json
{
  "cpu": 25.5,
  "memoria": 67.2,
  "disco": 45.8,
  "rede": 12.3
}
```

### GET /api/sistema/historico
Retorna histórico de métricas do sistema.

**Parâmetros de Query:**
- `horas` (opcional): Número de horas para histórico (padrão: 24)

**Resposta:**
```json
[
  {
    "id": 1,
    "cpu_percent": 25.5,
    "memoria_percent": 67.2,
    "disco_percent": 45.8,
    "rede_bytes_enviados": 1024000,
    "rede_bytes_recebidos": 2048000,
    "data_coleta": "2024-12-07T10:30:00Z"
  }
]
```

### GET /api/configuracoes
Retorna configurações do sistema.

**Resposta:**
```json
{
  "id": 1,
  "nome": "QA Dashboard",
  "versao": "1.0.0",
  "ambiente": "desenvolvimento",
  "configuracao": {
    "intervalo_atualizacao": 30,
    "retencao_logs": 30,
    "notificacoes_email": true,
    "backup_automatico": true
  },
  "data_criacao": "2024-12-07T00:00:00Z",
  "data_atualizacao": "2024-12-07T10:30:00Z"
}
```

### PUT /api/configuracoes
Atualiza configurações do sistema.

**Body:**
```json
{
  "nome": "QA Dashboard Atualizado",
  "configuracao": {
    "intervalo_atualizacao": 60,
    "notificacoes_email": false
  }
}
```

## 🔄 Endpoints de Pipelines

### GET /api/pipelines
Lista pipelines de CI/CD.

**Resposta:**
```json
[
  {
    "nome": "Build Principal",
    "status": "sucesso",
    "ultimaExecucao": "2 min atrás",
    "ambiente": "desenvolvimento",
    "branch": "main"
  },
  {
    "nome": "Testes de Integração",
    "status": "executando",
    "ultimaExecucao": "Executando...",
    "ambiente": "homologacao",
    "branch": "feature/nova-funcionalidade"
  }
]
```

### GET /api/pipelines/{id}
Obtém detalhes de um pipeline específico.

**Resposta:**
```json
{
  "id": 1,
  "nome": "Build Principal",
  "status": "sucesso",
  "ambiente": "desenvolvimento",
  "branch": "main",
  "commit_hash": "abc123def456",
  "duracao": 180,
  "url_build": "https://github.com/user/repo/actions/runs/123",
  "observacoes": "Build executado com sucesso",
  "data_inicio": "2024-12-07T10:00:00Z",
  "data_fim": "2024-12-07T10:03:00Z"
}
```

### POST /api/pipelines
Cria um novo pipeline.

**Body:**
```json
{
  "nome": "Novo Pipeline",
  "status": "pendente",
  "ambiente": "desenvolvimento",
  "branch": "feature/nova-funcionalidade",
  "observacoes": "Pipeline para nova funcionalidade"
}
```

## 📄 Endpoints de Relatórios

### GET /api/relatorios/{execucao_id}
Gera relatório detalhado de uma execução.

**Resposta:**
```json
{
  "execucao": {
    "id": 1,
    "tipo": "web",
    "status": "sucesso",
    "duracao": 180,
    "ambiente": "desenvolvimento"
  },
  "estatisticas": {
    "total_testes": 15,
    "testes_passaram": 15,
    "testes_falharam": 0,
    "testes_ignorados": 0,
    "taxa_sucesso": 100.0,
    "tempo_total": 180.5
  },
  "resultados": [
    {
      "id": 1,
      "nome_teste": "Teste Login - 1",
      "status": "passou",
      "tempo_execucao": 2.5,
      "mensagem_erro": null
    }
  ],
  "gerado_em": "2024-12-07T10:30:00Z"
}
```

## 🚨 Códigos de Erro

### 400 - Bad Request
Requisição malformada ou dados inválidos.

```json
{
  "erro": "Dados inválidos fornecidos"
}
```

### 404 - Not Found
Recurso não encontrado.

```json
{
  "erro": "Execução não encontrada"
}
```

### 405 - Method Not Allowed
Método HTTP não permitido para o endpoint.

```json
{
  "erro": "Método não permitido"
}
```

### 500 - Internal Server Error
Erro interno do servidor.

```json
{
  "erro": "Erro interno do servidor"
}
```

## 📝 Exemplos de Uso

### Executar Testes via cURL
```bash
# Executar testes web
curl -X POST http://localhost:5000/api/executar-testes \
  -H "Content-Type: application/json" \
  -d '{"tipo": "web", "ambiente": "desenvolvimento"}'

# Obter métricas
curl http://localhost:5000/api/metricas

# Listar execuções recentes
curl http://localhost:5000/api/execucoes?limite=5
```

### Executar Testes via Python
```python
import requests

# Executar testes
response = requests.post('http://localhost:5000/api/executar-testes', 
                        json={'tipo': 'web', 'ambiente': 'desenvolvimento'})
print(response.json())

# Obter métricas
response = requests.get('http://localhost:5000/api/metricas')
metricas = response.json()
print(f"Taxa de sucesso: {metricas['taxaSucesso']}%")
```

### Executar Testes via JavaScript
```javascript
// Executar testes
fetch('http://localhost:5000/api/executar-testes', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        tipo: 'web',
        ambiente: 'desenvolvimento'
    })
})
.then(response => response.json())
.then(data => console.log(data));

// Obter métricas
fetch('http://localhost:5000/api/metricas')
.then(response => response.json())
.then(metricas => {
    console.log(`Taxa de sucesso: ${metricas.taxaSucesso}%`);
});
```

## 🔧 Configuração e Deploy

### Variáveis de Ambiente
```bash
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_URL=sqlite:///qa_dashboard.db
```

### Health Check
```http
GET /health
```

**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-07T10:30:00Z",
  "uptime": "ativo"
}
```

## 📊 Monitoramento e Logs

### Logs da Aplicação
Os logs são gravados em:
- Console (desenvolvimento)
- Arquivo de log (produção)

### Métricas de Performance
- Tempo de resposta médio: < 2 segundos
- Throughput: > 100 requests/segundo
- Uptime: > 99.9%

## 🛡️ Segurança

### Headers de Segurança
A API inclui headers de segurança:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`

### Rate Limiting
- API endpoints: 10 requests/segundo
- Endpoints estáticos: 30 requests/segundo

## 📞 Suporte

Para dúvidas ou problemas com a API:
- **Desenvolvedora:** Isabella Barbosa
- **Email:** [seu-email@exemplo.com]
- **LinkedIn:** [seu-linkedin]

---

**📚 Documentação gerada automaticamente - QA Test Automation Dashboard v1.0.0**
