# Importando a classe OpenAI da biblioteca openai
from openai import OpenAI
# Importando a função load_dotenv do módulo dotenv
from dotenv import load_dotenv
# Importando o módulo os para acessar variáveis de ambiente
import os

# Carregando variáveis de ambiente do arquivo .env
load_dotenv()

# Criando uma instância da classe OpenAI com a chave de API fornecida nas variáveis de ambiente
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.5-turbo-1106"
prompt_sistema = f"""
        Você é um categorizador de produtos.
        Você deve assumir as categorias presentes na lista abaixo.

        # Lista de Categorias Válidas
            - Moda Sustentável
            - Produtos para o Lar
            - Beleza Natural
            - Eletrônicos Verdes
            - Higiene Pessoal

        # Formato da Saída
        Produto: Nome do Produto
        Categoria: apresente a categoria do produto

        # Exemplo de Saída
        Produto: Escova elétrica com recarga solar
        Categoria: Eletrônicos Verdes
    """

    

prompt_usuario = input ("Apresente o nome de um produto: ")

# Enviando uma solicitação para a API OpenAI para obter respostas para mensagens fornecidas
resposta = cliente.chat.completions.create(
    messages= [
        {
            "role": "system", 
            "content": prompt_sistema
            # Mensagem do sistema com instruções sobre listar nomes de produtos
        },
        {
            "role": "user",
            "content": prompt_usuario
            # Mensagem do usuário solicitando a listagem de 3 produtos sustentáveis
        }
    ],
    model=modelo, # Especificando o modelo GPT-4 para geração de texto
    temperature= 0, # Definindo a temperatura ou criatividade da resposta (0 para resposta determinística)
    max_tokens= 200, # Limitando o número máximo de tokens na resposta
    n = 1 # Especificando o número de respostas a serem geradas
)

# Imprimindo o conteúdo da primeira resposta fornecida pela API OpenAI
print(resposta.choices[0].message.content)

