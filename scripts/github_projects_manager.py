#!/usr/bin/env python3
"""
GitHub Projects Manager — Victor Lopes
Integração completa para gerenciar projetos e repositórios do GitHub.
"""

import os
import sys
import shutil
import subprocess
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import requests
import base64

# Carregar configurações
load_dotenv(Path('.venv') / '..' / '.env')
load_dotenv()
env_path = Path.cwd() / '.env'
if env_path.exists():
    load_dotenv(env_path)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'dev-victorlopes')

HEADERS = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
}

API_BASE = 'https://api.github.com'

print('=' * 70)
print('🔗 GITHUB PROJECTS MANAGER — Victor Lopes')
print('=' * 70)
print()

# ============================================================================
# FUNÇÕES DE API
# ============================================================================

def api_request(method, endpoint, data=None, params=None):
    """Faz requisição para a API do GitHub."""
    url = f'{API_BASE}{endpoint}'
    headers = HEADERS.copy()
    
    if method == 'GET':
        resp = requests.get(url, headers=headers, params=params)
    elif method == 'POST':
        resp = requests.post(url, headers=headers, json=data)
    elif method == 'PATCH':
        resp = requests.patch(url, headers=headers, json=data)
    elif method == 'PUT':
        resp = requests.put(url, headers=headers, json=data)
    elif method == 'DELETE':
        resp = requests.delete(url, headers=headers)
    else:
        raise ValueError(f'Método não suportado: {method}')
    
    return resp


def get_user():
    """Obtém dados do usuário autenticado."""
    resp = api_request('GET', '/user')
    if resp.status_code == 200:
        return resp.json()
    return None


def get_user_repos(visibility='all', sort='updated', per_page=100):
    """Lista repositórios do usuário."""
    resp = api_request('GET', f'/users/{GITHUB_USERNAME}/repos', 
                       params={'visibility': visibility, 'sort': sort, 
                               'per_page': per_page, 'type': 'all'})
    if resp.status_code == 200:
        return resp.json()
    return []


def create_repo(name, description='', private=False, auto_init=True, 
                license_template='mit', gitignore_template=None):
    """Cria um novo repositório."""
    data = {
        'name': name,
        'description': description,
        'private': private,
        'auto_init': auto_init,
    }
    if license_template:
        data['license_template'] = license_template
    if gitignore_template:
        data['gitignore_template'] = gitignore_template
    
    resp = api_request('POST', '/user/repos', data=data)
    if resp.status_code in [201, 422]:  # 422 se já existir
        return resp.json() if resp.status_code == 201 else {'exists': True}
    return None


def update_repo(repo_name, description=None, homepage=None, default_branch=None,
                topics=None, visibility=None):
    """Atualiza um repositório existente."""
    endpoint = f'/repos/{GITHUB_USERNAME}/{repo_name}'
    data = {}
    
    if description is not None:
        data['description'] = description
    if homepage is not None:
        data['homepage'] = homepage
    if default_branch is not None:
        data['default_branch'] = default_branch
    if topics is not None:
        data['topics'] = topics
    if visibility is not None:
        data['visibility'] = visibility
    
    resp = api_request('PATCH', endpoint, data=data)
    return resp.status_code == 200


def delete_repo(repo_name):
    """Exclui um repositório."""
    endpoint = f'/repos/{GITHUB_USERNAME}/{repo_name}'
    resp = api_request('DELETE', endpoint)
    return resp.status_code == 204


def update_repo_description(repo_name, description):
    """Atualiza apenas a descrição de um repositório."""
    return update_repo(repo_name, description=description)


def update_repo_topics(repo_name, topics):
    """Atualiza os tópicos (tags) de um repositório."""
    return update_repo(repo_name, topics=topics)


def create_file(repo_name, path, content, message, branch='main'):
    """Cria ou atualiza um arquivo no repositório."""
    endpoint = f'/repos/{GITHUB_USERNAME}/{repo_name}/contents/{path}'
    data = {
        'message': message,
        'content': base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        'branch': branch
    }
    resp = api_request('PUT', endpoint, data=data)
    return resp.status_code in [200, 201]


def get_file(repo_name, path, branch='main'):
    """Obtém o conteúdo de um arquivo."""
    endpoint = f'/repos/{GITHUB_USERNAME}/{repo_name}/contents/{path}'
    resp = api_request('GET', endpoint, params={'ref': branch})
    if resp.status_code == 200:
        data = resp.json()
        return base64.b64decode(data['content']).decode('utf-8')
    return None


