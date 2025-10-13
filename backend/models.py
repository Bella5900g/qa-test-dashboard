#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA Test Automation Dashboard - Modelos de Dados
Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

Modelos SQLAlchemy para gerenciamento de dados do dashboard.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import psutil

db = SQLAlchemy()

class ExecucaoTeste(db.Model):
    """Modelo para execuções de testes"""
    __tablename__ = 'execucoes_teste'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  # web, api, performance, integracao
    status = db.Column(db.String(20), nullable=False)  # sucesso, falha, executando, pendente
    duracao = db.Column(db.Integer, nullable=False)  # em segundos
    ambiente = db.Column(db.String(50), nullable=False)  # desenvolvimento, homologacao, producao
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com resultados
    resultados = db.relationship('ResultadoTeste', backref='execucao', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'tipo': self.tipo,
            'status': self.status,
            'duracao': self.duracao,
            'ambiente': self.ambiente,
            'observacoes': self.observacoes,
            'data_criacao': self.data_criacao.isoformat(),
            'data_atualizacao': self.data_atualizacao.isoformat(),
            'total_testes': len(self.resultados),
            'testes_passaram': len([r for r in self.resultados if r.status == 'passou']),
            'testes_falharam': len([r for r in self.resultados if r.status == 'falhou'])
        }
    
    @classmethod
    def get_metricas_gerais(cls):
        """Retorna métricas gerais das execuções"""
        total_execucoes = cls.query.count()
        execucoes_sucesso = cls.query.filter_by(status='sucesso').count()
        execucoes_falha = cls.query.filter_by(status='falha').count()
        
        taxa_sucesso = (execucoes_sucesso / total_execucoes * 100) if total_execucoes > 0 else 0
        
        # Tempo médio de execução
        tempo_medio = db.session.query(db.func.avg(cls.duracao)).scalar() or 0
        
        return {
            'total_execucoes': total_execucoes,
            'taxa_sucesso': round(taxa_sucesso, 2),
            'execucoes_sucesso': execucoes_sucesso,
            'execucoes_falha': execucoes_falha,
            'tempo_medio': round(tempo_medio, 2)
        }
    
    @classmethod
    def get_tendencias(cls, dias=30):
        """Retorna dados de tendências dos últimos N dias"""
        data_inicio = datetime.utcnow() - timedelta(days=dias)
        execucoes = cls.query.filter(cls.data_criacao >= data_inicio).all()
        
        # Agrupar por data
        dados_por_data = {}
        for execucao in execucoes:
            data = execucao.data_criacao.date()
            if data not in dados_por_data:
                dados_por_data[data] = {'total': 0, 'sucesso': 0, 'tempo_total': 0}
            
            dados_por_data[data]['total'] += 1
            if execucao.status == 'sucesso':
                dados_por_data[data]['sucesso'] += 1
            dados_por_data[data]['tempo_total'] += execucao.duracao
        
        # Preparar dados para o gráfico
        datas = sorted(dados_por_data.keys())
        sucesso_rates = []
        tempos_medios = []
        
        for data in datas:
            dados = dados_por_data[data]
            sucesso_rate = (dados['sucesso'] / dados['total'] * 100) if dados['total'] > 0 else 0
            tempo_medio = dados['tempo_total'] / dados['total'] if dados['total'] > 0 else 0
            
            sucesso_rates.append(round(sucesso_rate, 2))
            tempos_medios.append(round(tempo_medio, 2))
        
        return {
            'datas': [data.strftime('%d/%m') for data in datas],
            'sucesso': sucesso_rates,
            'tempo': tempos_medios
        }

class ResultadoTeste(db.Model):
    """Modelo para resultados individuais de testes"""
    __tablename__ = 'resultados_teste'
    
    id = db.Column(db.Integer, primary_key=True)
    execucao_id = db.Column(db.Integer, db.ForeignKey('execucoes_teste.id'), nullable=False)
    nome_teste = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # passou, falhou, ignorado
    tempo_execucao = db.Column(db.Float, nullable=False)  # em segundos
    mensagem_erro = db.Column(db.Text)
    stack_trace = db.Column(db.Text)
    screenshot_path = db.Column(db.String(500))
    data_execucao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'execucao_id': self.execucao_id,
            'nome_teste': self.nome_teste,
            'status': self.status,
            'tempo_execucao': self.tempo_execucao,
            'mensagem_erro': self.mensagem_erro,
            'stack_trace': self.stack_trace,
            'screenshot_path': self.screenshot_path,
            'data_execucao': self.data_execucao.isoformat()
        }

