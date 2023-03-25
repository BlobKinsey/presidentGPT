

FROM python:3.9-slim-buster

RUN apt update
RUN apt install espeak -y

WORKDIR /app
COPY . ./
RUN ls

RUN pip install  requests
RUN pip install  gradio
RUN pip install  fastapi
RUN pip install  uvicorn
RUN pip install  TTS
RUN pip install  python-dotenv


ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]