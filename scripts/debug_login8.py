#!/usr/bin/env python3
"""Login usando tecla Enter para submeter."""

import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
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
    
    # Preencher email e pressionar Enter
    email_result = page.evaluate("""(email) => {
        const input = document.querySelector('input[type="email"]');
        if (input) {
            input.value = email;
            input.setAttribute('value', email);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            console.log('Email preenchido');
            
            // Simular pressionar Enter
            input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', bubbles: true }));
            input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', bubbles: true }));
            console.log('Enter pressionado no email');
            return true;
        }
        return false;
    }""", "desenvolvedor.victorlopes@gmail.com")
    
    print(f"Email + Enter: {email_result}")
    time.sleep(6)
    
    print(f'URL após email+Enter: {page.url}')
    
    # Preencher senha e pressionar Enter
    password_result = page.evaluate("""(password) => {
        const input = document.querySelector('input[type="password"]');
        if (input) {
            input.value = password;
            input.setAttribute('value', password);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            console.log('Senha preenchida');
            
            // Simular pressionar Enter
            input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', bubbles: true }));
            input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', bubbles: true }));
            console.log('Enter pressionado na senha');
            return true;
        }
        return false;
    }""", "#LargeSystem33")
    
    print(f"Senha + Enter: {password_result}")
    time.sleep(10)
    
    print(f'URL final: {page.url}')
    
    if "login" in page.url.lower():
        print("❌ Ainda na página de login")
    else:
        print(f"✅ Logado! Redirecionado para: {page.url}")
    
    browser.close()
