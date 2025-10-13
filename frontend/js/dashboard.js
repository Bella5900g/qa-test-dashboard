// QA Test Dashboard - JavaScript Principal
// Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

class DashboardQA {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000/api';
        this.graficos = {};
        this.intervaloAtualizacao = null;
        this.inicializar();
    }

    // Inicialização do Dashboard
    inicializar() {
        console.log('🚀 Inicializando QA Test Dashboard...');
        this.carregarDadosIniciais();
        this.configurarAtualizacaoAutomatica();
        this.configurarEventos();
        this.animarEntrada();
    }

    // Carregar dados iniciais
    async carregarDadosIniciais() {
        try {
            await Promise.all([
                this.atualizarMetricas(),
                this.carregarExecucoesRecentes(),
                this.carregarStatusPipelines(),
                this.atualizarMonitoramentoSistema()
            ]);
            console.log('✅ Dados iniciais carregados com sucesso');
        } catch (erro) {
            console.error('❌ Erro ao carregar dados iniciais:', erro);
            this.mostrarNotificacao('Erro ao carregar dados iniciais', 'danger');
        }
    }

    // Configurar atualização automática
    configurarAtualizacaoAutomatica() {
        // Atualizar a cada 30 segundos
        this.intervaloAtualizacao = setInterval(() => {
            this.atualizarMetricas();
            this.atualizarMonitoramentoSistema();
        }, 30000);
    }

    // Configurar eventos
    configurarEventos() {
        // Evento de atualização manual
        window.atualizarMetricas = () => this.atualizarMetricas();
        window.executarTestes = () => this.executarTestes();
        
        // Eventos de teclado
        document.addEventListener('keydown', (evento) => {
            if (evento.ctrlKey && evento.key === 'r') {
                evento.preventDefault();
                this.atualizarMetricas();
            }
        });
    }

    // Animar entrada dos elementos
    animarEntrada() {
        const elementos = document.querySelectorAll('.metricas-card, .card');
        elementos.forEach((elemento, indice) => {
            elemento.style.opacity = '0';
            elemento.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                elemento.style.transition = 'all 0.5s ease';
                elemento.style.opacity = '1';
                elemento.style.transform = 'translateY(0)';
            }, indice * 100);
        });
    }

    // Atualizar métricas principais
    async atualizarMetricas() {
        try {
            const resposta = await fetch(`${this.apiBaseUrl}/metricas`);
            const dados = await resposta.json();
            
            this.atualizarCardsMetricas(dados);
            this.atualizarGraficoTendencias(dados.tendencias);
            this.atualizarGraficoDistribuicao(dados.distribuicao);
            this.atualizarGraficoPerformance(dados.performance);
            this.atualizarUltimaAtualizacao();
            
        } catch (erro) {
            console.error('❌ Erro ao atualizar métricas:', erro);
            this.mostrarNotificacao('Erro ao atualizar métricas', 'warning');
        }
    }

    // Atualizar cards de métricas
    atualizarCardsMetricas(dados) {
        const elementos = {
            'taxa-sucesso': dados.taxaSucesso || 0,
            'tempo-medio': dados.tempoMedio || '0s',
            'cobertura': dados.cobertura || 0,
            'bugs-encontrados': dados.bugsEncontrados || 0
        };

        Object.entries(elementos).forEach(([id, valor]) => {
            const elemento = document.getElementById(id);
            if (elemento) {
                this.animarValor(elemento, valor);
            }
        });
    }

    // Animar mudança de valores
    animarValor(elemento, novoValor) {
        const valorAtual = elemento.textContent;
        if (valorAtual !== novoValor.toString()) {
            elemento.style.transform = 'scale(1.1)';
            elemento.style.color = '#007bff';
            
            setTimeout(() => {
                elemento.textContent = novoValor;
                elemento.style.transform = 'scale(1)';
                elemento.style.color = '';
            }, 150);
        }
    }

    // Atualizar gráfico de tendências
    atualizarGraficoTendencias(dados) {
        const ctx = document.getElementById('graficoTendencias');
        if (!ctx) return;

        if (this.graficos.tendencias) {
            this.graficos.tendencias.destroy();
        }

        this.graficos.tendencias = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dados?.datas || [],
                datasets: [{
                    label: 'Taxa de Sucesso (%)',
                    data: dados?.sucesso || [],
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#28a745',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }, {
                    label: 'Tempo Médio (s)',
                    data: dados?.tempo || [],
                    borderColor: '#17a2b8',
                    backgroundColor: 'rgba(23, 162, 184, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#17a2b8',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }

    // Atualizar gráfico de distribuição
    atualizarGraficoDistribuicao(dados) {
        const ctx = document.getElementById('graficoDistribuicao');
        if (!ctx) return;

        if (this.graficos.distribuicao) {
            this.graficos.distribuicao.destroy();
        }

        this.graficos.distribuicao = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: dados?.tipos || ['Web', 'API', 'Performance'],
                datasets: [{
                    data: dados?.quantidades || [30, 25, 15],
                    backgroundColor: [
                        '#007bff',
                        '#28a745',
                        '#ffc107',
                        '#dc3545',
                        '#17a2b8'
                    ],
                    borderWidth: 3,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 15
                        }
                    }
                }
            }
        });
    }

    // Atualizar gráfico de performance
    atualizarGraficoPerformance(dados) {
        const ctx = document.getElementById('graficoPerformance');
        if (!ctx) return;

        if (this.graficos.performance) {
            this.graficos.performance.destroy();
        }

        this.graficos.performance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dados?.testes || ['Login', 'Navegação', 'Formulários', 'API'],
                datasets: [{
                    label: 'Tempo de Execução (ms)',
                    data: dados?.tempos || [1200, 800, 1500, 600],
                    backgroundColor: [
                        'rgba(0, 123, 255, 0.8)',
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        '#007bff',
                        '#28a745',
                        '#ffc107',
                        '#dc3545'
                    ],
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // Carregar execuções recentes
    async carregarExecucoesRecentes() {
        try {
            const resposta = await fetch(`${this.apiBaseUrl}/execucoes`);
            const execucoes = await resposta.json();
            
            const tbody = document.getElementById('tabela-execucoes');
            if (!tbody) return;

            tbody.innerHTML = '';
            
            execucoes.forEach(execucao => {
                const linha = this.criarLinhaExecucao(execucao);
                tbody.appendChild(linha);
            });

        } catch (erro) {
            console.error('❌ Erro ao carregar execuções:', erro);
        }
    }

    // Criar linha da tabela de execuções
    criarLinhaExecucao(execucao) {
        const linha = document.createElement('tr');
        linha.className = 'fade-in';
        
        const statusBadge = this.criarBadgeStatus(execucao.status);
        const acoes = this.criarBotoesAcoes(execucao.id);
        
        linha.innerHTML = `
            <td><strong>#${execucao.id}</strong></td>
            <td><span class="badge bg-secondary">${execucao.tipo}</span></td>
            <td>${statusBadge}</td>
            <td>${execucao.duracao}</td>
            <td>${this.formatarDataHora(execucao.data_criacao)}</td>
            <td>${acoes}</td>
        `;
        
        return linha;
    }

    // Criar badge de status
    criarBadgeStatus(status) {
        const classes = {
            'sucesso': 'badge bg-success',
            'falha': 'badge bg-danger',
            'executando': 'badge bg-warning',
            'pendente': 'badge bg-info'
        };
        
        const icones = {
            'sucesso': 'fas fa-check',
            'falha': 'fas fa-times',
            'executando': 'fas fa-spinner fa-spin',
            'pendente': 'fas fa-clock'
        };
        
        const classe = classes[status] || classes['pendente'];
        const icone = icones[status] || icones['pendente'];
        
        return `<span class="${classe}"><i class="${icone} me-1"></i>${status.toUpperCase()}</span>`;
    }

    // Criar botões de ações
    criarBotoesAcoes(id) {
        return `
            <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary" onclick="dashboard.verDetalhes(${id})" title="Ver Detalhes">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-outline-success" onclick="dashboard.baixarRelatorio(${id})" title="Baixar Relatório">
                    <i class="fas fa-download"></i>
                </button>
            </div>
        `;
    }

    // Carregar status dos pipelines
    async carregarStatusPipelines() {
        try {
            const resposta = await fetch(`${this.apiBaseUrl}/pipelines`);
            const pipelines = await resposta.json();
            
            const container = document.getElementById('status-pipelines');
            if (!container) return;

            container.innerHTML = '';
            
            pipelines.forEach(pipeline => {
                const item = this.criarItemPipeline(pipeline);
                container.appendChild(item);
            });

        } catch (erro) {
            console.error('❌ Erro ao carregar pipelines:', erro);
        }
    }

    // Criar item de pipeline
    criarItemPipeline(pipeline) {
        const item = document.createElement('div');
        item.className = 'pipeline-item slide-in-left';
        
        const statusClass = `status-${pipeline.status}`;
        const statusIcon = this.getStatusIcon(pipeline.status);
        
        item.innerHTML = `
            <div>
                <div class="pipeline-nome">${pipeline.nome}</div>
                <small class="text-muted">${pipeline.ultimaExecucao}</small>
            </div>
            <div class="pipeline-status">
                <div class="status-indicador ${statusClass}"></div>
                <span class="badge bg-${this.getStatusColor(pipeline.status)}">${statusIcon}</span>
            </div>
        `;
        
        return item;
    }

    // Obter ícone do status
    getStatusIcon(status) {
        const icones = {
            'sucesso': 'fas fa-check',
            'falha': 'fas fa-times',
            'executando': 'fas fa-spinner fa-spin',
            'pendente': 'fas fa-clock'
        };
        return icones[status] || icones['pendente'];
    }

    // Obter cor do status
    getStatusColor(status) {
        const cores = {
            'sucesso': 'success',
            'falha': 'danger',
            'executando': 'warning',
            'pendente': 'info'
        };
        return cores[status] || 'secondary';
    }

    // Atualizar monitoramento do sistema
    async atualizarMonitoramentoSistema() {
        try {
            const resposta = await fetch(`${this.apiBaseUrl}/sistema`);
            const dados = await resposta.json();
            
            this.atualizarBarraProgresso('cpu-usage', 'cpu-texto', dados.cpu);
            this.atualizarBarraProgresso('memory-usage', 'memory-texto', dados.memoria);
            this.atualizarBarraProgresso('disk-usage', 'disk-texto', dados.disco);
            this.atualizarBarraProgresso('network-usage', 'network-texto', dados.rede);

        } catch (erro) {
            console.error('❌ Erro ao atualizar monitoramento:', erro);
        }
    }

    // Atualizar barra de progresso
    atualizarBarraProgresso(idBarra, idTexto, valor) {
        const barra = document.getElementById(idBarra);
        const texto = document.getElementById(idTexto);
        
        if (barra && texto) {
            barra.style.width = `${valor}%`;
            texto.textContent = `${valor}%`;
            
            // Mudar cor baseada no valor
            barra.className = 'progress-bar';
            if (valor > 80) {
                barra.classList.add('bg-danger');
            } else if (valor > 60) {
                barra.classList.add('bg-warning');
            } else {
                barra.classList.add('bg-success');
            }
        }
    }

    // Executar testes
    async executarTestes() {
        const modal = new bootstrap.Modal(document.getElementById('modalCarregando'));
        modal.show();
        
        try {
            const resposta = await fetch(`${this.apiBaseUrl}/executar-testes`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tipo: 'completo',
                    ambiente: 'desenvolvimento'
                })
            });
            
            const resultado = await resposta.json();
            
            modal.hide();
            this.mostrarNotificacao('Testes executados com sucesso!', 'success');
            
            // Atualizar dados após execução
            setTimeout(() => {
                this.atualizarMetricas();
                this.carregarExecucoesRecentes();
            }, 1000);
            
        } catch (erro) {
            modal.hide();
            console.error('❌ Erro ao executar testes:', erro);
            this.mostrarNotificacao('Erro ao executar testes', 'danger');
        }
    }

    // Ver detalhes da execução
    verDetalhes(id) {
        this.mostrarNotificacao(`Visualizando detalhes da execução #${id}`, 'info');
        // Implementar modal de detalhes
    }

    // Baixar relatório
    baixarRelatorio(id) {
        this.mostrarNotificacao(`Baixando relatório da execução #${id}`, 'info');
        // Implementar download do relatório
    }

    // Atualizar última atualização
    atualizarUltimaAtualizacao() {
        const elemento = document.getElementById('ultima-atualizacao');
        if (elemento) {
            elemento.textContent = new Date().toLocaleString('pt-BR');
        }
    }

    // Mostrar notificação
    mostrarNotificacao(mensagem, tipo = 'info') {
        const alerta = document.createElement('div');
        alerta.className = `alert alert-${tipo} alert-dismissible fade show position-fixed`;
        alerta.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        alerta.innerHTML = `
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alerta);
        
        // Remover automaticamente após 5 segundos
        setTimeout(() => {
            if (alerta.parentNode) {
                alerta.remove();
            }
        }, 5000);
    }

    // Formatar data e hora
    formatarDataHora(dataHora) {
        if (!dataHora) return 'N/A';
        
        try {
            const data = new Date(dataHora);
            if (isNaN(data.getTime())) {
                return 'Data inválida';
            }
            return data.toLocaleString('pt-BR', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (erro) {
            console.error('Erro ao formatar data:', erro);
            return 'Data inválida';
        }
    }

    // Limpar recursos
    destruir() {
        if (this.intervaloAtualizacao) {
            clearInterval(this.intervaloAtualizacao);
        }
        
        Object.values(this.graficos).forEach(grafico => {
            if (grafico && typeof grafico.destroy === 'function') {
                grafico.destroy();
            }
        });
    }
}

// Inicializar dashboard quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DashboardQA();
});

// Limpar recursos quando a página for fechada
window.addEventListener('beforeunload', () => {
    if (window.dashboard) {
        window.dashboard.destruir();
    }
});
