# Configuração do GitHub — Guia Prático

## Problema Identificado

O token PAT configurado no arquivo `.env` está **inválido ou expirado**, retornando erro 401 (Bad credentials) na API do GitHub.

## Solução: Gerar Novo Token PAT

### Passo 1: Acesse a página de tokens

1. Vá para: https://github.com/settings/tokens
2. Ou: https://github.com/settings/tokens?type=beta (tokens novos)

### Passo 2: Gerar novo token

**Opção A: Token Classic (recomendado para este projeto)**

1. Clique em **"Generate new token"** → **"Generate new token (classic)"**
2. Descreva: `Perfil Profissional - Victor Lopes`
3. Selecione os escopos:
   - ✅ **repo** — Acesso total a repositórios (para criar/push)
   - ✅ **user** — Acesso a dados do usuário (para perfil)
   - ✅ **workflow** — Se for usar Actions no futuro
4. Clique em **"Generate token"**
5. **COPIE O TOKEN IMEDIATAMENTE** (não será mostrado novamente!)

**Opção B: Fine-grained token (mais seguro, mas menos compatível)**

1. Clique em **"Generate new token"**
2. Configure:
   - Repository access: **Only select repositories**
   - Selecione os repositórios que criará
   - Permissions:
     - ✅ Repository permissions: Read and write (for contents)
     - ✅ User permissions: Read-only (for profile)
3. Clique em **"Generate token"**

### Passo 3: Atualizar o arquivo .env

Edite o arquivo `.env` na raiz do projeto:

```bash
cd /home/victor/Documentos/Hermes_Agent/PROJETOS/perfil-profissional
nano .env
```

Atualize a linha:
```env
GITHUB_TOKEN=seu_novo_token_aqui
```

### Passo 4: Testar o token

```bash
cd /home/victor/Documentos/Hermes_Agent/PROJETOS/perfil-profissional
source .venv/bin/activate
python scripts/github_setup.py --validate
```

Se retornar "✅ Token válido!", está pronto!

## Próximos Passos Após Token Válido

### 1. Criar repositórios

```bash
python scripts/github_setup.py --create-repos
```

Isso criará:
- `perfil-profissional` — Portfólio
- `painel-omega` — Painel Ômega
- `sistema-gestao-empresarial` — Sistema Gestão
- `hermes-agency` — Dashboard Hermes

### 2. Preparar README de perfil

```bash
python scripts/github_setup.py --update-readme
```

Isso criará `github/profile-readme-updated.md` com o username correto.

### 3. Fazer push dos projetos

Para cada projeto local, faça:

```bash
cd /caminho/para/o/projeto
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/dev-victorlopes/nome-do-repo.git
git branch -M main
git push -u origin main
```

### 4. Configurar README de perfil

1. Acesse https://github.com/dev-victorlopes
2. Crie um arquivo `README.md` na raiz
3. Copie o conteúdo de `github/profile-readme-updated.md`
4. Salve

## Verificação Final

```bash
# Testar autenticação
python scripts/github_setup.py --validate

# Listar repositórios
python scripts/github_setup.py --check-repos

# Verificar status geral
python scripts/github_manager.py status
```

## Troubleshooting

### Token ainda falha após atualização?

1. Verifique se copiou o token completo (sem espaços)
2. Verifique se o arquivo .env não tem caracteres extras
3. Tente fazer login no GitHub com o navegador para confirmar a conta
4. Gere um novo token (às vezes o primeiro tem problema)

### Erro 403 Forbidden?

O token pode não ter permissão suficiente. Verifique os escopos:
- Para criar repositórios: precisa do escopo **repo**
- Para ler perfil: precisa do escopo **user**

### Erro de rate limit?

A API do GitHub tem limites de requisições. Aguarde alguns minutos e tente novamente.

## Links Úteis

- [Criar token PAT](https://github.com/settings/tokens)
- [Documentação API GitHub](https://docs.github.com/rest)
- [Escopos de token](https://docs.github.com/developers/apps/scopes-for-oauth-apps)
