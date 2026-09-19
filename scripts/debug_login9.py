#!/usr/bin/env python3
"""Login simplificado com fallback robusto."""

import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,  # Non-headless para evitar detecção
        args=["--disable-blink-features=AutomationControlled", "--window-size=1920,1080"]
    )
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1920, 'height': 1080},
        locale='pt-BR'
    )
    page = context.new_page()
    
    # Navegar para o login
    page.goto('https://www.linkedin.com/login', timeout=60000, wait_until='domcontentloaded')
    time.sleep(6)
    
    print(f'URL: {page.url}')
    
    # Preencher email com type() forçado
    email_input = page.locator("input[type='email']").first
    
    if email_input.count() > 0:
        # Forçar input para frente do viewport
        page.evaluate("""() => {
            const input = document.querySelector('input[type="email"]');
            if (input) {
                input.scrollIntoView({ block: 'center', inline: 'center' });
                input.style.position = 'fixed';
                input.style.top = '50%';
                input.style.left = '50%';
                input.style.zIndex = '9999';
                input.focus();
            }
        }""")
        time.sleep(1)
        
        # Usar type com force
        try:
            email_input.type("desenvolvedor.victorlopes@gmail.com", force=True)
            print("Email digitado com type()")
        except Exception as e:
            print(f"Erro no type do email: {e}")
            # Fallback para evaluate
            page.evaluate("""(email) => {
                const input = document.querySelector('input[type="email"]');
                if (input) {
                    input.value = email;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }""", "desenvolvedor.victorlopes@gmail.com")
            print("Email preenchido via evaluate")
        
        time.sleep(2)
        
        # Pressionar Enter
        page.keyboard.press("Enter")
        print("Enter pressionado no email")
        time.sleep(6)
    
    print(f'URL após email: {page.url}')
    
    # Preencher senha
    password_input = page.locator("input[type='password']").first
    
    if password_input.count() > 0:
        # Forçar input para frente do viewport
        page.evaluate("""() => {
            const input = document.querySelector('input[type="password"]');
            if (input) {
                input.scrollIntoView({ block: 'center', inline: 'center' });
                input.style.position = 'fixed';
                input.style.top = '50%';
                input.style.left = '50%';
                input.style.zIndex = '9999';
                input.focus();
            }
        }""")
        time.sleep(1)
        
        try:
            password_input.type("#LargeSystem33", force=True)
            print("Senha digitada com type()")
        except Exception as e:
            print(f"Erro no type da senha: {e}")
            page.evaluate("""(password) => {
                const input = document.querySelector('input[type="password"]');
                if (input) {
                    input.value = password;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }""", "#LargeSystem33")
            print("Senha preenchida via evaluate")
        
        time.sleep(2)
        
        # Pressionar Enter
        page.keyboard.press("Enter")
        print("Enter pressionado na senha")
        time.sleep(10)
    
    print(f'URL final: {page.url}')
    
    if "login" in page.url.lower():
        print("❌ Ainda na página de login")
    else:
        print(f"✅ Logado! Redirecionado para: {page.url}")
    
    # Manter aberto por 10 segundos para inspeção
    time.sleep(10)
    browser.close()
