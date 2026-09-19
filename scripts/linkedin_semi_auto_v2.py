#!/usr/bin/env python3
"""
Automação de Perfil LinkedIn — Victor Lopes (Semi-Automática v2)
Versão com detecção mais rápida de login.
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
    print(f"\r[{time.strftime('%H:%M:%S')}] {level}: {msg}", flush=True)


def wait_for_manual_login_v2(page, timeout=120):
    """
    Versão melhorada: verifica URL e conteúdo da página.
    """
    log("⏳ Aguardando login manual...")
    log("   ✅ Você está no LinkedIn - faça login quando pronto")
    log("   🔍 Detectando login em até {} segundos...".format(timeout))
    log("")
    
    start_time = time.time()
    last_detected_url = None
    
    while time.time() - start_time < timeout:
        current_url = page.url
        page_title = page.title()
        
        # Verificar mudança de URL
        if current_url != last_detected_url and "login" not in current_url.lower():
            elapsed = int(time.time() - start_time)
            log(f"✅ Login detectado após {elapsed}s!")
            log(f"   URL: {current_url}")
            log(f"   Título: {page_title}")
            return True
        
        # Verificar se saiu da página de login mesmo que URL ainda tenha "login"
        # (alguns redirecionamentos temporários mantêm "login" na URL)
        try:
            # Se a página de login não estiver mais visível, consideramos que logou
            login_page_elements = page.locator("input[type='email'], input[type='password']")
            if login_page_elements.count() == 0:
                # Não há campos de login - provavelmente mudou de página
                if current_url != last_detected_url:
                    elapsed = int(time.time() - start_time)
                    log(f"✅ Página de login não encontrada - provável login!")
                    log(f"   URL: {current_url}")
                    return True
        except:
            pass
        
        last_detected_url = current_url
        time.sleep(1)  # Verifica mais rápido (a cada 1 segundo)
    
    log("❌ Timeout aguardando login", "ERROR")
    return False


def update_headline(page):
    """Atualiza a headline do perfil."""
    log("📌 Atualizando headline...")
    
    try:
        page.goto("https://www.linkedin.com/me", timeout=60000, wait_until="domcontentloaded")
        time.sleep(4)
        
        edit_button = page.locator("text=Editar perfil")
        if edit_button.count() > 0:
            edit_button.click()
            time.sleep(3)
        
        headline_field = page.locator("textarea[aria-label='Headline']")
        if headline_field.count() > 0:
            headline_field.fill(PROFILE_DATA["headline"])
            save_button = page.locator("button:has-text('Save')").first
            if save_button.count() > 0:
                save_button.click()
                time.sleep(3)
                log("✅ Headline salva!")
            else:
                log("⚠️ Botão salvar não encontrado", "WARN")
        else:
            log("⚠️ Campo de headline não encontrado", "WARN")
        
        return True
    except Exception as e:
        log(f"Erro: {e}", "ERROR")
        return False


def update_about(page):
    """Atualiza a seção Sobre."""
    log("📝 Atualizando 'Sobre'...")
    
    try:
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        edit_button = page.locator("text=Editar perfil")
        if edit_button.count() > 0:
            edit_button.click()
            time.sleep(2)
        
        about_field = page.locator("textarea[aria-label='Sobre']")
        if about_field.count() > 0:
            about_field.fill(PROFILE_DATA["about"])
            save_button = page.locator("button:has-text('Save')").first
            if save_button.count() > 0:
                save_button.click()
                time.sleep(3)
                log("✅ 'Sobre' salvo!")
            else:
                log("⚠️ Botão salvar não encontrado", "WARN")
        else:
            log("⚠️ Campo 'Sobre' não encontrado", "WARN")
        
        return True
    except Exception as e:
        log(f"Erro: {e}", "ERROR")
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
            save_button = page.locator("button:has-text('Save')").first
            if save_button.count() > 0:
                save_button.click()
                time.sleep(3)
                log("✅ Localização salva!")
            else:
                log("⚠️ Botão salvar não encontrado", "WARN")
        else:
            log("⚠️ Campo de localização não encontrado", "WARN")
        
        return True
    except Exception as e:
        log(f"Erro: {e}", "ERROR")
        return False


def add_skills(page):
    """Adiciona habilidades ao perfil."""
    log("🛠 Adicionando habilidades...")
    
    try:
        page.goto("https://www.linkedin.com/in/me/edit/skills", timeout=60000, wait_until="domcontentloaded")
        time.sleep(4)
        
        for i, skill in enumerate(PROFILE_DATA["skills"], 1):
            log(f"  [{i}/{len(PROFILE_DATA['skills'])}] {skill}")
            
            try:
                search_field = page.locator("input[aria-label='Search skills']")
                if search_field.count() > 0:
                    search_field.fill(skill)
                    time.sleep(1)
                    
                    suggestion = page.locator("div[aria-label*='skill']").first
                    if suggestion.count() > 0:
                        suggestion.click()
                        time.sleep(0.5)
                    
                    time.sleep(0.5)
            except Exception as e:
                log(f"    Erro: {e}", "WARN")
        
        save_button = page.locator("button:has-text('Save')").first
        if save_button.count() > 0:
            save_button.click()
            time.sleep(3)
            log("✅ Habilidades salvas!")
        else:
            log("⚠️ Botão salvar não encontrado", "WARN")
        
        return True
    except Exception as e:
        log(f"Erro: {e}", "ERROR")
        return False


def add_projects(page):
    """Adiciona projetos ao perfil."""
    log("🚀 Adicionando projetos...")
    
    try:
        page.goto("https://www.linkedin.com/in/me/edit/projects", timeout=60000, wait_until="domcontentloaded")
        time.sleep(4)
        
        for i, project in enumerate(PROFILE_DATA["projects"], 1):
            log(f"  [{i}/{len(PROFILE_DATA['projects'])}] {project['name']}")
            
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
                    
                    save_button = page.locator("button:has-text('Save')").first
                    if save_button.count() > 0:
                        save_button.click()
                        time.sleep(2)
                        log(f"    ✅ Adicionado!")
                    else:
                        log(f"    ⚠️ Botão salvar não encontrado", "WARN")
                else:
                    log(f"    ⚠️ Botão adicionar não encontrado", "WARN")
                time.sleep(1)
            except Exception as e:
                log(f"    Erro: {e}", "WARN")
        
        return True
    except Exception as e:
        log(f"Erro: {e}", "ERROR")
        return False


def add_education(page):
    """Adiciona educação ao perfil."""
    log("🎓 Adicionando formação acadêmica...")
    
    try:
        page.goto("https://www.linkedin.com/in/me/edit/education", timeout=60000, wait_until="domcontentloaded")
        time.sleep(4)
        
        for i, edu in enumerate(PROFILE_DATA["education"], 1):
            log(f"  [{i}/{len(PROFILE_DATA['education'])}] {edu['school']} - {edu['degree']}")
            
            try:
                add_button = page.locator("button:has-text('Add education')")
                if add_button.count() > 0:
                    add_button.click()
                    time.sleep(2)
                    
                    school_field = page.locator("input[aria-label='School name']")
                    if school_field.count() > 0:
                        school_field.fill(edu["school"])
                        time.sleep(1)
                        
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
                    
                    save_button = page.locator("button:has-text('Save')").first
                    if save_button.count() > 0:
                        save_button.click()
                        time.sleep(2)
                        log(f"    ✅ Adicionado!")
                    else:
                        log(f"    ⚠️ Botão salvar não encontrado", "WARN")
                else:
                    log(f"    ⚠️ Botão adicionar não encontrado", "WARN")
                time.sleep(1)
            except Exception as e:
                log(f"    Erro: {e}", "WARN")
        
        return True
    except Exception as e:
        log(f"Erro: {e}", "ERROR")
        return False


def main():
    log("=" * 70)
    log("🔗 AUTOMAÇÃO V2 — Victor Lopes (LinkedIn Semi-Automático)")
    log("=" * 70)
    log("")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='pt-BR'
            )
            page = context.new_page()
            
            page.goto("https://www.linkedin.com/login", timeout=60000, wait_until="domcontentloaded")
            time.sleep(3)
            
            log("🌐 Navegador aberto - FAÇA LOGIN AGORA!")
            log("")
            
            if not wait_for_manual_login_v2(page, timeout=120):
                log("❌ Login não detectado", "ERROR")
                browser.close()
                return 1
            
            log("")
            log("=" * 70)
            log("INICIANDO AUTOMAÇÃO DOS CAMPOS")
            log("=" * 70)
            log("")
            
            update_headline(page)
            log("")
            update_about(page)
            log("")
            update_location(page)
            log("")
            add_skills(page)
            log("")
            add_projects(page)
            log("")
            add_education(page)
            log("")
            
            log("=" * 70)
            log("✅ AUTOMAÇÃO CONCLUÍDA!")
            log("=" * 70)
            log("")
            log("📌 Verifique: https://www.linkedin.com/in/dev-victorlopes")
            log("")
            
            time.sleep(30)
            browser.close()
            return 0
            
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
