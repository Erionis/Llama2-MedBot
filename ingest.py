from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 

# Define a path to the data
DATA_PATH = 'data/'
# Define a path to the vector database
DB_FAISS_PATH = 'vectorstore/db_faiss'


# Create vector database
def create_vector_db():
    # Load the documents
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf', 
                             loader_cls=PyPDFLoader)
    # Split the documents into chunks
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    create_vector_db()