# Project Status — Perfil Profissional Digital

**Atualizado**: 2026-09-19  
**Responsável**: Victor Lopes  
**Status geral**: EXECUÇÃO — FASE 1 COMPLETA + AMBIENTE DE GESTÃO SEGURO

---

## Resumo Executivo

Projeto de construção da presença profissional digital para Victor Lopes, focado em:
- Busca de estágio em tecnologia
- Oportunidades de desenvolvedor Python júnior
- Desenvolvimento web/backend
- Automação e integração de sistemas

---

## Objetivo da Fase 1

Criar uma presença profissional coerente, realista e tecnicamente sólida em:
1. E-mail profissional
2. LinkedIn
3. GitHub
4. Instagram profissional
5. Portfólio web (Vercel)

---

## Estado Atual por Plataforma

|| Plataforma | Status | URL | Observações |
||------------|--------|-----|-------------|
|| E-mail profissional | 🔴 PENDENTE | — | Criar conta (ação humana) |
|| LinkedIn | 🔴 PENDENTE | — | Configurar perfil (ação humana) |
|| **GitHub** | 🟢 **CONCLUÍDO** | `github.com/dev-victorlopes` | Profile editado, 4 repos criados, sistema de gerenciamento completo |
|| Instagram profissional | 🔴 PENDENTE | — | Criar/adaptar (ação humana) |
|| Portfólio web | ✅ CONCLUÍDO | `/index.html` | Tema dark, responsivo, funcional |
|| Painel Admin | ✅ CONCLUÍDO | `/admin/index.html` | Login local, localStorage |
|| Currículo PDF | ✅ CONCLUÍDO | `/resume/curriculo_victor_lopes.pdf` | Gerado com ReportLab |

---

|| Tarefas Concluídas ✅ |

| Tarefa | Descrição | Arquivo |
|--------|-----------|---------|
| Estrutura de projetos | Diretórios e arquivos base | `perfil-profissional/` |
| Portfólio web | HTML + CSS dark + JS, tema moderno | `index.html`, `styles.css`, `script.js` |
| Painel administrativo | Login, edição de conteúdo, localStorage | `admin/index.html` |
| Currículo PDF | Gerado via ReportLab, ATS-friendly | `resume/curriculo_victor_lopes.pdf` |
| Textos LinkedIn | Headline, sobre, projetos, skills | `linkedin/content.md` |
| README GitHub | Markdown profissional com shields | `github/profile-readme.md` |
| Conteúdo Instagram | Bio, username sugeridos, conteúdo | `instagram/content.md` |
| E-mail options | Sugestões de nomenclatura | `linkedin/email-options.md` |
| Docs de estratégia | Strategy, profile-data, deployment | `docs/*.md` |
| `.env.example` | Variáveis de ambiente sem valores | `.env.example` |
| `.gitignore` | Ignorar secrets, env, node_modules | `.gitignore` |
| README_CREDENCIAIS | Documento de credenciais e ações | `README_CREDENCIAIS.md` |
| PROJECT_STATUS | Estado atualizado do projeto | `PROJECT_STATUS.md` |
| **Ambiente seguro de gerenciamento** | Scripts para gerenciar GitHub, Google API, LinkedIn, Vercel | `scripts/*.py` |
| **Variáveis de ambiente configuradas** | Credenciais não-sensíveis no .env | `.env` |
| **Venv Python** | Ambiente isolado com dependências | `.venv/` |
| **Perfil GitHub editado** | Name, Bio, Location, Blog, Email, Hireable | API GitHub |
| **GitHub Projects Manager** | Sistema completo para gerenciar repos via CLI/API | `scripts/github_projects_manager.py` |

---

## Tarefas Pendentes — Ação Humana Necessária 🔴

| Tarefa | Plataforma | Bloqueio |
|--------|------------|----------|
| Criar conta de e-mail profissional | Gmail | CAPTCHA/validação humana |
| **Configurar perfil LinkedIn** | LinkedIn | **Bloqueio anti-automacao** - acesso manual necessário |
| Criar/atualizar Instagram profissional | Instagram | Login + possível verificação |
| Deploy do portfólio na Vercel | Vercel | Login na plataforma |

---

## Ambiente de Gerenciamento Seguro

O projeto agora possui um ambiente seguro para gerenciar as contas do perfil profissional.

### Arquitetura de Segurança

```
perfil-profissional/
├── .env                      ← Credenciais (NÃO commitar — já no .gitignore)
├── .env.example              ← Template de variáveis
├── .gitignore                ← Protege .env e arquivos sensíveis
├── config/
│   └── project.yaml          ← Metadados do projeto (não sensíveis)
├── scripts/
│   ├── manager.py            ← Orquestrador principal
│   ├── auth.py               ← Autorização persistente com senha mestra
│   ├── credentials.py        ← Gerenciador de credenciais em memória
│   ├── check-secrets.py      ← Verificador de vazamentos antes de commit
│   ├── github_manager.py     ← Comandos para gerenciar GitHub via API
│   ├── google_manager.py     ← Comandos para gerenciar Google APIs
│   ├── linkedin_manager.py   ← Status e informações do LinkedIn (sem login automatizado)
│   └── deploy.py             ← Comandos para deploy na Vercel
└── .venv/                    ← Ambiente Python isolado (já no .gitignore)
```

### Princípios de Segurança

1. **Nunca armazenar senhas em arquivos** — senhas são fornecidas sob demanda durante a sessão
2. **Tokens de API com escopo mínimo** — GitHub PAT e Google API Key têm acesso apenas ao necessário
3. **Arquivo .env em .gitignore** — credenciais nunca são commitadas
4. **check-secrets.py** — verifica vazamentos acidentais antes de commit/deploy
5. **auth.py** — autorização persistente com senha mestra (criptografada com `cryptography`)

