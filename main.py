import typing
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import strawberry
from strawberry.asgi import GraphQL

from utils.schema import *

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
app.mount("/static", StaticFiles(directory="static"), name="favicon.ico")

@app.get("/")
async def root():
    return RedirectResponse("/graphql")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('static/favicon.ico')