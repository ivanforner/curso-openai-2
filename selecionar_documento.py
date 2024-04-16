from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = 'gpt-3.5-turbo'

politicas_ecomart = carrega('dados/políticas_ecomart.txt')
dados_ecomart = carrega('dados/dados_ecomart.txt')
produtos_ecomart = carrega('dados/produtos_ecomart.txt')

def select_document(openai_res):
    if 'políticas' in openai_res:
        return dados_ecomart + "\n" + politicas_ecomart
    elif 'produtos' in openai_res:
        return dados_ecomart + '\n' + produtos_ecomart
    else:
        return dados_ecomart

def select_context(user_message):
    system_prompt = f"""
        A empresa ecomart possui três documentos principais que detalham diferentes aspectos do negócio:

        #Documento 1 "\n{dados_ecomart}"\n"
        #Documento 2 "\n{politicas_ecomart}"\n"
        #Documento 3 "\n{produtos_ecomart}"\n"

        Avalie o prompt do usuário e retorne o documento mais indicado para ser usado no contexto da resposta.
        Retorne dados se for o Documento 1, políticas de for o documento 2, produtos se for o documento 3.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': user_message
            }
        ],
        temperature=1
    )

    context = response.choices[0].message.content.lower()

    return context
    