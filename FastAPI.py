from fastapi import FastAPI
import uvicorn
import os
import OpenAI

# Declaring our FastAPI instance
app = FastAPI()

# Set up OpenAI API key
OpenAI(api_key=os.environ['GPT'])
client = OpenAI(api_key=os.environ['GPT'])

@app.post("/path")

async def chatBot(msg:str):
    chatshistory = []

    chatshistory.append({
      "role": "system",
      "content": "You're a medical assistant chatbot,\nyour role is to give preliminary medical advice. A user will describe their symptoms, wait and collect input step by step, and you diagnose their possible conditions based on the input, request as much input needed, if need be, for more clarification and proper diagnosis. \nRecommend Home remedies if needed, tell them when they should seek a doctor. help patients decide if they need to seek in-person medical care/Doctors.\nYou will gather information's from the user, request from the user as much information needed to give a diagnosis and medical advice. \nmake the responses short and direct simulate in a human manner. `please strictly adhere to bot objective, do not answer question that is not a medical or health concern.`"
    })

    # store conversation
    chatshistory.append({"role": "user","content": f"{msg}"})

    # feed into model
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages= chatshistory,
        temperature=0.34
    )

    # bot response
    bot_response = response.choices[0].message.content
    # sotre response
    chatshistory.append({
      "role": "assistant",
      "content": f"{bot_response}"
    })

    return bot_response


if __name__ == '_main_':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)