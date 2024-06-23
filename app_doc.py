from flask import Flask
from flask import jsonify
from flask import request
from src.functions.document_to_vectorstore import document_to_embeddings
import os

app = Flask(__name__)

@app.get("/")
def index():
    """ Endpoint raiz da aplicação
    """
    response = {"msg": "Seja Bem Vindo a api de tratamento e transformação de documentos!"}
    response = jsonify(response)
    response.status_code = 200
    return response

@app.post("/document")
def trata_documentos():
    """ Endpoint que recebe os documentos, trata os mesmos e transforma em embeddings para ser enviado ao Qdrant
    """   
    ## pegando todos arquivos que estão sendo enviados
    try:
        ## verifica se a requisição veio com o arquivo
        if len(request.files) == 0:
            msg_error = "Não foi enviado nenhum arquivo na requisição, por favor lembre de enviar um documento!"
            response = jsonify({"msg": msg_error})
            response.status_code = 400
            return response
        ## iterando dentro de todos os arquivos enviados e verificando se algum possui uma extensão fora do padrão
        lista_filenames = [file.filename for key, file in request.files.items()]
        lista_filtrada = [filename for filename in lista_filenames if filename.endswith(".pdf") or filename.endswith(".txt")]
        if len(lista_filtrada) != len(lista_filenames): ## condicional que verifica se as listas possui o mesmo tamanho
            msg_error = "O(s) arquivo(s) enviado(s) não está no formato aceito pela api, lembre de passar apenas documentos de texto com extensão (.pdf ou .txt)"
            response = jsonify({"msg": msg_error})
            response.status_code = 400
            return response
        ## iterando dentro dos arquivos enviados
        for item in request.files.items():
            key, file = item
            document_to_embeddings(file=file, collection_name="documentos_collection")
        ## caso todas as validações sejam aceitas
        response = jsonify({"msg": "Os documentos enviados foram processados!"})
        response.status_code = 200
        return response
    except Exception as e:
        msg_error = f"Ocorreu um erro ao realizar o upload do arquivo: {e=}"
        response = jsonify({"msg": msg_error})
        response.status_code = 500
        return response

if __name__ == "__main__":
    app.run(port=os.getenv("PORT_API_DOC"))