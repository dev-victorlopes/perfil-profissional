# Perfil Profissional — Guia de Uso do Ambiente Seguro

## Visão Geral

Você agora tem um ambiente seguro para gerenciar seu perfil profissional.
As credenciais são armazenadas localmente no arquivo `.env`, que **não é commitado** no git.

## Primeiros Passos

```bash
cd /home/victor/Documentos/Hermes_Agent/PROJETOS/perfil-profissional
source .venv/bin/activate
```

## Comandos Disponíveis

### Ver status do ambiente
```bash
python scripts/manager.py status
```

### Ver status de autorização
```bash
python scripts/manager.py auth-status
```

### Gerenciar GitHub
```bash
python scripts/github_manager.py status    # Verificar autenticação
python scripts/github_manager.py repos     # Listar repositórios
python scripts/github_manager.py sync      # Ver projetos locais
```

### Gerenciar Google API
```bash
python scripts/google_manager.py status    # Ver status da API key
python scripts/google_manager.py youtube   # Status do YouTube
```

### LinkedIn (informações, sem login automatizado)
```bash
python scripts/linkedin_manager.py profile-info   # Mostrar informações do perfil
```

### Deploy Vercel
```bash
python scripts/deploy.py check     # Verificar prontidão
python scripts/deploy.py deploy    # Fazer deploy
```

## Segurança

- ✅ `.env` está no `.gitignore` — nunca será commitado
- ✅ `.venv/` está no `.gitignore` — ambiente isolado
- ✅ `check-secrets.py` verifica vazamentos antes de commit
- ✅ `auth.py` oferece autorização persistente com senha mestra (opcional)
- ⚠️ A senha do LinkedIn NÃO deve ser armazenada em arquivos
- ⚠️ Revogue e gere novos tokens se suspeitar de vazamento

## Arquivos Sensíveis que NÃO devem ser commitados

- `.env` — variáveis de ambiente com credenciais
- `.env.backup`, `.env.temp` — backups temporários
- `auth.session` — estado de autorização criptografado
- `.auth/` — diretório de autorização
- `.venv/` — ambiente Python (já ignorado)
- Qualquer arquivo com senhas, tokens, CPF ou chaves privadas

## Se precisar de ajuda

```bash
python scripts/manager.py --help
python scripts/github_manager.py --help
python scripts/deploy.py --help
```
