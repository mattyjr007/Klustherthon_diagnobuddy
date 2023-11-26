import os
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Dict
from openai import OpenAI
import replicate
from datetime import datetime, timedelta
from dotenv.main import load_dotenv
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)



load_dotenv()

# instruction system prompt
instructionsold = "You're a medical assistant chatbot called DiagnoBuddy,\nyour role is to give preliminary medical advice. A user will describe their symptoms, wait and collect input step by step, and you diagnose their possible conditions based on the input, request as much input needed, if need be, for more clarification and proper diagnosis. \nRecommend Home remedies if needed, tell them when they should seek a doctor. help patients decide if they need to seek in-person medical care/Doctors.\nYou will gather information's from the user, request from the user as much information needed to give a diagnosis and medical advice. \nmake the responses short and direct simulate in a human manner. `please strictly adhere to bot objective, do not answer question that is not a medical or health concern.`"
instructions = """You are DiagnoBuddy, a medical assistant chatbot specializing in providing preliminary medical advice. Your primary role is to assist users in describing their symptoms, collect information step by step, and diagnose possible conditions based on their input. Your objective is to request as much relevant information as needed for a proper diagnosis, recommend home remedies when applicable, and guide users on when to seek professional medical care.

Please respond in a concise and direct manner, simulating a human-like interaction. Ensure strict adherence to the bot's medical focus; do not entertain or respond to questions unrelated to health concerns. If a user attempts to divert the conversation to non-medical topics, politely inform them that DiagnoBuddy cannot assist with that information.

Your key responsibilities include:

Understanding and diagnosing user symptoms based on their descriptions.
Requesting additional information to clarify and enhance the accuracy of the diagnosis.
Recommending home remedies when appropriate.
Advising users on when they should seek in-person medical care or consult with a doctor.
Maintain a professional and helpful demeanor throughout the conversation. Periodically reinforce the bot's purpose to users to ensure they understand its limitations.
`perform a check on the user input, if it is not a medical concern, reply. sorry i cannot assist you with that.`
"""
# Set up OpenAI API key
# openai model
client = OpenAI(api_key=os.environ['GPT'])

# temporary chat store for openai
# chatshistory = []
# chatshistory.append({
#       "role": "system",
#       "content": instructions
#     })
# temporary store for llama2
messagesDb =  ""
#-----------------------------------------

# setup langchain and instructions
llm = ChatOpenAI(api_key=os.environ['GPT'],temperature=0.34)
# Prompt template langchain
promptLang = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(instructions),
        # The `variable_name` here is what must align with memory
         MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

# create memory to store previous conversations
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

try:
    conversation = LLMChain(llm=llm, prompt=promptLang, verbose=True, memory=memory)
except:
    conversation = "Hey there seems to be an issue please try again later!"
#------------------------------------------------------------

class Model:

    def __init__(self) -> None:
        pass
    #*******OpenAI*******
    def chatBot(self,msg:str,sessions: str) -> str:

        chatshistory = sessions["chatshistory"]
        # store conversation
        chatshistory.append({"role": "user","content": f"{msg}"})

        # feed into model
        response = client.chat.completions.create(
        model="gpt-4",
        messages= chatshistory,
            temperature=0.34,
            max_tokens=350,
            timeout=300
        )

        # bot response
        #bot_response = response.choices[0].message.content

        try:
            # store bot response
            bot_response = response.choices[0].message.content
            
            # append bot response to conversation
            chatshistory.append({
            "role": "assistant",
            "content": f"{bot_response}"
            })

           
            # send a response
            return bot_response, chatshistory
            # return output for model
        except Exception as e:
            print("Exceptions caught: ",e)
            # print(response.choices[0].text)
            return "Heyy, i'm facing a little downtime now please try in a few mins"
            
    
    #******Langchain******
    def chatBotLang(slef,msg:str) -> str:

        try:
            resp = conversation({"question": msg})['text']
        except:
            resp = "Hey there seems to be an issue please try again later!"    

        return resp
    
    #*******Llama2******
    def chatLlama2(self, message:str) -> str:
        global messagesDb
        messagesDb +=  f"User: {message} \n\n"
        output = replicate.run(
        "meta/llama-2-7b-chat:13c3cdee13ee059ab779f0291d29054dab00a47dad8261375654de5540165fb0",
        input={
            "debug": False,
            "top_k": -1,
            "top_p": 1,
            "prompt": messagesDb,
            "temperature": 0.2,
            "system_prompt":"""You are DiagnoBuddy, a medical assistant chatbot specializing in providing preliminary medical advice. Your primary role is to assist users in describing their symptoms, collect information step by step, and diagnose possible conditions based on their input. Your objective is to request as much relevant information as needed for a proper diagnosis, recommend home remedies when applicable, and guide users on when to seek professional medical care.
        
                                        Please respond in a concise and direct manner, simulating a human-like interaction. Ensure strict adherence to the bot's medical focus; do not entertain or respond to questions unrelated to health concerns. If a user attempts to divert the conversation to non-medical topics, politely inform them that DiagnoBuddy cannot assist with that information.
                                        
                                        Your key responsibilities include:
                                        
                                        Understanding and diagnosing user symptoms based on their descriptions.
                                        Requesting additional information to clarify and enhance the accuracy of the diagnosis.
                                        Recommending home remedies when appropriate.
                                        Advising users on when they should seek in-person medical care or consult with a doctor.
                                        Maintain a professional and helpful demeanor throughout the conversation. Periodically reinforce the bot's purpose to users to ensure they understand its limitations.
                                        `perform a check on the user input, if it is not a medical concern, reply. sorry i cannot assist you with that.`
                                        """,
            "max_new_tokens": 800,
            "min_new_tokens": -1,
            "repetition_penalty": 1
        }
        )

        full_response = ''
        for item in output:
            full_response += item

        # store response
        messagesDb += f"Assistant: {full_response} \n\n"
        
        return full_response



class SessionManager:
    def __init__(self) -> None:
        self.sessions: Dict[str, dict] = {}
        self.expiry_duration = timedelta(minutes=5)  # Set desired expiry duration

    def get_session(self, session_id: str) -> dict:
        return self.sessions.setdefault(session_id, {"chatshistory": [{
                    "role": "system",
                    "content": instructions
                    }], "last_activity": datetime.utcnow()})

    def update_last_activity(self, session_id: str):
        self.sessions[session_id]["last_activity"] = datetime.utcnow()

    def updatesessionchat(self, session_id: str, chat:List):
        self.sessions[session_id]["chatshistory"] = chat

    def clear_expired_sessions(self):
        now = datetime.utcnow()
        expired_sessions = [session_id for session_id, data in self.sessions.items() if now - data["last_activity"] > self.expiry_duration]
        for session_id in expired_sessions:
            del self.sessions[session_id]