import typing
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import strawberry
from strawberry.asgi import GraphQL

from utils.schema import *

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/")
async def root():
    return RedirectResponse("/graphql")
