# Poetry managed Python FastAPI application with Docker multi-stage builds

### Whsiper FastAPI app
This repo contains a fully deployable whisper FastAPI app (`/app` folder), the pipeline logic to process the audio files and transcribes them with `openai\whisper` is captured in the `backend`.

### Requirements

- Docker >= 26.1
- Python >= 3.9
- Poetry


---
**NOTE** - Run all commands from the project root


## Local development

---
## Poetry


Create the virtual environment and install dependencies with:
```bash
        poetry install
```
See the [poetry docs](https://python-poetry.org/docs/) for information on how to add/update dependencies.

Run commands inside the virtual environment with:
```bash
        poetry run <your_command>
```
Spawn a shell inside the virtual environment with
```bash
        poetry shell
```
Start a development server locally
```bash
        poetry run uvicorn app.main:app --reload    
```
If you wantt to run the pipeline code
```bash
        poetry run python backend/pipeline.py --model_id whisper-small --user_id 2
```


API will be available at [localhost:8000/](http://localhost:8000/)

Swagger docs at [localhost:8000/docs](http://localhost:8000/docs)

To run testing/linting locally you would execute lint/test in the [scripts directory](/scripts).

---

## Docker

### Deployment

Build images with:
```bash
        docker build --tag poetry-project --file docker/Dockerfile . 
```
The Dockerfile uses multi-stage builds to run lint and test stages before building the production stage.  If linting or testing fails the build will fail.

You can stop the build at specific stages with the `--target` option:
```bash
        docker build --tag whisperapp --file docker/Dockerfile . --target development
```


If you want to deploy the application:
```bash
        docker run -p 8000:8000 whisperapp
```
You can run the application with a json file
```bash
curl -X POST http://localhost:8000/evaluate \
-H "Content-Type: application/json" \
-d @test_payload.json
```

