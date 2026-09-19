#!/usr/bin/env python3
"""
Automação de Perfil LinkedIn — Victor Lopes
Usando Chromium do Playwright com Selenium
"""

import os
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
except ImportError:
    pass

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


CHROME_PATH = os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome")
if not os.path.exists(CHROME_PATH):
    # Tentar versão alternativa
    CHROME_PATH = os.path.expanduser("~/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome")

LINKEDIN_EMAIL = os.environ.get("LINKEDIN_EMAIL", "desenvolvedor.victorlopes@gmail.com")
LINKEDIN_PASSWORD = "#LargeSystem33"

PROFILE_DATA = {
    "headline": "Python | Desenvolvimento Web | Backend | Estudante ADS",
    "about": """Sou Victor Lopes, estudante de Análise e Desenvolvimento de Sistemas (ADS) na Universidade Estácio e em treinamento em Programação Python pelo Senac Bonsucesso.

Atuo no desenvolvimento de soluções web e sistemas com Python, Django e tecnologias relacionadas. Tenho interesse em backend, APIs, automação e integração de sistemas.

Minha trajetória é construída através de projetos práticos: já desenvolvi painéis de controle financeiro, sistemas de gestão empresarial e dashboards de operação, utilizando Django, Supabase e deploy em Vercel.

Busco oportunidades de estágio ou nível júnior onde eu possa contribuir com meu conhecimento em Python e desenvolvimento web, enquanto continuo aprendendo e crescendo na área de tecnologia.

🔗 GitHub: https://github.com/dev-victorlopes
🔗 Portfólio: https://victorlopes.dev (em breve)
📧 Contato: desenvolvedor.victorlopes@gmail.com""",
    "skills": [
        "Python", "Django", "Desenvolvimento Web", "HTML/CSS",
        "JavaScript", "Bancos de Dados", "Supabase", "APIs",
        "Automação", "Git/GitHub",
    ],
}


def log(msg, level="INFO"):
    print(f"[{time.strftime('%H:%M:%S')}] {level}: {msg}")


def create_driver():
    """Cria o WebDriver usando Chromium do Playwright."""
    options = Options()
    options.binary_location = CHROME_PATH
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    
    # Remover detecção de webdriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })
    
    return driver


def login_linkedin(driver):
    """Realiza login no LinkedIn."""
    log("🔑 Iniciando login no LinkedIn...")
    
    try:
        driver.get("https://www.linkedin.com/login")
        time.sleep(5)
        
        # Preencher email
        email_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_field.clear()
        email_field.send_keys(LINKEDIN_EMAIL)
        log(f"Email preenchido: {LINKEDIN_EMAIL}")
        time.sleep(2)
        
        # Clicar em "Próximo"
        next_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        next_button.click()
        log("Clicado em 'Próximo'")
        time.sleep(5)
        
        # Verificar se campo de senha apareceu
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
        except TimeoutException:
            log("Campo de senha não apareceu - possível erro de login", "ERROR")
            return False
        
        # Preencher senha
        password_field.clear()
        password_field.send_keys(LINKEDIN_PASSWORD)
        log("Senha preenchida")
        time.sleep(2)
        
        # Clicar em "Entrar"
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        log("Clicado em 'Entrar'")
        time.sleep(10)
        
        # Verificar se logou
        current_url = driver.current_url
        if "login" in current_url.lower():
            log(f"Falha no login - ainda na URL: {current_url}", "ERROR")
            return False
        
        log(f"✅ Login realizado! Redirecionado para: {current_url}")
        return True
        
    except Exception as e:
        log(f"Erro durante login: {e}", "ERROR")
        return False


def update_profile(driver):
    """Atualiza o perfil do LinkedIn."""
    log("📝 Iniciando atualização do perfil...")
    
    try:
        driver.get("https://www.linkedin.com/me")
        time.sleep(5)
        
        # Clicar em editar perfil
        try:
            edit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Editar perfil') or contains(text(), 'Edit profile')]"))
            )
            edit_button.click()
            time.sleep(3)
            log("Editor de perfil aberto")
        except Exception as e:
            log(f"Erro ao abrir editor: {e}", "WARN")
        
        # Atualizar headline
        try:
            headline_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Headline']"))
            )
            headline_field.clear()
            headline_field.send_keys(PROFILE_DATA["headline"])
            log("Headline preenchida")
            
            save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
            save_button.click()
            time.sleep(2)
            log("✅ Headline salva!")
        except Exception as e:
            log(f"Erro ao atualizar headline: {e}", "WARN")
        
        # Atualizar localização
        try:
            location_field = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Location']")
            location_field.clear()
            location_field.send_keys("Rio de Janeiro, Rio de Janeiro, Brasil")
            log("Localização preenchida")
            
            save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
            save_button.click()
            time.sleep(2)
            log("✅ Localização salva!")
        except Exception as e:
            log(f"Erro ao atualizar localização: {e}", "WARN")
        
        # Atualizar sobre
        try:
            about_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Sobre']"))
            )
            about_field.clear()
            about_field.send_keys(PROFILE_DATA["about"])
            log("Seção 'Sobre' preenchida")
            
            save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
            save_button.click()
            time.sleep(2)
            log("✅ 'Sobre' salvo!")
        except Exception as e:
            log(f"Erro ao atualizar 'Sobre': {e}", "WARN")
        
        log("✅ Atualização do perfil básico concluída!")
        return True
        
    except Exception as e:
        log(f"Erro ao atualizar perfil: {e}", "ERROR")
        return False


def add_skills(driver):
    """Adiciona habilidades ao perfil."""
    log("🛠 Adicionando habilidades...")
    
    try:
        driver.get("https://www.linkedin.com/in/me/edit/skills")
        time.sleep(5)
        
        for skill in PROFILE_DATA["skills"]:
            log(f"  Adicionando: {skill}")
            
            search_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search skills']"))
            )
            search_field.clear()
            search_field.send_keys(skill)
            time.sleep(1)
            
            # Selecionar sugestão
            try:
                suggestion = driver.find_element(By.CSS_SELECTOR, "div[aria-label*='skill']")
                suggestion.click()
                time.sleep(0.5)
            except Exception:
                pass
            
            time.sleep(0.5)
        
        save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
        save_button.click()
        time.sleep(3)
        log("✅ Habilidades salvas!")
        
        return True
        
    except Exception as e:
        log(f"Erro ao adicionar habilidades: {e}", "ERROR")
        return False


def main():
    log("=" * 60)
    log("🔗 AUTOMAÇÃO DE PERFIL LINKEDIN — Victor Lopes")
    log("=" * 60)
    log(f"📍 Email: {LINKEDIN_EMAIL}")
    log(f"📌 Headline: {PROFILE_DATA['headline']}")
    log(f"📍 Chrome binary: {CHROME_PATH}")
    log(f"📍 Chrome exists: {os.path.exists(CHROME_PATH)}")
    log("")
    
    if not os.path.exists(CHROME_PATH):
        log(f"❌ Chrome binary não encontrado em: {CHROME_PATH}", "ERROR")
        return 1
    
    driver = None
    try:
        driver = create_driver()
        
        # Login
        if not login_linkedin(driver):
            log("❌ Falha no login. Abortando.", "ERROR")
            return 1
        
        # Atualizar perfil
        update_profile(driver)
        
        # Adicionar skills
        add_skills(driver)
        
        log("=" * 60)
        log("✅ AUTOMAÇÃO CONCLUÍDA!")
        log("=" * 60)
        
        time.sleep(30)
        return 0
        
    except Exception as e:
        log(f"❌ Erro: {e}", "ERROR")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    sys.exit(main())
