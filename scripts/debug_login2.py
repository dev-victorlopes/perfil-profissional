#!/usr/bin/env python3
"""Debug detalhado do login LinkedIn."""

import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1920, 'height': 1080}
    )
    page = context.new_page()
    
    # Navegar para o login
    page.goto('https://www.linkedin.com/login', timeout=60000, wait_until='domcontentloaded')
    time.sleep(4)
    
    print(f'URL inicial: {page.url}')
    
    # Preencher email via JS
    page.evaluate("""(email) => {
        const input = document.querySelector('input[type="email"]');
        if (input) {
            console.log('Email input encontrado:', input);
            input.value = email;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            console.log('Email preenchido:', input.value);
        }
        return true;
    }""", "desenvolvedor.victorlopes@gmail.com")
    
    print("Email preenchido")
    time.sleep(1)
    
    # Capturar estado antes de clicar
    print(f'URL antes de clicar: {page.url}')
    
    # Clicar em entrar
    result = page.evaluate("""() => {
        const button = document.querySelector('button[type="submit"]');
        console.log('Botão encontrado:', button);
        if (button) {
            button.click();
            console.log('Botão clicado');
        }
        return true;
    }""")
    
    print(f"Resultado do clique: {result}")
    time.sleep(6)
    
    print(f'URL após clique: {page.url}')
    
    # Verificar se há campos de senha
    password_input = page.locator("input[type='password']")
    print(f"Campo de senha existe: {password_input.count() > 0}")
    
    if password_input.count() > 0:
        # Preencher senha
        page.evaluate("""(password) => {
            const input = document.querySelector('input[type="password"]');
            if (input) {
                console.log('Senha input encontrado:', input);
                input.value = password;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                console.log('Senha preenchida');
            }
            return true;
        }""", "test123")
        
        print("Senha preenchida")
        time.sleep(1)
        
        # Clicar em entrar novamente
        result2 = page.evaluate("""() => {
            const button = document.querySelector('button[type="submit"]');
            console.log('Botão entrar encontrado:', button);
            if (button) {
                button.click();
                console.log('Botão entrar clicado');
            }
            return true;
        }""")
        
        print(f"Resultado do segundo clique: {result2}")
        time.sleep(8)
        
        print(f'URL final: {page.url}')
        
        # Verificar se logou
        if "login" in page.url.lower():
            print("❌ Ainda na página de login")
        else:
            print(f"✅ Logado! URL: {page.url}")
    
    browser.close()
