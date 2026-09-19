#!/usr/bin/env python3
"""Verificar estrutura completa da página de login."""

import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
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
    print(f'Título: {page.title()}')
    print()
    
    # Capturar HTML da página inteira
    html = page.content()
    print(f"Tamanho do HTML: {len(html)} caracteres")
    print()
    
    # Procurar por qualquer coisa relacionada a login/entrar
    print("=== Procurando botões de login ===")
    
    # Botões
    buttons = page.locator('button')
    btn_count = buttons.count()
    print(f"Total de botões: {btn_count}")
    
    for i in range(btn_count):
        btn = buttons.nth(i)
        try:
            text = btn.inner_text()[:50] if btn.inner_text() else 'N/A'
            html_content = btn.evaluate("el => el.outerHTML")[:200]
            print(f"  Button {i}: text='{text}'")
            print(f"    HTML: {html_content}")
        except Exception as e:
            print(f"  Button {i}: erro ({e})")
    
    print()
    print("=== Procurando elementos com 'submit' ===")
    submit_elements = page.locator('[type="submit"], [type="button"], button, input')
    count = submit_elements.count()
    print(f"Total: {count}")
    
    for i in range(count):
        elem = submit_elements.nth(i)
        try:
            elem_type = elem.get_attribute('type') or 'N/A'
            elem_name = elem.get_attribute('name') or 'N/A'
            elem_value = elem.get_attribute('value') or 'N/A'
            elem_text = elem.inner_text()[:30] if elem.inner_text() else 'N/A'
            print(f"  Element {i}: type={elem_type}, name={elem_name}, value={elem_value}, text={elem_text}")
        except Exception as e:
            print(f"  Element {i}: erro ({e})")
    
    print()
    print("=== Verificando forms ===")
    forms = page.locator('form')
    form_count = forms.count()
    print(f"Total de forms: {form_count}")
    
    for i in range(form_count):
        form = forms.nth(i)
        try:
            action = form.get_attribute('action') or 'N/A'
            method = form.get_attribute('method') or 'N/A'
            print(f"  Form {i}: action={action}, method={method}")
            
            inputs = form.locator('input')
            input_count = inputs.count()
            print(f"    Inputs: {input_count}")
            
            for j in range(input_count):
                input_elem = inputs.nth(j)
                input_type = input_elem.get_attribute('type') or 'N/A'
                input_name = input_elem.get_attribute('name') or 'N/A'
                input_id = input_elem.get_attribute('id') or 'N/A'
                print(f"      Input {j}: type={input_type}, name={input_name}, id={input_id}")
        except Exception as e:
            print(f"  Form {i}: erro ({e})")
    
    browser.close()
