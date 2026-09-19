#!/usr/bin/env python3
"""Investigar posicionamento do botão."""

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
    
    # Obter mais detalhes sobre o botão
    button_details = page.evaluate("""() => {
        const buttons = document.querySelectorAll('button');
        const results = [];
        for (const btn of buttons) {
            if (btn.innerText === 'Entrar') {
                const rect = btn.getBoundingClientRect();
                const style = window.getComputedStyle(btn);
                results.push({
                    text: btn.innerText,
                    type: btn.type,
                    rect: {
                        x: rect.x,
                        y: rect.y,
                        width: rect.width,
                        height: rect.height,
                        top: rect.top,
                        left: rect.left,
                        right: rect.right,
                        bottom: rect.bottom
                    },
                    visible: rect.width > 0 && rect.height > 0,
                    opacity: style.opacity,
                    display: style.display,
                    visibility: style.visibility,
                    position: style.position,
                    offsetParent: btn.offsetParent ? 'has parent' : 'no parent'
                });
            }
        }
        return results;
    }""")
    
    print("Detalhes dos botões 'Entrar':")
    for i, details in enumerate(button_details):
        print(f"  Button {i}:")
        for key, value in details.items():
            print(f"    {key}: {value}")
    
    print()
    
    # Tentar com page.evaluate para fazer o clique via dispatchEvent
    result = page.evaluate("""() => {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
            if (btn.innerText === 'Entrar' && btn.type === 'button') {
                console.log('Encontrou botão Entrar:', btn);
                
                // Criar e dispatchar evento de mouse
                const mouseDown = new MouseEvent('mousedown', {
                    bubbles: true,
                    cancelable: true,
                    clientX: btn.getBoundingClientRect().left + btn.offsetWidth / 2,
                    clientY: btn.getBoundingClientRect().top + btn.offsetHeight / 2
                });
                const mouseUp = new MouseEvent('mouseup', {
                    bubbles: true,
                    cancelable: true,
                    clientX: btn.getBoundingClientRect().left + btn.offsetWidth / 2,
                    clientY: btn.getBoundingClientRect().top + btn.offsetHeight / 2
                });
                const click = new MouseEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    clientX: btn.getBoundingClientRect().left + btn.offsetWidth / 2,
                    clientY: btn.getBoundingClientRect().top + btn.offsetHeight / 2
                });
                
                btn.dispatchEvent(mouseDown);
                btn.dispatchEvent(mouseUp);
                btn.dispatchEvent(click);
                
                console.log('Eventos de clique dispatchados');
                return true;
            }
        }
        console.log('Botão Entrar não encontrado');
        return false;
    }""")
    
    print(f"Resultado do clique via dispatchEvent: {result}")
    time.sleep(6)
    
    print(f'URL após clique: {page.url}')
    
    browser.close()
