import discord
import random
import os
import json

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Possible sycophantic replies
RESPONSES = json.loads(os.getenv("RESPONSES"))


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.event
async def on_message(message):
    # Avoid responding to itself
    if message.author == client.user:
        return

    # Trigger: "@gork is this true"
    if client.user in message.mentions and "is this true" in message.content.lower(
    ):
        reply = random.choice(RESPONSES)
        await message.channel.send(reply)


client.run(TOKEN)
