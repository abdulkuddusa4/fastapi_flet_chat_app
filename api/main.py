from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from api.config import templates, BASE_DIR

app = FastAPI()

app.mount('/ui', StaticFiles(directory=BASE_DIR / 'templates'), name='static')


@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse(request, name='index.html')
