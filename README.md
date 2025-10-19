# 🚀 QA Test Automation Dashboard

<div align="center">

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.13+-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)
![License](https://img.shields.io/badge/License-MIT-orange)

**Dashboard completo para automação e monitoramento de testes de qualidade de software**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Ver%20Dashboard-blue)](https://bella5900g.github.io/qa-test-dashboard/docs/dashboard-demo.html)
[![Documentação](https://img.shields.io/badge/📚%20Documentação-Ver%20Guia-green)](https://bella5900g.github.io/qa-test-dashboard/docs/)

</div>

---

## 🎯 **Sobre o Projeto**

Dashboard profissional para **engenheiros de QA** e **equipes de desenvolvimento** com métricas em tempo real, execução automatizada de testes e relatórios detalhados.

### ✨ **Principais Características**

- 📊 **Métricas em Tempo Real** - Taxa de sucesso, cobertura e performance
- 🚀 **Execução Automatizada** - Testes Web, API e Performance
- 📈 **Dashboards Interativos** - Gráficos dinâmicos com Chart.js
- 🔄 **Integração CI/CD** - Compatível com pipelines de integração contínua
- 📱 **Design Responsivo** - Interface moderna e adaptável
- 🐳 **Containerização** - Deploy fácil com Docker

---

## 🛠️ **Stack Tecnológico**

**Backend:** Python 3.13+ | Flask 3.1.2 | SQLAlchemy | SQLite | Pytest | Selenium | JMeter

**Frontend:** HTML5/CSS3 | JavaScript ES6+ | Bootstrap 5 | Chart.js | Font Awesome

**DevOps:** Docker | Docker Compose | Nginx | GitHub Actions | GitHub Pages

---

## 🚀 **Quick Start**

### **Pré-requisitos**
- Python 3.13+
- Docker (opcional)

### **Instalação Local**

```bash
# Clone o repositório
git clone https://github.com/Bella5900g/qa-test-dashboard.git
cd qa-test-dashboard

# Configure o ambiente Python
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Inicie o backend
python app.py
```

```bash
# Em outro terminal, inicie o frontend
cd frontend
python -m http.server 8000
```

### **Acesso**
- **Dashboard**: http://localhost:8000
- **API**: http://localhost:5000/api

### **Deploy com Docker**

```bash
# Build e execução completa
docker-compose up --build

# Acesso: http://localhost:80
```

---

## 📊 **Funcionalidades**

### **Dashboard Principal**
- ✅ **Métricas de Qualidade** - Taxa de sucesso, cobertura, bugs encontrados
- ✅ **Execuções Recentes** - Histórico completo de testes executados
- ✅ **Status dos Pipelines** - Monitoramento de CI/CD
- ✅ **Monitoramento do Sistema** - CPU, memória, disco, rede

### **Execução de Testes**
- ✅ **Testes Web** - Automação com Selenium
- ✅ **Testes de API** - Validação de endpoints REST
- ✅ **Testes de Performance** - Carga e stress com JMeter

### **Relatórios e Análises**
- ✅ **Relatórios HTML** - Documentação detalhada
- ✅ **Métricas de Performance** - Tempo de resposta, throughput
- ✅ **Análise de Tendências** - Evolução da qualidade ao longo do tempo

---

## 🔧 **API Endpoints**

```http
GET /api/metricas          # Métricas gerais
GET /api/execucoes         # Histórico de execuções
POST /api/executar-testes  # Executar testes
GET /api/sistema          # Status do sistema
GET /health               # Health check
```

---

## 🏗️ **Estrutura do Projeto**

```
qa-test-dashboard/
├── 📁 backend/           # API Flask
├── 📁 frontend/          # Interface web
├── 📁 automation/        # Testes automatizados
├── 📁 docker/           # Configurações Docker
└── 📁 docs/             # Documentação
```

---

## 🤝 **Contribuição**

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

---

## 📄 **Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👩‍💻 **Desenvolvedora**

<div align="center">

### **Isabella Vieira Barbosa**
**QA Chapter Lead | Automação & Performance**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/isabellavieiraqa/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/bella5900g)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-green?style=for-the-badge&logo=github)](https://bella5900g.github.io/isabella-vieira-portfolio/)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:bellacandy5900g@gmail.com)

</div>

**Sobre a Desenvolvedora:**
- 🎯 **QA Chapter Lead** com **10+ anos** de experiência
- 🏢 **Analista de QA Sênior** com 10+ anos de experiência
- 🏆 **Certificações**: ISTQB CTFL, ASTFCT
- 🚀 **Especialista** em automação, performance e liderança de QA

**Principais Conquistas:**
- ✅ **70%** redução de bugs em produção
- ✅ **30%** aceleração de releases
- ✅ **100%** retenção e promoção de analistas

---

<div align="center">

**💡 "Transformando qualidade em resultados mensuráveis"**

⭐ **Se este projeto foi útil para você, considere dar uma estrela!** ⭐

</div>