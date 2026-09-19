#!/usr/bin/env python3
"""
Automação de Perfil LinkedIn — Victor Lopes (Semi-Automática)

Fluxo:
1. Script abre o navegador no LinkedIn (não headless)
2. VOCÊ faz o login manualmente (digita email, senha, resolve CAPTCHA se houver)
3. Após o login, o script continua automaticamente:
   - Atualiza headline
   - Atualiza seção "Sobre"
   - Atualiza localização
   - Adiciona habilidades
   - Adiciona projetos
   - Adiciona educação

Uso:
    python scripts/linkedin_semi_auto.py
"""

import time
import argparse
from pathlib import Path

try:
    from dotenv import load_dotenv
    ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
except ImportError:
    pass

from playwright.sync_api import sync_playwright


LINKEDIN_EMAIL = "desenvolvedor.victorlopes@gmail.com"

PROFILE_DATA = {
    "headline": "Python | Desenvolvimento Web | Backend | Estudante ADS",
    "about": """Sou Victor Lopes, estudante de Análise e Desenvolvimento de Sistemas (ADS) na Universidade Estácio e em treinamento em Programação Python pelo Senac Bonsucesso.

Atuo no desenvolvimento de soluções web e sistemas com Python, Django e tecnologias relacionadas. Tenho interesse em backend, APIs, automação e integração de sistemas.

Minha trajetória é construída através de projetos práticos: já desenvolvi painéis de controle financeiro, sistemas de gestão empresarial e dashboards de operação, utilizando Django, Supabase e deploy em Vercel.

Busco oportunidades de estágio ou nível júnior onde eu possa contribuir com meu conhecimento em Python e desenvolvimento web, enquanto continuo aprendendo e crescendo na área de tecnologia.

🔗 GitHub: https://github.com/dev-victorlopes
🔗 Portfólio: https://victorlopes.dev (em breve)
📧 Contato: desenvolvedor.victorlopes@gmail.com""",
    "location": "Rio de Janeiro, Rio de Janeiro, Brasil",
    "skills": [
        "Python", "Django", "Desenvolvimento Web", "HTML/CSS",
        "JavaScript", "Bancos de Dados", "Supabase", "APIs",
        "Automação", "Git/GitHub",
    ],
    "projects": [
        {
            "name": "Painel Ômega — Controle de Fluxo Financeiro",
            "description": "Painel web para controle de fluxo financeiro com gestão de clientes, saídas, empréstimos e relatórios.",
            "role": "Desenvolvedor",
        },
        {
            "name": "Sistema de Gestão Empresarial",
            "description": "MVP de sistema web para pequenos negócios com gestão de estoque, fluxo de caixa, dashboard e exportação CSV/PDF.",
            "role": "Desenvolvedor",
        },
        {
            "name": "Hermes Agency — Dashboard de Operação",
            "description": "Dashboard para gerenciamento de leads, pipeline, propostas e atividades de agência digital.",
            "role": "Desenvolvedor",
        },
    ],
    "education": [
        {
            "school": "Universidade Estácio",
            "degree": "Análise e Desenvolvimento de Sistemas (ADS)",
            "start_date": "2026-08",
            "description": "Graduação em andamento.",
        },
        {
            "school": "Senac Bonsucesso",
            "degree": "Programação em Python",
            "start_date": "2025-02",
            "end_date": "2026-10",
            "description": "Formação técnica focada em Python.",
        },
    ],
}


def log(msg, level="INFO"):
    print(f"\r[{time.strftime('%H:%M:%S')}] {level}: {msg}")


