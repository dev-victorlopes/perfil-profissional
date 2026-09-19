#!/usr/bin/env python3
"""Tentativa de login com verificação de console e estratégias alternativas."""

import time
import json
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
    
    # Capturar console messages
    console_messages = []
    page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
    
    # Navegar para o login
    page.goto('https://www.linkedin.com/login', timeout=60000, wait_until='domcontentloaded')
    time.sleep(5)
    
    print(f'URL: {page.url}')
    
    # Preencher email
    page.evaluate("""(email) => {
        const input = document.querySelector('input[type="email"]');
        if (input) {
            input.focus();
            input.value = email;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.dispatchEvent(new Event('blur', { bubbles: true }));
            input.focus();
        }
        return true;
    }""", "desenvolvedor.victorlopes@gmail.com")
    
    time.sleep(2)
    
    # Tentar submeter o formulário diretamente
    print("Tentando submeter formulário...")
    result = page.evaluate("""() => {
        const form = document.querySelector('form');
        if (form) {
            console.log('Formulário encontrado:', form);
            form.submit();
            return true;
        }
        return false;
    }""")
    print(f"Submit do form: {result}")
    time.sleep(5)
    
    print(f'URL após submit: {page.url}')
    
    # Se não mudou, tentar clicar no botão
    if "login" in page.url.lower():
        print("Tentando clicar no botão...")
        
        # Tentar várias estratégias de clique
        strategies = [
            "button[type='submit']",
            "button:has-text('Entrar')",
            "input[type='submit']",
            "[data-test='join-form__submit-button']",
        ]
        
        for selector in strategies:
            try:
                button = page.locator(selector)
                if button.count() > 0:
                    print(f"Tentando: {selector}")
                    
                    # Forçar visibilidade
                    page.evaluate(f"""() => {{
                        const el = document.querySelector('{selector}');
                        if (el) {{
                            el.style.display = 'block';
                            el.style.visibility = 'visible';
                            el.style.opacity = '1';
                        }}
                    }}""")
                    
                    # Usar force: true
                    button.click(force=True)
                    print(f"Clique feito com force=True")
                    break
            except Exception as e:
                print(f"Falha com {selector}: {e}")
        
        time.sleep(6)
        print(f'URL após cliques: {page.url}')
    
    # Ver console messages
    if console_messages:
        print("\n=== Console Messages ===")
        for msg in console_messages[-10:]:
            print(msg)
    
    browser.close()
