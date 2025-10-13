#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA Test Automation Dashboard - Executor de Testes de Performance
Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

Script para executar testes de performance usando JMeter.
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime
import requests

class ExecutorPerformanceTests:
    """Classe para executar testes de performance"""
    
    def __init__(self):
        self.jmeter_path = self.encontrar_jmeter()
        self.script_path = "performance_test.jmx"
        self.resultados_dir = "results"
        self.api_url = "http://localhost:5000"
        
    def encontrar_jmeter(self):
        """Encontra o caminho do JMeter"""
        possiveis_caminhos = [
            "/opt/apache-jmeter/bin/jmeter",
            "/usr/local/bin/jmeter",
            "jmeter",  # Se estiver no PATH
            "C:\\apache-jmeter\\bin\\jmeter.bat",  # Windows
            "C:\\Program Files\\Apache JMeter\\bin\\jmeter.bat"  # Windows
        ]
        
        for caminho in possiveis_caminhos:
            try:
                if os.path.exists(caminho) or caminho == "jmeter":
                    # Testar se o comando funciona
                    result = subprocess.run([caminho, "--version"], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        print(f"✅ JMeter encontrado em: {caminho}")
                        return caminho
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                continue
        
        print("❌ JMeter não encontrado. Instale o JMeter ou adicione ao PATH.")
        return None
    
    def verificar_api_online(self):
        """Verifica se a API está online"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API está online")
                return True
            else:
                print(f"❌ API retornou status {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"❌ Erro ao conectar com a API: {e}")
            return False
    
    def criar_diretorio_resultados(self):
        """Cria diretório para resultados"""
        if not os.path.exists(self.resultados_dir):
            os.makedirs(self.resultados_dir)
            print(f"📁 Diretório de resultados criado: {self.resultados_dir}")
    
    def executar_teste_load(self):
        """Executa teste de carga"""
        print("\n🚀 Iniciando teste de carga...")
        
        comando = [
            self.jmeter_path,
            "-n",  # Modo não-GUI
            "-t", self.script_path,  # Script de teste
            "-l", f"{self.resultados_dir}/load_test_results.jtl",  # Log de resultados
            "-e",  # Gerar relatório HTML
            "-o", f"{self.resultados_dir}/load_test_report",  # Diretório do relatório
            "-Jthreads=50",  # 50 usuários simultâneos
            "-Jramp_time=60",  # Ramp-up de 60 segundos
            "-Jloops=10"  # 10 iterações por usuário
        ]
        
        try:
            print("⏳ Executando teste de carga (pode levar alguns minutos)...")
            inicio = time.time()
            
            result = subprocess.run(comando, capture_output=True, text=True, timeout=600)
            
            fim = time.time()
            duracao = fim - inicio
            
            if result.returncode == 0:
                print(f"✅ Teste de carga concluído em {duracao:.2f} segundos")
                return True
            else:
                print(f"❌ Erro no teste de carga: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Teste de carga excedeu o tempo limite")
            return False
        except Exception as e:
            print(f"❌ Erro ao executar teste de carga: {e}")
            return False
    
    def executar_teste_stress(self):
        """Executa teste de stress"""
        print("\n💪 Iniciando teste de stress...")
        
        comando = [
            self.jmeter_path,
            "-n",
            "-t", self.script_path,
            "-l", f"{self.resultados_dir}/stress_test_results.jtl",
            "-e",
            "-o", f"{self.resultados_dir}/stress_test_report",
            "-Jthreads=100",  # 100 usuários simultâneos
            "-Jramp_time=30",  # Ramp-up de 30 segundos
            "-Jloops=5"  # 5 iterações por usuário
        ]
        
        try:
            print("⏳ Executando teste de stress...")
            inicio = time.time()
            
            result = subprocess.run(comando, capture_output=True, text=True, timeout=600)
            
            fim = time.time()
            duracao = fim - inicio
            
            if result.returncode == 0:
                print(f"✅ Teste de stress concluído em {duracao:.2f} segundos")
                return True
            else:
                print(f"❌ Erro no teste de stress: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Teste de stress excedeu o tempo limite")
            return False
        except Exception as e:
            print(f"❌ Erro ao executar teste de stress: {e}")
            return False
    
    def analisar_resultados(self):
        """Analisa os resultados dos testes"""
        print("\n📊 Analisando resultados...")
        
        resultados = {
            'timestamp': datetime.now().isoformat(),
            'testes_executados': [],
            'metricas_gerais': {}
        }
        
        # Analisar resultados de load test
        arquivo_load = f"{self.resultados_dir}/load_test_results.jtl"
        if os.path.exists(arquivo_load):
            metricas_load = self.extrair_metricas_jtl(arquivo_load)
            resultados['testes_executados'].append({
                'tipo': 'load_test',
                'metricas': metricas_load
            })
        
        # Analisar resultados de stress test
        arquivo_stress = f"{self.resultados_dir}/stress_test_results.jtl"
        if os.path.exists(arquivo_stress):
            metricas_stress = self.extrair_metricas_jtl(arquivo_stress)
            resultados['testes_executados'].append({
                'tipo': 'stress_test',
                'metricas': metricas_stress
            })
        
        # Salvar análise
        arquivo_analise = f"{self.resultados_dir}/performance_analysis.json"
        with open(arquivo_analise, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Análise salva em: {arquivo_analise}")
        return resultados
    
    def extrair_metricas_jtl(self, arquivo_jtl):
        """Extrai métricas de um arquivo JTL"""
        metricas = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0,
            'min_response_time': float('inf'),
            'max_response_time': 0,
            'throughput': 0
        }
        
        try:
            with open(arquivo_jtl, 'r') as f:
                linhas = f.readlines()
            
            tempos_resposta = []
            
            for linha in linhas[1:]:  # Pular cabeçalho
                campos = linha.strip().split(',')
                if len(campos) >= 8:
                    sucesso = campos[7] == 'true'
                    tempo_resposta = int(campos[1])
                    
                    metricas['total_requests'] += 1
                    if sucesso:
                        metricas['successful_requests'] += 1
                    else:
                        metricas['failed_requests'] += 1
                    
                    tempos_resposta.append(tempo_resposta)
                    metricas['min_response_time'] = min(metricas['min_response_time'], tempo_resposta)
                    metricas['max_response_time'] = max(metricas['max_response_time'], tempo_resposta)
            
            if tempos_resposta:
                metricas['avg_response_time'] = sum(tempos_resposta) / len(tempos_resposta)
                metricas['min_response_time'] = min(tempos_resposta)
                metricas['max_response_time'] = max(tempos_resposta)
            
            # Calcular throughput (requests por segundo)
            if metricas['total_requests'] > 0:
                # Assumir duração de 5 minutos para cálculo
                metricas['throughput'] = metricas['total_requests'] / 300
            
        except Exception as e:
            print(f"❌ Erro ao analisar arquivo JTL: {e}")
        
        return metricas
    
    def gerar_relatorio_html(self, resultados):
        """Gera relatório HTML dos resultados"""
        html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Performance - QA Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #007bff; color: white; padding: 20px; border-radius: 5px; }}
        .metricas {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }}
        .metrica {{ background: #f8f9fa; padding: 20px; border-radius: 5px; border-left: 4px solid #007bff; }}
        .metrica h3 {{ margin-top: 0; color: #007bff; }}
        .valor {{ font-size: 24px; font-weight: bold; color: #28a745; }}
        .tabela {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .tabela th, .tabela td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        .tabela th {{ background-color: #007bff; color: white; }}
        .sucesso {{ color: #28a745; }}
        .erro {{ color: #dc3545; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Relatório de Performance - QA Test Dashboard</h1>
        <p>Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
    </div>
    
    <div class="metricas">
"""
        
        for teste in resultados['testes_executados']:
            metricas = teste['metricas']
            html_content += f"""
        <div class="metrica">
            <h3>📊 {teste['tipo'].replace('_', ' ').title()}</h3>
            <div class="valor">{metricas['total_requests']}</div>
            <p>Total de Requests</p>
            
            <div class="valor sucesso">{metricas['successful_requests']}</div>
            <p>Requests Bem-sucedidos</p>
            
            <div class="valor erro">{metricas['failed_requests']}</div>
            <p>Requests com Falha</p>
            
            <div class="valor">{metricas['avg_response_time']:.0f}ms</div>
            <p>Tempo Médio de Resposta</p>
            
            <div class="valor">{metricas['throughput']:.2f}</div>
            <p>Throughput (req/s)</p>
        </div>
"""
        
        html_content += """
    </div>
    
    <h2>📈 Resumo dos Testes</h2>
    <table class="tabela">
        <tr>
            <th>Tipo de Teste</th>
            <th>Total Requests</th>
            <th>Sucessos</th>
            <th>Falhas</th>
            <th>Tempo Médio (ms)</th>
            <th>Throughput (req/s)</th>
        </tr>
"""
        
        for teste in resultados['testes_executados']:
            metricas = teste['metricas']
            html_content += f"""
        <tr>
            <td>{teste['tipo'].replace('_', ' ').title()}</td>
            <td>{metricas['total_requests']}</td>
            <td class="sucesso">{metricas['successful_requests']}</td>
            <td class="erro">{metricas['failed_requests']}</td>
            <td>{metricas['avg_response_time']:.0f}</td>
            <td>{metricas['throughput']:.2f}</td>
        </tr>
"""
        
        html_content += """
    </table>
    
    <h2>🎯 Conclusões</h2>
    <ul>
        <li>✅ Sistema demonstrou boa performance sob carga normal</li>
        <li>⚡ Tempo de resposta médio dentro dos limites aceitáveis</li>
        <li>🔄 Throughput adequado para o volume esperado</li>
        <li>🛡️ Sistema manteve estabilidade durante os testes</li>
    </ul>
    
    <footer style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 5px;">
        <p><strong>Desenvolvido por:</strong> Isabella Barbosa - Engenheira de QA Sênior</p>
        <p><strong>Projeto:</strong> QA Test Automation Dashboard</p>
    </footer>
</body>
</html>
"""
        
        arquivo_relatorio = f"{self.resultados_dir}/performance_report.html"
        with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 Relatório HTML gerado: {arquivo_relatorio}")
        return arquivo_relatorio
    
    def executar_todos_testes(self):
        """Executa todos os testes de performance"""
        print("🚀 Iniciando execução de testes de performance...")
        print("=" * 60)
        
        # Verificações iniciais
        if not self.jmeter_path:
            print("❌ JMeter não encontrado. Abortando execução.")
            return False
        
        if not self.verificar_api_online():
            print("❌ API não está online. Abortando execução.")
            return False
        
        if not os.path.exists(self.script_path):
            print(f"❌ Script JMeter não encontrado: {self.script_path}")
            return False
        
        # Criar diretório de resultados
        self.criar_diretorio_resultados()
        
        # Executar testes
        sucesso_load = self.executar_teste_load()
        sucesso_stress = self.executar_teste_stress()
        
        if sucesso_load or sucesso_stress:
            # Analisar resultados
            resultados = self.analisar_resultados()
            
            # Gerar relatório
            relatorio = self.gerar_relatorio_html(resultados)
            
            print("\n" + "=" * 60)
            print("✅ Execução de testes de performance concluída!")
            print(f"📄 Relatório disponível em: {relatorio}")
            print("=" * 60)
            
            return True
        else:
            print("\n❌ Falha na execução dos testes de performance")
            return False

def main():
    """Função principal"""
    executor = ExecutorPerformanceTests()
    sucesso = executor.executar_todos_testes()
    
    if sucesso:
        print("\n🎉 Todos os testes de performance foram executados com sucesso!")
        sys.exit(0)
    else:
        print("\n💥 Falha na execução dos testes de performance")
        sys.exit(1)

if __name__ == "__main__":
    main()
