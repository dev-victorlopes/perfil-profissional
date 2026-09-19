#!/usr/bin/env python3
"""Tentativa de login com corrigido."""

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
    time.sleep(5)
    
    print(f'URL: {page.url}')
    
    # Preencher email
    email = "desenvolvedor.victorlopes@gmail.com"
    page.evaluate(f"""() => {{
        const input = document.querySelector('input[type="email"]');
        if (input) {{
            input.focus();
            input.value = "{email}";
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            input.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            input.focus();
        }}
        return true;
    }}""")
    
    time.sleep(2)
    print("Email preenchido")
    
    # Tentar clicar no botão usando page.evaluate com função pré-definida
    print("Tentando clicar no botão...")
    
    # Usar page.evaluate com uma função simples que não injeta strings
    clicked = page.evaluate("""() => {
        const buttons = document.querySelectorAll('button[type="submit"]');
        console.log('Botões encontrados:', buttons.length);
        for (const btn of buttons) {
            console.log('Botão:', btn);
            if (btn && btn.offsetParent !== null) {
                btn.click();
                console.log('Clique realizado');
                return true;
            }
        }
        return false;
    }""")
    
    print(f"Clique realizado: {clicked}")
    time.sleep(6)
    
    print(f'URL após clique: {page.url}')
    
    # Se não mudou, verificar o que aconteceu
    if "login" in page.url.lower():
        print("❌ Ainda na página de login")
        
        # Capturar HTML do botão
        html = page.evaluate("""() => {
            const btn = document.querySelector('button[type="submit"]');
            return btn ? btn.outerHTML : 'Nenhum botão encontrado';
        }""")
        print(f"HTML do botão: {html[:500]}")
    
    browser.close()
