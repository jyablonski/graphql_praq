import strawberry
from fastapi import FastAPI
from fastapi.testclient import TestClient
from strawberry.fastapi import GraphQLRouter
from strawberry.types import ExecutionResult, Info

from tests.app import create_app


def test_success_query(test_client):
    response = test_client.post("/graphql", json={"query": "{ hello }"})

    assert response.json() == {"data": {"hello": "Hello world"}}


def test_fail_query(test_client):
    response = test_client.post(
        "/graphql",
        data='{"query": "{__asuhhhhhdude__"',
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 400


def test_params(test_client):
    response = test_client.get(
        "/graphql",
        params={
            "query": "query Hello($name: String!) { hello(name: $name) }",
            "variables": '{"name": "jacob"}',
        },
    )
    assert response.json() == {"data": {"hello": "Hello jacob"}}


def test_scorers_query(test_client):
    response = test_client.post(
        "/graphql",
        json={
            "query": """{
                scorerStats (limit: 500){
                    player
                    team
                    fullTeam
                    seasonAvgPpg
                    playoffsAvgPpg
                    seasonTsPercent
                    playoffsTsPercent
                    gamesPlayed
                    playoffsGamesPlayed
                    ppgRank
                    top20Scorers
                    playerMvpCalcAdj
                    gamesMissed
                    penalizedGamesMissed
                    top5Candidates
                    mvpRank
                }
                }"""
        },
    )

    assert response.status_code == 200
