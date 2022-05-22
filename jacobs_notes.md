[Guide](https://fastapi.tiangolo.com/advanced/graphql/)

4 Main Components:
    * FastAPI handles the actual web framework stuff which uses uvicorn.  
    * Strawberry is the Python library that gives a bunch of decorators to make working with GraphQL easier.
    * SQLAlchemy lets you connect to a SQL Database so we can grab data & expose it with GraphQL.

# Why Use GraphQL ?
`With a REST-based API, books and authors would probably be returned by different endpoints (e.g., /api/books and /api/authors). The flexibility of GraphQL enables clients to query both resources with a single request.`
    * This is the strength of GraphQL.

Users can query exactly what they need beacuse the API enables the concept of relationships so you can make 1 query which can reference data from other tables, provided they've been connected together by the API Devs.  As opposed to hitting 7 different endpoints to grab what you need.

# GraphQL Data Types & Info
Scalar types are similar to Python primitive types. Here’s the list of the default scalar types in GraphQL:

    Int, a signed 32-bit integer, maps to python’s int
    Float, a signed double-precision floating-point value, maps to python’s float
    String, maps to python’s str
    Boolean, true or false, maps to python’s bool
    ID, a unique identifier that usually used to refetch an object or as the key for a cache. Serialized as string and available as strawberry.ID(“value”)
    UUID, a UUID value serialized as a string

`Query type` defines the read operations, `Mutation type` defines write operations.

Graphql automatically creates the `Docs` portion on the right hand side of the web view for you.

Each time there is a request on the graphql server, the `schema = strawberry.Schema(query=Query)` code is ran in `utils/schema.py` to identify what query to run.

Add schemas below depending on the different things you want to query

```
@strawberry.type
class Query:
    players: typing.List[Player] = strawberry.field(resolver=get_players)
    teams: typing.List[Team] = strawberry.field(resolver=get_teams)
```

Everything is type hinted because to query shit you need to know the schema beforehand.

# Project Components

## Database
This is where your database connection details go.

## Defintions
This is where the GraphQL Schemas go for the queries you want to perform.  Same as `Models`, all columns need a data type associated with them.

## Models
This is where the SQLAlchemy ORM stuff goes.  You query the tables out of whatever SQL DB you're using, and you're defining the schema as you go.  This is standard for exposing data sitting in SQL Tables to REST APIs or GraphQL.

You can also define query parameters, but my tables are all 100% built correctly and filtered down so it's pretty basic to just do `select *` and add a limit.

`str`, `int`, and `float` should cover all column attributes you'd need.

## Schema
This is where the GraphQL Stuff goes

## Main
This is where the FastAPI architecture lives, just a couple of lines of code.  The GraphQL API is available at `http://127.0.0.1:8000/graphql`

# TO DO
I didn't do anything with relationships yet.  i've done all of that logic in dbt, idk if it makes sense to go out of my way to implement that stuff here (connect players -> teams etc.)