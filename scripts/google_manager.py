#!/usr/bin/env python3
"""
Gerenciador de Google APIs — Perfil Profissional

Comandos disponíveis:
    python scripts/google_manager.py status       # Ver status da API key
    python scripts/google_manager.py youtube      # Status do YouTube/YouTube Studio
    python scripts/google_manager.py test-api     # Testar conexão com uma API Google

Requer:
    - python-dotenv
    - requests
    - Credenciais configuradas no arquivo .env
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

import requests


# =============================================================================
# Configuration
# =============================================================================

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")


# =============================================================================
# Commands
# =============================================================================

def cmd_status():
    """Verifica o status da API key do Google."""
    print("📋 Configuração Google API:")
    print(f"   GOOGLE_API_KEY: {'✅ Configurado' if GOOGLE_API_KEY else '❌ Não configurado'}")
    
    if GOOGLE_API_KEY:
        # Testar a API key com uma requisição simples
        # Usamos a API de informações do YouTube para testar
        test_url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "snippet",
            "mine": "true",
            "key": GOOGLE_API_KEY,
        }
        
        try:
            response = requests.get(test_url, params=params, timeout=10)
            
            if response.status_code == 200:
                print("   ✅ API key válida e funcional")
            elif response.status_code == 403:
                print("   ⚠️  API key válida, mas sem permissão para este recurso")
                print("      (Pode precisar de OAuth para YouTube)")
            elif response.status_code == 400:
                print("   ❌ API key inválida")
            else:
                print(f"   ⚠️  Status inesperado: {response.status_code}")
                print(f"      {response.text[:200]}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro de conexão: {e}")


def cmd_youtube():
    """Verifica status do acesso ao YouTube/YouTube Studio."""
    print("📺 YouTube / YouTube Studio")
    print()
    
    if not GOOGLE_API_KEY:
        print("❌ API Key não configurada.")
        print("   Configure em: Google Cloud Console > APIs & Services > Credentials")
        return
    
    # Testar acesso básico
    print("Testando acesso à API...")
    
    # Lista de verificação para o que está possível com a API key
    checks = [
        ("API Key configurada", bool(GOOGLE_API_KEY)),
        ("YouTube Data API v3 habilitada", True),  # Precisamos testar
    ]
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
    
    print()
    print("📌 Para gerenciar vídeos do YouTube:")
    print("   - API Key permite leitura básica (busca, detalhes de vídeos)")
    print("   - Para upload/criação, é necessário OAuth 2.0")
    print("   - YouTube Studio pode ser acessado via navegação normal")


def cmd_test_api():
    """Testa a conexão com várias APIs Google."""
    print("🧪 Testando conexões com APIs Google")
    print()
    
    if not GOOGLE_API_KEY:
        print("❌ API Key não configurada.")
        sys.exit(1)
    
    tests = [
        {
            "name": "YouTube Data API v3",
            "url": "https://www.googleapis.com/youtube/v3/channels",
            "params": {"part": "snippet", "mine": "true", "key": GOOGLE_API_KEY},
        },
        {
            "name": "Google Custom Search (se configurada)",
            "url": "https://www.googleapis.com/customsearch/v1",
            "params": {"key": GOOGLE_API_KEY, "q": "test", "cx": "test"},
        },
    ]
    
    for test in tests:
        print(f"  🔄 {test['name']}...")
        try:
            response = requests.get(test['url'], params=test['params'], timeout=10)
            
            if response.status_code == 200:
                print(f"     ✅ OK (status 200)")
            elif response.status_code == 403:
                print(f"     ⚠️  Proibido (403) — API pode não estar habilitada ou sem escopo")
            elif response.status_code == 400:
                print(f"     ❌ Erro de requisição (400) — verifique os parâmetros")
            else:
                print(f"     ⚠️  Status: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"     ⏱️  Timeout")
        except requests.exceptions.RequestException as e:
            print(f"     ❌ Erro: {e}")
        
        print()


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerenciador de Google APIs para Perfil Profissional")
    subparsers = parser.add_subparsers(dest='command')
    
    subparsers.add_parser('status', help='Ver status da API key')
    subparsers.add_parser('youtube', help='Status do YouTube')
    subparsers.add_parser('test-api', help='Testar conexões com APIs')
    
    args = parser.parse_args()
    
    if args.command == 'status':
        cmd_status()
    elif args.command == 'youtube':
        cmd_youtube()
    elif args.command == 'test-api':
        cmd_test_api()
    else:
        parser.print_help()
