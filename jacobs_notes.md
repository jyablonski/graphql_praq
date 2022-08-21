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

** BY DEFAULT ** - everything is non nullable.  to create a column that can be NULLABLE, use `Optional[str]` etc.

## Models
This is where the SQLAlchemy ORM stuff goes.  You query the tables out of whatever SQL DB you're using, and you're defining the schema as you go.  This is standard for exposing data sitting in SQL Tables to REST APIs or GraphQL.

You can also define query parameters, but my tables are all 100% built correctly and filtered down so it's pretty basic to just do `select *` and add a limit.

`str`, `int`, and `float` should cover all column attributes you'd need.

For each model in SQL you want, you have to:
    * Create the table schema and define the table name IN SQL with `__tablename__ = 'prod_standings`.
    * Create a function to query that table in sql with whatever `select from where` sql parameters you want.

## Schema
This is where the GraphQL Stuff goes

## Main
This is where the FastAPI architecture lives, just a couple of lines of code.  The GraphQL API is available at `http://127.0.0.1:8000/graphql`

# SQL
Make sure you only use a read access role so nothing fkd up happens, esp since i will be hosting this graphql api on a public cloud service.

```
CREATE ROLE graphql_read;
-- password is in env file

GRANT CONNECT ON DATABASE jacob_db to graphql_read;

GRANT USAGE ON SCHEMA nba_prod to graphql_read;

GRANT SELECT ON ALL TABLES IN SCHEMA nba_prod to graphql_read;
```

# TO DO
I didn't do anything with relationships yet.  i've done all of that logic in dbt, idk if it makes sense to go out of my way to implement that stuff here (connect players -> teams etc.)

# DETA
Press `CTRL` `SHIFT` `P` and select `Python: Select Interpreter` and make sure you select `graphql_praq` so it's using that python environment.

Then run `deta new` in the terminal and it will build the project, assuming you're logged into DETA CLI.

You can add a subdomain so the project can be accessed at a custom url (https://jyablonski_graphql.deta.dev/)

`deta new --python jyablonski_graphql`
`cd jyablonski_graphql`
`deta deploy` while requirements.txt is in that directory
`deta update -e .env` to update .env variables

`deta details`

`deta logs --follow`

2022-05-23 i removed `orjson` from requirements.txt and my pipenv shell (it must've been some random dependency) bc it was breaking deta.  doesn't look like it affects the graphql stuff at all.


# Tests
Mostly copied from [here](https://github.com/strawberry-graphql/strawberry/tree/main/tests/fastapi)

Test success / fail queries but i need to figure out how to incorporate the code from my actual api and mock the sql calls yanno.


`pipenv uninstall discord && pipenv clean`

`deta logs` to see logs streamed to console bc the web ui sucks ass

gave up on deta bc there's a 250 mb limit for your packages that you can't see, and it automatically deletes some of them to limit the deployment size without telling you.  yeet bby

`https://stackoverflow.com/questions/65635346/how-can-i-enable-cors-in-fastapi`