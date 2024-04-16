from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecionar_persona import *
import json
from tools_ecomart import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = 'gpt-4-turbo'
contexto = carrega("dados/ecomart.txt")

def criar_lista_ids():
    lista_ids_arquivos = []
    
    file_dados = client.files.create(
        file=open("dados/dados_ecomart.txt", "rb"),
        purpose="assistants"
    )
    
    lista_ids_arquivos.append(file_dados.id)

    file_dados = client.files.create(
        file=open("dados/políticas_ecomart.txt", "rb"),
        purpose="assistants"
    )
    
    lista_ids_arquivos.append(file_dados.id)

    file_dados = client.files.create(
        file=open("dados/produtos_ecomart.txt", "rb"),
        purpose="assistants"
    )
    
    lista_ids_arquivos.append(file_dados.id)

    return lista_ids_arquivos

def pegar_json():
    filename = 'assistentes.json'

    if not os.path.exists(filename):
        thread = create_thread()
        file_id_list = criar_lista_ids()
        assistant = create_assistant(file_id_list)
        
        data = {
            "assistant_id": assistant.id,
            "thread_id": thread.id,
            "file_ids": file_id_list
        }

        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print("Arquivo 'assistentes.json' criado com sucesso!")
    
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Arquivo 'assistentes.json' não encontrado.")

def create_assistant(file_ids=[]):
    assistant = client.beta.assistants.create(
        name="Atendente Ecomart",
        instructions=f"""
            Você é um chatbot de atendimento a clientes de um e-commerce. 
            Você não deve responder perguntas que não sejam dados do ecommerce informado!
            Além disso, acesse os arquivos associados a você e a thread para responder as perguntas.
        """,
        model=model,
        file_ids=file_ids,
        tools=minhas_tools
    )
    
    return assistant


def create_thread():
    return client.beta.threads.create()
