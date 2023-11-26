import time
import gunicorn
from fastapi import FastAPI,Depends, Request
from typing import Any
from pydantic import BaseModel
import uvicorn
import os
from Model import Model,SessionManager#, chatshistory

from openai import OpenAI
# from dotenv.main import load_dotenv

# load_dotenv()

# # Set up OpenAI API key
# client = OpenAI(api_key=os.environ['GPT'])
# Declaring our FastAPI instance
app = FastAPI()

model = Model()
session_manager = SessionManager()
# #Temporary Store the chat history
# chatshistory = []
# chatshistory.append({
#       "role": "system",
#       "content": "You're a medical assistant chatbot called DiagnoBuddy,\nyour role is to give preliminary medical advice. A user will describe their symptoms, wait and collect input step by step, and you diagnose their possible conditions based on the input, request as much input needed, if need be, for more clarification and proper diagnosis. \nRecommend Home remedies if needed, tell them when they should seek a doctor. help patients decide if they need to seek in-person medical care/Doctors.\nYou will gather information's from the user, request from the user as much information needed to give a diagnosis and medical advice. \nmake the responses short and direct simulate in a human manner. `please strictly adhere to bot objective, do not answer question that is not a medical or health concern.`"
#     })

# # chat bot gpt
# def chatBot(msg:str):

#     # store conversation
#     chatshistory.append({"role": "user","content": f"{msg}"})

#     # feed into model
#     response = client.chat.completions.create(
#       model="gpt-3.5-turbo",
#       messages= chatshistory,
#         temperature=0.34,
#         max_tokens=350,
#         timeout=300
#     )

#     # bot response
#     #bot_response = response.choices[0].message.content

#     try:
#          # bot response
#         bot_response = response.choices[0].message.content
        
#         chatshistory.append({
#           "role": "assistant",
#           "content": f"{bot_response}"
#         })
    
#         return bot_response
#         # return output for model
#     except:
#         # print(response.choices[0].text)
#         return "Heyy, i'm facing a little downtime now please try in a few mins"
        

# home page
@app.get("/")
def root():
    return {"message": "Hello World, please head over to /docs"}


# Text Model
@app.post("/api/gpmodel/")
async def chatModel(user_input:str, session_id: str) -> dict:

    # pass message to model
    
    try:
       # Get or create the session
        session = session_manager.get_session(session_id)

        # Update last activity time for the session
        session_manager.update_last_activity(session_id)

        response_msg,chts = model.chatBot(msg=user_input,sessions=session)
        
        session_manager.updatesessionchat(session_id=session_id,chat=chts)

        # Clear expired sessions
        session_manager.clear_expired_sessions()
        
    except Exception as e:
        print("Exception caught: ", e)
        response_msg = "Heyy!, there seems to be an issue please try again in a few secs!"

    
    # store response in dictionary
    reponse_out = {"AI_out":response_msg}

    return reponse_out


# Lang Model
@app.post("/api/langchainmodel/")
async def langModel(user_input:str) -> dict:

    # pass message to model
    
    try:
        response_msg = model.chatBotLang(msg=user_input)
    except:
        response_msg = "Heyy!, there seems to be an issue please try again in a few secs!"

    # store response in dictionary
    reponse_out = {"AI_out":response_msg}

    return reponse_out


# Text Model
@app.post("/api/llama2model/")
async def llamaModel(user_input:str) -> dict:

    # pass message to model
    
    try:
        response_msg = model.chatLlama2(message=user_input)
    except Exception as e:
        print("Exception caught: ", e)
        response_msg = "Heyy!, there seems to be an issue please try again in a few secs!"

    # store response in dictionary
    reponse_out = {"AI_out":response_msg}

    return reponse_out