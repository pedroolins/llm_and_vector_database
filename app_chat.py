from flask import Flask
from flask import jsonify
from flask import request
from src.functions.question_answer import chat
import os

app = Flask(__name__)

@app.get("/")
def index():
    """ Endpoint raiz da aplicação
    """
    response = {"msg": "Seja Bem Vindo a api de chat com a LLM!"}
    response = jsonify(response)
    response.status_code = 200
    return response


@app.post("/question")
def send_answer():
    """ Endpoint que recebe a pergunta e retorna a resposta do LLM baseada no contexto enviado
    """   
    ## pegando todos arquivos que estão sendo enviados
    try:
        data = request.get_json()
        ## validando se o payload tem a chave correta
        if "question" not in data:
            response = jsonify({"msg": "Seu payload não possui a chave 'question' com a pergunta como valor!"})
            response.status_code = 400
            return response
        ## caso o payload tenha a chave correta ele processa a pergunta no nosso pipeline
        question = data.get("question")
        collection_name = "documentos_collection"
        answer = chat(question=question, collection=collection_name)
        response = jsonify({"answer": answer})
        response.status_code = 200
        return response
    except Exception as e:
        msg_error = f"Ocorreu um erro ao realizar o processo de resposta, error: {e=}"
        response = jsonify({"msg": msg_error})
        response.status_code = 500
        return response
    

if __name__ == "__main__":
    app.run(port=os.getenv("PORT_API_CHAT"))