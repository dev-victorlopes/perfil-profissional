#!/usr/bin/env python3
"""
Automação de Perfil LinkedIn — Victor Lopes
Versão com correção para clicar no botão visível.
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
LINKEDIN_PASSWORD = "#LargeSystem33"  # Fornecida pelo usuário para automação


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
    print(f"[{time.strftime('%H:%M:%S')}] {level}: {msg}")


def login_linkedin(page):
    """Realiza login no LinkedIn usando botão visível."""
    log("🔑 Iniciando login no LinkedIn...")
    
    try:
        page.goto("https://www.linkedin.com/login", timeout=60000, wait_until="domcontentloaded")
        time.sleep(6)
        
        # Preencher email via evaluate
        page.evaluate("""(email) => {
            const input = document.querySelector('input[type="email"]');
            if (input) {
                input.value = email;
                input.setAttribute('value', email);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""", LINKEDIN_EMAIL)
        log(f"Email preenchido: {LINKEDIN_EMAIL}")
        time.sleep(2)
        
        # Clicar no botão "Entrar" usando dispatchEvent (botão visível)
        result = page.evaluate("""() => {
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.innerText === 'Entrar' && btn.type === 'button') {
                    const rect = btn.getBoundingClientRect();
                    // Só clicar se estiver visível (tem offsetParent)
                    if (rect.width > 0 && rect.height > 0 && btn.offsetParent) {
                        const mouseDown = new MouseEvent('mousedown', {
                            bubbles: true, cancelable: true,
                            clientX: rect.left + rect.width / 2,
                            clientY: rect.top + rect.height / 2
                        });
                        const mouseUp = new MouseEvent('mouseup', {
                            bubbles: true, cancelable: true,
                            clientX: rect.left + rect.width / 2,
                            clientY: rect.top + rect.height / 2
                        });
                        const click = new MouseEvent('click', {
                            bubbles: true, cancelable: true,
                            clientX: rect.left + rect.width / 2,
                            clientY: rect.top + rect.height / 2
                        });
                        btn.dispatchEvent(mouseDown);
                        btn.dispatchEvent(mouseUp);
                        btn.dispatchEvent(click);
                        console.log('Clique no botão Entrar realizado!');
                        return true;
                    }
                }
            }
            console.log('Botão Entrar visível não encontrado');
            return false;
        }""")
        
        if not result:
            log("Falha ao clicar no botão 'Entrar'", "ERROR")
            return False
        
        log("Botão 'Entrar' clicado")
        time.sleep(6)
        
        # Verificar se apareceu campo de senha
        password_input = page.locator("input[type='password']")
        if password_input.count() == 0:
            log("Campo de senha não apareceu", "ERROR")
            return False
        
        # Preencher senha
        page.evaluate("""(password) => {
            const input = document.querySelector('input[type="password"]');
            if (input) {
                input.value = password;
                input.setAttribute('value', password);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""", LINKEDIN_PASSWORD)
        log("Senha preenchida")
        time.sleep(2)
        
        # Clicar em entrar novamente
        result = page.evaluate("""() => {
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.innerText === 'Entrar' && btn.type === 'button') {
                    const rect = btn.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0 && btn.offsetParent) {
                        const mouseDown = new MouseEvent('mousedown', {
                            bubbles: true, cancelable: true,
                            clientX: rect.left + rect.width / 2,
                            clientY: rect.top + rect.height / 2
                        });
                        const mouseUp = new MouseEvent('mouseup', {
                            bubbles: true, cancelable: true,
                            clientX: rect.left + rect.width / 2,
                            clientY: rect.top + rect.height / 2
                        });
                        const click = new MouseEvent('click', {
                            bubbles: true, cancelable: true,
                            clientX: rect.left + rect.width / 2,
                            clientY: rect.top + rect.height / 2
                        });
                        btn.dispatchEvent(mouseDown);
                        btn.dispatchEvent(mouseUp);
                        btn.dispatchEvent(click);
                        console.log('Clique no botão Entrar (senha) realizado!');
                        return true;
                    }
                }
            }
            console.log('Botão Entrar visível não encontrado na segunda etapa');
            return false;
        }""")
        
        if not result:
            log("Falha ao clicar no botão 'Entrar' (senha)", "ERROR")
            return False
        
        log("Botão 'Entrar' (senha) clicado")
        time.sleep(10)
        
        # Verificar se logou
        current_url = page.url
        if "login" in current_url.lower():
            log(f"Falha no login - ainda na URL: {current_url}", "ERROR")
            return False
        
        log(f"✅ Login realizado! Redirecionado para: {current_url}")
        return True
        
    except Exception as e:
        log(f"Erro durante login: {e}", "ERROR")
        return False


def update_profile(page):
    """Atualiza o perfil do LinkedIn."""
    log("📝 Iniciando atualização do perfil...")
    
    try:
        # Navegar para o perfil
        page.goto("https://www.linkedin.com/me", timeout=60000, wait_until="domcontentloaded")
        time.sleep(5)
        log(f"Perfil carregado: {page.url}")
        
        # Editar perfil
        edit_button = page.locator("text=Editar perfil")
        if edit_button.count() > 0:
            edit_button.click()
            time.sleep(3)
            log("Editor de perfil aberto")
        
        # Atualizar headline
        headline_field = page.locator("textarea[aria-label='Headline']")
        if headline_field.count() > 0:
            headline_field.fill(PROFILE_DATA["headline"])
            log("Headline preenchida")
            
            save_button = page.locator("button:has-text('Save')")
            if save_button.count() > 0:
                save_button.click()
                time.sleep(2)
                log("✅ Headline salva!")
        
        # Atualizar localização
        location_field = page.locator("input[aria-label='Location']")
        if location_field.count() > 0:
            location_field.fill(PROFILE_DATA["location"])
            log("Localização preenchida")
            
            save_button = page.locator("button:has-text('Save')")
            if save_button.count() > 0:
                save_button.click()
                time.sleep(2)
                log("✅ Localização salva!")
        
        # Atualizar sobre
        about_field = page.locator("textarea[aria-label='Sobre']")
        if about_field.count() > 0:
            about_field.fill(PROFILE_DATA["about"])
            log("Seção 'Sobre' preenchida")
            
            save_button = page.locator("button:has-text('Save')")
            if save_button.count() > 0:
                save_button.click()
                time.sleep(2)
                log("✅ 'Sobre' salvo!")
        
        log("✅ Atualização do perfil concluída!")
        return True
        
    except Exception as e:
        log(f"Erro ao atualizar perfil: {e}", "ERROR")
        return False


def add_skills(page):
    """Adiciona habilidades ao perfil."""
    log("🛠 Adicionando habilidades...")
    
    try:
        page.goto("https://www.linkedin.com/in/me/edit/skills", timeout=60000, wait_until="domcontentloaded")
        time.sleep(4)
        
        for skill in PROFILE_DATA["skills"]:
            log(f"  Adicionando: {skill}")
            
            search_field = page.locator("input[aria-label='Search skills']")
            if search_field.count() > 0:
                search_field.fill(skill)
                time.sleep(1)
                
                # Selecionar suggestion
                suggestion = page.locator("div[aria-label*='skill']").first
                if suggestion.count() > 0:
                    suggestion.click()
                    time.sleep(0.5)
                
                time.sleep(0.5)
        
        # Salvar
        save_button = page.locator("button:has-text('Save')")
        if save_button.count() > 0:
            save_button.click()
            time.sleep(3)
            log("✅ Habilidades salvas!")
            return True
        
        log("Botão salvar não encontrado", "WARN")
        return False
        
    except Exception as e:
        log(f"Erro ao adicionar habilidades: {e}", "ERROR")
        return False


def add_projects(page):
    """Adiciona projetos ao perfil."""
    log("🚀 Adicionando projetos...")
    
    try:
        page.goto("https://www.linkedin.com/in/me/edit/projects", timeout=60000, wait_until="domcontentloaded")
        time.sleep(4)
        
        for project in PROFILE_DATA["projects"]:
            log(f"  Adicionando: {project['name']}")
            
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
        
        return True
        
    except Exception as e:
        log(f"Erro ao adicionar projetos: {e}", "ERROR")
        return False


def update_education(page):
    """Atualiza formação acadêmica."""
    log("🎓 Atualizando formação acadêmica...")
    
    try:
        page.goto("https://www.linkedin.com/in/me/edit/education", timeout=60000, wait_until="domcontentloaded")
        time.sleep(4)
        
        for edu in PROFILE_DATA["education"]:
            log(f"  Adicionando: {edu['school']} - {edu['degree']}")
            
            add_button = page.locator("button:has-text('Add education')")
            if add_button.count() > 0:
                add_button.click()
                time.sleep(2)
                
                school_field = page.locator("input[aria-label='School name']")
                if school_field.count() > 0:
                    school_field.fill(edu["school"])
                    time.sleep(1)
                    
                    # Esperar autocomplete
                    time.sleep(1)
                    
                    # Selecionar da lista
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
        
        return True
        
    except Exception as e:
        log(f"Erro ao atualizar educação: {e}", "ERROR")
        return False


def main():
    parser = argparse.ArgumentParser(description="Automação de Perfil LinkedIn")
    parser.add_argument("--headless", action="store_true", default=True, help="Modo headless")
    args = parser.parse_args()
    
    log("=" * 60)
    log("🔗 AUTOMAÇÃO DE PERFIL LINKEDIN — Victor Lopes")
    log("=" * 60)
    log(f"📍 Email: {LINKEDIN_EMAIL}")
    log(f"📌 Headline: {PROFILE_DATA['headline']}")
    log(f"📝 Sobre: {len(PROFILE_DATA['about'])} caracteres")
    log(f"🛠 Habilidades: {len(PROFILE_DATA['skills'])} itens")
    log(f"🚀 Projetos: {len(PROFILE_DATA['projects'])} itens")
    log(f"🎓 Educação: {len(PROFILE_DATA['education'])} itens")
    log("")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=args.headless,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='pt-BR'
            )
            page = context.new_page()
            
            # Login
            if not login_linkedin(page):
                log("❌ Falha no login. Abortando.", "ERROR")
                browser.close()
                return 1
            
            # Atualizar perfil básico
            update_profile(page)
            
            # Adicionar habilidades
            add_skills(page)
            
            # Adicionar projetos
            add_projects(page)
            
            # Atualizar educação
            update_education(page)
            
            log("=" * 60)
            log("✅ AUTOMAÇÃO CONCLUÍDA!")
            log("=" * 60)
            
            browser.close()
            return 0
            
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
