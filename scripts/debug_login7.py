#!/usr/bin/env python3
"""Login com JavaScript puro para contornar problemas de visibilidade."""

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
    
    # Usar JavaScript para preencher os campos e clicar
    # Isso contorna problemas de visibilidade
    
    # Preencher email
    result = page.evaluate("""(email) => {
        const input = document.querySelector('input[type="email"]');
        if (input) {
            input.value = email;
            input.setAttribute('value', email);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            console.log('Email preenchido:', input.value);
            return true;
        }
        console.log('Email input não encontrado');
        return false;
    }""", "desenvolvedor.victorlopes@gmail.com")
    
    print(f"Email preenchido: {result}")
    time.sleep(2)
    
    # Clicar no botão "Entrar"
    result = page.evaluate("""() => {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
            if (btn.innerText === 'Entrar' && btn.type === 'button') {
                console.log('Botão Entrar encontrado:', btn);
                btn.click();
                console.log('Clique realizado!');
                return true;
            }
        }
        console.log('Botão Entrar não encontrado');
        return false;
    }""")
    
    print(f"Botão clicado: {result}")
    time.sleep(6)
    
    print(f'URL após clique: {page.url}')
    
    # Preencher senha se necessário
    password_result = page.evaluate("""(password) => {
        const input = document.querySelector('input[type="password"]');
        if (input) {
            input.value = password;
            input.setAttribute('value', password);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            console.log('Senha preenchida');
            return true;
        }
        console.log('Senha input não encontrado');
        return false;
    }""", "#LargeSystem33")
    
    if password_result:
        print("Senha preenchida")
        time.sleep(2)
        
        # Clicar em entrar novamente
        result = page.evaluate("""() => {
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.innerText === 'Entrar' && btn.type === 'button') {
                    console.log('Botão Entrar encontrado:', btn);
                    btn.click();
                    console.log('Clique realizado!');
                    return true;
                }
            }
            console.log('Botão Entrar não encontrado');
            return false;
        }""")
        
        print(f"Segundoclique: {result}")
        time.sleep(10)
    
    print(f'URL final: {page.url}')
    
    if "login" in page.url.lower():
        print("❌ Ainda na página de login")
    else:
        print(f"✅ Logado! Redirecionado para: {page.url}")
    
    browser.close()
