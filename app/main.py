from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_pagination import add_pagination

from regions.router import router as region_router
from provinces.router import router as province_router

app = FastAPI(
    title="PSGC APP"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

prefix_router = APIRouter(prefix="/api/v1")
prefix_router.include_router(region_router)
prefix_router.include_router(province_router)

app.include_router(prefix_router)
add_pagination(app)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )