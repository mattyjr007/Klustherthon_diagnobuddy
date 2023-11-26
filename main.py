import time
import gunicorn
from fastapi import FastAPI
from typing import Any
from pydantic import BaseModel
import uvicorn
import os
from models import Model,SessionManager #, chatshistory

app = FastAPI()

model = Model()
session_manager = SessionManager()


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
        
        # update the sessions chathistory
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