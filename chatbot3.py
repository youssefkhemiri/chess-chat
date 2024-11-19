from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Initialize OpenAI API key
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the embeddings and ChromaDB
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Create a Chroma database or load an existing one
chroma_db = Chroma(embedding_function=embeddings, persist_directory="chroma_db")  # Set persist_directory to save the database

# Function to add data to the vector store
def add_data_to_vectorstore(data: list):
    """
    Add data (list of strings) to the vector store.
    """
    for doc in data:
        chroma_db.add_texts([doc])
    chroma_db.persist()  # Save changes

# Function to perform similarity search
def similarity_search(query: str, k: int = 3):
    """
    Perform similarity search in the vector store.
    """
    return chroma_db.similarity_search(query, k)

# Function to generate a response from GPT-4 using retrieved context
def gpt4_with_context(query: str, k: int = 3):
    """
    Retrieve relevant context from the vector store and call GPT-4.
    """
    # Perform similarity search
    relevant_docs = similarity_search(query, k)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    # Define the prompt
    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template="""
        You are a helpful chess assistant, you assist with question about chess, answer questions and rely on the context provided below if its relevant:\n\n
        Context:\n{context}\n\n
        Question:\n{query}\n\n
        Answer:
        """
    ).format(context=context, query=query)

    # Initialize the GPT-4 model
    gpt4 = ChatOpenAI(model_name="gpt-4", openai_api_key=openai_api_key)

    # Generate response
    return gpt4.predict(prompt)

# Example usage
if __name__ == "__main__":
    # Adding some data to the vector store
    chess_data = [
        "Chess is a strategic board game played between two players on an 8x8 grid.",
        "The game begins with each player having 16 pieces: 8 pawns, 2 knights, 2 bishops, 2 rooks, 1 queen, and 1 king.",
        "The objective of chess is to checkmate the opponent's king, where it is under threat of capture and no moves can prevent it.",
        "Castling is a special move in chess that involves the king and a rook.",
        "The pawn can be promoted to any piece (except the king) if it reaches the opponent's back rank."
    ] # you can add any string to the vector database
    add_data_to_vectorstore(chess_data)

    # Querying the vector store and generating a response
    user_query = "What is castling in chess, explain in detail?"
    response = gpt4_with_context(user_query)
    print("---------------")
    print("Response:", response)