def delete_file(repo_name, path, message, sha, branch='main'):
    """Exclui um arquivo do repositório."""
    endpoint = f'/repos/{GITHUB_USERNAME}/{repo_name}/contents/{path}'
    data = {
        'message': message,
        'sha': sha,
        'branch': branch
    }
    resp = api_request('DELETE', endpoint, data=data)
    return resp.status_code == 200


def get_repo_contents(repo_name, path='', branch='main'):
    """Lista o conteúdo de um diretório no repositório."""
    endpoint = f'/repos/{GITHUB_USERNAME}/{repo_name}/contents/{path}'
    resp = api_request('GET', endpoint, params={'ref': branch})
    if resp.status_code == 200:
        return resp.json()
    return []


def create_issue(repo_name, title, body='', labels=None, assignee=None):
    """Cria um issue no repositório."""
    endpoint = f'/repos/{GITHUB_USERNAME}/{repo_name}/issues'
    data = {'title': title, 'body': body}
    if labels:
        data['labels'] = labels
    if assignee:
        data['assignee'] = assignee
    
    resp = api_request('POST', endpoint, data=data)
    return resp.status_code == 201


def update_issue(repo_name, issue_number, title=None, body=None, state=None,
                 labels=None, assignee=None):
    """Atualiza um issue."""
    endpoint = f'/repos/{GITHUB_USERNAME}/{repo_name}/issues/{issue_number}'
    data = {}
    if title is not None:
        data['title'] = title
    if body is not None:
        data['body'] = body
    if state is not None:
        data['state'] = state
    if labels is not None:
        data['labels'] = labels
    if assignee is not None:
        data['assignee'] = assignee
    
    resp = api_request('PATCH', endpoint, data=data)
    return resp.status_code == 200


def get_repo_issues(repo_name, state='open'):
    """Lista issues de um repositório."""
    endpoint = f'/repos/{GITHUB_USERNAME}/{repo_name}/issues'
    resp = api_request('GET', endpoint, params={'state': state})
    if resp.status_code == 200:
        return resp.json()
    return []


def list_all_repos():
    """Lista todos os repositórios públicos do usuário."""
    repos = get_user_repos(visibility='all', sort='updated')
    print('\n📦 SEUS REPOSITORIOS:')
    print('=' * 70)
    
    if not repos:
        print('  Nenhum repositório encontrado.')
        return repos
    
    for i, repo in enumerate(repos, 1):
        name = repo['name']
        desc = repo.get('description', 'Sem descrição')
        lang = repo.get('language', 'N/A')
        stargazers = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        url = repo['html_url']
        private = repo.get('private', False)
        
        vis = '🔒' if private else '🌐'
        print(f'\n  {i}. {vis} {name}')
        print(f'     📍 {url}')
        print(f'     📝 {desc}')
        print(f'     🛠 Linguagem: {lang}')
        print(f'     ⭐ {stargazers}  🍴 {forks}')
    
    return repos

def search_repo(name):
    """Busca um repositório pelo nome."""
    repos = get_user_repos()
    for repo in repos:
        if name.lower() in repo['name'].lower():
            return repo
    return None

# ============================================================================
# FUNÇÕES DE GIT LOCAIS
# ============================================================================

def git_init(repo_path):
    """Inicializa um repositório git local."""
    path = Path(repo_path)
    if not path.exists():
        print(f'❌ Diretório não existe: {repo_path}')
        return False
    
    # Verificar se já é um repo git
    if (path / '.git').exists():
        print(f'✅ Já é um repositório git: {repo_path}')
        return True
    
    try:
        subprocess.run(['git', 'init'], cwd=path, check=True, capture_output=True)
        print(f'✅ Repositório git inicializado em: {repo_path}')
        return True
    except subprocess.CalledProcessError as e:
        print(f'❌ Erro ao inicializar git: {e.stderr.decode() if e.stderr else str(e)}')
        return False


def git_add_commit(repo_path, message='Initial commit'):
    """Adiciona todos os arquivos e faz commit."""
    path = Path(repo_path)
    if not (path / '.git').exists():
        print(f'❌ Não é um repositório git: {repo_path}')
        return False
    
    try:
        # Adicionar todos
        subprocess.run(['git', 'add', '.'], cwd=path, check=True, capture_output=True)
        # Commit
        subprocess.run(['git', 'commit', '-m', message], cwd=path, check=True, capture_output=True)
        print(f'✅ Commit realizado: {message}')
        return True
    except subprocess.CalledProcessError as e:
        print(f'❌ Erro no commit: {e.stderr.decode() if e.stderr else str(e)}')
        return False


