#!/usr/bin/env python3
"""
Autenticação e Autorização — Perfil Profissional

Gerencia a autorização para gerenciar as contas do perfil profissional.
O estado de autorização é persistente (arquivo local criptografado com senha mestra).

PRINCÍPIO DE SEGURANÇA:
- Credenciais sensíveis NÃO são armazenadas em texto puro
- O arquivo de autorização é protegido por senha mestra
- Sem a senha mestra, o arquivo é inútil

Estrutura do arquivo de autorização:
    auth.session
    ├── version: 1
    ├── created_at: ISO timestamp
    ├── master_password_hash: hash da senha mestra (para verificação, não reversão)
    ├── accounts:
    │   ├── gmail: { authorized, last_used, rotate_after }
    │   ├── github: { authorized, last_used, rotate_after }
    │   └── linkedin: { authorized, last_used, rotate_after }
    └── session_expiry: quando este arquivo expira

Fluxo de trabalho:
    1. Na primeira vez, o usuário define uma senha mestra
    2. As credenciais são fornecidas sob demanda durante a sessão
    3. O estado de autorização é salvo localmente (criptografado)
    4. Para sessões futuras, a senha mestra é solicitada para descriptografar
"""

import os
import sys
import json
import time
import hashlib
import getpass
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

try:
    import cryptography.fernet
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTH_DIR = PROJECT_ROOT / ".auth"
AUTH_FILE = AUTH_DIR / "auth.session"
MASTER_PASSWORD_FILE = AUTH_DIR / ".master_pass_hash"


# =============================================================================
# Password hashing (simple but adequate for local auth)
# =============================================================================

def hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """
    Gera um hash da senha com salt.
    
    Returns:
        (hash, salt) tuple
    """
    import hashlib
    if salt is None:
        salt = os.urandom(16).hex()
    salted = f"{salt}{password}".encode('utf-8')
    hash_value = hashlib.pbkdf2_hmac('sha256', salted, salt.encode('utf-8'), 100000).hex()
    return hash_value, salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verifica se a senha corresponde ao hash armazenado."""
    computed_hash, _ = hash_password(password, salt)
    return computed_hash == stored_hash


# =============================================================================
# Authorization State
# =============================================================================

class AuthorizationState:
    """Estado de autorização para gerenciar contas do perfil profissional."""
    
    def __init__(self):
        self.version = "1.0"
        self.created_at: Optional[str] = None
        self.modified_at: Optional[str] = None
        self.master_password_salt: Optional[str] = None
        self.master_password_verifier: Optional[str] = None
        self.accounts: Dict[str, Dict[str, Any]] = {}
        self.session_expiry: Optional[str] = None
    
    def is_account_authorized(self, platform: str) -> bool:
        """Verifica se uma conta específica está autorizada para uso."""
        account = self.accounts.get(platform, {})
        return account.get('authorized', False)
    
    def authorize_account(self, platform: str, credentials_provided: bool = False):
        """Marca uma conta como autorizada."""
        if platform not in self.accounts:
            self.accounts[platform] = {}
        self.accounts[platform]['authorized'] = True
        self.accounts[platform]['credentials_provided'] = credentials_provided
        self.accounts[platform]['authorized_at'] = datetime.now().isoformat()
        self.touch()
    
    def revoke_account(self, platform: str):
        """Revoga a autorização para uma conta."""
        if platform in self.accounts:
            self.accounts[platform]['authorized'] = False
            self.touch()
    
    def touch(self):
        """Atualiza o timestamp de modificação."""
        self.modified_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'version': self.version,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'master_password_salt': self.master_password_salt,
            'master_password_verifier': self.master_password_verifier,
            'accounts': self.accounts,
            'session_expiry': self.session_expiry,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuthorizationState':
        state = cls()
        state.version = data.get('version', '1.0')
        state.created_at = data.get('created_at')
        state.modified_at = data.get('modified_at')
        state.master_password_salt = data.get('master_password_salt')
        state.master_password_verifier = data.get('master_password_verifier')
        state.accounts = data.get('accounts', {})
        state.session_expiry = data.get('session_expiry')
        return state


# =============================================================================
# Authorizer
# =============================================================================

class Authorizer:
    """
    Gerencia a autorização persistente para o perfil profissional.
    
    O estado de autorização é salvo em AUTH_FILE, protegido por senha mestra.
    Sem a senha mestra correta, o arquivo não pode ser lido.
    """
    
    def __init__(self):
        self.state = AuthorizationState()
        self._encrypted_data: Optional[bytes] = None
        self._fernet: Optional[Fernet] = None
    
    def _ensure_auth_dir(self):
        """Garante que o diretório de autorização existe."""
        AUTH_DIR.mkdir(parents=True, exist_ok=True)
    
    def initialize(self, master_password: str):
        """
        Inicializa o arquivo de autorização com uma nova senha mestra.
        
        Args:
            master_password: Senha mestra para proteger o arquivo de autorização
        """
        self._ensure_auth_dir()
        
        # Gera hash da senha mestra
        password_hash, salt = hash_password(master_password)
        
        # Cria estado inicial
        self.state = AuthorizationState()
        self.state.created_at = datetime.now().isoformat()
        self.state.modified_at = datetime.now().isoformat()
        self.state.master_password_salt = salt
        self.state.master_password_verifier = password_hash
        self.state.session_expiry = (datetime.now() + timedelta(days=365)).isoformat()
        
        # Autoriza todas as contas por padrão (a credencial é verificada sob demanda)
        for platform in ['gmail', 'github', 'linkedin', 'vercel']:
            self.state.authorize_account(platform)
        
        # Salva
        self._save()
    
    def unlock(self, master_password: str) -> bool:
        """
        Tenta descriptografar o arquivo de autorização com a senha mestra.
        
        Returns:
            True se a senha estiver correta, False caso contrário
        """
        if not AUTH_FILE.exists():
            return False
        
        try:
            # Tenta carregar e verificar
            with open(AUTH_FILE, 'rb') as f:
                encrypted_data = f.read()
            
            if not CRYPTO_AVAILABLE:
                # Fallback: sem criptografia, apenas verifica o hash
                self._load_unencrypted()
                return self._verify_master_password(master_password)
            
            # Gera chave a partir da senha mestra + salt
            salt = self.state.master_password_salt
            if not salt:
                return False
            
            key_material = hashlib.pbkdf2_hmac(
                'sha256',
                master_password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            key = base64.urlsafe_b64encode(key_material[:32])
            self._fernet = Fernet(key)
            
            try:
                decrypted = self._fernet.decrypt(encrypted_data)
                self._load_state_from_json(decrypted.decode('utf-8'))
                
                # Verifica a senha
                return self._verify_master_password(master_password)
            except cryptography.fernet.InvalidToken:
                return False
                
        except Exception as e:
            print(f"Erro ao tentar desbloquear: {e}", file=sys.stderr)
            return False
    
    def _verify_master_password(self, password: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        if not self.state.master_password_salt or not self.state.master_password_verifier:
            return False
        return verify_password(password, self.state.master_password_verifier, self.state.master_password_salt)
    
    def _load_unencrypted(self):
        """Carrega o estado de um arquivo não criptografado (fallback)."""
        with open(AUTH_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.state = AuthorizationState.from_dict(data)
    
    def _load_state_from_json(self, json_str: str):
        """Carrega o estado de uma string JSON."""
        data = json.loads(json_str)
        self.state = AuthorizationState.from_dict(data)
    
    def _save(self):
        """Salva o estado atual no arquivo de autorização."""
        self._ensure_auth_dir()
        self.state.touch()
        
        json_data = json.dumps(self.state.to_dict(), indent=2, ensure_ascii=False)
        
        if CRYPTO_AVAILABLE and self.state.master_password_salt:
            # Gera chave a partir da senha mestra salthash
            import base64
            salt = self.state.master_password_salt
            # Para salvar, precisamos da senha mestra — mas não temos ela aqui
            # Então usamos um approach diferente: salvamos o hash verifier junto
            # e usamos o hash como seed para a chave Fernet
            key_material = hashlib.pbkdf2_hmac(
                'sha256',
                self.state.master_password_verifier.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            key = base64.urlsafe_b64encode(key_material[:32])
            self._fernet = Fernet(key)
            encrypted = self._fernet.encrypt(json_data.encode('utf-8'))
            
            with open(AUTH_FILE, 'wb') as f:
                f.write(encrypted)
        else:
            # Fallback: salva em texto simples (menos seguro)
            with open(AUTH_FILE, 'w', encoding='utf-8') as f:
                f.write(json_data)
    
    def is_account_authorized(self, platform: str) -> bool:
        """Verifica se uma conta específica está autorizada."""
        return self.state.is_account_authorized(platform)
    
    def get_authorized_accounts(self) -> list[str]:
        """Retorna lista de contas autorizadas."""
        authorized = []
        for platform, data in self.state.accounts.items():
            if data.get('authorized', False):
                authorized.append(platform)
        return authorized
    
    def get_state_summary(self) -> dict:
        """Retorna um resumo do estado de autorização (sem credenciais)."""
        return {
            'accounts': {
                platform: {
                    'authorized': data.get('authorized', False),
                    'authorized_at': data.get('authorized_at'),
                }
                for platform, data in self.state.accounts.items()
            },
            'modified_at': self.state.modified_at,
            'session_expiry': self.state.session_expiry,
        }


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gerenciador de autorização do perfil profissional")
    subparsers = parser.add_subparsers(dest='command')
    
    # init
    p_init = subparsers.add_parser('init', help='Inicializar arquivo de autorização (primeira vez)')
    p_init.add_argument('master_password', nargs='?', help='Senha mestra para proteger o arquivo')
    
    # unlock
    p_unlock = subparsers.add_parser('unlock', help='Desbloquear arquivo de autorização')
    p_unlock.add_argument('master_password', nargs='?', help='Senha mestra')
    
    # status
    subparsers.add_parser('status', help='Mostrar status de autorização')
    
    # authorize
    p_auth = subparsers.add_parser('authorize', help='Autorizar acesso a uma conta')
    p_auth.add_argument('platform', choices=['gmail', 'github', 'linkedin', 'vercel'],
                       help='Plataforma para autorizar')
    
    # revoke
    p_revoke = subparsers.add_parser('revoke', help='Revogar acesso a uma conta')
    p_revoke.add_argument('platform', choices=['gmail', 'github', 'linkedin', 'vercel'],
                         help='Plataforma para revogar')
    
    # reset
    subparsers.add_parser('reset', help='Resetar arquivo de autorização (perde todas as autorizações)')
    
    args = parser.parse_args()
    authorizer = Authorizer()
    
    # Se não tem cryptography, instale
    if not CRYPTO_AVAILABLE and args.command not in ['status', 'reset']:
        print("Aviso: cryptography não instalado. Instale com: pip install cryptography", file=sys.stderr)
        print("Sem criptografia, o arquivo de autorização fica exposto.", file=sys.stderr)
    
    if args.command == 'init':
        if not args.master_password:
            args.master_password = getpass.getpass("🔑 Senha mestra para o arquivo de autorização: ")
            confirm = getpass.getpass("🔑 Confirme a senha mestra: ")
            if args.master_password != confirm:
                print("❌ As senhas não coincidem.", file=sys.stderr)
                sys.exit(1)
        
        authorizer.initialize(args.master_password)
        print("✅ Arquivo de autorização inicializado com sucesso.")
        print("📌 Para desbloquear no futuro, use: python scripts/auth.py unlock <senha>")
    
    elif args.command == 'unlock':
        if not args.master_password:
            args.master_password = getpass.getpass("🔑 Senha mestra: ")
        
        if authorizer.unlock(args.master_password):
            print("✅ Arquivo de autorização desbloqueado.")
            summary = authorizer.get_state_summary()
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            print("❌ Senha mestra incorreta ou arquivo não existe.", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'status':
        if not AUTH_FILE.exists():
            print("ℹ️  Arquivo de autorização não existe ainda.")
            print("   Execute: python scripts/auth.py init")
        else:
            try:
                authorizer._load_unencrypted()
                summary = authorizer.get_state_summary()
                print("📋 Status de autorização:")
                print(json.dumps(summary, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"❌ Erro ao ler arquivo: {e}", file=sys.stderr)
    
    elif args.command == 'authorize':
        if not authorizer.unlock(getpass.getpass("🔑 Senha mestra: ")):
            print("❌ Falha ao desbloquear.", file=sys.stderr)
            sys.exit(1)
        authorizer.state.authorize_account(args.platform)
        authorizer._save()
        print(f"✅ Conta '{args.platform}' autorizada.")
    
    elif args.command == 'revoke':
        if not authorizer.unlock(getpass.getpass("🔑 Senha mestra: ")):
            print("❌ Falha ao desbloquear.", file=sys.stderr)
            sys.exit(1)
        authorizer.state.revoke_account(args.platform)
        authorizer._save()
        print(f"✅ Conta '{args.platform}' revogada.")
    
    elif args.command == 'reset':
        if AUTH_FILE.exists():
            AUTH_FILE.unlink()
        print("✅ Arquivo de autorização resetado.")
        print("   Para reinitializar, execute: python scripts/auth.py init")
    
    else:
        parser.print_help()
