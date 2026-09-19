#!/usr/bin/env python3
"""Verificar se há bloqueio/CAPTCHA."""

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
    page.evaluate("""(email) => {
        const input = document.querySelector('input[type="email"]');
        if (input) {
            input.value = email;
            input.setAttribute('value', email);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""", "desenvolvedor.victorlopes@gmail.com")
    time.sleep(2)
    
    # Verificar se há CAPTCHA antes de clicar
    captcha_before = page.evaluate("""() => {
        const captcha = document.querySelector('iframe[src*="captcha"]');
        const challenge = document.querySelector('.captcha-container, [data-test="captcha"]');
        const g_recaptcha = document.querySelector('.g-recaptcha');
        return {
            iframe_captcha: !!captcha,
            captcha_container: !!challenge,
            g_recaptcha: !!g_recaptcha,
            title: document.title
        };
    }""")
    print(f"Estado antes do clique: {captcha_before}")
    
    # Clicar no botão "Entrar"
    result = page.evaluate("""() => {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
            if (btn.innerText === 'Entrar' && btn.type === 'button') {
                const rect = btn.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0 && btn.offsetParent) {
                    const mouseDown = new MouseEvent('mousedown', {
                        bubbles: true, cancelable: true,
                        clientX: rect.left + rect.width / 2,
                        clientY: rect.top + rect.height / 2
                    });
                    const mouseUp = new MouseEvent('mouseup', {
                        bubbles: true, cancelable: true,
                        clientX: rect.left + rect.width / 2,
                        clientY: rect.top + rect.height / 2
                    });
                    const click = new MouseEvent('click', {
                        bubbles: true, cancelable: true,
                        clientX: rect.left + rect.width / 2,
                        clientY: rect.top + rect.height / 2
                    });
                    btn.dispatchEvent(mouseDown);
                    btn.dispatchEvent(mouseUp);
                    btn.dispatchEvent(click);
                    console.log('Clique no botão Entrar realizado!');
                    return true;
                }
            }
        }
        console.log('Botão Entrar visível não encontrado');
        return false;
    }""")
    print(f"Clique realizado: {result}")
    time.sleep(8)
    
    # Verificar estado após clique
    print(f'URL após clique: {page.url}')
    print(f'Título: {page.title()}')
    
    captcha_after = page.evaluate("""() => {
        const captcha = document.querySelector('iframe[src*="captcha"]');
        const challenge = document.querySelector('.captcha-container, [data-test="captcha"]');
        const g_recaptcha = document.querySelector('.g-recaptcha');
        const error_msg = document.querySelector('.error-message, .auth-error, [data-test="error"]');
        return {
            iframe_captcha: !!captcha,
            captcha_container: !!challenge,
            g_recaptcha: !!g_recaptcha,
            error_message: error_msg ? error_msg.innerText : null,
            title: document.title
        };
    }""")
    print(f"Estado após clique: {captcha_after}")
    
    # Verificar se há alguma mensagem de erro na página
    error_content = page.evaluate("""() => {
        const errors = document.querySelectorAll('.error, .auth-error, [data-test="error-message"], .alert');
        return Array.from(errors).map(e => e.innerText).filter(t => t);
    }""")
    print(f"Mensagens de erro: {error_content}")
    
    browser.close()