class ConfiguracaoSistema(db.Model):
    """Modelo para configurações do sistema"""
    __tablename__ = 'configuracoes_sistema'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    versao = db.Column(db.String(20), nullable=False)
    ambiente = db.Column(db.String(50), nullable=False)
    configuracao = db.Column(db.Text)  # JSON string
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_configuracao_dict(self):
        """Retorna a configuração como dicionário"""
        try:
            return json.loads(self.configuracao) if self.configuracao else {}
        except json.JSONDecodeError:
            return {}
    
    def set_configuracao_dict(self, config_dict):
        """Define a configuração a partir de um dicionário"""
        self.configuracao = json.dumps(config_dict)
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'versao': self.versao,
            'ambiente': self.ambiente,
            'configuracao': self.get_configuracao_dict(),
            'data_criacao': self.data_criacao.isoformat(),
            'data_atualizacao': self.data_atualizacao.isoformat()
        }

class PipelineCI(db.Model):
    """Modelo para pipelines de CI/CD"""
    __tablename__ = 'pipelines_ci'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # sucesso, falha, executando, pendente
    ambiente = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(100))
    commit_hash = db.Column(db.String(40))
    duracao = db.Column(db.Integer)  # em segundos
    url_build = db.Column(db.String(500))
    observacoes = db.Column(db.Text)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'status': self.status,
            'ambiente': self.ambiente,
            'branch': self.branch,
            'commit_hash': self.commit_hash,
            'duracao': self.duracao,
            'url_build': self.url_build,
            'observacoes': self.observacoes,
            'data_inicio': self.data_inicio.isoformat(),
            'data_fim': self.data_fim.isoformat() if self.data_fim else None
        }
    
    @classmethod
    def get_status_pipelines(cls):
        """Retorna status dos pipelines mais recentes"""
        pipelines = cls.query.order_by(cls.data_inicio.desc()).limit(10).all()
        return [pipeline.to_dict() for pipeline in pipelines]

class MetricaSistema(db.Model):
    """Modelo para métricas do sistema"""
    __tablename__ = 'metricas_sistema'
    
    id = db.Column(db.Integer, primary_key=True)
    cpu_percent = db.Column(db.Float, nullable=False)
    memoria_percent = db.Column(db.Float, nullable=False)
    disco_percent = db.Column(db.Float, nullable=False)
    rede_bytes_enviados = db.Column(db.BigInteger, default=0)
    rede_bytes_recebidos = db.Column(db.BigInteger, default=0)
    data_coleta = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'cpu_percent': self.cpu_percent,
            'memoria_percent': self.memoria_percent,
            'disco_percent': self.disco_percent,
            'rede_bytes_enviados': self.rede_bytes_enviados,
            'rede_bytes_recebidos': self.rede_bytes_recebidos,
            'data_coleta': self.data_coleta.isoformat()
        }
    
    @classmethod
    def get_metricas_atuais(cls):
        """Coleta e retorna métricas atuais do sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memória
            memoria = psutil.virtual_memory()
            memoria_percent = memoria.percent
            
            # Disco
            disco = psutil.disk_usage('/')
            disco_percent = (disco.used / disco.total) * 100
            
            # Rede
            rede = psutil.net_io_counters()
            rede_bytes_enviados = rede.bytes_sent
            rede_bytes_recebidos = rede.bytes_recv
            
            # Salvar métricas
            metrica = cls(
                cpu_percent=cpu_percent,
                memoria_percent=memoria_percent,
                disco_percent=disco_percent,
                rede_bytes_enviados=rede_bytes_enviados,
                rede_bytes_recebidos=rede_bytes_recebidos
            )
            db.session.add(metrica)
            db.session.commit()
            
            return {
                'cpu': round(cpu_percent, 2),
                'memoria': round(memoria_percent, 2),
                'disco': round(disco_percent, 2),
                'rede': round((rede_bytes_enviados + rede_bytes_recebidos) / 1024 / 1024, 2)  # MB
            }
            
        except Exception as e:
            print(f"Erro ao coletar métricas do sistema: {e}")
            return {
                'cpu': 0,
                'memoria': 0,
                'disco': 0,
                'rede': 0
            }
