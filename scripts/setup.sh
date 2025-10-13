#!/bin/bash
# QA Test Automation Dashboard - Script de Setup
# Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

set -e

echo "🚀 QA Test Automation Dashboard - Setup"
echo "========================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para verificar versão do Python
check_python() {
    print_message $BLUE "🐍 Verificando Python..."
    
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_message $GREEN "✅ Python $PYTHON_VERSION encontrado"
        return 0
    elif command_exists python; then
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        if [[ $PYTHON_VERSION == 3.* ]]; then
            print_message $GREEN "✅ Python $PYTHON_VERSION encontrado"
            return 0
        else
            print_message $RED "❌ Python 3 é necessário. Versão encontrada: $PYTHON_VERSION"
            return 1
        fi
    else
        print_message $RED "❌ Python não encontrado"
        return 1
    fi
}

# Função para verificar Node.js
check_node() {
    print_message $BLUE "📦 Verificando Node.js..."
    
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_message $GREEN "✅ Node.js $NODE_VERSION encontrado"
        return 0
    else
        print_message $YELLOW "⚠️ Node.js não encontrado (opcional para desenvolvimento)"
        return 1
    fi
}

# Função para verificar Docker
check_docker() {
    print_message $BLUE "🐳 Verificando Docker..."
    
    if command_exists docker; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        print_message $GREEN "✅ Docker $DOCKER_VERSION encontrado"
        
        if command_exists docker-compose; then
            COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | cut -d',' -f1)
            print_message $GREEN "✅ Docker Compose $COMPOSE_VERSION encontrado"
            return 0
        else
            print_message $YELLOW "⚠️ Docker Compose não encontrado"
            return 1
        fi
    else
        print_message $YELLOW "⚠️ Docker não encontrado (opcional)"
        return 1
    fi
}

# Função para configurar ambiente Python
setup_python_env() {
    print_message $BLUE "🔧 Configurando ambiente Python..."
    
    cd backend
    
    # Criar ambiente virtual
    if [ ! -d "venv" ]; then
        print_message $BLUE "📁 Criando ambiente virtual..."
        python3 -m venv venv
    fi
    
    # Ativar ambiente virtual
    print_message $BLUE "🔄 Ativando ambiente virtual..."
    source venv/bin/activate
    
    # Atualizar pip
    print_message $BLUE "⬆️ Atualizando pip..."
    pip install --upgrade pip
    
    # Instalar dependências
    print_message $BLUE "📦 Instalando dependências Python..."
    pip install -r requirements.txt
    
    print_message $GREEN "✅ Ambiente Python configurado com sucesso!"
    cd ..
}

# Função para configurar frontend
setup_frontend() {
    print_message $BLUE "🎨 Configurando frontend..."
    
    cd frontend
    
    # Verificar se arquivos existem
    if [ ! -f "index.html" ]; then
        print_message $RED "❌ Arquivo index.html não encontrado"
        return 1
    fi
    
    print_message $GREEN "✅ Frontend configurado com sucesso!"
    cd ..
}

# Função para configurar testes
setup_tests() {
    print_message $BLUE "🧪 Configurando testes..."
    
    # Criar diretórios necessários
    mkdir -p automation/selenium/screenshots
    mkdir -p automation/api/results
    mkdir -p automation/performance/results
    
    # Verificar dependências para testes
    if command_exists chromedriver; then
        print_message $GREEN "✅ ChromeDriver encontrado"
    else
        print_message $YELLOW "⚠️ ChromeDriver não encontrado (será baixado automaticamente)"
    fi
    
    print_message $GREEN "✅ Testes configurados com sucesso!"
}

# Função para configurar Docker
setup_docker() {
    print_message $BLUE "🐳 Configurando Docker..."
    
    if command_exists docker && command_exists docker-compose; then
        # Criar diretórios para volumes
        mkdir -p data logs results reports
        
        # Build das imagens
        print_message $BLUE "🏗️ Construindo imagens Docker..."
        docker-compose build
        
        print_message $GREEN "✅ Docker configurado com sucesso!"
    else
        print_message $YELLOW "⚠️ Docker não disponível, pulando configuração"
    fi
}

# Função para inicializar banco de dados
init_database() {
    print_message $BLUE "🗄️ Inicializando banco de dados..."
    
    cd backend
    source venv/bin/activate
    
    # Executar script de inicialização
    python -c "
from app import criar_aplicacao
app = criar_aplicacao()
print('✅ Banco de dados inicializado com sucesso!')
"
    
    cd ..
}

# Função para executar testes iniciais
run_initial_tests() {
    print_message $BLUE "🧪 Executando testes iniciais..."
    
    cd backend
    source venv/bin/activate
    
    # Executar testes básicos
    if python -c "import flask, sqlalchemy, pytest" 2>/dev/null; then
        print_message $GREEN "✅ Dependências Python OK"
    else
        print_message $RED "❌ Problema com dependências Python"
        return 1
    fi
    
    cd ..
    print_message $GREEN "✅ Testes iniciais executados com sucesso!"
}

# Função para mostrar informações finais
show_final_info() {
    print_message $GREEN "🎉 Setup concluído com sucesso!"
    echo ""
    print_message $BLUE "📋 Próximos passos:"
    echo ""
    echo "1. 🚀 Iniciar o backend:"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   python app.py"
    echo ""
    echo "2. 🎨 Iniciar o frontend:"
    echo "   cd frontend"
    echo "   python -m http.server 8000"
    echo ""
    echo "3. 🐳 Ou usar Docker:"
    echo "   docker-compose up -d"
    echo ""
    echo "4. 🌐 Acessar o dashboard:"
    echo "   http://localhost:8000"
    echo ""
    echo "5. 🔧 API disponível em:"
    echo "   http://localhost:5000/api"
    echo ""
    print_message $YELLOW "📚 Documentação disponível em: docs/"
    print_message $YELLOW "🔧 Troubleshooting: docs/TROUBLESHOOTING.md"
    echo ""
    print_message $GREEN "Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior"
}

# Função principal
main() {
    print_message $BLUE "🔍 Verificando pré-requisitos..."
    echo ""
    
    # Verificar pré-requisitos
    check_python || exit 1
    check_node || true
    check_docker || true
    
    echo ""
    print_message $BLUE "⚙️ Configurando ambiente..."
    echo ""
    
    # Configurar componentes
    setup_python_env
    setup_frontend
    setup_tests
    setup_docker
    
    echo ""
    print_message $BLUE "🗄️ Inicializando sistema..."
    echo ""
    
    # Inicializar sistema
    init_database
    run_initial_tests
    
    echo ""
    show_final_info
}

# Verificar se está no diretório correto
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_message $RED "❌ Execute este script no diretório raiz do projeto"
    exit 1
fi

# Executar função principal
main "$@"
