import os
import re
import unicodedata
import pandas as pd
import html
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

def normalize_filename(text):
    text = str(text)
    nfkd_form = unicodedata.normalize('NFKD', text)
    text = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    text = text.lower().strip()
    text = re.sub(r'\s+', '_', text)
    text = re.sub(r'[^\w]', '', text)
    return text

def normalize_local(text):
    text = str(text).strip()
    
    # Remove aspas (duplas ou simples) de qualquer lugar do texto
    text = text.replace('"', '').replace("'", "")
    
    # Remove caracteres estranhos do início e do final da string (como '<', '>', '-', '.')
    # Mantém apenas letras e números no início e no fim.
    text = re.sub(r'^[^a-zA-Z0-9À-ÿ]+', '', text)
    text = re.sub(r'[^a-zA-Z0-9À-ÿ]+$', '', text)
    
    # Substitui múltiplos espaços por um só
    text = " ".join(text.split())
    
    if text:
        # Coloca a primeira letra em maiúsculo (preservando o resto)
        text = text[0].upper() + text[1:]
    return text

def draw_certificate(c, tipo, dados, bg_image_path):
    width, height = A4
    margin = 60
    
    # 1. Logo at the top
    logo_width = 250
    logo_height = 120 
    logo_x = (width - logo_width) / 2
    logo_y = height - 160
    if os.path.exists(bg_image_path):
        c.drawImage(bg_image_path, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True, anchor='s')

    # 2. Header
    c.setFont("Helvetica", 9)
    header_text = [
        "UNIVERSIDADE FEDERAL DO PARANÁ",
        "Rua XV de Novembro, 1299,  - Bairro Centro, Curitiba/PR, CEP 80060-000",
        "Telefone: (41) 3360-5000  - ufpr.br"
    ]
    current_y = logo_y - 15
    for line in header_text:
        c.drawCentredString(width/2, current_y, line)
        current_y -= 12
    
    # 3. Title "CERTIFICADO"
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, logo_y - 70, "CERTIFICADO")
    
    # 4. Body Text
    if tipo == 'aluno':
        html_text = f"Certificamos que a estudante <b>{dados['nome_estudante']}</b>, registrada sob o nº de matrícula <b>{dados['matricula_estudante']}</b>, desenvolveu <b>{str(dados['horas_semanais']).zfill(2)}</b> horas semanais de atividades no <b>{dados['programa']}</b>, no período de <b>{dados['data_inicio']}</b> a <b>{dados['data_fim']}</b>, totalizando <b>{dados['horas_totais']}</b> horas, no <b>{dados['projeto']}</b>, sob a orientação da Professora <b>{dados['nome_orientador']}</b>, registrada sob o nº de matrícula <b>{dados['matricula_orientador']}</b>."
    else:
        html_text = f"Certificamos que a Professora <b>{dados['nome_orientador']}</b>, registrada sob o nº de matrícula <b>{dados['matricula_orientador']}</b> orientou, no <b>{dados['programa']}</b>, a estudante <b>{dados['nome_estudante']}</b>, registrada sob o nº de matrícula <b>{dados['matricula_estudante']}</b>, no período de <b>{dados['data_inicio']}</b> a <b>{dados['data_fim']}</b>, no <b>{dados['projeto']}</b>, com carga horária semanal de <b>{str(dados['horas_semanais']).zfill(2)}</b> horas, totalizando <b>{dados['horas_totais']}</b> horas."
        
    style_body = ParagraphStyle(name='Body', fontName='Helvetica', fontSize=12, leading=18, alignment=TA_JUSTIFY)
    p = Paragraph(html_text, style_body)
    
    p_w, p_h = p.wrap(width - 2*margin, height)
    # Adjust Y space since Processo is removed
    body_y = logo_y - 120 - p_h
    p.drawOn(c, margin, body_y)
    
    # 5. Date
    c.setFont("Helvetica", 12)
    c.drawRightString(width - margin, body_y - 50, "Curitiba, 25 de junho de 2026.")
    
    # 6. Signature Block
    sig_y = body_y - 130
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, sig_y, "MARIA STAEL BITTENCOURT MADUREIRA")
    c.setFont("Helvetica", 11)
    c.drawCentredString(width/2, sig_y - 15, "COORDENADORA DE APOIO A PROJETOS, PROGRAMAS E ESTÁGIOS - COAPPE")
    c.drawCentredString(width/2, sig_y - 30, "PRÓ - REITORIA DE GRADUAÇÃO E ENSINO PROFISSIONAL – PROGRAP")

