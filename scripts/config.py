#!/usr/bin/env python3
"""
Gerenciador de Configurações do Projeto — Perfil Profissional

Carrega configurações do projeto a partir de arquivos YAML.
NUNCA carrega credenciais — apenas metadados e configurações não-sensíveis.

Arquivos de configuração:
    config/environments.yaml   — ambientes disponíveis
    config/project-metadata.yaml — metadados do projeto

Uso:
    from scripts.config import load_config, get_project_meta

    config = load_config()
    meta = get_project_meta()
"""

import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Erro: pyyaml não instalado. Rode: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"


# =============================================================================
# Config loading
# =============================================================================

def load_yaml_file(path: Path) -> dict:
    """Carrega um arquivo YAML e retorna o conteúdo como dict."""
    if not path.exists():
        return {}
    
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def load_config() -> dict:
    """
    Carrega toda a configuração do projeto.
    
    Retorna um dict com:
        environments — configuração de ambientes
        project — metadados do projeto
    
    Credenciais NÃO são incluídas.
    """
    config = {
        'environments': load_yaml_file(CONFIG_DIR / 'environments.yaml'),
        'project': load_yaml_file(CONFIG_DIR / 'project-metadata.yaml'),
    }
    return config


def get_project_meta() -> dict:
    """Retorna apenas os metadados do projeto."""
    return load_config().get('project', {})


# =============================================================================
# Environment check
# =============================================================================

def get_active_environments() -> list[str]:
    """Retorna lista de nomes dos ambientes ativos."""
    envs = load_config().get('environments', {})
    active = []
    for name, cfg in envs.items():
        if isinstance(cfg, dict) and cfg.get('ativo', False):
            active.append(name)
    return active


# =============================================================================
# Safety check
# =============================================================================

def check_no_secrets_in_config() -> list[str]:
    """
    Verifica se arquivos de configuração contêm padrões de credenciais.
    Retorna lista de avisos se algo suspeito for encontrado.
    """
    import re
    
    warnings = []
    secret_pattern = re.compile(
        r'(password|senha|passwd|token|secret|segredo|api[_-]?key)\s*[:=]\s*["\']?[^\s"\']+',
        re.IGNORECASE,
    )
    
    for yaml_file in CONFIG_DIR.glob('*.yaml'):
        content = yaml_file.read_text(encoding='utf-8', errors='ignore')
        if secret_pattern.search(content):
            warnings.append(f"⚠️  {yaml_file.name}: possível padrão de credencial encontrado")
    
    return warnings


# =============================================================================
# CLI
# =============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Gerenciador de configurações do projeto.')
    subparsers = parser.add_subparsers(dest='command')
    
    # show
    p_show = subparsers.add_parser('show', help='Mostrar configuração atual')
    
    # envs
    p_envs = subparsers.add_parser('envs', help='Listar ambientes ativos')
    
    # check
    p_check = subparsers.add_parser('check', help='Verificar se config contém credenciais')
    
    args = parser.parse_args()
    
    if args.command == 'show':
        import json
        config = load_config()
        print(json.dumps(config, indent=2, ensure_ascii=False, default=str))
    
    elif args.command == 'envs':
        envs = get_active_environments()
        if envs:
            print('Ambientes ativos:')
            for e in envs:
                print(f'  • {e}')
        else:
            print('Nenhum ambiente ativo configurado.')
    
    elif args.command == 'check':
        warnings = check_no_secrets_in_config()
        if warnings:
            for w in warnings:
                print(w)
            sys.exit(1)
        else:
            print('✅ Arquivos de configuração estão limpos.')
            sys.exit(0)
    
    else:
        parser.print_help()
