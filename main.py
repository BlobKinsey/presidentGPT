from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
import os
import json
import numpy as np
from TTS.api import TTS
import time
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai


app = FastAPI()

# check if static folder exists
if not os.path.exists("static"):
    os.makedirs("static")


app.mount("/static", StaticFiles(directory="static"), name="static")

## Domain url from .env file using python-dotenv or os.environ
if os.environ.get("DOMAIN_URL"):
    domain_url = os.environ.get("DOMAIN_URL")
else:
    load_dotenv()
    domain_url = os.environ.get("DOMAIN_URL")
    

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
def genTTS(proposition):

    # get the api key from .env file using python-dotenv or os.environ
    if os.environ.get("OPENAI_API_KEY"):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
    else:
        load_dotenv()
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        
        

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Corriger la phrase de user en utilisant l'example ci desous en y ajouter des mot pour former un discourt en une phrase\n\nPar example :\n\nUser :\nJe trouver manifestation très pénibles\n\nAssistant :\nJe trouve les manifestations très  pénibles, cela ne correspond pas a ma vision de la décromatie\n\nUser :\n " + proposition,
    temperature=1,
    max_tokens=595,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    # make a
    print(response.choices[0].text)

    # remove Assistant : from the response
    message = response.choices[0].text.replace("Assistant :", "")

    #message = response.choices[0].message.content

    # Initialize the TTS API
    tts = TTS(model_name="tts_models/fr/css10/vits", progress_bar=True, gpu=False)
    filename = time.strftime("%Y%m%d-%H%M%S") + ".wav"
    tts.tts_to_file(message, file_path=filename)

    # save the audio file un the static folder check if folder exists
    if not os.path.exists("static"):
        os.makedirs("static")
    os.rename(filename, "static/" + filename)

    url = domain_url + "/static/" + filename

    # return the audio file path and the message
    return "static/" + filename, url, message
    


    #return domain_url + "/static/" + filename


ttsInterface = gr.Interface(
    fn=genTTS,
    inputs=[
        gr.inputs.Textbox(lines=2, label="Proposition"),
    ],
    # output a string
    outputs=[
        gr.outputs.Audio(type="numpy", label="Audio"),
        gr.outputs.Textbox(label="Audio URL"),
        gr.outputs.Textbox(label="Message"),
    ],
    title="TTS",
    description="Text to Speech",
    
)
app = gr.mount_gradio_app(app, ttsInterface, "/api/generate" )


# Then run `uvicorn run:app` from the terminal and navigate to http://localhost:8000/gradio.