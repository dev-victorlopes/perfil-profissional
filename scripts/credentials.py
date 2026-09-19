#!/usr/bin/env python3
"""
Helper de Credenciais — Perfil Profissional

ORIENTAÇÃO: Este arquivo é um esqueleto/placeholder.
Ele demonstra como carregar credenciais de forma segura, mas NÃO contém
nenhuma credencial real.

Fluxo de trabalho seguro:
1. Credenciais são armazenadas pelo usuário em:
   - Gerenciador de senhas local (Bitwarden, 1Password, KeePassXC, chaveiro do sistema)
   - Variáveis de ambiente no shell (export MANUAL)
   - Arquivo .env NO LOCAL (não commitado, ignorado pelo git)

2. Durante uma sessão de trabalho, quando uma credencial é necessária:
   a. O agente informa qual credencial é necessária e para qual finalidade
   b. Você fornece a credencial (copiar do gerenciador de senhas)
   c. O agente usa a credencial para a tarefa especificada
   d. A credencial NÃO é persistida em nenhum arquivo

3. Este arquivo mostra o padrão de como credenciais poderiam ser carregadas
   se você quisesse automatizar parte do fluxo no futuro.
"""

import os
import sys
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


 PROJECT_ROOT = Path(__file__).resolve().parent.parent
 ENV_FILE = PROJECT_ROOT / ".env"


# =============================================================================
# Load environment variables
# =============================================================================

def load_env():
    """
    Carrega variáveis de ambiente do arquivo .env LOCAL.
    
    ATENÇÃO: O arquivo .env NÃO deve ser commitado.
    Ele está listado no .gitignore.
    
    Se o arquivo .env não existir, nada é carregado — o programa continua.
    """
    if load_dotenv is None:
        print("Aviso: python-dotenv não instalado. Instale com: pip install python-dotenv", file=sys.stderr)
        return False
    
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
        return True
    return False


# =============================================================================
# Credential access (example patterns)
# =============================================================================