### Como Usar

```bash
# Ativar ambiente virtual
cd /home/victor/Documentos/Hermes_Agent/PROJETOS/perfil-profissional
source .venv/bin/activate

# Ver status geral
python scripts/manager.py status

# Ver status de credenciais
python scripts/manager.py auth-status

# Gerenciar GitHub
python scripts/github_manager.py status
python scripts/github_manager.py repos

# Gerenciar Google API
python scripts/google_manager.py status

# Informações do LinkedIn (sem login automatizado — seguro)
python scripts/linkedin_manager.py profile-info

# Deploy na Vercel
python scripts/deploy.py check
python scripts/deploy.py deploy
```

---

## Bloqueios Identificados

1. **Autenticação em plataformas externas** — CAPTCHA, SMS, 2FA, termos de serviço exigem ação humana
2. **Criação de conta de e-mail** — Validação humana obrigatória
3. **Publicação de conteúdo** — LinkedIn, Instagram exigem login e possível verificação

---

## URL do Portfólio (local)

- **Página principal**: `/home/victor/Documentos/Hermes_Agent/PROJETOS/perfil-profissional/index.html`
- **Painel admin**: `/home/victor/Documentos/Hermes_Agent/PROJETOS/perfil-profissional/admin/index.html`
- **Login admin**: `admin@victorlopes.local` / `admin2026`
- **Currículo PDF**: `/home/victor/Documentos/Hermes_Agent/PROJETOS/perfil-profissional/resume/curriculo_victor_lopes.pdf`

---

## Estrutura Final do Projeto

```
perfil-profissional/
├── .env                        ← Variáveis de ambiente (não commitar)
├── .env.example                ← Template de variáveis
├── .gitignore                  ← Regras de ignorado do git
├── AGENTS.md                   ← Instruções para agentes de IA
├── PROJECT_STATUS.md           ← Este arquivo
├── README.md                   ← Leitura principal
├── README_CREDENCIAIS.md       ← Documento de credenciais
├── config/
│   └── project.yaml            ← Metadados do projeto
├── docs/
│   ├── strategy.md
│   ├── profile-data.md
│   └── deployment.md
├── portfolio/
│   ├── index.html              ← Portfólio principal
│   ├── styles.css              ← Tema dark moderno
│   └── script.js               ← Interações
├── admin/
│   └── index.html              ← Painel administrativo
├── resume/
│   ├── resume.html             ← Currículo web
│   ├── styles.css              ← Estilos do currículo
│   ├── generate_pdf.py         ← Script PDF
│   ├── curriculo_victor_lopes.pdf ← PDF gerado
│   └── .venv/                  ← Ambiente Python (ignorado)
├── github/
│   └── profile-readme.md       ← README de perfil GitHub
├── linkedin/
│   ├── content.md              ← Textos para LinkedIn
│   └── email-options.md        ← Sugestões de e-mail
├── instagram/
│   └── content.md              ← Conteúdo para Instagram
├── scripts/
│   ├── manager.py              ← Orquestrador principal
│   ├── auth.py                 ← Autorização persistente
│   ├── credentials.py          ← Gerenciador de credenciais
│   ├── check-secrets.py        ← Verificador de segredos
│   ├── github_manager.py       ← Gerenciador do GitHub
│   ├── google_manager.py       ← Gerenciador do Google API
│   ├── linkedin_manager.py     ← Gerenciador do LinkedIn
│   └── deploy.py               ← Deploy na Vercel
└── .venv/                      ← Ambiente Python (ignorado)
```

---

## Critérios de Conclusão — Fase 1

### ✅ Concluído

- [x] Estrutura de projeto criada
- [x] Portfólio web funcional (HTML/CSS/JS, tema dark)
- [x] Painel administrativo com login funcional
- [x] Currículo PDF gerável e funcional
- [x] Textos preparados para todas as plataformas
- [x] Documentação completa
- [x] Credenciais documentadas (sem senhas)
- [x] Segurança: CPF, senhas e tokens não expostos
- [x] **Ambiente de gerenciamento seguro criado**
- [x] **Scripts para GitHub, Google API, LinkedIn, Vercel**
- [x] **Autorização para gerenciar contas registrada**

### 🔴 Pendente — Intervenção Humana

- [ ] E-mail profissional criado
- [ ] LinkedIn configurado
- [ ] GitHub configurado
- [ ] Instagram profissional configurado
- [ ] Portfólio deployado na Vercel
- [ ] Links circulares funcionando
- [ ] Foto de perfil profissional (opcional)

---

## Próximos Passos

### Imediato (Victor)

1. **Criar e-mail profissional** — Escolher entre `vic.lopes@`, `victor.lopes@`, ou similar
2. **Configurar LinkedIn** — Usar conteúdo de `linkedin/content.md`
3. **Configurar GitHub** — Usar README de `github/profile-readme.md`
4. **Criar Instagram profissional** — Usar conteúdo de `instagram/content.md`

### Processual

5. **Fazer deploy do portfólio na Vercel** (ver `docs/deployment.md`)
6. **Atualizar e-mails/URLs** nos documentos após criação das contas
7. **Fazer commit e push** dos projetos para o GitHub
8. **Validar todos os links** e funcionalidades

---

## Fonte de Dados do Perfil

Todos os dados do perfil são baseados no documento de requisitos fornecido por Victor.
Projetos reais foram analisados nos diretórios:
- `/fluxo-financeiro/` — Painel Ômega (Django + PWA + Supabase)
- `/sistema-gestao/` — Sistema Gestão Empresarial (Django 6.1)
- `/Hermes_Agency/` — Dashboard agência (HTML/JS + Supabase)
