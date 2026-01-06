from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

pdf_path = Path(__file__).parent / "nodejs.pdf"

#load pdf(https://docs.langchain.com/oss/python/integrations/document_loaders)
#load pdf using pypdf(https://docs.langchain.com/oss/python/integrations/document_loaders/pypdfloader)
loader = PyPDFLoader(pdf_path)

docs = loader.load()
# print('\033[38;2;184;47;5m'+'docs: ' + '\033[38;2;117;64;222m', docs[12], '\033[0m')

#split the docs into smaller chunks(https://docs.langchain.com/oss/python/integrations/splitters)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap=400
)
chunks = text_splitter.split_documents(documents=docs)
# print('\033[38;2;135;128;19m'+'chunks: ' + '\033[38;2;61;221;255m', chunks, '\033[0m')

#create vector embedding for this chunks. (https://docs.langchain.com/oss/python/integrations/text_embedding/openai)

# embedding_model = OpenAIEmbeddings(
#     model="text-embedding-3-large"
# )

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#embedding chunks using qdrant-db for langchain(https://docs.langchain.com/oss/python/integrations/vectorstores/qdrant)(http://localhost:6333/dashboard#/welcome)
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)
print("indexing of documents done")