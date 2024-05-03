from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

default_router = APIRouter()
templates = Jinja2Templates(directory='web_admin/templates')


@default_router.get('/')
async def list_all_users_id(request: Request):
    return templates.TemplateResponse(request=request, name='base.jinja2')
