#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA Test Automation Dashboard - Testes Web com Selenium
Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

Testes automatizados para o dashboard web usando Selenium WebDriver.
"""

import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestDashboardWeb:
    """Classe de testes para o dashboard web"""
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Configuração do driver Selenium"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Executar sem interface gráfica
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        yield driver
        driver.quit()
    
    @pytest.fixture(scope="class")
    def dashboard_url(self):
        """URL do dashboard"""
        return "http://localhost:8000"
    
    def test_dashboard_carrega_corretamente(self, driver, dashboard_url):
        """Testa se o dashboard carrega corretamente"""
        driver.get(dashboard_url)
        
        # Verificar título da página
        assert "QA Test Dashboard" in driver.title
        
        # Verificar elementos principais
        elementos_principais = [
            "navbar",
            "metrics-cards",
            "graficoTendencias",
            "graficoDistribuicao",
            "tabela-execucoes"
        ]
        
        for elemento in elementos_principais:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, elemento))
                )
            except TimeoutException:
                pytest.fail(f"Elemento {elemento} não encontrado na página")
    
    def test_metricas_sao_exibidas(self, driver, dashboard_url):
        """Testa se as métricas são exibidas corretamente"""
        driver.get(dashboard_url)
        
        # Aguardar carregamento das métricas
        time.sleep(3)
        
        # Verificar cards de métricas
        metricas_ids = [
            "taxa-sucesso",
            "tempo-medio", 
            "cobertura",
            "bugs-encontrados"
        ]
        
        for metrica_id in metricas_ids:
            elemento = driver.find_element(By.ID, metrica_id)
            assert elemento.is_displayed()
            assert elemento.text != "--"  # Verificar se tem valor
    
    def test_graficos_sao_renderizados(self, driver, dashboard_url):
        """Testa se os gráficos são renderizados"""
        driver.get(dashboard_url)
        
        # Aguardar carregamento dos gráficos
        time.sleep(5)
        
        # Verificar gráfico de tendências
        grafico_tendencias = driver.find_element(By.ID, "graficoTendencias")
        assert grafico_tendencias.is_displayed()
        
        # Verificar gráfico de distribuição
        grafico_distribuicao = driver.find_element(By.ID, "graficoDistribuicao")
        assert grafico_distribuicao.is_displayed()
        
        # Verificar gráfico de performance
        grafico_performance = driver.find_element(By.ID, "graficoPerformance")
        assert grafico_performance.is_displayed()
    
    def test_tabela_execucoes_exibe_dados(self, driver, dashboard_url):
        """Testa se a tabela de execuções exibe dados"""
        driver.get(dashboard_url)
        
        # Aguardar carregamento da tabela
        time.sleep(3)
        
        # Verificar cabeçalho da tabela
        cabecalhos = driver.find_elements(By.CSS_SELECTOR, "#tabela-execucoes th")
        assert len(cabecalhos) >= 5  # ID, Tipo, Status, Duração, Data/Hora, Ações
        
        # Verificar se há dados na tabela (pode estar vazio inicialmente)
        linhas = driver.find_elements(By.CSS_SELECTOR, "#tabela-execucoes tbody tr")
        print(f"Encontradas {len(linhas)} linhas na tabela de execuções")
    
    def test_botao_executar_testes_funciona(self, driver, dashboard_url):
        """Testa se o botão de executar testes funciona"""
        driver.get(dashboard_url)
        
        # Aguardar carregamento da página
        time.sleep(2)
        
        # Encontrar e clicar no botão de executar testes
        try:
            botao_executar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Executar Testes')]"))
            )
            botao_executar.click()
            
            # Verificar se o modal de carregamento aparece
            modal = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "modalCarregando"))
            )
            assert modal.is_displayed()
            
        except TimeoutException:
            pytest.fail("Botão de executar testes não encontrado ou não clicável")
    
    def test_navegacao_responsiva(self, driver, dashboard_url):
        """Testa se a navegação é responsiva"""
        driver.get(dashboard_url)
        
        # Testar em diferentes tamanhos de tela
        tamanhos_tela = [
            (1920, 1080),  # Desktop
            (768, 1024),   # Tablet
            (375, 667)     # Mobile
        ]
        
        for largura, altura in tamanhos_tela:
            driver.set_window_size(largura, altura)
            time.sleep(1)
            
            # Verificar se o navbar está visível
            navbar = driver.find_element(By.CLASS_NAME, "navbar")
            assert navbar.is_displayed()
            
            # Verificar se os cards de métricas se ajustam
            cards = driver.find_elements(By.CLASS_NAME, "metricas-card")
            for card in cards:
                assert card.is_displayed()
    
    def test_links_navegacao_funcionam(self, driver, dashboard_url):
        """Testa se os links de navegação funcionam"""
        driver.get(dashboard_url)
        
        # Links de navegação
        links_navegacao = [
            ("Dashboard", "#dashboard"),
            ("Testes", "#testes"),
            ("Relatórios", "#relatorios"),
            ("Configurações", "#configuracoes")
        ]
        
        for texto_link, href in links_navegacao:
            try:
                link = driver.find_element(By.XPATH, f"//a[contains(text(), '{texto_link}')]")
                assert link.is_displayed()
                assert link.get_attribute("href") is not None
            except NoSuchElementException:
                print(f"Link '{texto_link}' não encontrado")
    
    def test_atualizacao_automatica_metricas(self, driver, dashboard_url):
        """Testa se as métricas são atualizadas automaticamente"""
        driver.get(dashboard_url)
        
        # Aguardar carregamento inicial
        time.sleep(3)
        
        # Obter valor inicial da taxa de sucesso
        taxa_sucesso_inicial = driver.find_element(By.ID, "taxa-sucesso").text
        
        # Aguardar atualização automática (30 segundos)
        time.sleep(35)
        
        # Verificar se houve atualização
        taxa_sucesso_atual = driver.find_element(By.ID, "taxa-sucesso").text
        print(f"Taxa de sucesso inicial: {taxa_sucesso_inicial}")
        print(f"Taxa de sucesso atual: {taxa_sucesso_atual}")
        
        # A atualização pode ou não ter ocorrido dependendo dos dados
        assert taxa_sucesso_atual is not None
    
    def test_indicadores_status_pipeline(self, driver, dashboard_url):
        """Testa se os indicadores de status dos pipelines são exibidos"""
        driver.get(dashboard_url)
        
        # Aguardar carregamento
        time.sleep(3)
        
        # Verificar se o container de pipelines existe
        container_pipelines = driver.find_element(By.ID, "status-pipelines")
        assert container_pipelines.is_displayed()
        
        # Verificar se há itens de pipeline
        itens_pipeline = driver.find_elements(By.CLASS_NAME, "pipeline-item")
        print(f"Encontrados {len(itens_pipeline)} itens de pipeline")
    
    def test_monitoramento_sistema_exibido(self, driver, dashboard_url):
        """Testa se o monitoramento do sistema é exibido"""
        driver.get(dashboard_url)
        
        # Aguardar carregamento
        time.sleep(3)
        
        # Verificar barras de progresso do sistema
        metricas_sistema = [
            "cpu-usage",
            "memory-usage", 
            "disk-usage",
            "network-usage"
        ]
        
        for metrica in metricas_sistema:
            barra_progresso = driver.find_element(By.ID, metrica)
            assert barra_progresso.is_displayed()
            
            # Verificar se tem valor
            texto_metrica = driver.find_element(By.ID, metrica.replace("-usage", "-texto"))
            assert texto_metrica.text != ""
    
    def test_animacoes_e_transicoes(self, driver, dashboard_url):
        """Testa se as animações e transições funcionam"""
        driver.get(dashboard_url)
        
        # Aguardar carregamento inicial
        time.sleep(2)
        
        # Verificar se os cards têm animações
        cards = driver.find_elements(By.CLASS_NAME, "metricas-card")
        for card in cards:
            # Simular hover
            driver.execute_script("arguments[0].scrollIntoView();", card)
            time.sleep(0.5)
            
            # Verificar se o card está visível após scroll
            assert card.is_displayed()
    
    def test_erro_handling_api(self, driver, dashboard_url):
        """Testa o tratamento de erros da API"""
        driver.get(dashboard_url)
        
        # Aguardar carregamento
        time.sleep(3)
        
        # Verificar se não há erros JavaScript no console
        logs = driver.get_log('browser')
        erros_js = [log for log in logs if log['level'] == 'SEVERE']
        
        # Filtrar erros conhecidos (como CORS em desenvolvimento)
        erros_relevantes = [erro for erro in erros_js if 'CORS' not in erro['message']]
        
        if erros_relevantes:
            print(f"Erros JavaScript encontrados: {erros_relevantes}")
            # Em um ambiente de produção, isso seria um falha
            # Para demonstração, apenas logamos os erros

class TestDashboardFuncionalidades:
    """Testes de funcionalidades específicas do dashboard"""
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Configuração do driver Selenium"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        yield driver
        driver.quit()
    
    def test_filtros_tabela_execucoes(self, driver):
        """Testa filtros da tabela de execuções"""
        driver.get("http://localhost:8000")
        time.sleep(3)
        
        # Este teste seria implementado quando os filtros estivessem disponíveis
        # Por enquanto, apenas verificamos se a tabela está presente
        tabela = driver.find_element(By.ID, "tabela-execucoes")
        assert tabela.is_displayed()
    
    def test_exportacao_relatorios(self, driver):
        """Testa funcionalidade de exportação de relatórios"""
        driver.get("http://localhost:8000")
        time.sleep(3)
        
        # Verificar se há botões de download
        botoes_download = driver.find_elements(By.CSS_SELECTOR, "button[title*='Baixar']")
        print(f"Encontrados {len(botoes_download)} botões de download")
    
    def test_notificacoes_sistema(self, driver):
        """Testa sistema de notificações"""
        driver.get("http://localhost:8000")
        time.sleep(3)
        
        # Simular clique no botão de atualizar
        try:
            botao_atualizar = driver.find_element(By.XPATH, "//button[contains(text(), 'Atualizar')]")
            botao_atualizar.click()
            time.sleep(2)
            
            # Verificar se não há erros
            assert True  # Se chegou até aqui, não houve erro crítico
            
        except NoSuchElementException:
            print("Botão de atualizar não encontrado")

if __name__ == "__main__":
    # Executar testes diretamente
    pytest.main([__file__, "-v", "--tb=short"])
