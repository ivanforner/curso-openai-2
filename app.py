from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
from time import sleep
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.5-turbo"

app = Flask(__name__)
app.secret_key = 'alura'

def bot(prompt):
    maximo_tentativas = 1
    repeticoes = 0

    while True:
        try:
            prompt_do_sistema = """
                Você é um chatbot de atendimento a clientes de um e-comerce.
                Você não deve responder perguntas que não sejam dados do e-comerce informado!
            """

            response = cliente.chat.completions.create(
                messages=[
                    {
                        'role': 'system',
                        'content': prompt_do_sistema
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model=modelo
            )

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
    texto_resposta = resposta.choices[0].message.content
    return texto_resposta


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
