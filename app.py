from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
from time import sleep
import os
from helpers import *
from selecionar_persona import *
from selecionar_documento import *
from assistente_ecomart import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4-turbo"

app = Flask(__name__)
app.secret_key = 'alura'

assistant = pegar_json()
thread_id = assistant['thread_id']
assistant_id = assistant['assistant_id']
file_ids = assistant['file_ids']

STATUS_COMPLETED = 'completed'
STATUS_REQUIRES_ACTION = 'requires_action'

def bot(prompt):
    maximo_tentativas = 1
    repeticoes = 0

    while True:
        try:
            personalidade = persons[select_person(prompt)]

            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=f'''
                    Assuma, de agora em diante, a personalidade abaixo
                    Ignore as personalidades anteriores

                    # Persona:
                    {personalidade}
                ''',
                file_ids=file_ids
            )

            client.beta.threads.messages.create(
                thread_id=thread_id,
                role='user',
                content=prompt,
                file_ids=file_ids
            )

            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
            )

            while run.status != STATUS_COMPLETED:
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )

                print(f"Status: {run.status}")

                if run.status == STATUS_REQUIRES_ACTION:
                    tools_adicionadas = run.required_action.submit_tool_outputs.tool_calls
                    respostas_tools_acionadas = []
                    for tool in tools_adicionadas:
                        nome_funcao = tool.function.name
                        funcao_escolhida = minhas_funcoes[nome_funcao]
                        argumentos = json.loads(tool.function.arguments)
                        
                        print(argumentos)
                        
                        resposta_funcao = funcao_escolhida(argumentos)
                        respostas_tools_acionadas.append({
                            "tool_call_id": tool.id,
                            "output": resposta_funcao
                        })
                    
                    run = client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run.id,
                        tool_outputs=respostas_tools_acionadas
                    )

            historic = list(client.beta.threads.messages.list(thread_id=thread_id).data)
            response = historic[0]
            return response

        except Exception as erro:
            repeticoes += 1
            if repeticoes >= maximo_tentativas:
                return f'Erro no GPT: {erro}'
            print('Erro de comunicação com a openai', erro)
            sleep(1)

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    print(resposta)
    texto_resposta = resposta.content[0].text.value
    return texto_resposta


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