def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Obtém uma variável de ambiente de forma segura.
    
    Use esta função em vez de os.environ['VAR'] para evitar KeyError.
    
    Args:
        name: Nome da variável de ambiente
        default: Valor padrão se a variável não estiver definida
    
    Returns:
        Valor da variável ou default
    """
    return os.environ.get(name, default)


def require_env(name: str) -> str:
    """
    Obtém uma variável de ambiente obrigatória.
    
    Raises:
        ValueError: Se a variável não estiver definida
    """
    value = os.environ.get(name)
    if value is None:
        raise ValueError(
            f"Variável de ambiente '{name}' não definida. "
            f"Crie um arquivo .env local ou exporte a variável no shell."
        )
    return value


# =============================================================================
# Platform credentials (structure only — values come from env/user)
# =============================================================================

class CredentialStore:
    """
    Container para credenciais de plataformas.
    
    ATRIBUTOS NÃO SÃO PREENCHIDOS AUTOMATICAMENTE.
    Use os métodos de classe para carregar de variáveis de ambiente.
    
    Exemplo de uso:
        store = CredentialStore.from_env()
        github_token = store.github_pat
    """
    
    # GitHub
    github_username: Optional[str] = None
    github_pat: Optional[str] = None
    
    # Google / Gmail
    gmail_address: Optional[str] = None
    google_api_key: Optional[str] = None
    google_oauth_token: Optional[str] = None
    
    # LinkedIn
    linkedin_email: Optional[str] = None
    linkedin_password: Optional[str] = None
    
    # Vercel
    vercel_token: Optional[str] = None
    vercel_email: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'CredentialStore':
        """
        Carrega credenciais de variáveis de ambiente.
        
        Variáveis esperadas:
            GITHUB_USERNAME, GITHUB_PAT
            GMAIL_ADDRESS, GOOGLE_API_KEY, GOOGLE_OAUTH_TOKEN
            LINKEDIN_EMAIL, LINKEDIN_PASSWORD
            VERCEL_TOKEN, VERCEL_EMAIL
        
        Se uma variável não estiver definida, o campo correspondente
        será None — o chamador deve tratar isso.
        """
        store = cls()
        store.github_username = os.environ.get('GITHUB_USERNAME')
        store.github_pat = os.environ.get('GITHUB_PAT')
        store.gmail_address = os.environ.get('GMAIL_ADDRESS')
        store.google_api_key = os.environ.get('GOOGLE_API_KEY')
        store.google_oauth_token = os.environ.get('GOOGLE_OAUTH_TOKEN')
        store.linkedin_email = os.environ.get('LINKEDIN_EMAIL')
        store.linkedin_password = os.environ.get('LINKEDIN_PASSWORD')
        store.vercel_token = os.environ.get('VERCEL_TOKEN')
        store.vercel_email = os.environ.get('VERCEL_EMAIL')
        return store
    
    def is_complete_for(self, platform: str) -> bool:
        """Verifica se as credenciais para uma plataforma específica estão disponíveis."""
        checks = {
            'github': bool(self.github_username and self.github_pat),
            'gmail': bool(self.gmail_address),
            'google_api': bool(self.google_api_key),
            'linkedin': bool(self.linkedin_email),
            'vercel': bool(self.vercel_token),
        }
        return checks.get(platform, False)


# =============================================================================
# Manual credential input (when env vars are not available)
# =============================================================================

def prompt_credential(service: str, field: str) -> str:
    """
    Solicita uma credencial ao usuário via input.
    
    USE ESTA FUNÇÃO SOMENTE durante uma sessão interativa,
    e NÃO persista o valor retornado em nenhum arquivo.
    
    Args:
        service: Nome do serviço (ex: "GitHub", "Gmail")
        field: Nome do campo (ex: "token", "senha")
    
    Returns:
        Credencial fornecida pelo usuário
    
    ATENÇÃO: O valor retornado deve ser usado imediatamente e descartado.
    """
    import getpass
    
    label = f"{service} — {field}"
    return getpass.getpass(f"🔑 {label}: ")


# =============================================================================
# Safety: ensure .env is in .gitignore
# =============================================================================

def verify_env_is_ignored() -> bool:
    """
    Verifica se o arquivo .env está listado no .gitignore.
    
    Retorna True se estiver sido ignorado, False caso contrário.
    """
    gitignore_path = PROJECT_ROOT / ".gitignore"
    if not gitignore_path.exists():
        return False
    
    content = gitignore_path.read_text(encoding='utf-8')
    return '.env' in content or '.env*' in content


def ensure_env_in_gitignore():
    """Garante que .env esteja listado no .gitignore (adiciona se faltar)."""
    gitignore_path = PROJECT_ROOT / ".gitignore"
    
    if not gitignore_path.exists():
        gitignore_path.write_text('.env\n.env.*\n')
        print("✅ .gitignore criado com .env")
        return
    
    content = gitignore_path.read_text(encoding='utf-8')
    if '.env' not in content:
        with open(gitignore_path, 'a', encoding='utf-8') as f:
            f.write('\n# Credenciais e variáveis locais\n.env\n.env.*\n')
        print("✅ .env adicionado ao .gitignore")
    else:
        print("✅ .env já está no .gitignore")


# =============================================================================
# CLI
# =============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Helper de credenciais do projeto.')
    subparsers = parser.add_subparsers(dest='command')
    
    p_status = subparsers.add_parser('status', help='Mostrar status de credenciais disponíveis')
    p_verify = subparsers.add_parser('verify', help='Verificar se .env está no .gitignore')
    p_ensure = subparsers.add_parser('ensure-gitignore', help='Garantir que .env está no .gitignore')
    
    args = parser.parse_args()
    
    if args.command == 'status':
        load_env()
        store = CredentialStore.from_env()
        
        print("📋 Status de credenciais disponíveis:")
        print()
        
        platforms = [
            ('GitHub', store.github_username, store.github_pat),
            ('Gmail', store.gmail_address, None),
            ('Google API', store.google_api_key, None),
            ('Google OAuth', store.google_oauth_token, None),
            ('LinkedIn', store.linkedin_email, store.linkedin_password),
            ('Vercel', store.vercel_email, store.vercel_token),
        ]
        
        for name, identifier, secret in platforms:
            has_id = bool(identifier)
            has_secret = bool(secret)
            
            if has_id and has_secret:
                status = '✅ Configurado'
            elif has_id:
                status = '⚠️  Parcial (identificador apenas)'
            else:
                status = '🔴 Não configurado'
            
            print(f"  {name}: {status}")
            if has_id:
                print(f"    Identificador: {identifier[:20]}{'...' if len(identifier) > 20 else ''}")
            print()
        
        print("📌 Para configurar, exporte as variáveis no shell ou crie um arquivo .env")
        print("   (o arquivo .env NÃO deve ser commitado)")
    
    elif args.command == 'verify':
        if verify_env_is_ignored():
            print("✅ .env está listado no .gitignore — seguro para usar localmente.")
        else:
            print("❌ .env NÃO está listado no .gitignore!")
            print("   Adicione '.env' ao .gitignore imediatamente.")
            sys.exit(1)
    
    elif args.command == 'ensure-gitignore':
        ensure_env_in_gitignore()
    
    else:
        parser.print_help()
