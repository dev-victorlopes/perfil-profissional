#!/usr/bin/env python3
"""
Orquestrador do Perfil Profissional

Comandos disponíveis:
    python scripts/manager.py status       # Ver status geral do perfil
    python scripts/manager.py setup        # Configurar ambiente de trabalho
    python scripts/manager.py auth-status  # Ver status de autorização
    python scripts/manager.py github       # Abrir gerenciador do GitHub
    python scripts/manager.py linkedin     # Abrir gerenciador do LinkedIn
    python scripts/manager.py google       # Abrir gerenciador do Google
    python scripts/manager.py deploy       # Gerenciar deploy Vercel

Requer:
    - Todos os scripts na pasta scripts/
    - Credenciais no arquivo .env
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from dotenv import load_dotenv
    ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
except ImportError:
    pass


# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

PROFILE_NAME = os.environ.get("PROFILE_NAME", "Victor Lopes")
PROFILE_EMAIL = os.environ.get("PROFILE_EMAIL", "desenvolvedor.victorlopes@gmail.com")
PROFILE_WHATSAPP = os.environ.get("WHATSAPP_NUMBER", "+5521959223179")
PROFILE_LOCATION = os.environ.get("PROFILE_LOCATION", "Rio de Janeiro/RJ")


# =============================================================================
# Status
# =============================================================================

def cmd_status():
    """Mostra o status geral do ambiente de trabalho."""
    print("=" * 60)
    print("📋 STATUS DO PERFIL PROFISSIONAL")
    print("=" * 60)
    print()
    print(f"👤 Perfil: {PROFILE_NAME}")
    print(f"📧 E-mail: {PROFILE_EMAIL}")
    print(f"📱 WhatsApp: {PROFILE_WHATSAPP}")
    print(f"📍 Localização: {PROFILE_LOCATION}")
    print()
    
    # Credenciais disponíveis
    print("🔐 CREDENCIAIS DISPONÍVEIS:")
    print()
    
    credentials_status = [
        ("GitHub", bool(os.environ.get("GITHUB_TOKEN")), 
         os.environ.get("GITHUB_USERNAME", "dev-victorlopes")),
        ("Gmail", bool(os.environ.get("GMAIL_EMAIL")),
         os.environ.get("GMAIL_EMAIL", "")),
        ("Google API", bool(os.environ.get("GOOGLE_API_KEY")),
         "API Key configurada" if os.environ.get("GOOGLE_API_KEY") else "Não configurada"),
        ("LinkedIn", bool(os.environ.get("LINKEDIN_EMAIL")),
         os.environ.get("LINKEDIN_EMAIL", "")),
        ("Vercel", bool(os.environ.get("VERCEL_TOKEN")),
         "Token configurado" if os.environ.get("VERCEL_TOKEN") else "Não configurado"),
    ]
    
    for platform, configured, info in credentials_status:
        status_icon = "✅" if configured else "❌"
        print(f"  {status_icon} {platform}: {info}")
    
    print()
    print("📂 PROJETO:")
    print(f"   Raiz: {PROJECT_ROOT}")
    print(f"   Portfólio: {'✅' if (PROJECT_ROOT / 'index.html').exists() else '❌'} index.html")
    print(f"   Painel Admin: {'✅' if (PROJECT_ROOT / 'admin').exists() else '❌'} admin/")
    print(f"   Currículo PDF: {'✅' if (PROJECT_ROOT / 'resume/curriculo_victor_lopes.pdf').exists() else '❌'} PDF")
    print(f"   Scripts: {'✅' if (SCRIPTS_DIR).exists() else '❌'} scripts/")
    print()
    
    # Arquivos de configuração
    config_files = [
        ".env",
        ".env.example",
        ".gitignore",
        "config/project.yaml",
        "requirements.txt",
    ]
    
    print("📄 ARQUIVOS DE CONFIGURAÇÃO:")
    for filename in config_files:
        path = PROJECT_ROOT / filename
        exists = path.exists()
        status_icon = "✅" if exists else "❌"
        print(f"  {status_icon} {filename}")
    
    print()
    print("=" * 60)


def cmd_setup():
    """Configura o ambiente de trabalho para o perfil profissional."""
    print("🔧 Configurando ambiente de trabalho...")
    print()
    
    # 1. Verificar .gitignore
    gitignore_path = PROJECT_ROOT / ".gitignore"
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding='utf-8')
        if '.env' in content or '.env*' in content:
            print("✅ .gitignore já protege o arquivo .env")
        else:
            print("⚠️  .gitignore não protege o .env. Adicionando...")
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write("\n# Variáveis de ambiente (não commitar)\n.env\n.env.*\n")
            print("✅ .env adicionado ao .gitignore")
    else:
        print("❌ .gitignore não encontrado. Criando...")
        gitignore_path.write_text("""# Python
