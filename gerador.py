import os
import re
import unicodedata
import pandas as pd
import html

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties, MasterPage, PageLayout, PageLayoutProperties
from odf.text import P, Span
from odf.draw import Frame, Image

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
    text = text.replace('"', '').replace("'", "")
    text = re.sub(r'^[^a-zA-Z0-9À-ÿ]+', '', text)
    text = re.sub(r'[^a-zA-Z0-9À-ÿ]+$', '', text)
    text = " ".join(text.split())
    if text:
        text = text[0].upper() + text[1:]
    return text

def draw_certificate(doc, tipo, dados, bg_image_path):
    # Setup page layout (A4)
    pl = PageLayout(name="A4")
    pl.addElement(PageLayoutProperties(pagewidth="21cm", pageheight="29.7cm", margin="2cm"))
    doc.automaticstyles.addElement(pl)
    mp = MasterPage(name="Standard", pagelayoutname=pl)
    doc.masterstyles.addElement(mp)
    
    # Styles
    center_para = Style(name="Center", family="paragraph")
    center_para.addElement(ParagraphProperties(textalign="center"))
    doc.styles.addElement(center_para)
    
    right_para = Style(name="Right", family="paragraph")
    right_para.addElement(ParagraphProperties(textalign="end"))
    doc.styles.addElement(right_para)

    justify_para = Style(name="Justify", family="paragraph")
    justify_para.addElement(ParagraphProperties(textalign="justify", lineheight="150%"))
    doc.styles.addElement(justify_para)
    
    bold_text = Style(name="Bold", family="text")
    bold_text.addElement(TextProperties(fontweight="bold"))
    doc.styles.addElement(bold_text)
    
    title_text = Style(name="TitleText", family="text")
    title_text.addElement(TextProperties(fontsize="16pt", fontweight="bold"))
    doc.styles.addElement(title_text)

    header_text_style = Style(name="HeaderText", family="text")
    header_text_style.addElement(TextProperties(fontsize="9pt"))
    doc.styles.addElement(header_text_style)

    body_text_style = Style(name="BodyText", family="text")
    body_text_style.addElement(TextProperties(fontsize="12pt"))
    doc.styles.addElement(body_text_style)

    # 1. Logo at the top
    if os.path.exists(bg_image_path):
        photo = doc.addPicture(bg_image_path)
        p_img = P(stylename=center_para)
        df = Frame(width="8.8cm", height="4.2cm") 
        df.addElement(Image(href=photo))
        p_img.addElement(df)
        doc.text.addElement(p_img)

    # 2. Header
    header_text = [
        "UNIVERSIDADE FEDERAL DO PARANÁ",
        "Rua XV de Novembro, 1299,  - Bairro Centro, Curitiba/PR, CEP 80060-000",
        "Telefone: (41) 3360-5000  - ufpr.br"
    ]
    for line in header_text:
        p = P(stylename=center_para)
        p.addElement(Span(stylename=header_text_style, text=line))
        doc.text.addElement(p)
    
    # Spacing
    doc.text.addElement(P())
    doc.text.addElement(P())

    # 3. Title "CERTIFICADO"
    p_title = P(stylename=center_para)
    p_title.addElement(Span(stylename=title_text, text="CERTIFICADO"))
    doc.text.addElement(p_title)
    
    # Spacing
    doc.text.addElement(P())
    doc.text.addElement(P())

    # 4. Body Text
    if tipo == 'aluno':
        html_text = f"Certificamos que a estudante <b>{dados['nome_estudante']}</b>, registrada sob o nº de matrícula <b>{dados['matricula_estudante']}</b>, desenvolveu <b>{str(dados['horas_semanais']).zfill(2)}</b> horas semanais de atividades no <b>{dados['programa']}</b>, no período de <b>{dados['data_inicio']}</b> a <b>{dados['data_fim']}</b>, totalizando <b>{dados['horas_totais']}</b> horas, no <b>{dados['projeto']}</b>, sob a orientação da Professora <b>{dados['nome_orientador']}</b>, registrada sob o nº de matrícula <b>{dados['matricula_orientador']}</b>."
    else:
        html_text = f"Certificamos que a Professora <b>{dados['nome_orientador']}</b>, registrada sob o nº de matrícula <b>{dados['matricula_orientador']}</b> orientou, no <b>{dados['programa']}</b>, a estudante <b>{dados['nome_estudante']}</b>, registrada sob o nº de matrícula <b>{dados['matricula_estudante']}</b>, no período de <b>{dados['data_inicio']}</b> a <b>{dados['data_fim']}</b>, no <b>{dados['projeto']}</b>, com carga horária semanal de <b>{str(dados['horas_semanais']).zfill(2)}</b> horas, totalizando <b>{dados['horas_totais']}</b> horas."
        
    p_body = P(stylename=justify_para)
    parts = re.split(r'(<b>|</b>)', html_text)
    is_bold = False
    for part in parts:
        if part == '<b>':
            is_bold = True
        elif part == '</b>':
            is_bold = False
        elif part:
            if is_bold:
                p_body.addElement(Span(stylename=bold_text, text=part))
            else:
                p_body.addElement(Span(stylename=body_text_style, text=part))
                
    doc.text.addElement(p_body)
    
    # Spacing
    for _ in range(4):
        doc.text.addElement(P())
    
    # 5. Date
    p_date = P(stylename=right_para)
    p_date.addElement(Span(stylename=body_text_style, text="Curitiba, 25 de junho de 2026."))
    doc.text.addElement(p_date)
    
    # Spacing
    for _ in range(4):
        doc.text.addElement(P())

    # 6. Signature Block
    p_sig1 = P(stylename=center_para)
    p_sig1.addElement(Span(stylename=bold_text, text="MARIA STAEL BITTENCOURT MADUREIRA"))
    doc.text.addElement(p_sig1)
    
    p_sig2 = P(stylename=center_para)
    p_sig2.addElement(Span(stylename=body_text_style, text="COORDENADORA DE APOIO A PROJETOS, PROGRAMAS E ESTÁGIOS - COAPPE"))
    doc.text.addElement(p_sig2)
    
    p_sig3 = P(stylename=center_para)
    p_sig3.addElement(Span(stylename=body_text_style, text="PRÓ - REITORIA DE GRADUAÇÃO E ENSINO PROFISSIONAL – PROGRAP"))
    doc.text.addElement(p_sig3)

