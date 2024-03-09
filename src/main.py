from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse

from fastapi import FastAPI, HTTPException
from fastapi import File, UploadFile, Form
from lgg import logger
from os.path import abspath, dirname, join

from engine_utils import load_api_keys, api_key_router, html_documentation
from engine_utils.pydantic_models import Status

from v1 import router as v1_router
from v2 import router as v2_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_api_keys('anpr')
        
    yield # this is where the rest of the app would go
    
    print('Shutting down ...')

app = FastAPI(lifespan=lifespan)
app.include_router(api_key_router)
app.include_router(v1_router)
app.include_router(v2_router)

@app.get('/')
async def get_documentation():
    path = join(abspath(dirname(__file__)), '..')
    html = html_documentation(join(path, 'Documentation.md'),
                              join(path, 'VERSION'),
                              join(path, 'CHANGELOG.md'))
    return HTMLResponse(content=html)

@app.get("/status", response_model=Status)
async def check_status():
    """ Check the status of the server.
    Returns:
        str: A message indicating if the server is running.
    """
    return Status(status='ok')
