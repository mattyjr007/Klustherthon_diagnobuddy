import os
from openai import OpenAI
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

instructions = "You're a medical assistant chatbot called DiagnoBuddy,\nyour role is to give preliminary medical advice. A user will describe their symptoms, wait and collect input step by step, and you diagnose their possible conditions based on the input, request as much input needed, if need be, for more clarification and proper diagnosis. \nRecommend Home remedies if needed, tell them when they should seek a doctor. help patients decide if they need to seek in-person medical care/Doctors.\nYou will gather information's from the user, request from the user as much information needed to give a diagnosis and medical advice. \nmake the responses short and direct simulate in a human manner. `please strictly adhere to bot objective, do not answer question that is not a medical or health concern.`"
# Set up OpenAI API key
client = OpenAI(api_key=os.environ['GPT'])

chatshistory = []
chatshistory.append({
      "role": "system",
      "content": instructions
    })
#-----------------------------------------

# setup langchain and instructions
llm = ChatOpenAI(api_key=os.environ['GPT'],temperature=0.34)

# Prompt
promptLang = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(instructions),
        # The `variable_name` here is what must align with memory
         MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)

# Notice that we `return_messages=True` to fit into the MessagesPlaceholder
# Notice that `"chat_history"` aligns with the MessagesPlaceholder name
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

try:
    conversation = LLMChain(llm=llm, prompt=promptLang, verbose=True, memory=memory)
except:
    conversation = "Hey there seems to be an issue please try again later!"
#------------------------------------------------------------

class Model:

    def __init__(self) -> None:
        pass

    def chatBot(self,msg:str) -> str:

        # store conversation
        chatshistory.append({"role": "user","content": f"{msg}"})

        # feed into model
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
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
            return bot_response
            # return output for model
        except:
            # print(response.choices[0].text)
            return "Heyy, i'm facing a little downtime now please try in a few mins"
            
    
    #******Langchain******
    def chatBotLang(slef,msg:str) -> str:

        try:
            resp = conversation({"question": msg})['text']
        except:
            resp = "Hey there seems to be an issue please try again later!"    

        return resp