def git_remote_add(repo_path, remote_url):
    """Adiciona um remote ao repositório."""
    path = Path(repo_path)
    if not (path / '.git').exists():
        print(f'❌ Não é um repositório git: {repo_path}')
        return False
    
    # Verificar se remote já existe
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                               cwd=path, capture_output=True)
        if result.returncode == 0:
            print(f'✅ Remote "origin" já configurado para: {result.stdout.decode().strip()}')
            return True
    except:
        pass
    
    try:
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url], 
                      cwd=path, check=True, capture_output=True)
        print(f'✅ Remote "origin" adicionado: {remote_url}')
        return True
    except subprocess.CalledProcessError as e:
        print(f'❌ Erro ao adicionar remote: {e.stderr.decode() if e.stderr else str(e)}')
        return False


def git_push(repo_path, branch='main'):
    """Faz push para o remote."""
    path = Path(repo_path)
    if not (path / '.git').exists():
        print(f'❌ Não é um repositório git: {repo_path}')
        return False
    
    try:
        # Garantir que estamos na branch main
        subprocess.run(['git', 'branch', '-M', branch], cwd=path, check=True, capture_output=True)
        # Push
        result = subprocess.run(['git', 'push', '-u', 'origin', branch], 
                               cwd=path, capture_output=True, text=True)
        if result.returncode == 0:
            print(f'✅ Push realizado para origin/{branch}')
            return True
        else:
            print(f'⚠️  Erro no push: {result.stderr}')
            return False
    except subprocess.CalledProcessError as e:
        print(f'❌ Erro no push: {e.stderr.decode() if e.stderr else str(e)}')
        return False


def clone_repo(repo_name):
    """Clona um repositório localmente."""
    url = f'https://github.com/{GITHUB_USERNAME}/{repo_name}.git'
    path = Path.cwd() / repo_name
    
    if path.exists():
        print(f'⚠️  Diretório já existe: {path}')
        return False
    
    try:
        subprocess.run(['git', 'clone', url, str(path)], check=True, capture_output=True)
        print(f'✅ Repositório clonado em: {path}')
        return True
    except subprocess.CalledProcessError as e:
        print(f'❌ Erro ao clonar: {e.stderr.decode() if e.stderr else str(e)}')
        return False


# ============================================================================
# GESTÃO DE PROJETOS
# ============================================================================

def publish_project(project_path, repo_name=None, description='', topics=None):
    """Publica um projeto local no GitHub."""
    from pathlib import Path
    
    print('\n' + '=' * 70)
    print('📦 PUBLICANDO PROJETO NO GITHUB')
    print('=' * 70)
    
    path = Path(project_path)
    if not path.exists():
        print(f'❌ Projeto não encontrado: {project_path}')
        return False
    
    # Determinar nome do repositório
    if repo_name is None:
        repo_name = path.name
    
    # Verificar se já existe remoto
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                               cwd=path, capture_output=True)
        if result.returncode == 0:
            remote_url = result.stdout.decode().strip()
            print(f'✅ Projeto já tem remote: {remote_url}')
            print('   Para atualizar, faça: git push')
            return True
    except:
        pass
    
    # Criar repositório no GitHub se não existir
    existing = search_repo(repo_name)
    if not existing:
        print(f'\n📝 Criando repositório "{repo_name}" no GitHub...')
        result = create_repo(repo_name, description=description, 
                            private=False, auto_init=True)
        if result and 'exists' not in result:
            print(f'✅ Repositório criado: https://github.com/{GITHUB_USERNAME}/{repo_name}')
        elif result and result.get('exists'):
            print(f'⚠️  Repositório já existe')
        else:
            print(f'❌ Falha ao criar repositório')
            return False
    else:
        print(f'\n📝 Repositório "{repo_name}" já existe no GitHub')
    
    # Inicializar git local se necessário
    git_init(project_path)
    
    # Adicionar e commitar
    git_add_commit(project_path, f'Initial commit - {repo_name}')
    
    # Adicionar remote
    remote_url = f'https://github.com/{GITHUB_USERNAME}/{repo_name}.git'
    git_remote_add(project_path, remote_url)
    
    # Push
    print('\n📤 Fazendo push para o GitHub...')
    if git_push(project_path, 'main'):
        print(f'\n✅ PROJETO PUBLICADO: https://github.com/{GITHUB_USERNAME}/{repo_name}')
        return True
    else:
        print('\n⚠️  Falha no push - verifique as credenciais do git')
        return False


