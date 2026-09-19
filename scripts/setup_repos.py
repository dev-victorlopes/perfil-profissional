#!/usr/bin/env python3
"""
Setup completo dos repositórios do GitHub — Victor Lopes
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from dotenv import load_dotenv
import subprocess

# Load env
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'dev-victorlopes')

print('=' * 70)
print('🔗 SETUP COMPLETO DOS REPOSITORIOS — Victor Lopes')
print('=' * 70)

# Import functions - add scripts to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from github_projects_manager import (
    list_all_repos, create_file, get_file, update_repo_description,
    update_repo_topics, get_user_repos, api_request
)

# ============================================================================
# 1. Resolver push do perfil-profissional (já tem commit local)
# ============================================================================
print('\n1️⃣  PROCESSANDO perfil-profissional...')
proj_dir = Path(__file__).parent.parent
os.chdir(proj_dir)

# Configurar identidade
subprocess.run(['git', 'config', '--global', 'user.email', 
                'desenvolvedor.victorlopes@gmail.com'], 
               capture_output=True)
subprocess.run(['git', 'config', '--global', 'user.name', 'Victor Lopes'], 
               capture_output=True)

# Adicionar remote se não existir
result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                       capture_output=True, text=True)
if result.returncode != 0 or result.stdout.strip() == '':
    print('   Adicionando remote origin...')
    subprocess.run(['git', 'remote', 'add', 'origin', 
                   f'https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/perfil-profissional.git'],
                  capture_output=True)

# Configurar merge strategy
subprocess.run(['git', 'config', 'pull.rebase', 'false'], capture_output=True)

# Pull para merge com o README criado automaticamente
print('   Fazendo pull para mergear com README do GitHub...')
result = subprocess.run(['git', 'pull', 'origin', 'main', 
                        '--allow-unrelated-histories'], 
                       capture_output=True, text=True)
if result.returncode == 0:
    print('   ✅ Pull bem-sucedido!')
elif 'CONFLICT' in result.stderr or 'CONFLICT' in result.stdout:
    print('   ⚠️  Conflito detectado - resolvendo...')
    # Resolver conflito mantendo nosso README
    subprocess.run(['git', 'checkout', '--ours', 'README.md'], capture_output=True)
    subprocess.run(['git', 'add', 'README.md'], capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'Merge: usar README local'], capture_output=True)
    print('   ✅ Conflito resolvido')
else:
    print(f'   Resultado: {result.stderr[:200] if result.stderr else result.stdout[:200]}')

# Push
print('   Fazendo push...')
result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                       capture_output=True, text=True)
if result.returncode == 0:
    print('   ✅ Push realizado com sucesso!')
elif 'rejected' in result.stderr.lower():
    print(f'   ⚠️  Push rejeitado: {result.stderr[:200]}')
else:
    print(f'   Resultado: {result.stderr[:300] if result.stderr else "OK"}')

# ============================================================================
# 2. Sistema Gestão Empresarial
# ============================================================================
print('\n2️⃣  PROCESSANDO sistema-gestao-empresarial...')
sg_dir = Path('/home/victor/Documentos/Hermes_Agent/PROJETOS/sistema-gestao')
if sg_dir.exists():
    os.chdir(sg_dir)
    
    # Já é git? Verificar
    result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                           capture_output=True, text=True)
    if result.returncode == 0:
        print('   ✅ Já é repositório git')
        
        # Configurar identidade
        subprocess.run(['git', 'config', 'user.email', 
                       'desenvolvedor.victorlopes@gmail.com'], 
                      capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Victor Lopes'], 
                      capture_output=True)
        
        # Adicionar remote
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                               capture_output=True, text=True)
        remote_url = result.stdout.strip() if result.returncode == 0 else ''
        
        if not remote_url:
            print('   Adicionando remote origin...')
            subprocess.run(['git', 'remote', 'add', 'origin', 
                           f'https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/sistema-gestao-empresarial.git'],
                          capture_output=True)
            print('   ✅ Remote adicionado')
        elif GITHUB_USERNAME not in remote_url:
            print('   Atualizando remote para URL correta...')
            subprocess.run(['git', 'remote', 'set-url', 'origin', 
                           f'https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/sistema-gestao-empresarial.git'],
                          capture_output=True)
        
        # Push
        print('   Fazendo push...')
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print('   ✅ Push realizado!')
        else:
            print(f'   ⚠️  Erro: {result.stderr[:300]}')
    else:
        print('   ❌ Não é um repositório git válido')
else:
    print('   ⚠️  Diretório não encontrado:', sg_dir)

# ============================================================================
# 3. Atualizar READMEs dos outros repositórios via API
# ============================================================================
print('\n3️⃣  ATUALIZANDO READMEs via API...')

repos_to_setup = [
    ('painel-omega', 'Painel Ômega — Controle de Fluxo Financeiro',
     '''# Painel Ômega — Controle de Fluxo Financeiro

Painel web para controle financeiro com gestão de clientes, saídas, 
empréstimos e relatórios. Inclui PWA e deploy em Vercel.

## Funcionalidades

- 📊 Dashboard financeiro
- 👥 Gestão de clientes
- 💰 Controle de saídas e empréstimos
- 📈 Relatórios e gráficos
- 📱 PWA (Progressive Web App)
- 🔐 Autenticação de usuários

## Tecnologias

- **Backend**: Django
- **Banco de dados**: PostgreSQL (Supabase)
- **Frontend**: HTML/CSS/JS com PWA
- **Deploy**: Vercel

## Como Usar

1. Clone o repositório
2. Configure o banco de dados
3. Execute `python manage.py runserver`
4. Acesse http://localhost:8000

## Status

Em desenvolvimento — busca de estágio/dev júnior

## Autor

**Victor Lopes**
- GitHub: https://github.com/dev-victorlopes
- Email: desenvolvedor.victorlopes@gmail.com
'''),
    ('hermes-agency', 'Hermes Agency — Dashboard de Operação',
     '''# Hermes Agency — Dashboard de Operação

Dashboard para gestão de agência com operações, clientes e métricas.

## Funcionalidades

- 📊 Dashboard de operações
- 👥 Gestão de clientes
- 📈 Métricas e relatórios
- 🔔 Notificações em tempo real
- 📱 Acesso responsivo

## Tecnologias

- **Frontend**: HTML/CSS/JavaScript
- **Banco de dados**: Supabase (PostgreSQL)
- **Deploy**: Vercel

## Como Usar

1. Clone o repositório
2. Configure as variáveis de ambiente
3. Abra index.html no navegador ou faça deploy

## Status

Em desenvolvimento — busca de estágio/dev júnior

## Autor

**Victor Lopes**
- GitHub: https://github.com/dev-victorlopes
- Email: desenvolvedor.victorlopes@gmail.com
''')
]

for repo_name, description, readme_content in repos_to_setup:
    print(f'\n   Processando {repo_name}...')
    
    # Verificar se README existe
    try:
        existing = get_file(repo_name, 'README.md')
        if existing:
            print(f'   ✅ README existe, atualizando...')
            result = create_file(repo_name, 'README.md', readme_content,
                               f'Atualizar README - {repo_name}')
        else:
            print(f'   Criando README...')
            result = create_file(repo_name, 'README.md', readme_content,
                               f'Adicionar README - {repo_name}')
        
        if result:
            print(f'   ✅ README atualizado em https://github.com/{GITHUB_USERNAME}/{repo_name}')
    except Exception as e:
        print(f'   ⚠️  Erro: {e}')

# ============================================================================
# 4. Atualizar descrições e tópicos
# ============================================================================
print('\n4️⃣  ATUALIZANDO DESCRIÇÕES E TÓPICOS...')

topics_map = {
    'perfil-profissional': ['portifolio', 'html', 'css', 'javascript', 'vercel', 'profile'],
    'painel-omega': ['django', 'python', 'postgres', 'supabase', 'pwa', 'vercel', 'finance'],
    'sistema-gestao-empresarial': ['django', 'python', 'postgres', 'supabase', 'erp', 'enterprise'],
    'hermes-agency': ['html', 'css', 'javascript', 'supabase', 'vercel', 'dashboard'],
}

for repo_name, desc in [
    ('perfil-profissional', 'Portfólio profissional de Victor Lopes'),
    ('painel-omega', 'Painel Ômega — Controle de Fluxo Financeiro'),
    ('sistema-gestao-empresarial', 'Sistema de Gestão Empresarial'),
    ('hermes-agency', 'Hermes Agency — Dashboard de Operação'),
]:
    print(f'\n   {repo_name}...')
    
    # Atualizar descrição
    if update_repo_description(repo_name, desc):
        print(f'   ✅ Descrição atualizada')
    
    # Atualizar tópicos
    if repo_name in topics_map:
        if update_repo_topics(repo_name, topics_map[repo_name]):
            print(f'   ✅ Tópicos atualizados: {", ".join(topics_map[repo_name])}')

# ============================================================================
# 5. Verificação final
# ============================================================================
print('\n' + '=' * 70)
print('✅ VERIFICAÇÃO FINAL')
print('=' * 70)

repos = list_all_repos()
print(f'\nTotal de repositórios: {len(repos)}')

for repo in repos:
    name = repo['name']
    desc = repo.get('description', 'Sem descrição')
    topics = repo.get('topics', [])
    print(f'\n  📁 {name}')
    print(f'     📝 {desc}')
    if topics:
        print(f'     🏷️  {", ".join(topics)}')
    print(f'     🔗 {repo["html_url"]}')

print('\n' + '=' * 70)
print('✅ SETUP COMPLETO!')
print('=' * 70)
print()
print('Próximos passos:')
print('  1. Verificar README de perfil em https://github.com/dev-victorlopes')
print('  2. Atualizar perfil GitHub com README de perfil (pode ser necessário manualmente)')
print('  3. Desenvolver os projetos painel-omega e hermes-agency')
print('  4. Fazer deploy em Vercel quando pronto')
