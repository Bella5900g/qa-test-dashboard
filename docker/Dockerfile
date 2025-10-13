# QA Test Automation Dashboard - Dockerfile
# Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

# Multi-stage build para otimização
FROM python:3.11-slim as base

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# STAGE 1: Backend API
# =============================================================================
FROM base as backend

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY backend/ .

# Criar usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expor porta
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando para iniciar a aplicação
CMD ["python", "app.py"]

# =============================================================================
# STAGE 2: Frontend
# =============================================================================
FROM nginx:alpine as frontend

# Copiar arquivos do frontend
COPY frontend/ /usr/share/nginx/html/

# Configurar nginx
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Expor porta
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# =============================================================================
# STAGE 3: Testes
# =============================================================================
FROM base as tests

# Instalar dependências para testes
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Definir variáveis para Chrome headless
ENV CHROME_BIN=/usr/bin/chromium \
    CHROME_PATH=/usr/bin/chromium \
    DISPLAY=:99

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código dos testes
COPY automation/ ./automation/
COPY backend/ ./backend/

# Criar diretórios para resultados
RUN mkdir -p /app/results /app/reports

# Script para executar testes
COPY docker/run_tests.sh /app/run_tests.sh
RUN chmod +x /app/run_tests.sh

# Comando padrão
CMD ["/app/run_tests.sh"]

# =============================================================================
# STAGE 4: Production (Multi-service)
# =============================================================================
FROM base as production

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY backend/ .
COPY frontend/ /var/www/html/

# Configurar nginx
COPY docker/nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Configurar supervisor
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app \
    && chown -R app:app /var/www/html

# Expor portas
EXPOSE 80 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Comando para iniciar todos os serviços
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
