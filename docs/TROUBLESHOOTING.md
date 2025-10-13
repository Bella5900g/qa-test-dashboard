# 🔧 Guia de Troubleshooting - QA Test Automation Dashboard

## 📋 Visão Geral

Este guia fornece soluções para problemas comuns encontrados durante o uso do QA Test Automation Dashboard, desde problemas de instalação até questões de performance.

## 🚨 Problemas Críticos

### 1. Aplicação não inicia

#### Sintomas
- Erro ao executar `python app.py`
- Container Docker não inicia
- Porta 5000 não responde

#### Soluções

**Problema de Dependências Python:**
```bash
# Verificar versão do Python
python --version

# Recriar ambiente virtual
rm -rf venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Reinstalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

**Problema de Porta em Uso:**
```bash
# Verificar processos na porta 5000
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Matar processo se necessário
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# Usar porta alternativa
export FLASK_RUN_PORT=5001
python app.py
```

**Problema de Permissões:**
```bash
# Corrigir permissões
chmod +x app.py
chmod -R 755 backend/
```

### 2. Banco de dados não funciona

#### Sintomas
- Erro "database is locked"
- Tabelas não são criadas
- Dados não persistem

#### Soluções

**Problema de Lock do SQLite:**
```bash
# Verificar processos usando o banco
lsof qa_dashboard.db

# Remover arquivo de lock
rm -f qa_dashboard.db-journal
rm -f qa_dashboard.db-wal
rm -f qa_dashboard.db-shm

# Recriar banco
rm -f qa_dashboard.db
python -c "from app import criar_aplicacao; app = criar_aplicacao()"
```

**Problema de Permissões do Banco:**
```bash
# Corrigir permissões
chmod 664 qa_dashboard.db
chown $USER:$USER qa_dashboard.db
```

### 3. Frontend não carrega

#### Sintomas
- Página em branco
- Erro 404 no navegador
- Recursos não carregam

#### Soluções

**Problema de CORS:**
```bash
# Verificar configuração CORS no backend
# Em app.py, verificar:
CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000'])
```

**Problema de Servidor Web:**
```bash
# Usar servidor HTTP adequado
cd frontend

# Python
python -m http.server 8000

# Node.js
npx serve -s . -l 8000

# Verificar se arquivos existem
ls -la index.html css/ js/
```

## 🧪 Problemas de Testes

### 1. Testes Selenium falham

#### Sintomas
- Erro "WebDriver not found"
- Timeout em elementos
- Screenshots não são gerados

#### Soluções

**Problema de WebDriver:**
```bash
# Instalar Chrome/Chromium
sudo apt install chromium-browser  # Ubuntu/Debian
brew install chromium  # macOS

# Verificar versão do Chrome
google-chrome --version

# Atualizar webdriver-manager
pip install --upgrade webdriver-manager
```

**Problema de Timeout:**
```python
# Aumentar timeout nos testes
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "elemento"))
)
```

**Problema de Headless:**
```python
# Configurar Chrome headless corretamente
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
```

### 2. Testes de API falham

#### Sintomas
- Erro de conexão
- Timeout em requisições
- Status codes inesperados

#### Soluções

**Problema de Conectividade:**
```bash
# Verificar se backend está rodando
curl http://localhost:5000/health

# Verificar firewall
sudo ufw status
sudo ufw allow 5000
```

**Problema de Timeout:**
```python
# Aumentar timeout nas requisições
response = requests.get(url, timeout=30)
```

**Problema de Dados:**
```python
# Verificar se dados de teste existem
# Executar inicialização manual
python -c "from backend.app import inicializar_dados_exemplo; inicializar_dados_exemplo()"
```

### 3. Testes de Performance falham

#### Sintomas
- JMeter não encontrado
- Erro de memória
- Relatórios não gerados

#### Soluções

**Problema de JMeter:**
```bash
# Instalar JMeter
wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.5.tgz
tar -xzf apache-jmeter-5.5.tgz
export PATH=$PATH:./apache-jmeter-5.5/bin

# Verificar instalação
jmeter --version
```

**Problema de Memória:**
```bash
# Aumentar heap do JMeter
export HEAP="-Xms1g -Xmx4g -XX:MaxMetaspaceSize=256m"
jmeter -n -t script.jmx
```

## 🐳 Problemas de Docker

### 1. Container não inicia

#### Sintomas
- Erro "container exited with code 1"
- Logs mostram erro de dependência
- Porta não mapeada

#### Soluções

**Problema de Build:**
```bash
# Rebuild sem cache
docker-compose build --no-cache

# Verificar Dockerfile
docker build -f docker/Dockerfile --target backend .

# Verificar logs de build
docker-compose logs backend
```

**Problema de Porta:**
```bash
# Verificar mapeamento de portas
docker-compose ps

# Verificar se porta está em uso
netstat -tulpn | grep :5000

# Usar porta alternativa
# Em docker-compose.yml:
ports:
  - "5001:5000"
```

**Problema de Volume:**
```bash
# Verificar volumes
docker volume ls

# Limpar volumes órfãos
docker volume prune

# Recriar volumes
docker-compose down -v
docker-compose up -d
```

### 2. Problemas de Rede

#### Sintomas
- Containers não se comunicam
- Erro de DNS
- Timeout entre serviços

#### Soluções

**Problema de Rede Docker:**
```bash
# Verificar redes
docker network ls

