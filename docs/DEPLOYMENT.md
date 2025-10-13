# 🚀 Guia de Deploy - QA Test Automation Dashboard

## 📋 Visão Geral

Este guia fornece instruções completas para deploy do QA Test Automation Dashboard em diferentes ambientes, desde desenvolvimento local até produção.

## 🛠️ Pré-requisitos

### Requisitos do Sistema
- **Python:** 3.8 ou superior
- **Node.js:** 16 ou superior (opcional, para desenvolvimento)
- **Docker:** 20.10 ou superior
- **Docker Compose:** 2.0 ou superior
- **Git:** 2.30 ou superior

### Recursos Mínimos
- **CPU:** 2 cores
- **RAM:** 4GB
- **Disco:** 10GB livres
- **Rede:** Conexão estável com internet

## 🏠 Deploy Local (Desenvolvimento)

### 1. Clone do Repositório
```bash
git clone <repository-url>
cd qa-test-dashboard
```

### 2. Configuração do Backend
```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python app.py
```

### 3. Configuração do Frontend
```bash
cd frontend

# Servir arquivos estáticos
# Opção 1: Python
python -m http.server 8000

# Opção 2: Node.js
npx serve -s . -l 8000

# Opção 3: Abrir diretamente no navegador
# Abrir index.html no navegador
```

### 4. Verificação
- **Backend:** http://localhost:5000
- **Frontend:** http://localhost:8000
- **API Health:** http://localhost:5000/health

## 🐳 Deploy com Docker

### 1. Deploy Básico
```bash
# Build e execução
docker-compose up --build

# Execução em background
docker-compose up -d --build
```

### 2. Deploy com Perfis Específicos
```bash
# Apenas serviços principais
docker-compose --profile main up -d

# Com monitoramento
docker-compose --profile main --profile monitoring up -d

# Com logging
docker-compose --profile main --profile logging up -d

# Com testes
docker-compose --profile main --profile testing up -d
```

### 3. Verificação dos Containers
```bash
# Status dos containers
docker-compose ps

# Logs dos serviços
docker-compose logs backend
docker-compose logs frontend

# Health check
curl http://localhost/health
```

## ☁️ Deploy em Produção

### 1. Preparação do Servidor

#### Ubuntu/Debian
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
```

#### CentOS/RHEL
```bash
# Instalar Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io

# Iniciar Docker
sudo systemctl start docker
sudo systemctl enable docker

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Configuração de Produção

#### Arquivo de Ambiente
```bash
# Criar arquivo .env
cat > .env << EOF
# Configurações de Produção
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE_URL=sqlite:///data/qa_dashboard.db

# Configurações de Segurança
SECRET_KEY=your-super-secret-key-here
CORS_ORIGINS=https://yourdomain.com

# Configurações de Monitoramento
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true

# Configurações de Backup
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * *
EOF
```

#### Docker Compose de Produção
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile
      target: production
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile
      target: frontend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped
```

### 3. Deploy em Produção
```bash
# Clone do repositório
git clone <repository-url>
cd qa-test-dashboard

# Configurar ambiente
cp .env.example .env
# Editar .env com suas configurações

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Verificar status
docker-compose -f docker-compose.prod.yml ps
```

## 🌐 Deploy com Nginx (Proxy Reverso)

### 1. Configuração do Nginx
```nginx
# /etc/nginx/sites-available/qa-dashboard
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Frontend
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # API
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
        add_header Access-Control-Allow-Headers "Origin, X-Requested-With, Content-Type, Accept, Authorization";
    }
}
```

### 2. Ativar Site
```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/qa-dashboard /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Recarregar Nginx
sudo systemctl reload nginx
```

## 🔒 Configuração SSL/TLS

### 1. Let's Encrypt (Certbot)
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Renovação automática
sudo crontab -e
# Adicionar linha:
0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. Certificado Auto-assinado (Desenvolvimento)
```bash
# Gerar chave privada
openssl genrsa -out key.pem 2048

# Gerar certificado
openssl req -new -x509 -key key.pem -out cert.pem -days 365

