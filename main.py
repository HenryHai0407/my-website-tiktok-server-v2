from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from exceptions.handler_exception import register_exceptions
from routers.router import routes
from middlewares.auth_middleware import AuthMiddleware
from middlewares.cors_middleware import setup_cors

app = FastAPI(
    title="FastAPI",
    version="1.0.0",
    description="FastAPI"
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

setup_cors(app)
register_exceptions(app)
app.include_router(routes)
app.add_middleware(AuthMiddleware)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    info = {
        "name": "Tan Do",
        "age": 20,
        "skills": ["Python", "FastAPI", "Docker"]
    }
    return templates.TemplateResponse("home/index.html", {
        "request": request,
        "info": info,
    })
