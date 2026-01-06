#retrieval code
import os
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI


load_dotenv()


# embedding_model = OpenAIEmbeddings(
#     model="text-embedding-3-large"
# )

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model,
)

#take the user input 
user_query = input("Ask something...")

#now we will similarity search
search_result = vector_db.similarity_search(user_query) #this will return relevant search from the vector db

#--------------------------------------
context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number:{result.metadata['page_label']}\nFile Location:{result.metadata['source']}" for result in search_result])
print('\033[38;2;150;132;96m'+'context: ' + '\033[38;2;105;109;6m', context, '\033[0m')

SYSTEM_PROMPT = f"""
You are a helpful AI assistant.

Rules:
- Use ONLY the information provided in the context.
- Answer in clear, simple language.
- ALWAYS return valid JSON.
- The JSON must contain exactly ONE key: "response".
- The value of "response" must be a plain text explanation.
- Add page numbers at the end of the response as:
  "Reference: Page X" or "Reference: Pages X–Y"

If the answer is not found in the context, return:
{{ "response": "I couldn't find this information in the provided document." }}

Context:
{context}
"""

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":user_query},
    ] 
)

print("=====================",response.choices[0].message.content)