def wait_for_manual_login(page, timeout=300):
    """
    Aguarda o usuário fazer login manualmente.
    Retorna True se o login foi detectado, False se timeout.
    """
    log("⏳ Aguardo login manual...")
    log("   1. Digite seu email: desenvolvedor.victorlopes@gmail.com")
    log("   2. Clique em 'Próximo'")
    log("   3. Digite sua senha")
    log("   4. Clique em 'Entrar'")
    log("   5. Resolva CAPTCHA se aparecer")
    log("")
    log(f"   Tempo limite: {timeout} segundos")
    log("")
    
    start_time = time.time()
    last_url = page.url
    
    while time.time() - start_time < timeout:
        current_url = page.url
        
        # Verificar se saiu da página de login
        if "login" not in current_url.lower() and current_url != last_url:
            log(f"✅ Login detectado! Redirecionado para: {current_url}")
            return True
        
        # Verificar se há CAPTCHA
        if page.locator("iframe[src*='captcha']").count() > 0:
            log("⚠️  CAPTCHA detectado! Resolva e aguarde...", "WARN")
        
        time.sleep(2)
        
        if int(time.time() - start_time) % 10 == 0:
            elapsed = int(time.time() - start_time)
            log(f"   Aguardo login... {elapsed}s / {timeout}s", "INFO")
    
    log("❌ Timeout aguardando login", "ERROR")
    return False


def update_headline(page):
    """Atualiza a headline do perfil."""
    log("📌 Atualizando headline...")
    
    try:
        # Navegar para o perfil
        page.goto("https://www.linkedin.com/me", timeout=60000, wait_until="domcontentloaded")
        time.sleep(5)
        
        # Clicar em editar perfil
        edit_button = page.locator("text=Editar perfil")
        if edit_button.count() > 0:
            edit_button.click()
            time.sleep(3)
            log("Editor de perfil aberto")
        
        # Preencher headline
        headline_field = page.locator("textarea[aria-label='Headline']")
        if headline_field.count() > 0:
            headline_field.fill(PROFILE_DATA["headline"])
            log(f"Headline preenchida: {PROFILE_DATA['headline']}")
            
            # Salvar
            save_button = page.locator("button:has-text('Save')")
            if save_button.count() > 0:
                save_button.click()
                time.sleep(3)
                log("✅ Headline salva!")
            else:
                log("Botão salvar não encontrado", "WARN")
        else:
            log("Campo de headline não encontrado", "WARN")
        
        return True
        
    except Exception as e:
        log(f"Erro ao atualizar headline: {e}", "ERROR")
        return False


def update_about(page):
    """Atualiza a seção Sobre."""
    log("📝 Atualizando seção 'Sobre'...")
    
    try:
        # Esperar página carregar
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        # Clicar em editar perfil se necessário
        edit_button = page.locator("text=Editar perfil")
        if edit_button.count() > 0:
            edit_button.click()
            time.sleep(2)
        
        # Preencher sobre
        about_field = page.locator("textarea[aria-label='Sobre']")
        if about_field.count() > 0:
            about_field.fill(PROFILE_DATA["about"])
            log(f"'Sobre' preenchido ({len(PROFILE_DATA['about'])} caracteres)")
            
            # Salvar
            save_button = page.locator("button:has-text('Save')")
            if save_button.count() > 0:
                save_button.click()
                time.sleep(3)
                log("✅ 'Sobre' salvo!")
            else:
                log("Botão salvar não encontrado", "WARN")
        else:
            log("Campo 'Sobre' não encontrado", "WARN")
        
        return True
        
    except Exception as e:
        log(f"Erro ao atualizar 'Sobre': {e}", "ERROR")
        return False


def update_location(page):
    """Atualiza a localização."""
    log("📍 Atualizando localização...")
    
    try:
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        location_field = page.locator("input[aria-label='Location']")
        if location_field.count() > 0:
            location_field.fill(PROFILE_DATA["location"])
            log(f"Localização preenchida: {PROFILE_DATA['location']}")
            
            save_button = page.locator("button:has-text('Save')")
            if save_button.count() > 0:
                save_button.click()
                time.sleep(3)
                log("✅ Localização salva!")
            else:
                log("Botão salvar não encontrado", "WARN")
        else:
            log("Campo de localização não encontrado", "WARN")
        
        return True
        
    except Exception as e:
        log(f"Erro ao atualizar localização: {e}", "ERROR")
        return False


