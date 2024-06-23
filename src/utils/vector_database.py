## importando módulos que ajudam a criar nossa coleção
from qdrant_client.http.models import Distance, VectorParams
## importando o OpenAi embeddings
from langchain_openai import OpenAIEmbeddings
## importando o client do Qdrant
from qdrant_client import QdrantClient
## importando o Qdrant como vector store do langchain
from langchain_qdrant import Qdrant
## load_dotenv para carregar as variáveis de ambiente
from dotenv import load_dotenv
import os

load_dotenv()

def get_vector_store(collection:str) -> Qdrant:
    """ Função que retorna a nossa vector_store configurada

    Args:
        collection (str): o Nome da collection que queremos configurar

    Returns:
        Qdrant: vector_store configurada
    """
    ## verificando se estamos rodando pelo terminal ou dentro do container para definir o Host do client do Qdrant
    hostname = os.getenv("IN_CONTAINER", "localhost")
    ## pegando a porta do nosso vector database
    port = os.getenv("PORT_VECTOR_DATABASE")
    ## instanciando nosso client do Qdrant
    client = QdrantClient(host=hostname, port=port)
    ## usando o client para verificar se a collection já existe, caso contrário ele irá criar uma
    collection_exists = client.collection_exists(collection_name=collection)
    ## verifica se a collection não existe
    if not collection_exists:
        ## agora vamos criar a nossa coleção
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
    ## vamos instanciar o OpenAiEmbeddings() lembrado que já temos a nossa variável de ambiente com a chave de api na nomenclatura padrão
    embeddings = OpenAIEmbeddings() ## aqui estou usando o modelo padrão "text-embedding-ada-002"
    vector_store = Qdrant(
        client=client,
        collection_name=collection,
        embeddings=embeddings
    )
    return vector_store


if __name__ == "__main__":
    vector_store = get_vector_store(collection="documentos_collection")