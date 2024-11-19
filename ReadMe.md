####

## install libraries
pip install -r requirements.txt


add gpt-4 api in the .env file
####
#first test by running chatbot3.py #ignore the warnings
## Run the api

uvicorn chat_api:app --reload

## API

#### Add Data to the Vector Database
Send a POST request to /add-data with a JSON body in this format:

{
  "data": [
    "Chess is a strategic board game played between two players on an 8x8 grid.",
    "The objective of chess is to checkmate the opponent's king.",
    "Castling is a special move in chess that involves the king and a rook."
  ]
}

#### Query the Chatbot
Send a POST request to /query-chatbot with a JSON body:


{
  "query": "What is castling in chess?",
  "k": 3
}


#### you will find many comment explaining the code too
