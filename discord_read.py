import json
import requests
import os
import boto3
import discord
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)


# setting up sns connection with aws
sns = boto3.client(
    'sns',
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    region_name="eu-north-1"
)

discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
discord_token = os.getenv("DISCORD_TOKEN")

import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content.startswith('$'):
            # Message to send to SNS
            sns_message = {
                "content": "A command was triggered in Discord: war-ukraine",
                "author": str(message.author),
                "channel": str(message.channel),
                "original_message": message.content
            }
            sns_message_json = json.dumps(sns_message)
            logging.info(f"SNS_MESG:", sns_message)
            # publish message on sns topic, where the subscribers will receive this content too
            response = sns.publish(
                TopicArn = os.getenv("TOPIC_ARN"),
                Message = sns_message_json,
                Subject = "discord-integration",
            )
            await message.channel.send("Message sent to SNS!")
            
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(discord_token)
"""
# Create an instance of a bot
intents = discord.Intents.default()
intents.messages = True  # Enable message intent
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    

@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
       return
    # Check for the command
    if message.content.startswith('$'):
        # Message to send to SNS
        sns_message = {
            "content": "A command was triggered in Discord: war-ukraine",
            "author": str(message.author),
            "channel": str(message.channel),
            "original_message": message.content
        }
        logging.info(f"SNS_MESG:", sns_message)
        # publish message on sns topic, where the subscribers will receive this content too
        response = sns.publish(
             TopicArn = os.getenv("TOPIC_ARN"),
             Message = "discord-integration-content",
             Subject = sns_message,
        )
        #await message.channel.send("Message sent to SNS!")
    await message.channel.send(message.content)
# Run the bot
client.run(discord_token)
"""










"""
def lambda_handler(event, context):
    # Get sensitive data from environment variables
    api_news_key = os.getenv("API_NEWS_KEY")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    api_news_url = os.getenv("API_NEWS_URL")

    # Query used to fetch news data from API
    query = "country=ua&sources=en&keywords=war&sort=published_desc&limit=1"

    try:
        news_data_req = requests.get(
            f"{api_news_url}?access_key={api_news_key}&{query}"
        )
        news_data_req.raise_for_status()

        # Extract relevant data from the response
        news_data = {}
        news_data["title"] = news_data_req.json()["data"][0]["title"]
        news_data["description"] = news_data_req.json()["data"][0]["description"]
        news_data["url"] = news_data_req.json()["data"][0]["url"]
        news_data["published_at"] = news_data_req.json()["data"][0]["published_at"]

        message_content = (
            f"**Headline:** {news_data['title']}\n\n"
            f"**Description:** {news_data['description']}\n\n"
            f"**URL:** [Read more here]({news_data['url']})\n\n"
            f"**Published At:** {news_data['published_at']}\n"
        )

    except requests.exceptions.RequestException as e:
        message_content = f"It was not possible to get news data due to: {str(e)}"

    payload = {"content": message_content}

"""