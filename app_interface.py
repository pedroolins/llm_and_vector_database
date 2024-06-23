### importando o streamlit e o streamlit_chat que irá auxiliar na construção do chat
from streamlit_chat import message
from dotenv import load_dotenv
import streamlit as st
## importando o request para fazer as requests para as apis construídas 
import requests
import os

load_dotenv()


def main():
    st.set_page_config(page_title="Hotinho", page_icon="img/hot_simbolo_3.png")
    st.header("Converse com seus arquivos, faça uma pergunta ao Hotinho:fire::rocket:")
    user_question = st.text_input("Faça uma pergunta!")
    
    ## verifica se exite a lista com o histórico de perguntas e repostas baseados no state da página
    if "list_conversation" not in st.session_state:
        st.session_state.list_conversation = []
    ## botão que faz o envio da mensagem
    if st.button("Enviar pergunta"):
        ## verifica se existe uma pergunta do usuário
        if user_question:
            ## monta a requisição para a api_chat
            payload = {"question": user_question}
            # response_json = requests.post(url="http://localhost:5000/question", json=payload).json()
            host_api_chat = os.getenv("HOST_API_CHAT", "localhost")
            port_api_chat = os.getenv("PORT_API_CHAT")
            url_api_chat = f"http://{host_api_chat}:{port_api_chat}/question"
            response_json = requests.post(url=url_api_chat, json=payload).json()
            ## trata a resposta
            response = response_json.get("answer")
            ## coloca a pergunta e resposta dentro da lista de histórico de conversa
            st.session_state.list_conversation.append((user_question, response))
        else:
            st.write("Por favor, escreva uma pergunta!")
    ## itera dentro da lista de histórico de conversa para poder mostrar na ferramenta
    for i, qa in enumerate(st.session_state.list_conversation):
        user_question, response = qa 
        message(user_question, is_user=True, key=f"{i}_user", avatar_style="adventurer")
        message(response, is_user=False, key=f"{i}_llm")


    with st.sidebar:
        st.subheader("Seus Arquivos")
        st.write("lembre-se você pode carregar mais de um arquivo, se preferir!")
        documents = st.file_uploader("Arquivos em formato .pdf ou .txt", accept_multiple_files=True, type=["pdf","txt"])
                
        if st.button("Processar Documentos"):
            ## caso a lista de documentos esteja vazia
            if len(documents) == 0:
                st.write("Por favor, adicione algum documento para realizar a pergunta!")
            else:
                ## iterar dentre os arquivos enviados e gerar o dicionário da request para api que recebe os documentos
                files_list = []
                for doc in documents:
                    filename = doc.name
                    filetype = doc.type 
                    file = doc.getvalue()
                    files_list.append((filename, file, filetype))
                ## montando request para api que processa os documentos 
                request_files = {f"file{i}": item for i, item in enumerate(files_list)}
                # url_api_doc = "http://localhost:8080/document"
                host_api_doc = os.getenv("HOST_API_DOC", "localhost")
                port_api_doc = os.getenv("PORT_API_DOC")
                url_api_doc = f"http://{host_api_doc}:{port_api_doc}/document"
                response = requests.post(url_api_doc, files=request_files)
                response = response.json()
                ## escrevendo a resposta da api na ferramenta
                st.write(response.get("msg"))



if __name__ == '__main__':
    main()