# Copiar para diretório SSL
sudo mkdir -p /etc/nginx/ssl
sudo cp cert.pem key.pem /etc/nginx/ssl/
```

## 📊 Monitoramento e Logs

### 1. Configuração de Logs
```bash
# Criar diretórios de log
mkdir -p logs/{backend,frontend,nginx}

# Configurar rotação de logs
sudo tee /etc/logrotate.d/qa-dashboard << EOF
/opt/qa-dashboard/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
}
EOF
```

### 2. Monitoramento com Prometheus
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'qa-dashboard'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

### 3. Alertas
```yaml
# alerts.yml
groups:
  - name: qa-dashboard
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
```

## 🔄 Backup e Restore

### 1. Backup Automático
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/opt/backups/qa-dashboard"
DATE=$(date +%Y%m%d_%H%M%S)

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
docker exec qa-dashboard-backend sqlite3 /app/data/qa_dashboard.db ".backup $BACKUP_DIR/db_$DATE.db"

# Backup de configurações
cp -r /opt/qa-dashboard/config $BACKUP_DIR/config_$DATE

# Backup de logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /opt/qa-dashboard/logs

# Limpar backups antigos (manter 30 dias)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup concluído: $DATE"
```

### 2. Restore
```bash
#!/bin/bash
# restore.sh

BACKUP_FILE=$1
BACKUP_DIR="/opt/backups/qa-dashboard"

if [ -z "$BACKUP_FILE" ]; then
    echo "Uso: $0 <arquivo_backup>"
    exit 1
fi

# Parar serviços
docker-compose down

# Restaurar banco de dados
docker run --rm -v qa-dashboard_data:/data -v $BACKUP_DIR:/backup alpine cp /backup/$BACKUP_FILE /data/qa_dashboard.db

# Iniciar serviços
docker-compose up -d

echo "Restore concluído: $BACKUP_FILE"
```

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. Container não inicia
```bash
# Verificar logs
docker-compose logs backend

# Verificar recursos
docker stats

# Verificar portas
netstat -tulpn | grep :5000
```

#### 2. Erro de permissão
```bash
# Corrigir permissões
sudo chown -R $USER:$USER /opt/qa-dashboard
chmod -R 755 /opt/qa-dashboard
```

#### 3. Problema de conectividade
```bash
# Testar conectividade
curl -v http://localhost:5000/health

# Verificar firewall
sudo ufw status
sudo ufw allow 80
sudo ufw allow 443
```

#### 4. Problema de memória
```bash
# Verificar uso de memória
free -h
docker system df

# Limpar recursos Docker
docker system prune -a
```

### Logs de Debug
```bash
# Ativar logs detalhados
export FLASK_DEBUG=1
export FLASK_ENV=development

# Logs do sistema
journalctl -u docker -f

# Logs da aplicação
tail -f logs/backend/app.log
```

## 📈 Otimização de Performance

### 1. Configurações do Docker
```yaml
# docker-compose.override.yml
version: '3.8'

services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
    environment:
      - WORKERS=4
      - TIMEOUT=30
```

### 2. Configurações do Nginx
```nginx
# Otimizações de performance
worker_processes auto;
worker_connections 1024;

http {
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    
    # Caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🔧 Manutenção

### 1. Atualizações
```bash
# Atualizar código
git pull origin main

# Rebuild containers
docker-compose build --no-cache

# Deploy com zero downtime
docker-compose up -d --force-recreate
```

### 2. Limpeza
```bash
# Limpeza semanal
docker system prune -f
docker volume prune -f

# Limpeza de logs
find logs/ -name "*.log" -mtime +30 -delete
```

### 3. Monitoramento de Saúde
```bash
# Health check script
#!/bin/bash
curl -f http://localhost/health || {
    echo "Health check failed"
    # Enviar alerta
    exit 1
}
```

## 📞 Suporte

Para problemas de deploy:
- **Documentação:** [Link para docs]
- **Issues:** [Link para issues]
- **Email:** [seu-email@exemplo.com]

---

**🚀 Guia de Deploy - QA Test Automation Dashboard v1.0.0**
