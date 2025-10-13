#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA Test Automation Dashboard - Testes de API
Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

Testes automatizados para a API REST do dashboard.
"""

import pytest
import requests
import json
import time
from datetime import datetime, timedelta

class TestAPIEndpoints:
    """Classe de testes para endpoints da API"""
    
    @pytest.fixture(scope="class")
    def api_base_url(self):
        """URL base da API"""
        return "http://localhost:5000/api"
    
    @pytest.fixture(scope="class")
    def headers(self):
        """Headers padrão para requisições"""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def test_api_health_check(self, api_base_url):
        """Testa se a API está funcionando"""
        response = requests.get(f"{api_base_url.replace('/api', '')}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_endpoint_metricas(self, api_base_url, headers):
        """Testa endpoint de métricas"""
        response = requests.get(f"{api_base_url}/metricas", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        
        # Verificar campos obrigatórios
        campos_obrigatorios = [
            'taxaSucesso', 'tempoMedio', 'cobertura', 'bugsEncontrados',
            'tendencias', 'distribuicao', 'performance', 'timestamp'
        ]
        
        for campo in campos_obrigatorios:
            assert campo in data, f"Campo '{campo}' não encontrado na resposta"
        
        # Verificar tipos de dados
        assert isinstance(data['taxaSucesso'], (int, float))
        assert isinstance(data['tempoMedio'], str)
        assert isinstance(data['cobertura'], (int, float))
        assert isinstance(data['bugsEncontrados'], int)
        assert isinstance(data['tendencias'], dict)
        assert isinstance(data['distribuicao'], dict)
        assert isinstance(data['performance'], dict)
    
    def test_endpoint_metricas_detalhadas(self, api_base_url, headers):
        """Testa endpoint de métricas detalhadas"""
        response = requests.get(f"{api_base_url}/metricas/detalhadas", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        
        # Verificar estrutura da resposta
        assert 'execucoes_por_status' in data
        assert 'execucoes_por_ambiente' in data
        assert 'tempo_por_tipo' in data
        assert 'timestamp' in data
    
    def test_endpoint_execucoes(self, api_base_url, headers):
        """Testa endpoint de execuções"""
        response = requests.get(f"{api_base_url}/execucoes", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        # Se há execuções, verificar estrutura
        if data:
            execucao = data[0]
            campos_obrigatorios = [
                'id', 'tipo', 'status', 'duracao', 'ambiente',
                'data_criacao', 'data_atualizacao'
            ]
            
            for campo in campos_obrigatorios:
                assert campo in execucao, f"Campo '{campo}' não encontrado na execução"
    
    def test_endpoint_execucoes_com_filtros(self, api_base_url, headers):
        """Testa endpoint de execuções com filtros"""
        # Teste com limite
        response = requests.get(f"{api_base_url}/execucoes?limite=5", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) <= 5
        
        # Teste com filtro de tipo
        response = requests.get(f"{api_base_url}/execucoes?tipo=web", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        for execucao in data:
            assert execucao['tipo'] == 'web'
    
    def test_endpoint_execucao_especifica(self, api_base_url, headers):
        """Testa endpoint de execução específica"""
        # Primeiro, obter uma execução
        response = requests.get(f"{api_base_url}/execucoes", headers=headers)
        assert response.status_code == 200
        
        execucoes = response.json()
        if execucoes:
            execucao_id = execucoes[0]['id']
            
            # Testar endpoint específico
            response = requests.get(f"{api_base_url}/execucoes/{execucao_id}", headers=headers)
            assert response.status_code == 200
            
            data = response.json()
            assert data['id'] == execucao_id
        else:
            pytest.skip("Nenhuma execução encontrada para teste")
    
    def test_endpoint_resultados_execucao(self, api_base_url, headers):
        """Testa endpoint de resultados de execução"""
        # Primeiro, obter uma execução
        response = requests.get(f"{api_base_url}/execucoes", headers=headers)
        assert response.status_code == 200
        
        execucoes = response.json()
        if execucoes:
            execucao_id = execucoes[0]['id']
            
            # Testar endpoint de resultados
            response = requests.get(f"{api_base_url}/execucoes/{execucao_id}/resultados", headers=headers)
            assert response.status_code == 200
            
            data = response.json()
            assert 'execucao' in data
            assert 'resultados' in data
            assert isinstance(data['resultados'], list)
        else:
            pytest.skip("Nenhuma execução encontrada para teste")
    
    def test_endpoint_executar_testes(self, api_base_url, headers):
        """Testa endpoint de execução de testes"""
        payload = {
            "tipo": "web",
            "ambiente": "desenvolvimento"
        }
        
        response = requests.post(
            f"{api_base_url}/executar-testes",
            headers=headers,
            json=payload
        )
        assert response.status_code == 202
        
        data = response.json()
        assert 'mensagem' in data
        assert 'execucao_id' in data
        assert 'status' in data
        assert data['status'] == 'executando'
    
    def test_endpoint_sistema(self, api_base_url, headers):
        """Testa endpoint de métricas do sistema"""
        response = requests.get(f"{api_base_url}/sistema", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        
        # Verificar campos obrigatórios
        campos_obrigatorios = ['cpu', 'memoria', 'disco', 'rede']
        for campo in campos_obrigatorios:
            assert campo in data, f"Campo '{campo}' não encontrado na resposta"
            assert isinstance(data[campo], (int, float))
            assert 0 <= data[campo] <= 100  # Percentuais devem estar entre 0 e 100
    
    def test_endpoint_sistema_historico(self, api_base_url, headers):
        """Testa endpoint de histórico do sistema"""
        response = requests.get(f"{api_base_url}/sistema/historico", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        # Se há histórico, verificar estrutura
        if data:
            metrica = data[0]
            campos_obrigatorios = [
                'id', 'cpu_percent', 'memoria_percent', 'disco_percent',
                'data_coleta'
            ]
            
            for campo in campos_obrigatorios:
                assert campo in metrica, f"Campo '{campo}' não encontrado na métrica"
    
    def test_endpoint_configuracoes(self, api_base_url, headers):
        """Testa endpoint de configurações"""
        # GET configurações
        response = requests.get(f"{api_base_url}/configuracoes", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert 'nome' in data
        assert 'versao' in data
        assert 'ambiente' in data
        assert 'configuracao' in data
    
    def test_endpoint_pipelines(self, api_base_url, headers):
        """Testa endpoint de pipelines"""
        response = requests.get(f"{api_base_url}/pipelines", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        # Se há pipelines, verificar estrutura
        if data:
            pipeline = data[0]
            campos_obrigatorios = ['nome', 'status', 'ultimaExecucao']
            
            for campo in campos_obrigatorios:
                assert campo in pipeline, f"Campo '{campo}' não encontrado no pipeline"
    
    def test_endpoint_relatorio(self, api_base_url, headers):
        """Testa endpoint de relatório"""
        # Primeiro, obter uma execução
        response = requests.get(f"{api_base_url}/execucoes", headers=headers)
        assert response.status_code == 200
        
        execucoes = response.json()
        if execucoes:
            execucao_id = execucoes[0]['id']
            
            # Testar endpoint de relatório
            response = requests.get(f"{api_base_url}/relatorios/{execucao_id}", headers=headers)
            assert response.status_code == 200
            
            data = response.json()
            assert 'execucao' in data
            assert 'estatisticas' in data
            assert 'resultados' in data
            assert 'gerado_em' in data
        else:
            pytest.skip("Nenhuma execução encontrada para teste")

class TestAPIPerformance:
    """Testes de performance da API"""
    
    @pytest.fixture(scope="class")
    def api_base_url(self):
        """URL base da API"""
        return "http://localhost:5000/api"
    
    def test_tempo_resposta_metricas(self, api_base_url):
        """Testa tempo de resposta do endpoint de métricas"""
        inicio = time.time()
        response = requests.get(f"{api_base_url}/metricas")
        fim = time.time()
        
        tempo_resposta = fim - inicio
        assert response.status_code == 200
        assert tempo_resposta < 2.0  # Deve responder em menos de 2 segundos
    
    def test_tempo_resposta_execucoes(self, api_base_url):
        """Testa tempo de resposta do endpoint de execuções"""
        inicio = time.time()
        response = requests.get(f"{api_base_url}/execucoes")
        fim = time.time()
        
        tempo_resposta = fim - inicio
        assert response.status_code == 200
        assert tempo_resposta < 1.0  # Deve responder em menos de 1 segundo
    
    def test_tempo_resposta_sistema(self, api_base_url):
        """Testa tempo de resposta do endpoint de sistema"""
        inicio = time.time()
        response = requests.get(f"{api_base_url}/sistema")
        fim = time.time()
        
        tempo_resposta = fim - inicio
        assert response.status_code == 200
        assert tempo_resposta < 1.0  # Deve responder em menos de 1 segundo
    
    def test_concorrencia_requests(self, api_base_url):
        """Testa múltiplas requisições simultâneas"""
        import concurrent.futures
        import threading
        
        def fazer_requisicao():
            response = requests.get(f"{api_base_url}/metricas")
            return response.status_code == 200
        
        # Fazer 10 requisições simultâneas
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fazer_requisicao) for _ in range(10)]
            resultados = [future.result() for future in futures]
        
        # Todas as requisições devem ter sucesso
        assert all(resultados)

class TestAPIErrorHandling:
    """Testes de tratamento de erros da API"""
    
    @pytest.fixture(scope="class")
    def api_base_url(self):
        """URL base da API"""
        return "http://localhost:5000/api"
    
    def test_endpoint_inexistente(self, api_base_url):
        """Testa endpoint que não existe"""
        response = requests.get(f"{api_base_url}/endpoint-inexistente")
        assert response.status_code == 404
    
    def test_execucao_inexistente(self, api_base_url):
        """Testa busca por execução que não existe"""
        response = requests.get(f"{api_base_url}/execucoes/99999")
        assert response.status_code == 404
    
    def test_relatorio_execucao_inexistente(self, api_base_url):
        """Testa relatório de execução que não existe"""
        response = requests.get(f"{api_base_url}/relatorios/99999")
        assert response.status_code == 404
    
    def test_metodo_nao_permitido(self, api_base_url):
        """Testa método HTTP não permitido"""
        response = requests.post(f"{api_base_url}/metricas")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_requisicao_malformada(self, api_base_url):
        """Testa requisição com dados malformados"""
        headers = {'Content-Type': 'application/json'}
        payload = "dados inválidos"
        
        response = requests.post(
            f"{api_base_url}/executar-testes",
            headers=headers,
            data=payload
        )
        # Pode retornar 400 (Bad Request) ou 500 (Internal Server Error)
        assert response.status_code in [400, 500]

class TestAPIDataValidation:
    """Testes de validação de dados da API"""
    
    @pytest.fixture(scope="class")
    def api_base_url(self):
        """URL base da API"""
        return "http://localhost:5000/api"
    
    def test_metricas_tipos_dados(self, api_base_url):
        """Testa se os tipos de dados das métricas estão corretos"""
        response = requests.get(f"{api_base_url}/metricas")
        assert response.status_code == 200
        
        data = response.json()
        
        # Verificar tipos específicos
        assert isinstance(data['taxaSucesso'], (int, float))
        assert 0 <= data['taxaSucesso'] <= 100
        
        assert isinstance(data['bugsEncontrados'], int)
        assert data['bugsEncontrados'] >= 0
        
        # Verificar estrutura de tendências
        tendencias = data['tendencias']
        assert isinstance(tendencias, dict)
        if 'datas' in tendencias:
            assert isinstance(tendencias['datas'], list)
        if 'sucesso' in tendencias:
            assert isinstance(tendencias['sucesso'], list)
    
    def test_execucoes_estrutura_dados(self, api_base_url):
        """Testa estrutura de dados das execuções"""
        response = requests.get(f"{api_base_url}/execucoes")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        if data:
            execucao = data[0]
            
            # Verificar tipos de campos
            assert isinstance(execucao['id'], int)
            assert isinstance(execucao['tipo'], str)
            assert isinstance(execucao['status'], str)
            assert isinstance(execucao['duracao'], int)
            assert isinstance(execucao['ambiente'], str)
            
            # Verificar valores válidos
            assert execucao['tipo'] in ['web', 'api', 'performance', 'integracao']
            assert execucao['status'] in ['sucesso', 'falha', 'executando', 'pendente']
            assert execucao['duracao'] >= 0

if __name__ == "__main__":
    # Executar testes diretamente
    pytest.main([__file__, "-v", "--tb=short"])
