# Gerador de Certificados UFPR (PVA)

Este é um guia passo a passo completo para você conseguir instalar tudo e gerar os certificados facilmente, mesmo que nunca tenha usado programação ou linha de comando antes.

---

## Passo 1: Instalar o Python no computador
O **Python** é o programa necessário para rodar o gerador. Você só precisa instalá-lo uma única vez.

1. Acesse o site oficial: [python.org/downloads](https://www.python.org/downloads/)
2. Clique no botão amarelo **Download Python**.
3. Abra o arquivo baixado para iniciar o instalador.
4. **⚠️ MUITO IMPORTANTE (No Windows):** Na primeira tela da instalação, marque a caixinha **"Add python.exe to PATH"** (ou "Adicionar Python ao PATH") na parte inferior da janela antes de clicar em "Install Now".

---

## Passo 2: Organizar os arquivos do gerador
Coloque os três arquivos abaixo **juntos na mesma pasta** do seu computador (por exemplo, na pasta `Documentos` ou em uma pasta criada na `Área de Trabalho`):

1. O arquivo do programa: `gerador.py`
2. A imagem do cabeçalho: `ufpr_25.jpg`
3. A sua planilha com os dados: Ela **precisa** se chamar exatamente `Relatório PVA.xlsx`. 

*(Se a sua planilha tiver outro nome, clique nela com o botão direito, escolha "Renomear" e altere para `Relatório PVA`).*

---

## Passo 3: Abrir a tela de comandos (Terminal / Prompt de Comando)

### No Windows:
1. Abra a pasta onde você colocou os 3 arquivos.
2. Clique na barra de endereço (onde mostra o caminho da pasta no topo da janela).
3. Digite `cmd` e aperte a tecla **ENTER**. A janela de comando abrirá automaticamente apontando para a pasta correta.

### No Linux ou Mac:
1. Abra o aplicativo **Terminal**.
2. Digite `cd ` (com um espaço depois do cd) e arraste a pasta onde estão os arquivos para dentro da janela do terminal.
3. Aperte **ENTER**.

---

## Passo 4: Instalar os pacotes necessários (Só na primeira vez)
Com a janela do Terminal / Prompt de Comando aberta:

1. Copie o comando abaixo, cole na janela e aperte **ENTER**:

```bash
pip install pandas odfpy openpyxl
```
2. Aguarde alguns segundos até que a instalação seja totalmente concluída.

---

## Passo 5: Gerar os certificados

1. Na mesma janela de comandos, copie e cole o comando abaixo e aperte **ENTER**:

```bash
python gerador.py
```

2. Pronto! O programa processará a planilha e criará automaticamente uma pasta chamada `certificados_gerados`. 
3. Todos os certificados estarão salvos nessa pasta no formato de documento de texto (`.odt`), prontos para serem abertos no LibreOffice ou Microsoft Word.

---

### 🛑 Resolução de problemas
Caso algum estudante ou professor na planilha esteja com informações incompletas (por exemplo, se estiver faltando o preenchimento do "Local de atividades"), o programa não vai parar de funcionar. Ele apenas salvará as linhas com pendências em um arquivo separado chamado `linhas_sem_local.xlsx` para que você possa verificar e corrigir depois.
