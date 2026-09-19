#!/usr/bin/env python3
"""
Credencial e Segurança Check — Perfil Profissional

Verifica se há vazamentos acidentais de credenciais no projeto antes de
qualquer commit, push ou deploy.
"""

import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SECRET_PATTERNS = [
    (r'AIza[0-9A-Za-z\-_]{35}', 'Google API key'),
    (r'AQ\.[A-Za-z0-9\-_]{20,}', 'Google OAuth token'),
    (r'github_pat_[a-zA-Z0-9_]{30,}', 'GitHub PAT'),
    (r'ghp_[a-zA-Z0-9]{30,}', 'GitHub PAT (old format)'),
    (r'gho_[a-zA-Z0-9]{30,}', 'GitHub OAuth token'),
    (r'ghu_[a-zA-Z0-9]{30,}', 'GitHub user token'),
    (r'ghs_[a-zA-Z0-9]{30,}', 'GitHub server token'),
    (r'ghr_[a-zA-Z0-9]{30,}', 'GitHub refresh token'),
    (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\'][a-zA-Z0-9_-]{20,}["\']', 'API key literal'),
    (r'(?i)(token|bearer)\s*[=:]\s*["\'][a-zA-Z0-9\-_\.]{20,}["\']', 'Token literal'),
    (r'(?i)(password|senha|passwd)\s*[=:]\s*["\'][^"\']{4,}["\']', 'Password literal'),
    (r'(?i)(secret|segredo)\s*[=:]\s*["\'][^"\']{8,}["\']', 'Secret literal'),
    (r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b', 'CPF pattern'),
]

EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env'}


def scan_file(path: Path) -> list[dict]:
    try:
        content = path.read_text(encoding='utf-8', errors='ignore')
    except (IOError, UnicodeDecodeError):
        return []
    
    findings = []
    for i, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith(('#', '//', '/*')):
            continue
        for pattern, desc in SECRET_PATTERNS:
            if match := re.search(pattern, line, re.IGNORECASE):
                findings.append({
                    'file': str(path.relative_to(PROJECT_ROOT)),
                    'line': i,
                    'description': desc,
                    'content': line.strip()[:120],
                })
    return findings


def main():
    findings = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in files:
            path = Path(root) / name
            if path.suffix in {'.pyc', '.pyo', '.pyd'}:
                continue
            if 'node_modules' in str(path) or '.venv' in str(path):
                continue
            findings.extend(scan_file(path))
    
    if not findings:
        print('✅ Limpo — nenhum padrão de credencial encontrado.')
        return 0
    
    print(f'⚠️  Encontrados {len(findings)} possível(is) vazamento(s):')
    print()
    for f in findings:
        print(f"  📄 {f['file']}:{f['line']}")
        print(f"     Tipo: {f['description']}")
        print(f"     Linha: {f['content']}")
        print()
    print('⚠️  Revise os arquivos acima antes de commitar ou fazer deploy.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
