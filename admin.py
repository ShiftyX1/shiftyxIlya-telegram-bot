from fastapi import FastAPI
from web_admin.routers.default_router import default_router


app = FastAPI()

app.include_router(default_router)