# Recriar rede
docker-compose down
docker network prune
docker-compose up -d
```

**Problema de DNS:**
```bash
# Verificar resolução DNS
docker exec -it qa-dashboard-backend nslookup backend

# Usar IP ao invés de hostname
# Em docker-compose.yml:
extra_hosts:
  - "backend:172.20.0.2"
```

## 📊 Problemas de Performance

### 1. Aplicação lenta

#### Sintomas
- Tempo de resposta alto
- Interface travando
- Timeout em requisições

#### Soluções

**Problema de Recursos:**
```bash
# Verificar uso de CPU/RAM
htop
docker stats

# Aumentar recursos no docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 2G
```

**Problema de Banco:**
```bash
# Otimizar SQLite
sqlite3 qa_dashboard.db "PRAGMA optimize;"
sqlite3 qa_dashboard.db "VACUUM;"

# Verificar tamanho do banco
ls -lh qa_dashboard.db
```

**Problema de Cache:**
```python
# Implementar cache Redis
# Em app.py:
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### 2. Problemas de Memória

#### Sintomas
- Erro "out of memory"
- Aplicação trava
- Container é morto

#### Soluções

**Problema de Memory Leak:**
```bash
# Verificar uso de memória
docker stats --no-stream

# Limitar memória
docker run -m 1g qa-dashboard-backend

# Monitorar com htop
htop
```

**Problema de Garbage Collection:**
```python
# Forçar garbage collection
import gc
gc.collect()

# Configurar limites de memória
import resource
resource.setrlimit(resource.RLIMIT_AS, (1024*1024*1024, -1))
```

## 🔍 Problemas de Debug

### 1. Logs não aparecem

#### Sintomas
- Sem logs no console
- Arquivos de log vazios
- Erro não é registrado

#### Soluções

**Problema de Configuração de Log:**
```python
# Configurar logging adequadamente
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

**Problema de Permissões de Log:**
```bash
# Corrigir permissões
chmod 755 logs/
chmod 644 logs/*.log
```

### 2. Debug não funciona

#### Sintomas
- Breakpoints não param
- Variáveis não mostram valores
- Stack trace incompleto

#### Soluções

**Problema de Debugger:**
```python
# Usar pdb para debug
import pdb; pdb.set_trace()

# Ou usar ipdb
import ipdb; ipdb.set_trace()
```

**Problema de IDE:**
```bash
# Configurar VS Code
# .vscode/launch.json:
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "program": "app.py",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            }
        }
    ]
}
```

## 🛠️ Ferramentas de Diagnóstico

### 1. Scripts de Diagnóstico

**health-check.sh:**
```bash
#!/bin/bash
echo "=== QA Dashboard Health Check ==="

# Verificar Python
echo "Python version:"
python --version

# Verificar dependências
echo "Dependencies:"
pip list | grep -E "(Flask|SQLAlchemy|pytest)"

# Verificar banco
echo "Database:"
ls -la qa_dashboard.db

# Verificar portas
echo "Ports:"
netstat -tulpn | grep -E ":(5000|8000)"

# Verificar processos
echo "Processes:"
ps aux | grep -E "(python|flask)"

# Testar API
echo "API Test:"
curl -f http://localhost:5000/health || echo "API not responding"
```

**system-info.sh:**
```bash
#!/bin/bash
echo "=== System Information ==="

# Sistema
echo "OS:"
uname -a

# Recursos
echo "CPU:"
lscpu | grep "Model name"

echo "Memory:"
free -h

echo "Disk:"
df -h

# Docker
echo "Docker:"
docker --version
docker-compose --version

# Network
echo "Network:"
ip addr show
```

### 2. Comandos Úteis

```bash
# Verificar logs em tempo real
docker-compose logs -f backend

# Entrar no container
docker exec -it qa-dashboard-backend bash

# Verificar variáveis de ambiente
docker exec qa-dashboard-backend env

# Testar conectividade
docker exec qa-dashboard-backend curl http://localhost:5000/health

# Verificar volumes
docker volume inspect qa-test-dashboard_backend_data

# Limpar recursos Docker
docker system prune -a
docker volume prune
docker network prune
```

## 📞 Suporte e Recursos

### 1. Logs Importantes

**Localização dos Logs:**
- **Backend:** `logs/backend/app.log`
- **Frontend:** `logs/frontend/access.log`
- **Docker:** `docker-compose logs`
- **Sistema:** `/var/log/syslog`

### 2. Arquivos de Configuração

**Arquivos Importantes:**
- `backend/app.py` - Aplicação principal
- `backend/requirements.txt` - Dependências Python
- `docker-compose.yml` - Configuração Docker
- `frontend/index.html` - Interface principal

### 3. Contatos de Suporte

- **Documentação:** [Link para docs]
- **Issues:** [Link para issues do GitHub]
- **Email:** [seu-email@exemplo.com]
- **LinkedIn:** [seu-linkedin]

### 4. Recursos Adicionais

- **Flask Documentation:** https://flask.palletsprojects.com/
- **Docker Documentation:** https://docs.docker.com/
- **Selenium Documentation:** https://selenium-python.readthedocs.io/
- **Pytest Documentation:** https://docs.pytest.org/

---

**🔧 Guia de Troubleshooting - QA Test Automation Dashboard v1.0.0**
