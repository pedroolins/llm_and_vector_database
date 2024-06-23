## Importando função que auxilia na quebra de textos em chunks
from langchain.text_splitter import CharacterTextSplitter
## importando nossa vector store
from src.utils.vector_database import get_vector_store
## importando diretórios temporários
from tempfile import TemporaryDirectory
## importando o pydf para auxiliar a leitura de documentos em PDF
from PyPDF2 import PdfReader
import os


def get_chunks(text:str) -> list:
    """ Função que recebe o nosso texto e quebra ele em chunks

    Args:
        text (str): o texto do nosso documento

    Returns:
        list: uma lista de chunks do nosso texto bruto
    """    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks


def read_files(file_path:str) -> str:
    """Função que lê os arquivos no formato .pdf ou .txt passado

    Args:
        file_path (str): caminho do arquivo

    Returns:
        str: string do texto retirado do arquivo
    """  
    ## condicional que verifica se é um pdf e lê o mesmo  
    if file_path.endswith(".pdf"):
        ## variável que irá armazenar todo o texto
        raw_text = ""
        pdf = PdfReader(file_path)
        for pages in pdf.pages:
            raw_text += pages.extract_text()
    ## condicional que verifica se é um .txt e lê o mesmo 
    elif file_path.endswith(".txt"):
        ## abrindo o arquivo para extrair todo texto do mesmo
        with open(file_path) as file_txt:
            raw_text = file_txt.read()
    ## retornando o texto bruto do arquivo
    return raw_text


def document_to_embeddings(file, collection_name:str) -> None:
    """ função que pega nosso documento, transforma ele em embeddings e envia pro nosso vector database Qdrant

    Args:
        file (FileStorage): arquivo que vem do request.files do flask
        collection_name (str): nome da collection do Qdrant que vc quer adicionar os embeddings

    Returns:
        _type_: _description_
    """    
    file_name = file.filename
    with TemporaryDirectory() as temp:
        file_path = os.path.join(temp, file_name)
        ## salvando o arquivo dentro do diretório temporário
        file.save(file_path)
        ## abrindo o arquivo
        raw_text = read_files(file_path=file_path)
        chunks = get_chunks(text=raw_text)
        vector_store = get_vector_store(collection=collection_name)
        vector_store.add_texts(chunks)
    return None


if __name__ == '__main__':
    raw_text = read_files("data/base_dados.txt")
    collection_name = "documentos_collection"
    chunks = get_chunks(text=raw_text)
    vector_store = get_vector_store(collection=collection_name)
    vector_store.add_texts(chunks)