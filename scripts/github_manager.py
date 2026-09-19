#!/usr/bin/env python3
"""
Gerenciador de GitHub — Perfil Profissional

Comandos disponíveis:
    python scripts/github_manager.py status       # Ver status da conta
    python scripts/github_manager.py repos        # Listar repositórios
    python scripts/github_manager.py create-repo <nome> [descricao]  # Criar repositório
    python scripts/github_manager.py update-readme  # Atualizar README do perfil
    python scripts/github_manager.py sync         # Sincronizar projetos locais com GitHub

Requer:
    - python-dotenv
    - requests
    - Credenciais configuradas no arquivo .env
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

# Try to load .env
try:
    from dotenv import load_dotenv
    ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
except ImportError:
    pass  # python-dotenv não instalado, mas podemos tentar sem ele

import requests


# =============================================================================
# Configuration
# =============================================================================

GITHUB_API = "https://api.github.com"
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "dev-victorlopes")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


# =============================================================================
# Helpers
# =============================================================================

def get_headers() -> dict:
    """Retorna headers para requisições à API do GitHub."""
    if not GITHUB_TOKEN:
        print("❌ GitHub Token não configurado. Configure no arquivo .env", file=sys.stderr)
        sys.exit(1)
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def api_request(method: str, endpoint: str, **kwargs) -> dict | list | None:
    """Faz uma requisição à API do GitHub."""
    url = f"{GITHUB_API}{endpoint}"
    headers = get_headers()
    
    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na API: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status: {e.response.status_code}", file=sys.stderr)
            print(f"   Resposta: {e.response.text[:200]}", file=sys.stderr)
        return None


# =============================================================================
# Commands
# =============================================================================

def cmd_status():
    """Verifica o status da conta GitHub."""
    print(f"👤 Usuário: {GITHUB_USERNAME}")
    
    # Verificar autenticação
    user = api_request("GET", "/user")
    if user:
        print(f"✅ Autenticação: OK")
        print(f"   Login: {user.get('login')}")
        print(f"   Name: {user.get('name', 'Não definido')}")
        print(f"   Email: {user.get('email', 'Não definido')}")
        print(f"   Bio: {user.get('bio', 'Não definido')}")
        print(f"   Público: {user.get('public_repos', 0)} repositórios")
    else:
        print("❌ Falha na autenticação. Verifique o token.")
    
    print()
    print("📋 Configuração:")
    print(f"   GITHUB_USERNAME: {GITHUB_USERNAME}")
    print(f"   GITHUB_TOKEN: {'✅ Configurado' if GITHUB_TOKEN else '❌ Não configurado'}")


def cmd_repos():
    """Lista os repositórios do usuário."""
    repos = api_request("GET", "/user/repos?per_page=100&sort=updated")
    if not repos:
        return
    
    print(f"📦 Repositórios de {GITHUB_USERNAME}:")
    print("-" * 60)
    
    for repo in repos:
        name = repo.get('name')
        desc = repo.get('description') or '(sem descrição)'
        lang = repo.get('language') or '-'
        stars = repo.get('stargazers_count', 0)
        updated = repo.get('updated_at', '')[:10]
        is_private = repo.get('private', False)
        privacy = "🔒 Privado" if is_private else "🌐 Público"
        
        print(f"\n  {name}")
        print(f"    {privacy} | {lang} | ⭐ {stars}")
        print(f"    {desc}")
        print(f"    Atualizado: {updated}")
    
    print(f"\nTotal: {len(repos)} repositórios")


def cmd_create_repo(name: str, description: str = ""):
    """Cria um novo repositório público."""
    print(f"📦 Criando repositório '{name}'...")
    
    data = {
        "name": name,
        "description": description,
        "private": False,
        "auto_init": True,
    }
    
    result = api_request("POST", "/user/repos", json=data)
    if result:
        print(f"✅ Repositório '{name}' criado com sucesso!")
        print(f"   URL: {result.get('html_url')}")
        print(f"   Clone: git clone {result.get('clone_url')}")
    
    return result


def cmd_update_readme():
    """Atualiza o README do perfil com o conteúdo do projeto."""
    from pathlib import Path
    
    readme_path = Path(__file__).resolve().parent.parent / "github" / "profile-readme.md"
    
    if not readme_path.exists():
        print(f"❌ Arquivo README não encontrado: {readme_path}", file=sys.stderr)
        print("   Verifique se o arquivo github/profile-readme.md existe.", file=sys.stderr)
        sys.exit(1)
    
    readme_content = readme_path.read_text(encoding='utf-8')
    
    # Substituir username
    readme_content = readme_content.replace("victorlopes", GITHUB_USERNAME)
    
    # Salvar versão atualizada
    updated_path = Path(__file__).resolve().parent.parent / "github" / "profile-readme-updated.md"
    updated_path.write_text(readme_content, encoding='utf-8')
    
    print(f"📝 README do perfil preparado para {GITHUB_USERNAME}:")
    print(f"   Arquivo: {updated_path}")
    print()
    print("Próximos passos:")
    print(f"  1. Copie o conteúdo de {updated_path}")
    print(f"  2. Acesse https://github.com/{GITHUB_USERNAME}")
    print(f"  3. Crie um arquivo README.md na raiz do perfil (se não existir)")
    print(f"  4. Cole o conteúdo e salve")
    
    # Se o repositório de perfil existir, podemos tentar atualizar via API
    # (isso atualizaria o README.md do repositório github-profile)
    profile_repo = api_request("GET", f"/repos/{GITHUB_USERNAME}/{GITHUB_USERNAME}")
    if profile_repo:
        print(f"\n🔄 Repositório de perfil encontrado: {GITHUB_USERNAME}/{GITHUB_USERNAME}")
        print("   O README.md do repositório pode ser atualizado via GitHub UI.")


def cmd_sync():
    """Sincroniza os projetos locais com o GitHub."""
    from pathlib import Path
    
    project_root = Path(__file__).resolve().parent.parent
    
    print(f"🔄 Sincronizando projetos com GitHub ({GITHUB_USERNAME})")
    print()
    
    # Mapeamento de projetos locais para repositórios suggestion
    local_projects = [
        ("perfil-profissional", "perfil-profissional", "Portfólio profissional"),
        ("../../fluxo-financeiro", "painel-omega", "Painel Ômega — Controle Financeiro"),
        ("../../sistema-gestao", "sistema-gestao-empresarial", "Sistema de Gestão Empresarial"),
        ("../../Hermes_Agency", "hermes-agency", "Hermes Agency — Dashboard de Operação"),
    ]
    
    for local_path, repo_name, description in local_projects:
        full_local_path = project_root.parent / local_path
        
        print(f"📁 {repo_name}")
        print(f"   Descrição: {description}")
        print(f"   Local: {full_local_path}")
        
        if full_local_path.exists():
            # Verificar se é um repo git
            git_dir = full_local_path / ".git"
            if git_dir.exists():
                print(f"   ✅ Já é um repositório Git")
                
                # Verificar remote
                try:
                    result = subprocess.run(
                        ["git", "remote", "-v"],
                        cwd=full_local_path,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    remotes = result.stdout.strip()
                    if remotes:
                        print(f"   Remotes: {remotes.split(chr(10))[0]}")
                    else:
                        print(f"   ⚠️  Sem remote configurado")
                except Exception as e:
                    print(f"   ℹ️  Não foi possível verificar remotes: {e}")
            else:
                print(f"   ❌ Não é um repositório Git")
        else:
            print(f"   ℹ️  Diretório não encontrado (pode ser um projeto futuro)")
        
        print()


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerenciador de GitHub para Perfil Profissional")
    subparsers = parser.add_subparsers(dest='command')
    
    # status
    subparsers.add_parser('status', help='Ver status da conta GitHub')
    
    # repos
    subparsers.add_parser('repos', help='Listar repositórios')
    
    # create-repo
    create_parser = subparsers.add_parser('create-repo', help='Criar novo repositório')
    create_parser.add_argument('name', help='Nome do repositório')
    create_parser.add_argument('description', nargs='?', default='', help='Descrição')
    
    # update-readme
    subparsers.add_parser('update-readme', help='Preparar README do perfil')
    
    # sync
    subparsers.add_parser('sync', help='Sincronizar projetos locais')
    
    args = parser.parse_args()
    
    if not GITHUB_TOKEN:
        print("❌ GitHub Token não configurado.", file=sys.stderr)
        print("   Configure no arquivo .env: GITHUB_TOKEN=seu_token_aqui", file=sys.stderr)
        sys.exit(1)
    
    if args.command == 'status':
        cmd_status()
    elif args.command == 'repos':
        cmd_repos()
    elif args.command == 'create-repo':
        cmd_create_repo(args.name, args.description)
    elif args.command == 'update-readme':
        cmd_update_readme()
    elif args.command == 'sync':
        cmd_sync()
    else:
        parser.print_help()
