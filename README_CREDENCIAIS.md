# Credenciais e Acesso — Perfil Profissional Digital

**Última atualização**: 2026-09-19  
**Projeto**: Perfil Profissional Digital — Victor Lopes

---

## ⚠️ AVISO DE SEGURANÇA

Este documento contém **apenas informações públicas** (URLs, usernames, endereços de e-mail).

**NUNCA** incluir aqui:
- Senhas
- CPF
- Tokens de API
- Chaves privadas
- Qualquer dado sensível

As senhas devem ser armazenadas apenas no 관리자 do usuário (gerenciador de senhas) ou no `.env` local.

---

## 1. PORTFOILO WEB

| Campo | Valor |
|-------|-------|
| **Status** | Em desenvolvimento local |
| **URL (local)** | `file:///.../perfil-profissional/index.html` |
| **URL (Vercel)** | *Pendente de deploy* |
| **Stack** | HTML + CSS + JavaScript |
| **Painel Admin** | `/admin/index.html` |
| **Login Admin** | admin@victorlopes.local / admin2026 |

### Deploy Vercel (pendente)

```bash
# No diretório do projeto:
cd /home/victor/Documentos/Hermes_Agent/PROJETOS/perfil-profissional

# Login na Vercel
vercel login

# Deploy
vercel --prod
```

Após Deploy:
- URL será algo como: `https://perfil-profissional-git-main.victorlopes.vercel.app`
- Configurar domínio personalizado (opcional): `victorlopes.dev` ou similar

---

## 2. E-MAIL PROFISSIONAL

| Campo | Valor |
|-------|-------|
| **Status** | **PENDENTE** — Criar conta |
| **Opção principal sugerida** | `vic.lopes@gmail.com` |
| **Alternativas** | victor.lopes@..., victorhls@... |
| **Domínio** | gmail.com (ou outlook.com/proton.me) |

### Ação necessária (humana)

1. Acessar gmail.com
2. Clicar em "Criar conta"
3. Preencher: Primeiro nome: Victor, Sobrenome: Lopes
4. Escolher endereço disponível
5. Criar senha forte (armazenar em gerenciador de senhas)
6. Verificar CAPTCHA/telefone (intervenção humana necessária)

---

## 3. LINKEDIN

| Campo | Valor |
|-------|-------|
| **Status** | **PENDENTE** — Criar/Configurar perfil |
| **URL alvo** | `https://linkedin.com/in/victorlopes` |
| **Username** | victorlopes (verificar disponibilidade) |

### Conteúdo preparado

- **Headline**: `Python | Desenvolvimento Web | Backend | Estudante ADS`
- **Sobre**: Ver `linkedin/content.md`
- **Formação**: ADS (Estácio) + Python (Senac)
- **Habilidades**: Python, Django, Desenvolvimento Web, etc.

### Ação necessária (humana)

1. Acessar linkedin.com
2. Criar conta ou fazer login
3. Editar perfil com as informações preparadas
4. Adicionar foto de perfil profissional
5. Inserir links para portfólio e GitHub (quando disponíveis)

---

## 4. GITHUB

| Campo | Valor |
|-------|-------|
| **Status** | 🟡 **PARCIAL** — Conta existe, Token PAT inválido |
| **URL alvo** | `https://github.com/dev-victorlopes` |
| **Username** | `dev-victorlopes` (já verificado) |
| **Token PAT** | ❌ Inválido — gerar novo em GitHub Settings |
| **README de perfil** | Preparado em `github/profile-readme-updated.md` |

### Repositórios a criar

1. `perfil-profissional` — Este portfólio (HTML/CSS/JS)
2. `painel-omega` — Painel Ômega (Django + Supabase)
3. `sistema-gestao-empresarial` — Sistema Gestão (Django 6.1)
4. `hermes-agency` — Dashboard Hermes (HTML/JS + Supabase)

### Ação necessária

1. **Gerar novo Token PAT**: https://github.com/settings/tokens
   - Escopos: `repo`, `user`
   - Atualizar no arquivo `.env`