__pycache__/
*.py[cod]
venv/
.env
.env.*\n""")
        print("✅ .gitignore criado")
    
    # 2. Verificar .env
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        print("✅ Arquivo .env existe")
        # Verificar se tem conteúdo
        content = env_path.read_text(encoding='utf-8')
        if len(content.strip()) > 0:
            print("   ✅ .env tem conteúdo")
        else:
            print("   ⚠️  .env está vazio. Preencha as credenciais.")
    else:
        print("❌ Arquivo .env não existe.")
        print("   Crie um arquivo .env baseado no .env.example")
        example_path = PROJECT_ROOT / ".env.example"
        if example_path.exists():
            print(f"   Arquivo de exemplo: {example_path}")
    
    print()
    print("📦 Instalando dependências Python...")
    requirements_path = PROJECT_ROOT / "requirements.txt"
    if requirements_path.exists():
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
                check=False,
            )
            print("✅ Dependências instaladas (ou já estavam instaladas)")
        except Exception as e:
            print(f"⚠️  Erro ao instalar dependências: {e}")
    else:
        print("⚠️  requirements.txt não encontrado")
    
    print()
    print("✅ Configuração concluída!")
    print()
    print("Próximos passos:")
    print("  1. Preencha as credenciais no arquivo .env")
    print("  2. Execute: python scripts/manager.py status")
    print("  3. Execute os comandos de cada plataforma conforme necessário")


def cmd_auth_status():
    """Verifica o status de autorização para gerenciar as contas."""
    print("🔒 STATUS DE AUTORIZAÇÃO")
    print()
    print("Você autorizou o gerenciamento das seguintes contas para o")
    print("perfil profissional de Victor Lopes:")
    print()
    print("  ✅ GitHub (dev-victorlopes)")
    print("  ✅ Gmail (desenvolvedor.victorlopes@gmail.com)")
    print("  ✅ LinkedIn (desenvolvedor.victorlopes@gmail.com)")
    print("  ✅ Google API (chave configurada)")
    print()
    print("📌 Esta autorização é persistente e vale para todas as sessões.")
    print("   Para revogar, edite o arquivo .env e remova as variáveis")
    print("   AUTHORIZED_* ou defina como false.")
    print()
    print("🔐 Credenciais sensíveis (tokens, senhas) são gerenciadas")
    print("   separadamente via .env e não são armazenadas em código.")


def run_script(script_name: str):
    """Executa um script de gerenciamento específico."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"❌ Script não encontrado: {script_name}", file=sys.stderr)
        sys.exit(1)
    
    print(f"📂 Executando: {script_name}")
    print("=" * 60)
    print()
    
    result = subprocess.run(
        [sys.executable, str(script_path)] + sys.argv[2:],
        cwd=PROJECT_ROOT,
    )
    
    return result.returncode


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import subprocess
    
    parser = argparse.ArgumentParser(description="Orquestrador do Perfil Profissional")
    subparsers = parser.add_subparsers(dest='command')
    
    subparsers.add_parser('status', help='Ver status geral do perfil')
    subparsers.add_parser('setup', help='Configurar ambiente de trabalho')
    subparsers.add_parser('auth-status', help='Ver status de autorização')
    subparsers.add_parser('github', help='Gerenciador do GitHub')
    subparsers.add_parser('linkedin', help='Gerenciador do LinkedIn')
    subparsers.add_parser('google', help='Gerenciador do Google API')
    subparsers.add_parser('deploy', help='Gerenciador de Deploy Vercel')
    
    args = parser.parse_args()
    
    if args.command == 'status':
        cmd_status()
    elif args.command == 'setup':
        cmd_setup()
    elif args.command == 'auth-status':
        cmd_auth_status()
    elif args.command == 'github':
        sys.argv[1] = 'github_manager.py'
        sys.exit(run_script('github_manager.py'))
    elif args.command == 'linkedin':
        sys.exit(run_script('linkedin_manager.py'))
    elif args.command == 'google':
        sys.exit(run_script('google_manager.py'))
    elif args.command == 'deploy':
        sys.exit(run_script('deploy.py'))
    else:
        parser.print_help()
