# Importando as bibliotecas necessárias
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializando o cliente OpenAI com a chave API carregada do arquivo .env
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

# Função para carregar o conteúdo de um arquivo
def carrega(nome_do_arquivo):
    try:
        # Tentativa de abrir e ler o arquivo
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        # Tratamento de erro em caso de falha ao ler o arquivo
        print(f"Erro: {e}")

# Função para análise de sentimentos de um produto
def analisador_sentimentos(produto): 
    # Prompt do sistema que será enviado ao cliente OpenAI
    prompt_sistema = f"""
    Você é um analisador de sentimentos de avaliações de produtos.
    Escreva um parágrafo com até 50 palavras resumindo as avaliações e 
    depois atribua qual o sentimento geral para o produto.
    Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

    # Formato de Saída

    Nome do Produto:
    Resumo das Avaliações:
    Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
    Ponto fortes: lista com três bullets
    Pontos fracos: lista com três bullets
    """

    # Carrega o prompt do usuário do arquivo
    prompt_usuario = carrega(f"./dados/avaliacoes-{produto}.txt")
    print(f"Iniciou a análise de sentimentos do produto {produto}")

    # Lista de mensagens para enviar ao cliente OpenAI
    lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ]

    # Chama a API da OpenAI para análise de sentimentos
    resposta = cliente.chat.completions.create(
        messages=lista_mensagens,
        model=modelo
    )

    # Obtém o texto da resposta e o salva em um arquivo
    texto_resposta = resposta.choices[0].message.content
    salva(f"./dados/analise-{produto}.txt", texto_resposta)

# Função para salvar texto em um arquivo
def salva(nome_do_arquivo, texto):
    try:
        # Tentativa de abrir e escrever no arquivo
        with open(nome_do_arquivo, "w") as arquivo:
            arquivo.write(texto)
    except IOError as e:
        # Tratamento de erro em caso de falha ao salvar o arquivo
        print(f"Erro ao salvar o arquivo: {e}")

# Exemplo de chamada da função analisador_sentimentos
analisador_sentimentos("talher-de-bambu")
