# Gerador de Certificados UFPR (PVA)

Um script automatizado em Python para gerar milhares de certificados em formato PDF a partir de relatórios do **Programa de Voluntariado Acadêmico (PVA)**, replicando o modelo oficial gerado pelo SEI.

## 🚀 Como funciona

O script utiliza as bibliotecas `pandas` e `reportlab` para:
1. Ler uma planilha CSV contendo os dados dos docentes e discentes.
2. Filtrar os registros que possuem um Local de Atividade válido, separando as anomalias num arquivo à parte.
3. Sanitizar e normalizar nomes de locais (ex: remover caracteres indesejados e alinhar as letras maiúsculas).
4. Gerar **dois** PDFs idênticos ao layout original do SEI para cada linha da tabela:
   - **Certificado do Estudante:** constando suas horas e informações.
   - **Certificado do Professor:** atestando sua orientação daquele respectivo estudante.

## ⚙️ Pré-requisitos

Certifique-se de ter o Python 3 instalado e execute:
```bash
pip install pandas reportlab
```

## 📁 Estrutura de Arquivos

Coloque o script e os recursos no mesmo diretório:
- `gerador.py`: O código principal.
- `ufpr_25.jpg`: A imagem da logomarca usada no cabeçalho do documento com as devidas proporções originais.
- O arquivo `.csv` a ser lido (deve ser renomeado ou apontado corretamente no código).

## 🏃 Como usar

Pelo terminal, basta rodar o comando:
```bash
python gerador.py
```

Os certificados serão criados na pasta `certificados_gerados/`, e eventuais erros da planilha serão salvos em `linhas_sem_local.csv`.
