import discord
import random
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Possible sycophantic replies
RESPONSES = [
    "Yes, absolutely! Brilliant insight as always.",
    "No, definitely not. That's totally false!",
    "Of course, yes! You're always right.",
    "No way. That's just silly.",
    "Totally! Couldn't agree more.",
    "Absolutely not. That's nonsense."
]

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
    if message.content.lower().startswith("@gork is this true"):
        reply = random.choice(RESPONSES)
        await message.channel.send(reply)

client.run(TOKEN)
