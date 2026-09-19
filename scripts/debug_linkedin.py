#!/usr/bin/env python3
"""Debug script para investigar o login do LinkedIn."""

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
    time.sleep(5)
    
    print(f'URL: {page.url}')
    print(f'Título: {page.title()}')
    print()
    
    # Verificar todos os inputs
    inputs = page.locator('input')
    count = inputs.count()
    print(f'Total de inputs: {count}')
    
    for i in range(count):
        input_elem = inputs.nth(i)
        name = input_elem.get_attribute('name') or 'N/A'
        id_attr = input_elem.get_attribute('id') or 'N/A'
        placeholder = input_elem.get_attribute('placeholder') or 'N/A'
        aria_label = input_elem.get_attribute('aria-label') or 'N/A'
        input_type = input_elem.get_attribute('type') or 'N/A'
        print(f'  Input {i}: id={id_attr}, name={name}, type={input_type}, placeholder={placeholder[:30]}, aria-label={aria_label[:30]}')
    
    print()
    
    # Verificar botões
    buttons = page.locator('button')
    btn_count = buttons.count()
    print(f'Total de botões: {btn_count}')
    
    for i in range(min(btn_count, 10)):
        btn = buttons.nth(i)
        text = btn.inner_text()[:30] if btn.inner_text() else 'N/A'
        aria_label = btn.get_attribute('aria-label') or 'N/A'
        print(f'  Botão {i}: text="{text}", aria-label={aria_label[:30]}')
    
    # Capturar snapshot do HTML
    print()
    print("Estrutura HTML relevante (formulário):")
    form_html = page.locator('form').inner_html()[:2000] if page.locator('form').count() > 0 else "Nenhum form encontrado"
    print(form_html)
    
    browser.close()
