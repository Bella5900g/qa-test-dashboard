#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA Test Automation Dashboard - Backend API
Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

API Flask para gerenciamento de testes automatizados e métricas de qualidade.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random
import psutil
import os
import json
from models import db, ExecucaoTeste, ResultadoTeste, ConfiguracaoSistema
from routes import metricas_bp, execucoes_bp, sistema_bp, pipelines_bp

def criar_aplicacao():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = 'qa-dashboard-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qa_dashboard.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    db.init_app(app)
    CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000'])
    
    # Registrar blueprints
    app.register_blueprint(metricas_bp, url_prefix='/api')
    app.register_blueprint(execucoes_bp, url_prefix='/api')
    app.register_blueprint(sistema_bp, url_prefix='/api')
    app.register_blueprint(pipelines_bp, url_prefix='/api')
    
    # Rota principal
    @app.route('/')
    def index():
        return jsonify({
            'mensagem': 'QA Test Automation Dashboard API',
            'versao': '1.0.0',
            'desenvolvedora': 'Isabella Barbosa',
            'endpoints': {
                'metricas': '/api/metricas',
                'execucoes': '/api/execucoes',
                'sistema': '/api/sistema',
                'pipelines': '/api/pipelines',
                'executar_testes': '/api/executar-testes'
            }
        })
    
    # Rota de health check
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'uptime': 'ativo'
        })
    
    # Criar tabelas do banco
    with app.app_context():
        db.create_all()
        inicializar_dados_exemplo()
    
    return app

def inicializar_dados_exemplo():
    """Inicializa o banco com dados de exemplo"""
    # Verificar se já existem dados
    if ExecucaoTeste.query.first():
        return
    
    print("Inicializando dados de exemplo...")
    
    # Criar execuções de exemplo
    tipos_teste = ['web', 'api', 'performance', 'integracao']
    status_possiveis = ['sucesso', 'falha', 'executando', 'pendente']
    
    for i in range(20):
        execucao = ExecucaoTeste(
            tipo=random.choice(tipos_teste),
            status=random.choice(status_possiveis),
            duracao=random.randint(30, 300),
            ambiente='desenvolvimento',
            observacoes=f'Execução de teste {i+1}'
        )
        db.session.add(execucao)
    
    # Criar resultados de teste
    for execucao in ExecucaoTeste.query.all():
        for j in range(random.randint(5, 15)):
            resultado = ResultadoTeste(
                execucao_id=execucao.id,
                nome_teste=f'Teste {j+1} - {execucao.tipo}',
                status=random.choice(['passou', 'falhou', 'ignorado']),
                tempo_execucao=random.randint(1, 30),
                mensagem_erro='' if random.choice([True, False]) else 'Erro de validação'
            )
            db.session.add(resultado)
    
    # Criar configurações do sistema
    configuracao = ConfiguracaoSistema(
        nome='QA Dashboard',
        versao='1.0.0',
        ambiente='desenvolvimento',
        configuracao=json.dumps({
            'intervalo_atualizacao': 30,
            'retencao_logs': 30,
            'notificacoes_email': True,
            'backup_automatico': True
        })
    )
    db.session.add(configuracao)
    
    db.session.commit()
    print("Dados de exemplo criados com sucesso!")

if __name__ == '__main__':
    app = criar_aplicacao()
    
    print("Iniciando QA Test Dashboard API...")
    print("Dashboard disponível em: http://localhost:5000")
    print("API endpoints em: http://localhost:5000/api")
    print("Health check em: http://localhost:5000/health")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
