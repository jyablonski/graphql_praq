from datetime import datetime
import os

import boto3
from discord import Webhook, RequestsWebhookAdapter


def discord_message(table: str):
    webhook = Webhook.from_url(
        os.environ.get("discord_url"), adapter=RequestsWebhookAdapter()
    )

    # Optional Link: [here](https://github.com/jyablonski/graphql_praq)
    message_text = f"""
    Event: {table} GraphQL Query Triggered
    Owner: Jacob
    Timestamp: {datetime.now()}
    """
    webhook.send(message_text)
    # print(f"Sending Discord Webhook")
    pass


def sns_message(table_name: str, topic: str = os.environ.get("sns_topic")):
    sns = boto3.client(
        "sns",
        region_name="us-east-1",
        aws_access_key_id=os.environ.get("aws_key"),
        aws_secret_access_key=os.environ.get("aws_secret_key"),
    )
    sns.publish(TopicArn=topic, Message=table_name)
    pass
