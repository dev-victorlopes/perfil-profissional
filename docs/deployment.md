# Deployment Guide — Perfil Profissional

## Portfólio Web (Vercel)

### Pré-requisitos
- Conta Vercel
- Projeto Git (opcional para deploy direto)

### Deploy Estático (HTML/CSS/JS)

```bash
# Instalar Vercel CLI (se necessário)
npm install -g vercel

# Navegar até o diretório do portfólio
cd portfolio/

# Login na Vercel
vercel login

# Deploy
vercel
```

### Variáveis de Ambiente (Painel Admin)

Se o portfólio incluir painel administrativo com autenticação:

```
# Supabase (se usado)
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...  # SOMENTE servidor-side, nunca no frontend

# Segredo de sessão
SESSION_SECRET=...
```

### Configuração do Domínio (Opcional)

1. Comprar domínio (ex: namecheap, godaddy)
2. No Vercel: Project Settings → Domains
3. Adicionar domínio personalizado
4. Configurar DNS conforme instruções do Vercel

---

## Segurança no Deploy

### Nunca commitar:
- `.env` com valores reais
- Chaves de API
- Tokens
- CPF
- Senhas

### Verificações antes do deploy:
```bash
# Verificar se há secrets no código
grep -r "password\|token\|api_key\|cpf\|secret" --exclude-dir=.git --exclude-dir=node_modules .

# Verificar .gitignore
cat .gitignore

# Verificar histórico do git
git log --all --full-history --oneline
```

---

## Atualização do Portfólio

O painel administrativo deve permitir:
1. Login com credenciais seguras
2. Edição de conteúdo (sobre, projeos, formação)
3. Atualização do currículo
4. Salvamento das alterações

Após edição, o conteúdo é atualizado diretamente no site (não requer novo deploy se usar approach client-side ou API).
