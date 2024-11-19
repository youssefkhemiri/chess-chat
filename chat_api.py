from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot3 import add_data_to_vectorstore, gpt4_with_context

# Initialize FastAPI
app = FastAPI()

# Pydantic Models
class AddDataRequest(BaseModel):
    data: list[str]  # List of strings to add to the vector database

class QueryChatbotRequest(BaseModel):
    query: str  # User query
    k: int = 3  # Number of top results to retrieve

# Add data to the vector database
@app.post("/add-data")
async def add_data(request: AddDataRequest):
    try:
        add_data_to_vectorstore(request.data)
        return {"message": "Data added to vector database successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding data: {str(e)}")

# Query the chatbot
@app.post("/query-chatbot")
async def query_chatbot(request: QueryChatbotRequest):
    try:
        response = gpt4_with_context(request.query, request.k)
        return {"query": request.query, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying chatbot: {str(e)}")
