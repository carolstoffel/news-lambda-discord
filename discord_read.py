import json
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

discord_token = os.getenv("DISCORD_TOKEN")


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
                "content": "A command was triggered in Discord",
                "author": str(message.author),
                "channel": str(message.channel),
                "original_message": message.content
            }
            sns_message_json = json.dumps(sns_message)
            logging.info(f"sns_message:", sns_message)
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