def add_skills(page):
    """Adiciona habilidades ao perfil."""
    log("🛠 Adicionando habilidades...")
    
    try:
        page.goto("https://www.linkedin.com/in/me/edit/skills", timeout=60000, wait_until="domcontentloaded")
        time.sleep(4)
        
        for i, skill in enumerate(PROFILE_DATA["skills"], 1):
            log(f"  [{i}/{len(PROFILE_DATA['skills'])}] Adicionando: {skill}")
            
            try:
                search_field = page.locator("input[aria-label='Search skills']")
                if search_field.count() > 0:
                    search_field.fill(skill)
                    time.sleep(1)
                    
                    # Selecionar sugestão
                    suggestion = page.locator("div[aria-label*='skill']").first
                    if suggestion.count() > 0:
                        suggestion.click()
                        time.sleep(0.5)
                    
                    time.sleep(0.5)
                else:
                    log(f"    Campo de busca não encontrado", "WARN")
                    
            except Exception as e:
                log(f"    Erro: {e}", "WARN")
        
        # Salvar
        try:
            save_button = page.locator("button:has-text('Save')")
            if save_button.count() > 0:
                save_button.click()
                time.sleep(3)
                log("✅ Habilidades salvas!")
            else:
                log("Botão salvar não encontrado", "WARN")
        except Exception as e:
            log(f"Erro ao salvar habilidades: {e}", "WARN")
        
        return True
        
    except Exception as e:
        log(f"Erro ao adicionar habilidades: {e}", "ERROR")
        return False


def add_projects(page):
    """Adiciona projetos ao perfil."""
    log("🚀 Adicionando projetos...")
    
    try:
        page.goto("https://www.linkedin.com/in/me/edit/projects", timeout=60000, wait_until="domcontentloaded")
        time.sleep(4)
        
        for i, project in enumerate(PROFILE_DATA["projects"], 1):
            log(f"  [{i}/{len(PROFILE_DATA['projects'])}] Adicionando: {project['name']}")
            
            try:
                add_button = page.locator("button:has-text('Add project')")
                if add_button.count() > 0:
                    add_button.click()
                    time.sleep(2)
                    
                    name_field = page.locator("input[aria-label='Project name']")
                    if name_field.count() > 0:
                        name_field.fill(project["name"])
                        time.sleep(0.5)
                    
                    desc_field = page.locator("textarea[aria-label='Project description']")
                    if desc_field.count() > 0:
                        desc_field.fill(project["description"])
                        time.sleep(0.5)
                    
                    role_field = page.locator("input[aria-label='Your role']")
                    if role_field.count() > 0:
                        role_field.fill(project["role"])
                        time.sleep(0.5)
                    
                    save_button = page.locator("button:has-text('Save')")
                    if save_button.count() > 0:
                        save_button.click()
                        time.sleep(2)
                        log(f"    ✅ {project['name']} adicionado!")
                    else:
                        log(f"    ⚠️ Botão salvar não encontrado", "WARN")
                else:
                    log(f"    ⚠️ Botão adicionar não encontrado", "WARN")
                time.sleep(1)
            except Exception as e:
                log(f"    Erro: {e}", "WARN")
        
        return True
        
    except Exception as e:
        log(f"Erro ao adicionar projetos: {e}", "ERROR")
        return False


