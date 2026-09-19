#!/usr/bin/env python3
"""
Gerador de Currículo PDF — Victor Lopes

Gera um currículo PDF ATS-friendly a partir dos dados do perfil.
ATS-friendly significa: formato simples, sem gráficos, hierarquia clara,
tipografia legível, linguagem objetiva.
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.platypus.flowables import HRFlowable


# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "curriculo_victor_lopes.pdf")


# Paleta de cores
PRIMARY = HexColor("#1d4ed8")      # Azul primário
DARK = HexColor("#1e293b")        # Texto principal
GRAY = HexColor("#64748b")        # Texto secundário
LIGHT_GRAY = HexColor("#f1f5f9")  # Fundo de seções
WHITE = HexColor("#ffffff")
BLACK = HexColor("#000000")


def create_styles():
    """Cria os estilos de texto para o PDF."""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        'ResumeName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=DARK,
        alignment=TA_LEFT,
        spaceAfter=2,
    ))
    
    styles.add(ParagraphStyle(
        'ResumeSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        textColor=GRAY,
        alignment=TA_LEFT,
        spaceAfter=2,
    ))
    
    styles.add(ParagraphStyle(
        'ResumeTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=PRIMARY,
        alignment=TA_LEFT,
        spaceAfter=6,
    ))
    
    styles.add(ParagraphStyle(
        'ResumeSection',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=PRIMARY,
        alignment=TA_LEFT,
        spaceBefore=10,
        spaceAfter=4,
    ))
    
    styles.add(ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=DARK,
        alignment=TA_LEFT,
        leading=14,
        spaceAfter=3,
    ))
    
    styles.add(ParagraphStyle(
        'ResumeBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=DARK,
        alignment=TA_LEFT,
        leading=14,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=2,
    ))
    
    styles.add(ParagraphStyle(
        'ResumeSmall',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=GRAY,
        alignment=TA_LEFT,
        spaceAfter=2,
    ))
    
    styles.add(ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=GRAY,
        alignment=TA_RIGHT,
        spaceAfter=1,
    ))
    
    return styles


def build_resume():
    """Constroi o documento PDF do currículo."""
    styles = create_styles()
    
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
    )
    
    story = []
    
    # ===== CABEÇALHO =====
    header_data = [
        [
            Paragraph("Victor Hugo Lopes da Silva", styles['ResumeName']),
            Paragraph("Rio de Janeiro/RJ, Brasil", styles['ResumeContact']),
        ],
        [
            Paragraph("Victor Lopes", styles['ResumeSubtitle']),
            Paragraph("+55 21 95922-3179", styles['ResumeContact']),
        ],
        [
            Paragraph("Desenvolvedor em Formação", styles['ResumeTitle']),
            Paragraph("[e-mail profissional]", styles['ResumeContact']),
        ],
        [
            Paragraph("Python | Backend | Web | Automação | Estágio", styles['ResumeSmall']),
            Paragraph("[LinkedIn] | [GitHub]", styles['ResumeContact']),
        ],
    ]
    
    header_table = Table(header_data, colWidths=[120*mm, 50*mm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY))
    story.append(Spacer(1, 8*mm))
    
    # ===== OBJETIVO =====
    story.append(Paragraph("OBJETIVO", styles['ResumeSection']))
    story.append(Paragraph(
        "Transição para a área de tecnologia, buscando oportunidades de estágio e "
        "nível júnior em desenvolvimento Python, backend, desenvolvimento web, APIs, "
        "automação e integração de sistemas.",
        styles['ResumeBody']
    ))
    
    # ===== FORMAÇÃO =====
    story.append(Paragraph("FORMAÇÃO", styles['ResumeSection']))
    
    formation_data = [
        [
            Paragraph("<b>Universidade Estácio</b>", styles['ResumeBody']),
            Paragraph("Aug 2026 — Atual", styles['ResumeSmall']),
        ],
        [
            Paragraph("Análise e Desenvolvimento de Sistemas (ADS) — Graduação", styles['ResumeSmall']),
            Paragraph("", styles['ResumeSmall']),
        ],
        [
            Paragraph("Em andamento", styles['ResumeSmall']),
            Paragraph("", styles['ResumeSmall']),
        ],
        [Spacer(1, 4*mm), Spacer(1, 4*mm)],
        [
            Paragraph("<b>Senac Bonsucesso</b>", styles['ResumeBody']),
            Paragraph("Em andamento", styles['ResumeSmall']),
        ],
        [
            Paragraph("Programação em Python — Formação Técnica", styles['ResumeSmall']),
            Paragraph("", styles['ResumeSmall']),
        ],
        [
            Paragraph("Previsão de conclusão: Outubro 2026", styles['ResumeSmall']),
            Paragraph("", styles['ResumeSmall']),
        ],
    ]
    
    formation_table = Table(formation_data, colWidths=[120*mm, 50*mm])
    formation_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 3), (-1, 3), 2),
    ]))
    story.append(formation_table)
    
    # ===== PROJETOS =====
    story.append(Paragraph("PROJETOS", styles['ResumeSection']))
    
    # Projeto 1
    story.append(Paragraph(
        "<b>Painel Ômega — Controle de Fluxo Financeiro</b>", styles['ResumeBody']
    ))
    story.append(Paragraph(
        "Painel web para controle de fluxo financeiro, com gestão de clientes, "
        "saídas, empréstimos, sugestões inteligentes de negociação e relatórios "
        "CSV/Excel. Inclui PWA e deploy em Vercel.",
        styles['ResumeBody']
    ))
    story.append(Paragraph(
        "<b>Tecnologias:</b> Django 5+, PostgreSQL (Supabase), PWA, WhiteNoise, Vercel",
        styles['ResumeBody']
    ))
    story.append(Paragraph("<b>Status:</b> Funcional", styles['ResumeSmall']))
    story.append(Spacer(1, 4*mm))
    
    # Projeto 2
    story.append(Paragraph(
        "<b>Sistema de Gestão Empresarial</b>", styles['ResumeBody']
    ))
    story.append(Paragraph(
        "MVP de sistema web para pequenos negócios, com gestão de estoque, "
        "fluxo de caixa, dashboard, exportação CSV/PDF e tema claro/escuro.",
        styles['ResumeBody']
    ))
    story.append(Paragraph(
        "<b>Tecnologias:</b> Django 6.1, PostgreSQL (Supabase), django-pwa, "
        "ReportLab, Vercel",
        styles['ResumeBody']
    ))
    story.append(Paragraph("<b>Status:</b> Funcional", styles['ResumeSmall']))
    story.append(Spacer(1, 4*mm))
    
    # Projeto 3
    story.append(Paragraph(
        "<b>Hermes Agency — Dashboard de Operação</b>", styles['ResumeBody']
    ))
    story.append(Paragraph(
        "Dashboard para gerenciamento de leads, pipeline, propostas e atividades "
        "de agência digital.",
        styles['ResumeBody']
    ))
    story.append(Paragraph(
        "<b>Tecnologias:</b> HTML, CSS, JavaScript, Supabase, Vercel",
        styles['ResumeBody']
    ))
    story.append(Paragraph("<b>Status:</b> Funcional (demo)", styles['ResumeSmall']))
    
    # ===== TECNOLOGIAS =====
    story.append(Paragraph("TECNOLOGIAS", styles['ResumeSection']))
    
    tech_data = [
        [
            Paragraph("<b>Linguagens</b>", styles['ResumeBody']),
            Paragraph("Python, JavaScript, HTML, CSS", styles['ResumeBody']),
        ],
        [
            Paragraph("<b>Frameworks/Ferramentas</b>", styles['ResumeBody']),
            Paragraph("Django, Supabase, Vercel, Git/GitHub", styles['ResumeBody']),
        ],
        [
            Paragraph("<b>Banco de Dados</b>", styles['ResumeBody']),
            Paragraph("PostgreSQL, SQL", styles['ResumeBody']),
        ],
        [
            Paragraph("<b>Conceitos</b>", styles['ResumeBody']),
            Paragraph(
                "Desenvolvimento Web, APIs, Automação, "
                "Integração de Sistemas, PWA",
                styles['ResumeBody']
            ),
        ],
    ]
    
    tech_table = Table(tech_data, colWidths=[50*mm, 120*mm])
    tech_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(tech_table)
    
    # ===== HABILIDADES COMPORTAMENTAIS =====
    story.append(Paragraph("HABILIDADES COMPORTAMENTAIS", styles['ResumeSection']))
    
    soft_skills = [
        "Aprendizado rápido",
        "Construção prática de projetos",
        "Resolução de problemas",
        "Interesse em automação e eficiência",
        "Trabalho autônomo",
    ]
    
    for skill in soft_skills:
        story.append(Paragraph(f"• {skill}", styles['ResumeBullet']))
    
    # ===== RODAPÉ =====
    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        f"Currículo gerado em {datetime.now().strftime('%d de %B de %Y')}. "
        "Dados baseados em: docs/profile-data.md",
        styles['ResumeSmall']
    ))
    
    # Build
    doc.build(story)
    print(f"✅ PDF gerado: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    output = build_resume()
