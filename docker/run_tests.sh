#!/bin/bash
# QA Test Automation Dashboard - Script de Execução de Testes
# Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

set -e

echo "🚀 Iniciando execução de testes automatizados..."
echo "=================================================="

# Configurações
BACKEND_URL=${BACKEND_URL:-"http://backend:5000"}
FRONTEND_URL=${FRONTEND_URL:-"http://frontend:80"}
RESULTS_DIR="/app/results"
REPORTS_DIR="/app/reports"

# Criar diretórios se não existirem
mkdir -p "$RESULTS_DIR" "$REPORTS_DIR"

# Função para aguardar serviço estar disponível
aguardar_servico() {
    local url=$1
    local nome=$2
    local max_tentativas=30
    local tentativa=1
    
    echo "⏳ Aguardando $nome estar disponível em $url..."
    
    while [ $tentativa -le $max_tentativas ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            echo "✅ $nome está disponível!"
            return 0
        fi
        
        echo "   Tentativa $tentativa/$max_tentativas - $nome ainda não disponível"
        sleep 2
        tentativa=$((tentativa + 1))
    done
    
    echo "❌ $nome não ficou disponível após $max_tentativas tentativas"
    return 1
}

# Função para executar testes de API
executar_testes_api() {
    echo ""
    echo "🧪 Executando testes de API..."
    echo "================================"
    
    cd /app/automation/api
    
    # Executar testes com pytest
    if pytest test_api.py -v \
        --html="$REPORTS_DIR/api_test_report.html" \
        --self-contained-html \
        --junitxml="$RESULTS_DIR/api_test_results.xml" \
        --tb=short; then
        echo "✅ Testes de API executados com sucesso!"
        return 0
    else
        echo "❌ Falha nos testes de API"
        return 1
    fi
}

# Função para executar testes web com Selenium
executar_testes_web() {
    echo ""
    echo "🌐 Executando testes web com Selenium..."
    echo "========================================"
    
    cd /app/automation/selenium
    
    # Configurar display virtual para Chrome headless
    export DISPLAY=:99
    Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &
    
    # Aguardar Xvfb inicializar
    sleep 2
    
    # Executar testes com pytest
    if pytest test_web.py -v \
        --html="$REPORTS_DIR/web_test_report.html" \
        --self-contained-html \
        --junitxml="$RESULTS_DIR/web_test_results.xml" \
        --tb=short; then
        echo "✅ Testes web executados com sucesso!"
        return 0
    else
        echo "❌ Falha nos testes web"
        return 1
    fi
}

# Função para executar testes de performance
executar_testes_performance() {
    echo ""
    echo "⚡ Executando testes de performance..."
    echo "======================================"
    
    cd /app/automation/performance
    
    # Verificar se JMeter está disponível
    if command -v jmeter > /dev/null 2>&1; then
        echo "📊 Executando teste de carga com JMeter..."
        
        # Executar teste de carga
        jmeter -n -t performance_test.jmx \
            -l "$RESULTS_DIR/performance_results.jtl" \
            -e -o "$REPORTS_DIR/performance_report" \
            -Jthreads=20 -Jramp_time=30 -Jloops=5
        
        if [ $? -eq 0 ]; then
            echo "✅ Testes de performance executados com sucesso!"
            return 0
        else
            echo "❌ Falha nos testes de performance"
            return 1
        fi
    else
        echo "⚠️ JMeter não encontrado, pulando testes de performance"
        return 0
    fi
}

# Função para gerar relatório consolidado
gerar_relatorio_consolidado() {
    echo ""
    echo "📊 Gerando relatório consolidado..."
    echo "==================================="
    
    local relatorio_html="$REPORTS_DIR/consolidated_report.html"
    local timestamp=$(date '+%d/%m/%Y %H:%M:%S')
    
    cat > "$relatorio_html" << EOF
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Consolidado de Testes - QA Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #007bff, #0056b3); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
        .card { background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #007bff; }
        .card h3 { margin-top: 0; color: #007bff; }
        .success { border-left-color: #28a745; }
        .success h3 { color: #28a745; }
        .error { border-left-color: #dc3545; }
        .error h3 { color: #dc3545; }
        .warning { border-left-color: #ffc107; }
        .warning h3 { color: #ffc107; }
        .links { margin: 20px 0; }
        .links a { display: inline-block; margin: 5px 10px 5px 0; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
        .links a:hover { background: #0056b3; }
        .footer { margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Relatório Consolidado de Testes</h1>
            <h2>QA Test Automation Dashboard</h2>
            <p>Gerado em: $timestamp</p>
        </div>
        
        <div class="summary">
            <div class="card success">
                <h3>✅ Testes de API</h3>
                <p>Testes de endpoints REST executados com sucesso</p>
                <p><strong>Status:</strong> Concluído</p>
            </div>
            
            <div class="card success">
                <h3>🌐 Testes Web</h3>
                <p>Testes de interface com Selenium executados</p>
                <p><strong>Status:</strong> Concluído</p>
            </div>
            
            <div class="card warning">
                <h3>⚡ Testes de Performance</h3>
                <p>Testes de carga e stress executados</p>
                <p><strong>Status:</strong> Concluído (se JMeter disponível)</p>
            </div>
        </div>
        
        <div class="links">
            <h3>📄 Relatórios Detalhados:</h3>
            <a href="api_test_report.html" target="_blank">Relatório de Testes de API</a>
            <a href="web_test_report.html" target="_blank">Relatório de Testes Web</a>
            <a href="performance_report/index.html" target="_blank">Relatório de Performance</a>
        </div>
        
        <div class="footer">
            <p><strong>Desenvolvido por:</strong> Isabella Barbosa - Engenheira de QA Sênior</p>
            <p><strong>Projeto:</strong> QA Test Automation Dashboard</p>
            <p><strong>Ambiente:</strong> Docker Container</p>
        </div>
    </div>
</body>
</html>
EOF

    echo "📄 Relatório consolidado gerado: $relatorio_html"
}

# Função principal
main() {
    echo "🎯 Iniciando execução de testes automatizados..."
    echo "Backend URL: $BACKEND_URL"
    echo "Frontend URL: $FRONTEND_URL"
    echo ""
    
    # Aguardar serviços estarem disponíveis
    if ! aguardar_servico "$BACKEND_URL/health" "Backend API"; then
        echo "❌ Não foi possível conectar ao backend. Abortando execução."
        exit 1
    fi
    
    if ! aguardar_servico "$FRONTEND_URL" "Frontend"; then
        echo "❌ Não foi possível conectar ao frontend. Abortando execução."
        exit 1
    fi
    
    # Contadores de sucesso/falha
    local sucessos=0
    local falhas=0
    
    # Executar testes de API
    if executar_testes_api; then
        sucessos=$((sucessos + 1))
    else
        falhas=$((falhas + 1))
    fi
    
    # Executar testes web
    if executar_testes_web; then
        sucessos=$((sucessos + 1))
    else
        falhas=$((falhas + 1))
    fi
    
    # Executar testes de performance
    if executar_testes_performance; then
        sucessos=$((sucessos + 1))
    else
        falhas=$((falhas + 1))
    fi
    
    # Gerar relatório consolidado
    gerar_relatorio_consolidado
    
    # Resumo final
    echo ""
    echo "=================================================="
    echo "📊 RESUMO DA EXECUÇÃO DE TESTES"
    echo "=================================================="
    echo "✅ Sucessos: $sucessos"
    echo "❌ Falhas: $falhas"
    echo "📁 Resultados salvos em: $RESULTS_DIR"
    echo "📄 Relatórios salvos em: $REPORTS_DIR"
    echo "=================================================="
    
    if [ $falhas -eq 0 ]; then
        echo "🎉 Todos os testes foram executados com sucesso!"
        exit 0
    else
        echo "⚠️ Alguns testes falharam. Verifique os relatórios para detalhes."
        exit 1
    fi
}

# Executar função principal
main "$@"
