#!/usr/bin/env python3
"""
GitHub Profile Setup — Victor Lopes
Edita perfil e publica README de perfil.
"""

import os
import re
import base64
import sys
from pathlib import Path
from dotenv import load_dotenv

import requests

# Carregar configurações
load_dotenv(Path('.env'))
token = os.environ.get('GITHUB_TOKEN', '')
username = os.environ.get('GITHUB_USERNAME', 'dev-victorlopes')

headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
}

print('=' * 60)
print('📝 PUBLICANDO README DE PERFIL NO GITHUB')
print('=' * 60)
print()

# Ler o README preparado
readme_path = Path('github/profile-readme-updated.md')
if not readme_path.exists():
    print(f'❌ Arquivo não encontrado: {readme_path}')
    sys.exit(1)

readme_content = readme_path.read_text(encoding='utf-8')

# Extrair o conteúdo markdown entre as marcações ```markdown ... ```
# O arquivo tem formato: texto + ```markdown\n(conteúdo)\n```
match = re.search(r'```markdown\n(.*?)\n```', readme_content, re.DOTALL)
if match:
    md_content = match.group(1).strip()
    print(f'✅ Conteúdo markdown extraído: {len(md_content)} caracteres')
else:
    # Fallback: usar todo o conteúdo como markdown
    md_content = readme_content
    print(f'⚠️  Extração falhou, usando conteúdo completo: {len(md_content)} caracteres')

# O README de perfil usa um endpoint especial do GitHub
# https://docs.github.com/rest/repos/contents#create-or-update-file-contents
# Para perfil, o caminho é: /repos/{username}/{username}/contents/README.md

url = f'https://api.github.com/repos/{username}/{username}/contents/README.md'

data = {
    'message': 'Adicionar README de perfil - Victor Lopes',
    'content': base64.b64encode(md_content.encode('utf-8')).decode('utf-8'),
    'committer': {
        'name': 'Victor Lopes',
        'email': 'desenvolvedor.victorlopes@gmail.com'
    },
    'author': {
        'name': 'Victor Lopes',
        'email': 'desenvolvedor.victorlopes@gmail.com'
    }
}

print()
print(f'📤 Enviando para: {url}')
print()

resp = requests.put(url, headers=headers, json=data)

if resp.status_code == 201:
    print('✅ README DE PERFIL PUBLICADO COM SUCESSO!')
    print()
    print(f'📄 Perfil: https://github.com/{username}')
    print(f'📝 README: https://github.com/{username}/blob/main/README.md')
    print()
    print('=' * 60)
    print('✅ PERFIL GITHUB COMPLETO!')
    print('=' * 60)
elif resp.status_code == 404:
    print('⚠️  Repo de perfil não encontrado.')
    print()
    print('O README de perfil precisa ser configurado manualmente:')
    print(f'1. Acesse https://github.com/{username}')
    print('2. Clique em "Add README"')
    print('3. Cole o conteúdo de github/profile-readme-updated.md')
    print('4. Salve')
elif resp.status_code == 409:
    print('⚠️  README já existe. Atualizando...')
    # Tenta atualizar
    # Primeiro precisa pegar o SHA
    get_resp = requests.get(url, headers=headers)
    if get_resp.status_code == 200:
        existing = get_resp.json()
        data['sha'] = existing['sha']
        resp2 = requests.put(url, headers=headers, json=data)
        if resp2.status_code == 200:
            print('✅ README ATUALIZADO!')
        else:
            print(f'❌ Falha ao atualizar: {resp2.status_code}')
    else:
        print('❌ Não foi possível atualizar')
else:
    print(f'❌ Erro: {resp.status_code}')
    print(resp.text[:500])