def main():
    base_dir = r"c:\Users\bruno\OneDrive - ufpr.br\estágio\Coappe\Criação de certificados"
    csv_input = os.path.join(base_dir, "Relatório PVA.csv")
    bg_image = os.path.join(base_dir, "ufpr_25.jpg")
    output_dir = os.path.join(base_dir, "certificados_gerados")
    csv_skipped = os.path.join(base_dir, "linhas_sem_local.csv")
    
    if not os.path.exists(csv_input):
        print(f"Erro: CSV não encontrado em {csv_input}")
        return
        
    os.makedirs(output_dir, exist_ok=True)
    
    print("Lendo dados do CSV...")
    try:
        df = pd.read_csv(csv_input, sep=';', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_input, sep=';', encoding='latin1')
    
    linhas_invalidas = []
    
    total = len(df)
    gerados = 0
    
    for index, row in df.iterrows():
        local = str(row.get('Local de atividades', '')).strip()
        
        # Filtro: Se local for vazio ou '-', separar e não gerar
        if not local or local == '-':
            linhas_invalidas.append(row)
            continue
            
        local_norm = normalize_local(local)
        
        # Dados para preencher no texto com escape de HTML (evita erros com '<' e '>')
        dados = {
            'nome_estudante': html.escape(str(row.get('Discente', '')).strip()),
            'matricula_estudante': html.escape(str(row.get('GRR', '')).strip()),
            'nome_orientador': html.escape(str(row.get('Nome docente', '')).strip()),
            'matricula_orientador': html.escape(str(row.get('Matrícula SIAD docente', '')).strip()),
            'programa': html.escape(str(row.get('Tipo', 'PROGRAMA DE VOLUNTARIADO ACADÊMICO')).strip()),
            'data_inicio': html.escape(str(row.get('Início', '')).strip()),
            'data_fim': html.escape(str(row.get('Fim', '')).strip()),
            'horas_semanais': html.escape(str(row.get('Carga Horaria Semanal', '')).strip()),
            'horas_totais': html.escape(str(row.get('Carga Horaria Total', '')).strip()),
            'projeto': html.escape(local_norm)
        }
        
        # Gerar certificado ALUNO
        if dados['nome_estudante'] and dados['nome_estudante'] != '-':
            filename_aluno = f"certificado_aluno_{normalize_filename(dados['nome_estudante'])}.pdf"
            filepath_aluno = os.path.join(output_dir, filename_aluno)
            c_aluno = canvas.Canvas(filepath_aluno, pagesize=A4)
            draw_certificate(c_aluno, 'aluno', dados, bg_image)
            c_aluno.showPage()
            c_aluno.save()
            gerados += 1
            
        # Gerar certificado PROFESSOR
        if dados['nome_orientador'] and dados['nome_orientador'] != '-' and dados['matricula_orientador'] != '0':
            # Para evitar sobrepor PDFs do mesmo professor (já que ele pode orientar vários alunos),
            # incluimos o nome do aluno no nome do arquivo do professor
            filename_prof = f"certificado_professor_{normalize_filename(dados['nome_orientador'])}_orientando_{normalize_filename(dados['nome_estudante'])}.pdf"
            filepath_prof = os.path.join(output_dir, filename_prof)
            c_prof = canvas.Canvas(filepath_prof, pagesize=A4)
            draw_certificate(c_prof, 'professor', dados, bg_image)
            c_prof.showPage()
            c_prof.save()
            gerados += 1
            
        # Print progress for large files
        if index % 500 == 0:
            print(f"Processando linha {index}/{total}...")
            
    # Salvar as linhas que não tinham local
    if linhas_invalidas:
        df_invalidas = pd.DataFrame(linhas_invalidas)
        df_invalidas.to_csv(csv_skipped, sep=';', index=False, encoding='utf-8-sig')
        print(f"\nATENÇÃO: {len(linhas_invalidas)} linhas foram ignoradas por não terem 'Local de atividades'.")
        print(f"Elas foram salvas no arquivo: {csv_skipped}")
        
    print(f"\nConcluído com sucesso! {gerados} certificados foram gerados em 'certificados_gerados'.")

if __name__ == '__main__':
    main()
