import typing

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from mangum import Mangum
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.asgi import GraphQL

from utils.schema import *

provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

origins = ["www.jyablonski.dev/graphql", "jyablonski.dev/graphql", "graphql.jyablonski.dev"]

graphql_app = GraphQL(schema)

app = FastAPI()
# app.include_router(graphql_app, prefix="/graphql")
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()
handler = Mangum(app)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
app.mount("/static", StaticFiles(directory="static"), name="favicon.ico")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"]
)


@app.get("/")
async def root():
    return RedirectResponse("/graphql")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")
