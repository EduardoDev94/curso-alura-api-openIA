from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa um cliente OpenAI com a chave de API obtida das variáveis de ambiente
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

# Define uma função chamada carrega que recebe o nome de um arquivo como parâmetro
def carrega(nome_do_arquivo):
    try:
        # Abre o arquivo especificado em modo leitura e codificação utf-8
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            # Lê o conteúdo do arquivo
            dados = arquivo.read()
            # Retorna os dados lidos do arquivo
            return dados
    # Captura a exceção IOError (Erro de E/S)
    except IOError as e:
        # Imprime uma mensagem de erro indicando o problema
        print(f"Erro no carregamento de arquivo: {e}")

# Define uma função chamada salva que recebe o nome de um arquivo e o conteúdo a ser salvo como parâmetros
def salva(nome_do_arquivo, conteudo):
    try:
        # Abre o arquivo especificado em modo escrita e codificação utf-8
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            # Escreve o conteúdo no arquivo
            arquivo.write(conteudo)
    # Captura a exceção IOError (Erro de E/S)
    except IOError as e:
        # Imprime uma mensagem de erro indicando o problema
        print(f"Erro ao salvar arquivo: {e}")

# Define uma função chamada analisar_transacao que recebe uma lista de transações como parâmetro
def analisar_transacao(lista_transacoes):
    # Imprime uma mensagem indicando que a análise de transação está sendo executada
    print("1. Executando análise de transação")
    # Define o prompt do sistema para orientar a análise das transações
    prompt_sistema =  """
    Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada". 
    Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

    Cada nova transação deve ser inserida dentro da lista do JSON.

    # Possíveis indicações de fraude
    - Transações com valores muito discrepantes
    - Transações que ocorrem em locais muito distantes um do outro
    
        Adote o formato de resposta abaixo para compor sua resposta.
        
    # Formato Saída 
    {
        "transacoes": [
            {
            "id": "id",
            "tipo": "crédito ou débito",
            "estabelecimento": "nome do estabelecimento",
            "horário": "horário da transação",
            "valor": "R$XX,XX",
            "nome_produto": "nome do produto",
            "localização": "cidade - estado (País)"
            "status": ""
            },
        ]
    } 
    """
    # Define uma lista de mensagens contendo o prompt do sistema e o prompt do usuário
    lista_mensagens = [
    {
        "role": "system",
        "content": prompt_sistema
        },
    {
        
            "role": "user",
    "content": f"Considere o CSV abaixo, onde cada linha é uma transação diferente: {lista_de_transacoes}. Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)"
        }
    ]
    # Cria uma resposta usando o cliente OpenAI, passando as mensagens, o modelo e a temperatura
    resposta = cliente.chat.completions.create(
    messages=lista_mensagens,
    model=modelo,
    temperature=0
    )
    # Substitui as aspas simples por aspas duplas no conteúdo da resposta e armazena em conteudo
    conteudo = resposta.choices[0].message.content.replace("'", '"')
    # Imprime o conteúdo da resposta
    print("\nConteúdo:", conteudo)
    # Carrega o conteúdo da resposta em formato JSON e armazena em json_resultado
    json_resultado = json.loads(conteudo)
    # Imprime o JSON resultante
    print("\nJSON:", json_resultado)
    # Retorna o JSON resultante
    return json_resultado

# Define uma função chamada gerar_parecer que recebe uma transação como parâmetro
def gerar_parecer(transacao):
    # Imprime uma mensagem indicando que o parecer está sendo gerado para a transação
    print("2. Gerando parecer para transacao ", transacao["id"])
    # Define o prompt do sistema para orientar a geração do parecer
    prompt_sistema = f"""
    Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". Indique no parecer uma justificativa para que você identifique uma fraude.
    Transação: {transacao}

    ## Formato de Resposta
    "id": "id",
    "tipo": "crédito ou débito",
    "estabelecimento": "nome do estabelecimento",
    "horario": "horário da transação",
    "valor": "R$XX,XX",
    "nome_produto": "nome do produto",
    "localizacao": "cidade - estado (País)"
    "status": "",
    "parecer" : "Colocar Não Aplicável se o status for Aprovado"
    """
    # Define uma lista de mensagens contendo o prompt do sistema
    lista_mensagens = [
    {
        "role": "user",
        "content": prompt_sistema
        }
    ]
    # Cria uma resposta usando o cliente OpenAI, passando as mensagens e o modelo
    resposta = cliente.chat.completions.create(
    messages=lista_mensagens,
    model=modelo,
    )
    # Armazena o conteúdo da resposta em conteudo
    conteudo = resposta.choices[0].message.content
    # Imprime uma mensagem indicando que a geração do parecer foi finalizada
    print("Finalizou a geração de parecer")
    # Retorna o conteúdo do parecer gerado
    return conteudo

def gerar_recomendacao(parecer):
    print("3. Gerando recomendações")
    prompt_sistema = f"""
    Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da transação da Transação: {parecer}

    As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude" ou "Realizar Verificação Manual".
    Elas devem ser escritas no formato técnico.

    Inclua também uma classificação do tipo de fraude, se aplicável. 
    """
   
    lista_mensagens = [
            {
                "role": "system",
                "content": prompt_sistema
            }
    ]

    resposta = cliente.chat.completions.create(
            messages = lista_mensagens,
            model=modelo,
    )
    # código omitido

    conteudo = resposta.choices[0].message.content
    print("Finalizou a geração de recomendação")
    return conteudo

# código omitido


# código omitido



# Carrega as transações do arquivo "transacoes.csv"
lista_de_transacoes = carrega("transacoes.csv")
# Realiza a análise das transações e armazena o resultado em transacoes_analisadas
transacoes_analisadas = analisar_transacao(lista_de_transacoes)

# Itera sobre cada transação no resultado da análise
for uma_transacao in transacoes_analisadas["transacoes"]:
    # Verifica se o status da transação é "Possível Fraude"
    if uma_transacao["status"] == "Possível Fraude":
        # Gera um parecer para a transação e armazena em um_parecer
        um_parecer = gerar_parecer(uma_transacao)
        recomendacao = gerar_recomendacao(um_parecer)
        id_transacao = uma_transacao["id"]
        produto_transacao = uma_transacao["nome_produto"]
        status_transacao = uma_transacao["status"]
        salva(f"transacao-{id_transacao}-{produto_transacao}-{status_transacao}.txt", recomendacao)
        
        