def add_education(page):
    """Adiciona educação ao perfil."""
    log("🎓 Adicionando formação acadêmica...")
    
    try:
        page.goto("https://www.linkedin.com/in/me/edit/education", timeout=60000, wait_until="domcontentloaded")
        time.sleep(4)
        
        for i, edu in enumerate(PROFILE_DATA["education"], 1):
            log(f"  [{i}/{len(PROFILE_DATA['education'])}] Adicionando: {edu['school']} - {edu['degree']}")
            
            try:
                add_button = page.locator("button:has-text('Add education')")
                if add_button.count() > 0:
                    add_button.click()
                    time.sleep(2)
                    
                    school_field = page.locator("input[aria-label='School name']")
                    if school_field.count() > 0:
                        school_field.fill(edu["school"])
                        time.sleep(1)
                        
                        # Tentar selecionar da autocomplete
                        try:
                            suggestion = page.locator("div[aria-label*='school']").first
                            if suggestion.count() > 0:
                                suggestion.click()
                                time.sleep(1)
                        except:
                            pass
                    
                    degree_field = page.locator("input[aria-label='Degree']")
                    if degree_field.count() > 0:
                        degree_field.fill(edu["degree"])
                        time.sleep(0.5)
                    
                    start_field = page.locator("input[aria-label='Start date']")
                    if start_field.count() > 0:
                        start_field.fill(edu["start_date"])
                        time.sleep(0.5)
                    
                    if edu.get("end_date"):
                        end_field = page.locator("input[aria-label='End date']")
                        if end_field.count() > 0:
                            end_field.fill(edu["end_date"])
                            time.sleep(0.5)
                    
                    desc_field = page.locator("textarea[aria-label='Description']")
                    if desc_field.count() > 0:
                        desc_field.fill(edu.get("description", ""))
                        time.sleep(0.5)
                    
                    save_button = page.locator("button:has-text('Save')")
                    if save_button.count() > 0:
                        save_button.click()
                        time.sleep(2)
                        log(f"    ✅ {edu['school']} adicionado!")
                    else:
                        log(f"    ⚠️ Botão salvar não encontrado", "WARN")
                else:
                    log(f"    ⚠️ Botão adicionar não encontrado", "WARN")
                time.sleep(1)
            except Exception as e:
                log(f"    Erro: {e}", "WARN")
        
        return True
        
    except Exception as e:
        log(f"Erro ao adicionar educação: {e}", "ERROR")
        return False


def main():
    parser = argparse.ArgumentParser(description="Automação Semi-Automática de Perfil LinkedIn")
    parser.add_argument("--headless", action="store_true", help="Modo headless (não recomendado para login manual)")
    args = parser.parse_args()
    
    headless = args.headless
    
    log("=" * 70)
    log("🔗 AUTOMAÇÃO SEMI-AUTOMÁTICA DE PERFIL LINKEDIN — Victor Lopes")
    log("=" * 70)
    log("")
    log("📋 RESUMO DO QUE SERÁ FEITO:")
    log(f"  📌 Headline: {PROFILE_DATA['headline']}")
    log(f"  📝 Sobre: {len(PROFILE_DATA['about'])} caracteres")
    log(f"  📍 Localização: {PROFILE_DATA['location']}")
    log(f"  🛠 Habilidades: {len(PROFILE_DATA['skills'])} itens")
    log(f"  🚀 Projetos: {len(PROFILE_DATA['projects'])} itens")
    log(f"  🎓 Educação: {len(PROFILE_DATA['education'])} itens")
    log("")
    
    if headless:
        log("⚠️  Modo headless ativado - login manual não será possível!", "WARN")
        log("   Recomenda-se executar SEM --headless para login manual", "WARN")
        log("")
    
    log("=" * 70)
    log("INÍCIO DA AUTOMAÇÃO")
    log("=" * 70)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='pt-BR'
            )
            page = context.new_page()
            
            # Navegar para o login
            page.goto("https://www.linkedin.com/login", timeout=60000, wait_until="domcontentloaded")
            time.sleep(3)
            
            log("")
            log("🌐 Navegador aberto no LinkedIn")
            log("")
            
            # Aguardo login manual
            if not wait_for_manual_login(page, timeout=300):
                log("")
                log("❌ Login não realizado. Encerrando.", "ERROR")
                browser.close()
                return 1
            
            log("")
            log("=" * 70)
            log("LOGIN CONCLUÍDO - INICIANDO AUTOMAÇÃO DOS CAMPOS")
            log("=" * 70)
            log("")
            
            # Atualizar headline
            update_headline(page)
            log("")
            
            # Atualizar sobre
            update_about(page)
            log("")
            
            # Atualizar localização
            update_location(page)
            log("")
            
            # Adicionar habilidades
            add_skills(page)
            log("")
            
            # Adicionar projetos
            add_projects(page)
            log("")
            
            # Adicionar educação
            add_education(page)
            log("")
            
            log("=" * 70)
            log("✅ AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
            log("=" * 70)
            log("")
            log("📌 Acesse https://www.linkedin.com/in/dev-victorlopes para verificar")
            log("")
            
            # Manter aberto para inspeção
            log("Navegador permanecerá aberto por 60 segundos...")
            time.sleep(60)
            
            browser.close()
            return 0
            
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
