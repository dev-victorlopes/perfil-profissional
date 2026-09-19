#!/usr/bin/env python3
"""
Gerenciador de LinkedIn — Perfil Profissional

⚠️  AVISO DE SEGURANÇA:
    A senha da conta LinkedIn NÃO deve ser armazenada em arquivos.
    Forneça a senha sob demanda durante a sessão de trabalho.
    
    Para automação em escala, considere usar a LinkedIn API oficial
    com OAuth 2.0 (https://learn.microsoft.com/en-us/linkedin/).

Comandos disponíveis (manual):
    python scripts/linkedin_manager.py status       # Ver status de configuração
    python scripts/linkedin_manager.py profile-info # Mostrar informações do perfil

Para operações que exigem login (criar/editar perfil, postar):
    - Acesse linkedin.com diretamente
    - Ou use a API oficial com OAuth
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from dotenv import load_dotenv
    ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
except ImportError:
    pass


# =============================================================================
# Configuration (non-sensitive only)
# =============================================================================

LINKEDIN_EMAIL = os.environ.get("LINKEDIN_EMAIL", "desenvolvedor.victorlopes@gmail.com")
LINKEDIN_PROFILE_URL = f"https://www.linkedin.com/in/victorlopes"


# =============================================================================
# Commands
# =============================================================================

def cmd_status():
    """Verifica o status de configuração do LinkedIn."""
    print("📋 Configuração LinkedIn:")
    print(f"   Email: {LINKEDIN_EMAIL}")
    print(f"   Perfil: {LINKEDIN_PROFILE_URL}")
    print()
    print("🔐 Segurança:")
    print("   A senha NÃO está armazenada em arquivos (correto).")
    print("   Forneça sob demanda durante a sessão de trabalho.")
    print()
    print("📌 Operações disponíveis:")
    print("   - Criar/editar perfil: Acesse linkedin.com manualmente")
    print("   - Postar conteúdo: Acesse linkedin.com ou use API oficial")
    print("   - Automatização em escala: Use LinkedIn API com OAuth")
    print()
    print("📝 Conteúdo preparado (já disponível no projeto):")
    print("   - linkedin/content.md — Textos para headline, sobre, projetos, skills")


def cmd_profile_info():
    """Mostra as informações do perfil que devem ser configuradas no LinkedIn."""
    print("👤 Informações do Perfil LinkedIn")
    print("=" * 50)
    print()
    
    # Headline
    print("📌 HEADLINE (40 caracteres ideais):")
    print("   Python | Desenvolvimento Web | Backend | Estudante ADS")
    print()
    print("   Alternativas:")
    print("   - Desenvolvedor Python em formação | Estágio")
    print("   - Python Backend | Web Development | Estudante")
    print()
    
    # Sobre
    print("📝 SOBRE:")
    print("   Sou Victor Lopes, estudante de Análise e Desenvolvimento de Sistemas")
    print("   (ADS) na Universidade Estácio e em treinamento em Programação Python")
    print("   pelo Senac Bonsucesso.")
    print()
    print("   Atuo no desenvolvimento de soluções web e sistemas com Python, Django e")
    print("   tecnologias relacionadas. Tenho interesse em backend, APIs, automação e")
    print("   integração de sistemas.")
    print()
    print("   Minha trajetória é construída através de projetos práticos: já desenvolvi")
    print("   painéis de controle financeiro, sistemas de gestão empresarial e dashboards")
    print("   de operação, utilizando Django, Supabase e deploy em Vercel.")
    print()
    print("   Busco oportunidades de estágio ou nível júnior onde eu possa contribuir com")
    print("   meu conhecimento em Python e desenvolvimento web, enquanto continuo")
    print("   aprendendo e crescendo na área de tecnologia.")
    print()
    
    # Skills
    print("🛠 COMPETÊNCIAS:")
    skills = [
        "Python", "Django", "Desenvolvimento Web", "HTML/CSS",
        "JavaScript", "Bancos de Dados", "Supabase", "APIs",
        "Automação", "Git/GitHub"
    ]
    for i, skill in enumerate(skills, 1):
        print(f"   {i}. {skill}")
    print()
    
    # Projetos
    print("🚀 PROJETOS:")
    print("   1. Painel Ômega — Controle de Fluxo Financeiro")
    print("      Django, PostgreSQL (Supabase), PWA, Vercel")
    print()
    print("   2. Sistema de Gestão Empresarial")
    print("      Django 6.1, PostgreSQL, ReportLab, Vercel")
    print()
    print("   3. Hermes Agency — Dashboard de Operação")
    print("      HTML/CSS/JS, Supabase, Vercel")
    print()
    
    print("📊 Para configurar no LinkedIn:")
    print("   1. Acesse linkedin.com")
    print("   2. Clique em 'Meu perfil' > 'Editar perfil'")
    print("   3. Configure cada seção com as informações acima")
    print("   4. Adicione foto de perfil profissional")
    print("   5. Inclua links para portfólio e GitHub")


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerenciador de LinkedIn para Perfil Profissional")
    subparsers = parser.add_subparsers(dest='command')
    
    subparsers.add_parser('status', help='Ver status de configuração')
    subparsers.add_parser('profile-info', help='Mostrar informações do perfil')
    
    args = parser.parse_args()
    
    if args.command == 'status':
        cmd_status()
    elif args.command == 'profile-info':
        cmd_profile_info()
    else:
        parser.print_help()