def setup_project_readme(project_path, title, description):
    """Configura ou atualiza o README.md de um projeto."""
    from pathlib import Path
    
    readme_path = Path(project_path) / 'README.md'
    
    # Verificar se já tem README
    if readme_path.exists():
        print(f'✅ README.md já existe em: {project_path}')
        return True
    
    # Criar README padrão
    readme_content = f'''# {title}

{description}

## Tecnologias

- [Tecnologia 1]
- [Tecnologia 2]

## Como Usar

```bash
# Clonar o repositório
git clone https://github.com/{GITHUB_USERNAME}/{Path(project_path).name}.git

# Entrar na pasta
cd {Path(project_path).name}

# Instalar dependências (se aplicável)
pip install -r requirements.txt

# Executar
python main.py
```

## Autor

**Victor Lopes**
- GitHub: https://github.com/{GITHUB_USERNAME}
- LinkedIn: https://linkedin.com/in/dev-victorlopes
- Email: desenvolvedor.victorlopes@gmail.com

## Licença

Este projeto está sob licença MIT.
'''
    
    readme_path.write_text(readme_content, encoding='utf-8')
    print(f'✅ README.md criado em: {readme_path}')
    return True


# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def show_menu():
    """Mostra o menu de opções."""
    print('\n' + '=' * 70)
    print('🔗 GITHUB PROJECTS MANAGER — Victor Lopes')
    print('=' * 70)
    print()
    print('1. 📋 Listar todos os repositórios')
    print('2. 🔍 Buscar repositório')
    print('3. ➕ Criar novo repositório')
    print('4. 📝 Atualizar descrição de repositório')
    print('5. 🏷️  Atualizar tópicos (tags)')
    print('6. 🗑️  Excluir repositório')
    print('7. 📤 Publicar projeto local no GitHub')
    print('8. 📋 Ver conteúdo de repositório')
    print('9. 📄 Criar/atualizar arquivo no repositório')
    print('10. 🗑️  Excluir arquivo do repositório')
    print('11. 🎫 Criar issue')
    print('12. 📋 Listar issues')
    print('13. 📊 Ver estatísticas do perfil')
    print('0. 🚪 Sair')
    print()