def main():
    base_dir = r"c:\Users\bruno\OneDrive - ufpr.br\estágio\Coappe\Criação de certificados"
    excel_input = os.path.join(base_dir, "Relatório PVA.xlsx")
    bg_image = os.path.join(base_dir, "ufpr_25.jpg")
    output_dir = os.path.join(base_dir, "certificados_gerados")
    excel_skipped = os.path.join(base_dir, "linhas_sem_local.xlsx")
    
    if not os.path.exists(excel_input):
        print(f"Erro: Arquivo Excel não encontrado em {excel_input}")
        return
        
    os.makedirs(output_dir, exist_ok=True)
    
    print("Lendo dados da planilha Excel...")
    df = pd.read_excel(excel_input)
    
    linhas_invalidas = []
    
    total = len(df)
    gerados = 0
    
    for index, row in df.iterrows():
        local = str(row.get('Local de atividades', '')).strip()
        
        if not local or local == '-':
            linhas_invalidas.append(row)
            continue
            
        local_norm = normalize_local(local)
        
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
        
        if dados['nome_estudante'] and dados['nome_estudante'] != '-':
            filename_aluno = f"certificado_aluno_{normalize_filename(dados['nome_estudante'])}.odt"
            filepath_aluno = os.path.join(output_dir, filename_aluno)
            doc_aluno = OpenDocumentText()
            draw_certificate(doc_aluno, 'aluno', dados, bg_image)
            doc_aluno.save(filepath_aluno)
            gerados += 1
            
        if dados['nome_orientador'] and dados['nome_orientador'] != '-' and dados['matricula_orientador'] != '0':
            filename_prof = f"certificado_professor_{normalize_filename(dados['nome_orientador'])}_orientando_{normalize_filename(dados['nome_estudante'])}.odt"
            filepath_prof = os.path.join(output_dir, filename_prof)
            doc_prof = OpenDocumentText()
            draw_certificate(doc_prof, 'professor', dados, bg_image)
            doc_prof.save(filepath_prof)
            gerados += 1
            
        if index % 500 == 0:
            print(f"Processando linha {index}/{total}...")
            
    if linhas_invalidas:
        df_invalidas = pd.DataFrame(linhas_invalidas)
        df_invalidas.to_excel(excel_skipped, index=False)
        print(f"\nATENÇÃO: {len(linhas_invalidas)} linhas foram ignoradas por não terem 'Local de atividades'.")
        print(f"Elas foram salvas no arquivo: {excel_skipped}")
        
    print(f"\nConcluído com sucesso! {gerados} certificados foram gerados em 'certificados_gerados'.")

if __name__ == '__main__':
    main()
