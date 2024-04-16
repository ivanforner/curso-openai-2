def carrega(nome_do_arquivo):
    try:
        with open (nome_do_arquivo, 'r') as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as error:
        print(f"Erro ao carregar o arquivo. {error}")
        

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
    except IOError as error:
        print(f"Erro ao salvar o arquivo. {error}")