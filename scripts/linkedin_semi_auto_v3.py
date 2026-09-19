#!/usr/bin/env python3
"""
Automação de Perfil LinkedIn — Victor Lopes (v3 - Corrigida)
"""

import time
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


def click_edit_profile(page):
    """Clica em 'Editar perfil' de forma robusta."""
    log("✏️  Tentando abrir editor de perfil...")
    
    strategies = [
        "text=Editar perfil",
        "text=Edit profile",
        "//button[contains(text(), 'Editar')]",
        "//button[contains(text(), 'Edit')]",
        "button[data-test='profile-edit-btn']",
    ]
    
    for selector in strategies:
        try:
            if selector.startswith("//"):
                element = page.locator(selector)
            else:
                element = page.locator(selector)
            
            if element.count() > 0:
                # Aguarde até estar clicável
                page.wait_for_selector(selector, state="visible", timeout=5000)
                element.first.click()
                time.sleep(3)
                log(f"✅ Editor aberto via: {selector}")
                return True
        except Exception as e:
            log(f"  Tentativa '{selector}' falhou: {e}", "DEBUG")
    
    log("❌ Não conseguiu abrir editor de perfil", "WARN")
    return False


def update_headline(page):
    """Atualiza a headline do perfil."""
    log("📌 Atualizando headline...")
    
    # Clicar em editar perfil primeiro
    click_edit_profile(page)
    time.sleep(2)
    
    try:
        headline_field = page.locator("textarea[aria-label='Headline']")
        if headline_field.count() > 0:
            headline_field.fill(PROFILE_DATA["headline"])
            log(f"Headline preenchida")
            
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
    
    click_edit_profile(page)
    time.sleep(2)
    
    try:
        about_field = page.locator("textarea[aria-label='Sobre']")
        if about_field.count() > 0:
            about_field.fill(PROFILE_DATA["about"])
            log(f"'Sobre' preenchido")
            
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
    
    click_edit_profile(page)
    time.sleep(2)
    
    try:
        location_field = page.locator("input[aria-label='Location']")
        if location_field.count() > 0:
            location_field.fill(PROFILE_DATA["location"])
            log(f"Localização preenchida")
            
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
    log("🔗 AUTOMAÇÃO V3 — Victor Lopes (LinkedIn)")
    log("=" * 70)
    
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
            
            log("🌐 Navegador aberto - FAÇA LOGIN!")
            log("")
            
            # Login manual
            start_time = time.time()
            while time.time() - start_time < 120:
                current_url = page.url
                if "login" not in current_url.lower():
                    elapsed = int(time.time() - start_time)
                    log(f"✅ Login detectado após {elapsed}s!")
                    log(f"   URL: {current_url}")
                    break
                time.sleep(1)
            else:
                log("❌ Timeout no login", "ERROR")
                browser.close()
                return 1
            
            log("")
            log("=" * 70)
            log("INICIANDO AUTOMAÇÃO")
            log("=" * 70)
            log("")
            
            # Atualizar campos básicos (precisam clicar em editar primeiro)
            update_headline(page)
            log("")
            update_about(page)
            log("")
            update_location(page)
            log("")
            
            # Habilidades, projetos e educação são em páginas separadas
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
