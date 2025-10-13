@echo off
REM QA Test Automation Dashboard - Script de Execução (Windows)
REM Desenvolvido por Isabella Barbosa - Engenheira de QA Sênior

echo 🚀 QA Test Automation Dashboard - Execução
echo ========================================

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Instale Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

REM Verificar se estamos no diretório correto
if not exist "backend\app.py" (
    echo ❌ Execute este script no diretório raiz do projeto
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Configurar backend
echo 🔧 Configurando backend...
cd backend

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo 📁 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar ambiente virtual
echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo 📦 Instalando dependências...
pip install -r requirements.txt

REM Inicializar banco de dados
echo 🗄️ Inicializando banco de dados...
python -c "from app import criar_aplicacao; app = criar_aplicacao(); print('✅ Banco inicializado!')"

REM Iniciar backend
echo 🚀 Iniciando backend...
start "QA Dashboard Backend" cmd /k "python app.py"

cd ..

REM Aguardar backend inicializar
echo ⏳ Aguardando backend inicializar...
timeout /t 5 /nobreak >nul

REM Iniciar frontend
echo 🎨 Iniciando frontend...
cd frontend
start "QA Dashboard Frontend" cmd /k "python -m http.server 8000"

cd ..

echo.
echo ✅ QA Test Automation Dashboard iniciado!
echo.
echo 🌐 Dashboard: http://localhost:8000
echo 🔧 API: http://localhost:5000/api
echo 💚 Health: http://localhost:5000/health
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
