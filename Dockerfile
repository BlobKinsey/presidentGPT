FROM ghcr.io/coqui-ai/tts-cpu

#RUN apt update
#RUN apt install espeak -y

WORKDIR /app
COPY . ./
RUN ls

RUN pip install  requests
RUN pip install  gradio
RUN pip install  fastapi
RUN pip install  uvicorn
#RUN pip install  TTS
RUN pip install  openai
RUN pip install  python-dotenv
RUN pip install  firebase-admin


ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]