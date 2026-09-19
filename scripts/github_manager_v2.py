#!/usr/bin/env python3
"""
GitHub Manager — Victor Lopes
Gerenciador de operações GitHub com fallback para operações públicas.
"""

import os
import sys
import time
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


GITHUB_API = "https://api.github.com"
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "dev-victorlopes")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


def log(msg, level="INFO"):
    print(f"[{time.strftime('%H:%M:%S')}] {level}: {msg}", flush=True)


def get_headers():
    if GITHUB_TOKEN:
        return {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    return {"Accept": "application/vnd.github+json"}


def test_auth():
    """Testa autenticação."""
    if not GITHUB_TOKEN:
        log("⚠️ Token não configurado", "WARN")
        return None
    
    try:
        response = requests.get(f"{GITHUB_API}/user", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            user = response.json()
            log(f"✅ Autenticado como: {user.get('login')}")
            return user
        elif response.status_code == 401:
            log("❌ Token inválido", "ERROR")
            return None
        else:
            log(f"⚠️ Status inesperado: {response.status_code}", "WARN")
            return None
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        return None


def get_public_profile(username):
    """Obtém perfil público (funciona sem token)."""
    log(f"📋 Obtendo perfil público de {username}...")
    
    try:
        response = requests.get(f"{GITHUB_API}/users/{username}", timeout=10)
        if response.status_code == 200:
            user = response.json()
            log(f"✅ Perfil encontrado: {user.get('login')}")
            log(f"   Name: {user.get('name', 'N/A')}")
            log(f"   Public repos: {user.get('public_repos', 0)}")
            log(f"   Followers: {user.get('followers', 0)}")
            log(f"   Following: {user.get('following', 0)}")
            log(f"   Bio: {user.get('bio', 'N/A')}")
            return user
        elif response.status_code == 404:
            log(f"❌ Usuário {username} não encontrado", "ERROR")
            return None
        else:
            log(f"⚠️ Status: {response.status_code}", "WARN")
            return None
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        return None


def check_repo_exists(username, repo_name):
    """Verifica se um repositório existe."""
    log(f"🔍 Verificando se '{repo_name}' existe em {username}...")
    
    try:
        # Usar API pública (sem token)
        response = requests.get(f"{GITHUB_API}/repos/{username}/{repo_name}", timeout=10)
        
        if response.status_code == 200:
            repo = response.json()
            log(f"✅ Repositório existe: {repo.get('html_url')}")
            return True
        elif response.status_code == 404:
            log(f"❌ Repositório não existe")
            return False
        else:
            log(f"⚠️ Status: {response.status_code}", "WARN")
            return None
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        return None


def create_repo(username, repo_name, description="", private=False):
    """Cria um repositório (requer token válido)."""
    log(f"📦 Criando repositório '{repo_name}'...")
    
    if not GITHUB_TOKEN:
        log("❌ Token necessário para criar repositório", "ERROR")
        return None
    
    try:
        data = {
            "name": repo_name,
            "description": description,
            "private": private,
            "auto_init": True,
        }
        
        response = requests.post(
            f"{GITHUB_API}/user/repos",
            headers=get_headers(),
            json=data,
            timeout=30
        )
        
        if response.status_code == 201:
            repo = response.json()
            log(f"✅ Repositório '{repo_name}' criado!")
            log(f"   URL: {repo.get('html_url')}")
            return repo
        elif response.status_code == 422:
            log(f"⚠️ Repositório '{repo_name}' já existe")
            return None
        elif response.status_code == 401:
            log("❌ Token inválido", "ERROR")
            return None
        else:
            log(f"❌ Erro: {response.status_code}")
            log(f"   {response.text[:200]}")
            return None
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        return None


def update_readme_content():
    """Prepara README de perfil."""
    log("📝 Preparando README de perfil...")
    
    readme_path = Path(__file__).resolve().parent.parent / "github" / "profile-readme.md"
    
    if not readme_path.exists():
        log(f"❌ Arquivo não encontrado: {readme_path}", "ERROR")
        return False
    
    content = readme_path.read_text(encoding='utf-8')
    content = content.replace("victorlopes", GITHUB_USERNAME)
    
    updated_path = Path(__file__).resolve().parent.parent / "github" / "profile-readme-updated.md"
    updated_path.write_text(content, encoding='utf-8')
    
    log(f"✅ README preparado para {GITHUB_USERNAME}")
    log(f"   Salvo em: {updated_path}")
    log("")
    log("Para usar:")
    log(f"  1. Copie {updated_path}")
    log(f"  2. Acesse https://github.com/{GITHUB_USERNAME}")
    log(f"  3. Crie README.md na raiz do perfil")
    log(f"  4. Cole e salve")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="GitHub Manager — Victor Lopes")
    parser.add_argument("--check-profile", action="store_true", help="Verificar perfil público")
    parser.add_argument("--check-repos", action="store_true", help="Verificar repositórios existentes")
    parser.add_argument("--create-repo", nargs=2, metavar=("NOME", "DESCRICAO"), help="Criar repositório")
    parser.add_argument("--update-readme", action="store_true", help="Preparar README de perfil")
    parser.add_argument("--test-auth", action="store_true", help="Testar autenticação")
    parser.add_argument("--all", action="store_true", help="Executar verificações básicas")
    
    args = parser.parse_args()
    
    log("=" * 60)
    log("📦 GITHUB MANAGER — Victor Lopes")
    log("=" * 60)
    log(f"📍 Username: {GITHUB_USERNAME}")
    log(f"🔑 Token: {'Configurado' if GITHUB_TOKEN else 'NÃO CONFIGURADO'}")
    log("")
    
    if args.test_auth or args.all:
        test_auth()
        log("")
    
    if args.check_profile or args.all:
        get_public_profile(GITHUB_USERNAME)
        log("")
    
    if args.check_repos or args.all:
        repos_to_check = [
            "perfil-profissional",
            "painel-omega", 
            "sistema-gestao-empresarial",
            "hermes-agency"
        ]
        for repo in repos_to_check:
            check_repo_exists(GITHUB_USERNAME, repo)
        log("")
    
    if args.update_readme or args.all:
        update_readme_content()
        log("")
    
    if args.create_repo:
        name, description = args.create_repo
        create_repo(GITHUB_USERNAME, name, description)
        log("")
    
    if not args.test_auth and not args.check_profile and not args.check_repos and not args.create_repo and not args.update_readme and not args.all:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
