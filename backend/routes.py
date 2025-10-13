#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA Test Automation Dashboard - Rotas da API
Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

Endpoints REST para o dashboard de automação de testes.
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import random
from models import db, ExecucaoTeste, ResultadoTeste, ConfiguracaoSistema, PipelineCI, MetricaSistema

# Blueprints para organização das rotas
metricas_bp = Blueprint('metricas', __name__)
execucoes_bp = Blueprint('execucoes', __name__)
sistema_bp = Blueprint('sistema', __name__)
pipelines_bp = Blueprint('pipelines', __name__)

# =============================================================================
# ROTAS DE MÉTRICAS
# =============================================================================

@metricas_bp.route('/metricas', methods=['GET'])
def obter_metricas():
    """Retorna métricas gerais do dashboard"""
    try:
        # Métricas gerais
        metricas_gerais = ExecucaoTeste.get_metricas_gerais()
        
        # Tendências dos últimos 30 dias
        tendencias = ExecucaoTeste.get_tendencias(30)
        
        # Distribuição por tipo de teste
        distribuicao = db.session.query(
            ExecucaoTeste.tipo,
            db.func.count(ExecucaoTeste.id).label('quantidade')
        ).group_by(ExecucaoTeste.tipo).all()
        
        distribuicao_dict = {
            'tipos': [item.tipo for item in distribuicao],
            'quantidades': [item.quantidade for item in distribuicao]
        }
        
        # Performance dos testes (dados simulados para demonstração)
        performance = {
            'testes': ['Login', 'Navegação', 'Formulários', 'API', 'Performance'],
            'tempos': [1200, 800, 1500, 600, 3000]
        }
        
        # Calcular cobertura (simulada)
        total_testes = sum(distribuicao_dict['quantidades'])
        cobertura = min(95, 70 + (total_testes * 0.5))  # Simulação baseada no número de testes
        
        # Bugs encontrados (simulados)
        bugs_encontrados = random.randint(5, 25)
        
        return jsonify({
            'taxaSucesso': metricas_gerais['taxa_sucesso'],
            'tempoMedio': f"{metricas_gerais['tempo_medio']:.1f}s",
            'cobertura': round(cobertura, 1),
            'bugsEncontrados': bugs_encontrados,
            'tendencias': tendencias,
            'distribuicao': distribuicao_dict,
            'performance': performance,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@metricas_bp.route('/metricas/detalhadas', methods=['GET'])
def obter_metricas_detalhadas():
    """Retorna métricas detalhadas com mais informações"""
    try:
        # Execuções por status
        execucoes_por_status = db.session.query(
            ExecucaoTeste.status,
            db.func.count(ExecucaoTeste.id).label('quantidade')
        ).group_by(ExecucaoTeste.status).all()
        
        # Execuções por ambiente
        execucoes_por_ambiente = db.session.query(
            ExecucaoTeste.ambiente,
            db.func.count(ExecucaoTeste.id).label('quantidade')
        ).group_by(ExecucaoTeste.ambiente).all()
        
        # Tempo médio por tipo de teste
        tempo_por_tipo = db.session.query(
            ExecucaoTeste.tipo,
            db.func.avg(ExecucaoTeste.duracao).label('tempo_medio')
        ).group_by(ExecucaoTeste.tipo).all()
        
        return jsonify({
            'execucoes_por_status': {item.status: item.quantidade for item in execucoes_por_status},
            'execucoes_por_ambiente': {item.ambiente: item.quantidade for item in execucoes_por_ambiente},
            'tempo_por_tipo': {item.tipo: round(item.tempo_medio, 2) for item in tempo_por_tipo},
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# =============================================================================
# ROTAS DE EXECUÇÕES
# =============================================================================

@execucoes_bp.route('/execucoes', methods=['GET'])
def listar_execucoes():
    """Lista execuções de testes recentes"""
    try:
        limite = request.args.get('limite', 10, type=int)
        tipo = request.args.get('tipo')
        status = request.args.get('status')
        
        query = ExecucaoTeste.query
        
        if tipo:
            query = query.filter(ExecucaoTeste.tipo == tipo)
        if status:
            query = query.filter(ExecucaoTeste.status == status)
        
        execucoes = query.order_by(ExecucaoTeste.data_criacao.desc()).limit(limite).all()
        
        return jsonify([execucao.to_dict() for execucao in execucoes])
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@execucoes_bp.route('/execucoes/<int:execucao_id>', methods=['GET'])
def obter_execucao(execucao_id):
    """Obtém detalhes de uma execução específica"""
    try:
        execucao = ExecucaoTeste.query.get_or_404(execucao_id)
        return jsonify(execucao.to_dict())
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@execucoes_bp.route('/execucoes/<int:execucao_id>/resultados', methods=['GET'])
def obter_resultados_execucao(execucao_id):
    """Obtém resultados de uma execução específica"""
    try:
        execucao = ExecucaoTeste.query.get_or_404(execucao_id)
        resultados = ResultadoTeste.query.filter_by(execucao_id=execucao_id).all()
        
        return jsonify({
            'execucao': execucao.to_dict(),
            'resultados': [resultado.to_dict() for resultado in resultados]
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@execucoes_bp.route('/executar-testes', methods=['POST'])
def executar_testes():
    """Executa uma nova suite de testes"""
    try:
        dados = request.get_json() or {}
        tipo_teste = dados.get('tipo', 'completo')
        ambiente = dados.get('ambiente', 'desenvolvimento')
        
        # Criar nova execução
        execucao = ExecucaoTeste(
            tipo=tipo_teste,
            status='executando',
            duracao=0,
            ambiente=ambiente,
            observacoes=f'Execução iniciada via API - {datetime.now().strftime("%d/%m/%Y %H:%M")}'
        )
        
        db.session.add(execucao)
        db.session.commit()
        
        # Simular execução de testes (em produção, isso seria feito em background)
        import threading
        thread = threading.Thread(target=simular_execucao_testes, args=(execucao.id,))
        thread.start()
        
        return jsonify({
            'mensagem': 'Execução de testes iniciada',
            'execucao_id': execucao.id,
            'status': 'executando'
        }), 202
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

def simular_execucao_testes(execucao_id):
    """Simula a execução de testes em background"""
    try:
        import time
        execucao = ExecucaoTeste.query.get(execucao_id)
        if not execucao:
            return
        
        # Simular tempo de execução (reduzido para demonstração)
        tempo_execucao = random.randint(5, 15)  # 5-15 segundos
        
        # Simular execução em tempo real
        time.sleep(tempo_execucao)
        
        # Simular resultados de teste
        tipos_teste = ['Login', 'Navegação', 'Formulários', 'API', 'Performance']
        status_possiveis = ['passou', 'falhou', 'ignorado']
        
        for i, tipo_teste in enumerate(tipos_teste):
            resultado = ResultadoTeste(
                execucao_id=execucao_id,
                nome_teste=f'Teste {tipo_teste} - {i+1}',
                status=random.choice(status_possiveis),
                tempo_execucao=random.randint(5, 30),
                mensagem_erro='' if random.choice([True, False]) else 'Erro de validação'
            )
            db.session.add(resultado)
        
        # Atualizar execução
        execucao.duracao = tempo_execucao
        execucao.status = 'sucesso' if random.random() > 0.2 else 'falha'
        execucao.data_atualizacao = datetime.utcnow()
        
        db.session.commit()
        
    except Exception as e:
        print(f"Erro na simulação de execução: {e}")

# =============================================================================
# ROTAS DO SISTEMA
# =============================================================================

@sistema_bp.route('/sistema', methods=['GET'])
def obter_metricas_sistema():
    """Retorna métricas atuais do sistema"""
    try:
        metricas = MetricaSistema.get_metricas_atuais()
        return jsonify(metricas)
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@sistema_bp.route('/sistema/historico', methods=['GET'])
def obter_historico_sistema():
    """Retorna histórico de métricas do sistema"""
    try:
        horas = request.args.get('horas', 24, type=int)
        data_inicio = datetime.utcnow() - timedelta(hours=horas)
        
        metricas = MetricaSistema.query.filter(
            MetricaSistema.data_coleta >= data_inicio
        ).order_by(MetricaSistema.data_coleta.desc()).all()
        
        return jsonify([metrica.to_dict() for metrica in metricas])
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@sistema_bp.route('/configuracoes', methods=['GET'])
def obter_configuracoes():
    """Retorna configurações do sistema"""
    try:
        configuracao = ConfiguracaoSistema.query.first()
        if configuracao:
            return jsonify(configuracao.to_dict())
        else:
            return jsonify({'erro': 'Configuração não encontrada'}), 404
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@sistema_bp.route('/configuracoes', methods=['PUT'])
def atualizar_configuracoes():
    """Atualiza configurações do sistema"""
    try:
        dados = request.get_json()
        configuracao = ConfiguracaoSistema.query.first()
        
        if not configuracao:
            return jsonify({'erro': 'Configuração não encontrada'}), 404
        
        if 'nome' in dados:
            configuracao.nome = dados['nome']
        if 'versao' in dados:
            configuracao.versao = dados['versao']
        if 'ambiente' in dados:
            configuracao.ambiente = dados['ambiente']
        if 'configuracao' in dados:
            configuracao.set_configuracao_dict(dados['configuracao'])
        
        configuracao.data_atualizacao = datetime.utcnow()
        db.session.commit()
        
        return jsonify(configuracao.to_dict())
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# =============================================================================
# ROTAS DE PIPELINES
# =============================================================================

@pipelines_bp.route('/pipelines', methods=['GET'])
def listar_pipelines():
    """Lista pipelines de CI/CD"""
    try:
        pipelines = PipelineCI.get_status_pipelines()
        
        # Se não houver pipelines, criar alguns de exemplo
        if not pipelines:
            pipelines = criar_pipelines_exemplo()
        
        return jsonify(pipelines)
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@pipelines_bp.route('/pipelines/<int:pipeline_id>', methods=['GET'])
def obter_pipeline(pipeline_id):
    """Obtém detalhes de um pipeline específico"""
    try:
        pipeline = PipelineCI.query.get_or_404(pipeline_id)
        return jsonify(pipeline.to_dict())
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@pipelines_bp.route('/pipelines', methods=['POST'])
def criar_pipeline():
    """Cria um novo pipeline"""
    try:
        dados = request.get_json()
        
        pipeline = PipelineCI(
            nome=dados.get('nome'),
            status=dados.get('status', 'pendente'),
            ambiente=dados.get('ambiente', 'desenvolvimento'),
            branch=dados.get('branch'),
            commit_hash=dados.get('commit_hash'),
            url_build=dados.get('url_build'),
            observacoes=dados.get('observacoes')
        )
        
        db.session.add(pipeline)
        db.session.commit()
        
        return jsonify(pipeline.to_dict()), 201
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

def criar_pipelines_exemplo():
    """Cria pipelines de exemplo para demonstração"""
    pipelines_exemplo = [
        {
            'nome': 'Build Principal',
            'status': 'sucesso',
            'ultimaExecucao': '2 min atrás',
            'ambiente': 'desenvolvimento',
            'branch': 'main'
        },
        {
            'nome': 'Testes de Integração',
            'status': 'executando',
            'ultimaExecucao': 'Executando...',
            'ambiente': 'homologacao',
            'branch': 'feature/nova-funcionalidade'
        },
        {
            'nome': 'Deploy Produção',
            'status': 'pendente',
            'ultimaExecucao': 'Aguardando aprovação',
            'ambiente': 'producao',
            'branch': 'release/v1.2.0'
        },
        {
            'nome': 'Testes de Performance',
            'status': 'falha',
            'ultimaExecucao': '15 min atrás',
            'ambiente': 'homologacao',
            'branch': 'main'
        }
    ]
    
    return pipelines_exemplo

# =============================================================================
# ROTAS DE RELATÓRIOS
# =============================================================================

@execucoes_bp.route('/relatorios/<int:execucao_id>', methods=['GET'])
def gerar_relatorio(execucao_id):
    """Gera relatório de uma execução"""
    try:
        execucao = ExecucaoTeste.query.get_or_404(execucao_id)
        resultados = ResultadoTeste.query.filter_by(execucao_id=execucao_id).all()
        
        # Estatísticas do relatório
        total_testes = len(resultados)
        testes_passaram = len([r for r in resultados if r.status == 'passou'])
        testes_falharam = len([r for r in resultados if r.status == 'falhou'])
        testes_ignorados = len([r for r in resultados if r.status == 'ignorado'])
        
        tempo_total = sum(r.tempo_execucao for r in resultados)
        
        relatorio = {
            'execucao': execucao.to_dict(),
            'estatisticas': {
                'total_testes': total_testes,
                'testes_passaram': testes_passaram,
                'testes_falharam': testes_falharam,
                'testes_ignorados': testes_ignorados,
                'taxa_sucesso': (testes_passaram / total_testes * 100) if total_testes > 0 else 0,
                'tempo_total': round(tempo_total, 2)
            },
            'resultados': [resultado.to_dict() for resultado in resultados],
            'gerado_em': datetime.now().isoformat()
        }
        
        return jsonify(relatorio)
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
