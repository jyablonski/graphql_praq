from datetime import datetime
import os

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
