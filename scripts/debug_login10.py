#!/usr/bin/env python3
"""Login usando coordenadas do mouse para clicar."""

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
    
    # Preencher email via evaluate
    page.evaluate("""(email) => {
        const input = document.querySelector('input[type="email"]');
        if (input) {
            input.value = email;
            input.setAttribute('value', email);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""", "desenvolvedor.victorlopes@gmail.com")
    print("Email preenchido")
    time.sleep(2)
    
    # Obter posição do botão "Entrar"
    button_info = page.evaluate("""() => {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
            if (btn.innerText === 'Entrar' && btn.type === 'button') {
                const rect = btn.getBoundingClientRect();
                return {
                    found: true,
                    x: rect.x + rect.width / 2,
                    y: rect.y + rect.height / 2,
                    text: btn.innerText
                };
            }
        }
        return { found: false };
    }""")
    
    print(f"Botão info: {button_info}")
    
    if button_info.get('found'):
        # Clicar usando coordenadas do mouse
        page.mouse.click(button_info['x'], button_info['y'])
        print(f"Clique no botão 'Entrar' em ({button_info['x']}, {button_info['y']})")
    else:
        print("Botão 'Entrar' não encontrado")
        browser.close()
        exit(1)
    
    time.sleep(6)
    print(f'URL após clique: {page.url}')
    
    # Preencher senha se necessário
    password_input = page.locator("input[type='password']")
    if password_input.count() > 0:
        page.evaluate("""(password) => {
            const input = document.querySelector('input[type="password"]');
            if (input) {
                input.value = password;
                input.setAttribute('value', password);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""", "#LargeSystem33")
        print("Senha preenchida")
        time.sleep(2)
        
        # Obter posição do botão "Entrar" novamente
        button_info2 = page.evaluate("""() => {
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.innerText === 'Entrar' && btn.type === 'button') {
                    const rect = btn.getBoundingClientRect();
                    return {
                        found: true,
                        x: rect.x + rect.width / 2,
                        y: rect.y + rect.height / 2,
                        text: btn.innerText
                    };
                }
            }
            return { found: false };
        }""")
        
        if button_info2.get('found'):
            page.mouse.click(button_info2['x'], button_info2['y'])
            print(f"Clique no botão 'Entrar' em ({button_info2['x']}, {button_info2['y']})")
        else:
            print("Botão 'Entrar' não encontrado na segunda etapa")
        
        time.sleep(10)
    
    print(f'URL final: {page.url}')
    
    if "login" in page.url.lower():
        print("❌ Ainda na página de login")
    else:
        print(f"✅ Logado! Redirecionado para: {page.url}")
    
    browser.close()
