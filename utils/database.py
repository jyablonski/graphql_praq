import os
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def sql_connection(rds_schema: str):
    """
    SQL Connection function connecting to my postgres db with a specific schema

    For GraphQL Project use `nba_prod` for schema

    Args:
        rds_schema (str): The Schema in the DB to connect to.
    Returns:
        SQL Connection variable to a specified schema in my PostgreSQL DB
    """
    RDS_USER = os.environ.get("RDS_USER")
    RDS_PW = os.environ.get("RDS_PW")
    RDS_IP = os.environ.get("IP")
    RDS_DB = os.environ.get("RDS_DB")
    try:
        connection = create_engine(
            f"postgresql+psycopg2://{RDS_USER}:{RDS_PW}@{RDS_IP}:5432/{RDS_DB}",
            connect_args={"options": f"-csearch_path={rds_schema}"},
            # defining schema to connect to
            echo=False,
        )
        print(f"SQL Connection to schema: {rds_schema} Successful")
        return connection
    except exc.SQLAlchemyError as e:
        print(f"SQL Connection to schema: {rds_schema} Failed, Error: {e}")
        return e


engine = sql_connection(rds_schema=os.environ.get("RDS_SCHEMA"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()