2. Testar token: `python scripts/github_setup.py --validate`
3. Criar repositórios: `python scripts/github_setup.py --create-repos`
4. Preparar README: `python scripts/github_setup.py --update-readme`
5. Fazer push dos projetos para os repositórios
6. Configurar README de perfil no GitHub

---

## 5. INSTAGRAM PROFISSIONAL

| Campo | Valor |
|-------|-------|
| **Status** | **PENDENTE** — Criar/Configurar perfil |
| **Username sugerido** | @victorhls ou @victor.dev |
| **Nome de exibição** | Victor Lopes |

### Bio preparada

```
💻 Python | Backend | Web
🎓 ADS @ Estácio | Python @ Senac
📍 Rio de Janeiro
🔗 Portfólio: [link]
```

### Ação necessária (humana)

1. Acessar Instagram
2. Criar nova conta (separada do pessoal)
3. Configurar username e foto de perfil
4. Adicionar bio preparada
5. Adicionar link do portfólio na bio

---

## 6. VERCEL

| Campo | Valor |
|-------|-------|
| **Status** | **PENDENTE** — Verificar/Criar conta |
| **URL** | `https://vercel.com/victorlopes` |
| **Função** | Hospedagem do portfólio |

### Ação necessária (humana)

1. Acessar vercel.com
2. Criar conta (GitHub/Email)
3. Verificar projetos existentes
4. Configurar deploy do portfólio

---

## 7. DOMÍNIO (FUTURO)

| Campo | Valor |
|-------|-------|
| **Status** | Não comprado |
| **Sugestão** | `victorlopes.dev` ou `victorhls.dev` |
| **Registradora sugerida** | Namecheap, Cloudflare, ou similar |

---

## RESUMO — O QUE FAZER AGORA

### Automático (pode continuar)

- [ ] Testar o portfólio localmente
- [ ] Verificar se o PDF do currículo funciona
- [ ] Acessar admin e testar o painel de edição
- [ ] Revisar o conteúdo de todas as plataformas

### Humano (intervenção necessária)

- [ ] Criar e-mail profissional (Gmail)
- [ ] Criar/Editar perfil LinkedIn
- [ ] Criar/Configurar GitHub
- [ ] Criar Instagram profissional
- [ ] Fazer deploy do portfólio na Vercel
- [ ] Configurar domínio (opcional, futuro)

---

## AGENDAMENTO SUGERIDO

| Etapa | Plataforma | Prioridade |
|-------|------------|------------|
| 1 | Criar e-mail profissional | 🔴 Alta |
| 2 | Configurar LinkedIn | 🔴 Alta |
| 3 | Configurar GitHub | 🔴 Alta |
| 4 | Deploy portfólio na Vercel | 🟠 Média |
| 5 | Criar Instagram profissional | 🟡 Baixa |
| 6 | Configurar domínio (futuro) | ⚪ Futuro |

---

## CREDENCIALES DE ACESSO (POR NÃO ARMANZENAR AQUI)

| Serviço | O que guardar | Onde guardar |
|---------|---------------|----------|
| E-mail profissional | Senha | Gerenciador de senhas |
| LinkedIn | Senha | Gerenciador de senhas |
| GitHub | Senha + 2FA | Gerenciador de senhas |
| Instagram | Senha | Gerenciador de senhas |
| Vercel | Senha | Gerenciador de senhas |
| Domínio | Credenciais registrar | Gerenciador de senhas |

---

## VALIDAÇÃO FINAL

Ao concluir todas as etapas, verificar:

- [ ] Todos os links do portfólio funcionam
- [ ] Download do PDF funciona
- [ ] Painel admin permite edição
- [ ] LinkedIn está consistente com o portfólio
- [ ] GitHub está consistente com o portfólio
- [ ] Instagram está consistente com o portfólio
- [ ] Nenhuma senha/CPF/token exposto em código
- [ ] `.gitignore` está configurado corretamente
- [ ] PROJECT_STATUS.md atualizado

---

**Gerenciado por**: Victor Lopes  
**Última revisão**: 2026-09-19
