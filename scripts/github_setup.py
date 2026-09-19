#!/usr/bin/env python3
"""
Setup Completo do GitHub — Victor Lopes

Prepara tudo para quando o token PAT for corrigido.
Inclui:
1. Validação do token
2. Criação de repositórios
3. Atualização do README de perfil
4. Configuração de repositórios existentes
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
    """Retorna headers para requisições à API do GitHub."""
    if not GITHUB_TOKEN:
        return None
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "appliation/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def test_token():
    """Testa se o token é válido."""
    log("🔑 Testando token do GitHub...")
    
    if not GITHUB_TOKEN:
        log("❌ Token não configurado", "ERROR")
        return False
    
    try:
        response = requests.get(
            f"{GITHUB_API}/user",
            headers=get_headers(),
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            log(f"✅ Token válido!")
            log(f"   Login: {user_data.get('login')}")
            log(f"   Name: {user_data.get('name', 'Não definido')}")
            log(f"   Email: {user_data.get('email', 'Não definido')}")
            return True
        elif response.status_code == 401:
            log("❌ Token inválido ou expirado", "ERROR")
            log("   Regenere o token em: GitHub Settings > Developer settings > Personal access tokens")
            return False
        else:
            log(f"❌ Erro inesperado: {response.status_code}", "ERROR")
            log(f"   {response.text[:200]}")
            return False
    except Exception as e:
        log(f"❌ Erro de conexão: {e}", "ERROR")
        return False


def create_repository(name, description="", private=False):
    """Cria um novo repositório."""
    log(f"📦 Criando repositório '{name}'...")
    
    if not GITHUB_TOKEN:
        log("❌ Token não configurado", "ERROR")
        return None
    
    try:
        data = {
            "name": name,
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
            log(f"✅ Repositório '{name}' criado!")
            log(f"   URL: {repo.get('html_url')}")
            log(f"  Clone: git clone {repo.get('clone_url')}")
            return repo
        elif response.status_code == 422:
            log(f"⚠️ Repositório '{name}' já existe", "WARN")
            return None
        else:
            log(f"❌ Erro: {response.status_code}", "ERROR")
            log(f"   {response.text[:200]}")
            return None
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        return None


def update_profile_readme():
    """Prepara o README de perfil para GitHub."""
    log("📝 Preparando README de perfil...")
    
    readme_path = Path(__file__).resolve().parent.parent / "github" / "profile-readme.md"
    
    if not readme_path.exists():
        log(f"❌ Arquivo não encontrado: {readme_path}", "ERROR")
        return False
    
    # Ler o README
    readme_content = readme_path.read_text(encoding='utf-8')
    
    # Substituir username
    readme_content = readme_content.replace("victorlopes", GITHUB_USERNAME)
    
    # Salvar versão atualizada
    updated_path = Path(__file__).resolve().parent.parent / "github" / "profile-readme-updated.md"
    updated_path.write_text(readme_content, encoding='utf-8')
    
    log(f"✅ README preparado para {GITHUB_USERNAME}")
    log(f"   Arquivo: {updated_path}")
    log("")
    log("Próximos passos:")
    log(f"  1. Copie o conteúdo de {updated_path}")
    log(f"  2. Acesse https://github.com/{GITHUB_USERNAME}")
    log(f"  3. Crie README.md na raiz do perfil (se não existir)")
    log(f"  4. Cole o conteúdo e salve")
    
    return True


def check_existing_repos():
    """Lista repositórios existentes."""
    log("📦 Verificando repositórios existentes...")
    
    if not GITHUB_TOKEN:
        log("❌ Token não configurado", "ERROR")
        return []
    
    try:
        response = requests.get(
            f"{GITHUB_API}/user/repos?per_page=100&sort=updated",
            headers=get_headers(),
            timeout=30
        )
        
        if response.status_code == 200:
            repos = response.json()
            log(f"✅ {len(repos)} repositórios encontrados")
            
            for repo in repos:
                name = repo.get('name')
                desc = repo.get('description') or '(sem descrição)'
                is_private = repo.get('private', False)
                visibility = "🔒 Privado" if is_private else "🌐 Público"
                log(f"  {visibility} {name}: {desc[:60]}")
            
            return repos
        else:
            log(f"❌ Erro: {response.status_code}", "ERROR")
            return []
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        return []


def setup_git_repo(local_path, remote_url):
    """Configura um repositório local com remote."""
    log(f"🔧 Configurando {local_path}...")
    
    if not os.path.exists(local_path):
        log(f"❌ Diretório não encontrado: {local_path}", "ERROR")
        return False
    
    try:
        import subprocess
        
        # Verificar se é um repo git
        git_dir = Path(local_path) / ".git"
        if not git_dir.exists():
            log(f"   Inicializando git...")
            subprocess.run(["git", "init"], cwd=local_path, check=True, capture_output=True)
        
        # Adicionar remote
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=local_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            log(f"   Remote já configurado: {result.stdout.strip()}")
        else:
            log(f"   Adicionando remote: {remote_url}")
            subprocess.run(
                ["git", "remote", "add", "origin", remote_url],
                cwd=local_path,
                check=True,
                capture_output=True
            )
        
        log(f"✅ Configurado!")
        return True
        
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        return False


def main():
    parser = argparse.ArgumentParser(description="Setup do GitHub para Perfil Profissional")
    parser.add_argument("--validate", action="store_true", help="Validar token")
    parser.add_argument("--create-repos", action="store_true", help="Criar repositórios")
    parser.add_argument("--update-readme", action="store_true", help="Preparar README")
    parser.add_argument("--check-repos", action="store_true", help="Listar repositórios")
    parser.add_argument("--all", action="store_true", help="Executar tudo")
    
    args = parser.parse_args()
    
    log("=" * 60)
    log("📦 SETUP DO GITHUB — Victor Lopes")
    log("=" * 60)
    log("")
    log(f"📍 Username: {GITHUB_USERNAME}")
    log(f"🔑 Token: {'Configurado' if GITHUB_TOKEN else 'NÃO CONFIGURADO'}")
    log("")
    
    # Se nenhum comando especificado, executar tudo
    if not any([args.validate, args.create_repos, args.update_readme, args.check_repos, args.all]):
        args.all = True
    
    success = True
    
    if args.validate or args.all:
        if not test_token():
            log("")
            log("❌ Token inválido. Corrija antes de continuar.", "ERROR")
            log("")
            log("Para gerar um novo token:")
            log("  1. Acesse: https://github.com/settings/tokens")
            log("  2. Clique em 'Generate new token' > 'Generate new token (classic)'")
            log("  3. Selecione os escopos: repo, user")
            log("  4. Copie o token e atualize no arquivo .env")
            return 1
    
    if args.check_repos or args.all:
        check_existing_repos()
        log("")
    
    if args.update_readme or args.all:
        update_profile_readme()
        log("")
    
    if args.create_repos or args.all:
        log("📦 Criando repositórios...")
        log("")
        
        repos_to_create = [
            ("perfil-profissional", "Portfólio profissional de Victor Lopes"),
            ("painel-omega", "Painel Ômega — Controle de Fluxo Financeiro"),
            ("sistema-gestao-empresarial", "Sistema de Gestão Empresarial"),
            ("hermes-agency", "Hermes Agency — Dashboard de Operação"),
        ]
        
        for name, description in repos_to_create:
            create_repository(name, description)
            log("")
    
    if args.all:
        log("=" * 60)
        log("✅ SETUP CONCLUÍDO!")
        log("=" * 60)
        log("")
        log("Próximos passos:")
        log("  1. Fazer push dos projetos para os repositórios")
        log("  2. Configurar GitHub Pages se necessário")
        log("  3. Adicionar links no README de perfil")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