def main():
    """Loop principal do menu."""
    while True:
        show_menu()
        choice = input('Escolha uma opção: ').strip()
        
        if choice == '0':
            print('👋 Até logo!')
            break
        
        elif choice == '1':
            list_all_repos()
        
        elif choice == '2':
            name = input('Nome do repositório: ').strip()
            repo = search_repo(name)
            if repo:
                print(f'\n✅ Repositório encontrado:')
                print(f'  Nome: {repo["name"]}')
                print(f'  URL: {repo["html_url"]}')
                print(f'  Descrição: {repo.get("description", "N/A")}')
                print(f'  Linguagem: {repo.get("language", "N/A")}')
                print(f'  Privado: {repo.get("private", False)}')
            else:
                print(f'\n❌ Repositório "{name}" não encontrado')
        
        elif choice == '3':
            name = input('Nome do repositório: ').strip()
            desc = input('Descrição (opcional): ').strip()
            private = input('Privado? (s/n, padrão: n): ').strip().lower() == 's'
            
            result = create_repo(name, desc, private, auto_init=True)
            if result and 'exists' not in result:
                print(f'\n✅ Repositório criado: https://github.com/{GITHUB_USERNAME}/{name}')
            elif result and result.get('exists'):
                print(f'\n⚠️  Repositório "{name}" já existe')
            else:
                print('\n❌ Falha ao criar repositório')
        
        elif choice == '4':
            name = input('Nome do repositório: ').strip()
            new_desc = input('Nova descrição: ').strip()
            
            if update_repo_description(name, new_desc):
                print(f'\n✅ Descrição atualizada para "{name}"')
            else:
                print('\n❌ Falha ao atualizar descrição')
        
        elif choice == '5':
            name = input('Nome do repositório: ').strip()
            topics_str = input('Tópicos (separados por vírgula): ').strip()
            topics = [t.strip() for t in topics_str.split(',') if t.strip()]
            
            if topics:
                if update_repo_topics(name, topics):
                    print(f'\n✅ Tópicos atualizados para "{name}"')
                else:
                    print('\n❌ Falha ao atualizar tópicos')
            else:
                print('\n❌ Nenhum tópico fornecido')
        
        elif choice == '6':
            name = input('Nome do repositório para excluir: ').strip()
            confirm = input(f'Tem certeza que deseja excluir "{name}"? (s/n): ').strip().lower()
            
            if confirm == 's':
                if delete_repo(name):
                    print(f'\n✅ Repositório "{name}" excluído')
                else:
                    print('\n❌ Falha ao excluir repositório')
            else:
                print('\n❌ Operação cancelada')
        
        elif choice == '7':
            project_path = input('Caminho do projeto local: ').strip()
            repo_name = input('Nome do repositório (deixe vazio para usar nome da pasta): ').strip()
            description = input('Descrição: ').strip()
            
            repo_name = repo_name if repo_name else Path(project_path).name
            
            if publish_project(project_path, repo_name, description):
                print('\n✅ Projeto publicado com sucesso!')
            else:
                print('\n❌ Falha ao publicar projeto')
        
        elif choice == '8':
            name = input('Nome do repositório: ').strip()
            path = input('Caminho dentro do repo (deixe vazio para raiz): ').strip()
            
            contents = get_repo_contents(name, path if path else '')
            if contents:
                print(f'\n📁 Conteúdo de {name}/{path or "/"}:')
                for item in contents:
                    if isinstance(item, dict):
                        if item.get('type') == 'file':
                            print(f'  📄 {item.get("name")}')
                        elif item.get('type') == 'dir':
                            print(f'  📁 {item.get("name")}/')
            else:
                print('\n❌ Falha ao obter conteúdo')
        
        elif choice == '9':
            name = input('Nome do repositório: ').strip()
            file_path = input('Caminho do arquivo (ex: README.md): ').strip()
            content = input('Conteúdo do arquivo: ').strip()
            message = input('Mensagem do commit: ').strip()
            
            if create_file(name, file_path, content, message):
                print(f'\n✅ Arquivo criado/atualizado em {name}/{file_path}')
            else:
                print('\n❌ Falha ao criar arquivo')
        
        elif choice == '10':
            name = input('Nome do repositório: ').strip()
            file_path = input('Caminho do arquivo: ').strip()
            
            try:
                file_info = get_file(name, file_path)
                if file_info:
                    print(f'\nArquivo encontrado: {file_path}')
                    # Para deletar precisamos do SHA
                    # Isso requer uma requisição adicional
                    print('⚠️  Função de delete requer implementação adicional de SHA')
            except:
                print(f'\n❌ Arquivo não encontrado: {file_path}')
        
        elif choice == '11':
            name = input('Nome do repositório: ').strip()
            title = input('Título do issue: ').strip()
            body = input('Descrição (opcional): ').strip()
            
            if create_issue(name, title, body):
                print(f'\n✅ Issue criado em {name}')
            else:
                print('\n❌ Falha ao criar issue')
        
        elif choice == '12':
            name = input('Nome do repositório: ').strip()
            state = input('Estado (open/closed/all, padrão: open): ').strip() or 'open'
            
            issues = get_repo_issues(name, state)
            if issues:
                print(f'\n📋 Issues de {name} ({len(issues)} encontrados):')
                for issue in issues:
                    print(f'\n  #{issue["number"]} - {issue["title"]}')
                    print(f'    Estado: {issue["state"]}')
                    if issue.get('labels'):
                        print(f'    Labels: {", ".join(l["name"] for l in issue["labels"])}')
            else:
                print('\n❌ Falha ao obter issues')
        
        elif choice == '13':
            user = get_user()
            if user:
                print(f'\n📊 ESTATÍSTICAS DO PERFIL')
                print('=' * 70)
                print(f'  👤 Login: {user.get("login")}')
                print(f'  👤 Nome: {user.get("name", "N/A")}')
                print(f'  📝 Bio: {user.get("bio", "N/A")}')
                print(f'  📍 Local: {user.get("location", "N/A")}')
                print(f'  🌐 Site: {user.get("blog", "N/A")}')
                print(f'  📧 Email: {user.get("email", "N/A")}')
                print(f'  ⭐ Seguidores: {user.get("followers", 0)}')
                print(f'  ➕ Seguindo: {user.get("following", 0)}')
                print(f'  📦 Repositórios públicos: {user.get("public_repos", 0)}')
                print(f'  🌟 Estrelas: {user.get("public_gists", 0)}')
            else:
                print('\n❌ Falha ao obter dados do perfil')
        
        else:
            print('\n❌ Opção inválida. Tente novamente.')


if __name__ == '__main__':
    main()
