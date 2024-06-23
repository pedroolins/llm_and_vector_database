## importando nossa vector store
from src.utils.vector_database import get_vector_store
## importando o módulo que facilita o uso de vector stores em QA(question answering)
from langchain.chains import RetrievalQA
## importando a llm
from langchain_openai import OpenAI


def chat(question:str, collection:str) -> str:
    """Função que recebe uma pergunta, transforma em embedding e envia para o LLM,
    junto com os embeddings mais similares como contexto 

    Args:
        question (str): pergunta recebida
        collection (str): nome da coleção do qdrant que iremos usar como contexto

    Returns:
        str: reposta do LLM
    """  
    ## instanciando nosso vector_store
    vector_store = get_vector_store(collection=collection)
    ## montando a arquitetura de recebimento da pergunta, transformação em embedding, 
    ## busca por similaridade na nossa collection do vector database e envio do contexto para o LLM
    question_answer = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    dict_answer = question_answer.invoke(question)
    ## pegando apenas a resposta da LLM
    answer = dict_answer.get("result")
    return answer


if __name__ == '__main__':
    question = "A hotmart possui calculadora de infoproduto?"
    collection_name = "documentos_collection"
    response = chat(question=question, collection=collection_name)

