# Gerador de Certificados UFPR (PVA)

Este é um guia passo a passo simplificado para você conseguir gerar os certificados facilmente, sem precisar de conhecimentos avançados em informática.

## Passo 1: Organizar os arquivos
Para que tudo funcione corretamente, os três arquivos abaixo precisam estar **juntos na mesma pasta** do seu computador:
1. O arquivo do programa: `gerador.py`
2. A imagem do cabeçalho: `ufpr_25.jpg`
3. A sua planilha de dados: Ela **precisa** se chamar exatamente `Relatório PVA.xlsx`. 

*(Atenção: Se a sua planilha tiver outro nome, clique nela com o botão direito, selecione "Renomear" e altere o nome para "Relatório PVA").*

## Passo 2: Preparar o ambiente
Este passo só precisa ser feito uma única vez no seu computador para instalar os pacotes necessários.
1. Abra o "Terminal" (ou "Prompt de Comando" se estiver no Windows).
2. Copie o comando abaixo, cole na tela do terminal e aperte a tecla **ENTER**:

```bash
pip install pandas odfpy openpyxl
```
Aguarde alguns segundos até que a instalação seja totalmente concluída.

## Passo 3: Gerar os certificados
Sempre que você quiser gerar novos certificados, siga os passos abaixo:
1. No terminal, navegue até a pasta onde você guardou os três arquivos do Passo 1.
2. Copie e cole o comando abaixo no terminal e aperte **ENTER**:

```bash
python gerador.py
```

Pronto! O programa irá processar a sua planilha e criará automaticamente uma nova pasta chamada `certificados_gerados`. Todos os seus certificados estarão armazenados lá, no formato de documento de texto (.odt), prontos para serem abertos no LibreOffice ou Microsoft Word.

### Resolução de problemas
Caso algum estudante ou professor na planilha esteja com informações incompletas (por exemplo, se estiver faltando o preenchimento do "Local de atividades"), o programa não vai parar de funcionar. Ele apenas ignorará o erro e salvará os dados com problema em um arquivo separado chamado `linhas_sem_local.xlsx`. Você poderá abrir esse arquivo depois para verificar o que precisa ser corrigido.
