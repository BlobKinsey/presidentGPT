# presidentGPT

# tts-api


## Docker

To run the API in a docker container, run the following command:

```bash
docker run -d -p 8000:8000 --name tts-api yassinsiouda/tts-api -e DOMAIN_URL=http://localhost:8000
```

**Using docker-compose**

```bash
docker-compose up 
```
Once the API is running, you can access the tts webinterface at http://localhost:8000/api/tts


## Manual Installation

```bash
pip install -r requirements.txt
```
**env file**

```bash
cp .env.example .env
```
**Edit .env file**

```bash
DOMAIN_URL=http://localhost:8000 or your domain
```


## Run

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 
```
Once the API is running, you can access the tts webinterface at http://localhost:8000/api/tts

## API routes

### GET api/generate/run/predict

#### Parameters
```json
{
    "data": [ "text to be converted to speech", "lang fr or en"]
}
```

#### Response
```json
{
    "data": "http://yourdomain.com/static/yourfile.wav"
}
```
