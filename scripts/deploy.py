#!/usr/bin/env python3
"""
Deploy do Portfólio — Vercel

Comandos disponíveis:
    python scripts/deploy.py check        # Verificar se está pronto para deploy
    python scripts/deploy.py login        # Login na Vercel (se necessário)
    python scripts/deploy.py deploy       # Fazer deploy do portfólio
    python scripts/deploy.py status       # Ver status do último deploy

Requer:
    - Vercel CLI (vercel) instalado globalmente ou via npx
    - VERCEL_TOKEN configurado no .env (opcional — pode fazer login interativo)
"""

import os
import sys
import subprocess
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
VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN", "")
VERCEL_EMAIL = os.environ.get("VERCEL_EMAIL", "")

# O portfólio é estático (HTML/CSS/JS), então o deploy é simples
PORTFOLIO_DIR = PROJECT_ROOT  # O index.html está na raiz


# =============================================================================
# Commands
# =============================================================================

def cmd_check():
    """Verifica se está pronto para fazer deploy."""
    print("🔍 Verificando prontidão para deploy")
    print()
    
    checks = []
    
    # 1. Verificar se os arquivos existen
    index_html = PORTFOLIO_DIR / "index.html"
    styles_css = PORTFOLIO_DIR / "styles.css"
    script_js = PORTFOLIO_DIR / "script.js"
    
    for path, name in [(index_html, "index.html"), (styles_css, "styles.css"), (script_js, "script.js")]:
        exists = path.exists()
        checks.append((f"Arquivo {name}", exists))
        status = "✅" if exists else "❌"
        print(f"  {status} {name}")
    
    print()
    
    # 2. Verificar Vercel CLI
    try:
        result = subprocess.run(["vercel", "--version"], capture_output=True, text=True, check=False)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"  ✅ Vercel CLI instalado: {version}")
        else:
            print("  ❌ Vercel CLI não encontrado ou não funcional")
            print("     Instale com: npm install -g vercel")
    except FileNotFoundError:
        print("  ❌ Vercel CLI não instalado")
        print("     Instale com: npm install -g vercel")
    
    print()
    
    # 3. Verificar Vercel token
    if VERCEL_TOKEN:
        print("  ✅ Vercel Token configurado")
    else:
        print("  ℹ️  Vercel Token não configurado (fará login interativo se necessário)")
    
    print()
    
    # Resumo
    all_ok = all(result for _, result in checks)
    if all_ok:
        print("✅ Pronto para deploy!")
    else:
        print("❌ Alguns arquivos estão faltando. Corrija antes de continuar.")
    
    return all_ok


def cmd_login():
    """Faz login na Vercel."""
    print("🔑 Fazendo login na Vercel...")
    print()
    
    try:
        result = subprocess.run(
            ["vercel", "login"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            print("✅ Login realizado com sucesso!")
            print(result.stdout)
        else:
            print("❌ Login falhou:")
            print(result.stderr or result.stdout)
    except FileNotFoundError:
        print("❌ Vercel CLI não instalado.")
        print("   Instale com: npm install -g vercel")


def cmd_deploy():
    """Faz deploy do portfólio na Vercel."""
    print("🚀 Fazendo deploy do portfólio na Vercel...")
    print()
    
    if not (PORTFOLIO_DIR / "index.html").exists():
        print("❌ index.html não encontrado. Não há o que deployar.")
        sys.exit(1)
    
    # Verificar Vercel CLI
    try:
        subprocess.run(["vercel", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ Vercel CLI não instalado ou não funcional.")
        print("   Instale com: npm install -g vercel")
        sys.exit(1)
    
    # Se tiver token, configurar
    if VERCEL_TOKEN:
        print("Configurando token Vercel...")
        env = os.environ.copy()
        env["VERCEL_TOKEN"] = VERCEL_TOKEN
    else:
        env = None
    
    try:
        result = subprocess.run(
            ["vercel", "--prod", "--confirm"],
            cwd=PORTFOLIO_DIR,
            capture_output=True,
            text=True,
            env=env,
        )
        
        if result.returncode == 0:
            print("✅ Deploy concluído com sucesso!")
            print()
            print("📌 URLs:")
            print(result.stdout)
        else:
            print("❌ Deploy falhou:")
            print(result.stderr or result.stdout)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")


def cmd_status():
    """Verifica o status do deploy atual."""
    print("📊 Status do deploy Vercel")
    print()
    
    try:
        result = subprocess.run(
            ["vercel", "ls"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Não foi possível listar os deployments.")
            print(result.stderr or result.stdout)
    except FileNotFoundError:
        print("❌ Vercel CLI não instalado.")


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy do portfólio na Vercel")
    subparsers = parser.add_subparsers(dest='command')
    
    subparsers.add_parser('check', help='Verificar se está pronto para deploy')
    subparsers.add_parser('login', help='Fazer login na Vercel')
    subparsers.add_parser('deploy', help='Fazer deploy do portfólio')
    subparsers.add_parser('status', help='Ver status do deploy')
    
    args = parser.parse_args()
    
    if args.command == 'check':
        cmd_check()
    elif args.command == 'login':
        cmd_login()
    elif args.command == 'deploy':
        cmd_deploy()
    elif args.command == 'status':
        cmd_status()
    else:
        parser.print_help()
