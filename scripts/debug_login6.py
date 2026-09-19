#!/usr/bin/env python3
"""Tentativa de login corrigida - botão type="button"."""

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
    
    # Preencher email
    email = "desenvolvedor.victorlopes@gmail.com"
    email_input = page.locator("input[type='email']").first
    if email_input.count() > 0:
        email_input.fill(email)
        print(f"Email preenchido: {email}")
    else:
        print("Email input não encontrado")
        browser.close()
        exit(1)
    
    time.sleep(2)
    
    # Clicar no botão "Entrar" (type="button", não type="submit")
    print("Clicando no botão 'Entrar'...")
    
    # O botão de "Entrar" é type="button", não type="submit"
    # Usar o first button que tem text "Entrar"
    enter_button = page.locator("button:has-text('Entrar')").first
    
    if enter_button.count() > 0:
        # Clicar com force
        enter_button.click(force=True)
        print("Botão 'Entrar' clicado!")
    else:
        print("Botão 'Entrar' não encontrado")
        browser.close()
        exit(1)
    
    time.sleep(6)
    print(f'URL após clique: {page.url}')
    
    # Se redirecionou para o campo de senha
    password_input = page.locator("input[type='password']")
    if password_input.count() > 0:
        print("Campo de senha encontrado")
        
        # Preencher senha
        password_input.fill("#LargeSystem33")
        print("Senha preenchida")
        
        time.sleep(2)
        
        # Clicar em entrar novamente
        enter_button2 = page.locator("button:has-text('Entrar')").first
        if enter_button2.count() > 0:
            enter_button2.click(force=True)
            print("Botão 'Entrar' clicado novamente!")
        
        time.sleep(10)
        print(f'URL final: {page.url}')
        
        if "login" in page.url.lower():
            print("❌ Ainda na página de login")
        else:
            print(f"✅ Logado! Redirecionado para: {page.url}")
    else:
        print("Campo de senha não encontrado")
    
    browser.close()
