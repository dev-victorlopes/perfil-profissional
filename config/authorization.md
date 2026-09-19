# Registro de Autorização — Perfil Profissional

Este arquivo registra a autorização para gerenciar as contas do perfil profissional.
**NÃO contém credenciais** — apenas metadata de autorização.

**Última atualização**: 2026-09-19  
**Autorizado por**: Victor Lopes

---

## Contas Autorizadas para Gerenciamento

| Plataforma | Identificador | Autorização | Observações |
|------------|--------------|-------------|-------------|
| GitHub | dev-victorlopes | Autorizado | Uso da API via token PAT |
| Gmail | desenvolvedor.victorlopes@gmail.com | Autorizado | Uso para envio de e-mails |
| Google API | API Key configurada | Autorizado | YouTube Studio e outras APIs |
| LinkedIn | desenvolvedor.victorlopes@gmail.com | Autorizado | Configuração de perfil (sem automação de login) |
| Vercel | (token pendente) | Condicional | Deploy do portfólio |

---

## Autorização para Gerenciamento

Declaro que autorizo o gerenciamento das contas listadas acima para fins de:
- Configuração e atualização do perfil profissional
- Gerenciamento de repositórios GitHub
- Deploy do portfólio web na Vercel
- Uso de APIs Google para funcionalidades do portfólio

**Escopo da autorização:**
- GitHub: gerenciamento de repositórios públicos, README de perfil
- Gmail: envio de e-mails profissionais (se implementado)
- Google API: uso de APIs para funcionalidades do portfólio
- LinkedIn: configuração manual de perfil (sem automação de login)
- Vercel: deploy do portfólio

**Limitações:**
- Não há autorização para ações financeiras ou de pagamento
- Não há autorização para enviar mensagens em nome de terceiros
- LinkedIn: não há automação de login/postagem (somente consulta de status)

**Validade:** Esta autorização é persistente e vale para todas as sessões de trabalho no projeto perfil-profissional.

---

## Segurança

- Credenciais sensíveis (tokens, senhas) NÃO estão registradas aqui
- Credenciais estão no arquivo .env (local, não commitado)
- O arquivo .env está protegido pelo .gitignore
- O script check-secrets.py verifica vazamentos acidentais
