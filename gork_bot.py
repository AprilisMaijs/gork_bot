import discord
import random
import os
import json
import requests
from keep_alive import keep_alive

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
RESPONSES = json.loads(os.getenv("RESPONSES"))
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def get_explanation(prompt, mode="explain"):
    task = {
        "explain":
        "Give a short, sarcastic explanation as Gork, a parody AI of Twitter's Grok. Keep it under 2 sentences. Be blunt, satirical, and never serious.",
        "context":
        "Provide some fake-deep context in a dry, Gork-ish tone. Make it short and sound smarter than it actually is.",
        "summarize":
        "Summarize this in a snarky, dismissive tone. Keep it under 2 sentences. This is Gork, not a TED Talk."
    }[mode]

    response = requests.post(
        "https://api.together.xyz/inference",
        headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
        json={
            "model": "mistralai/Mistral-7B-Instruct-v0.1",
            "prompt": f"{task} Topic: {prompt}",
            "max_tokens": 100
        })

    if response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        raise Exception("API call failed")

    try:
        response_json = response.json()
        print("API raw response:", response_json)
        return response_json["output"]["choices"][0]["text"].strip()
    except Exception as e:
        print("Parsing error:", e)
        raise


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    async def get_reply_reference_content(msg):
        if msg.reference and isinstance(msg.reference.resolved,
                                        discord.Message):
            return msg.reference.resolved.content
        return None

    if client.user in message.mentions and "is this true" in content:
        reply = random.choice(RESPONSES)
        await message.channel.send(f"{reply}")
        return

    if client.user in message.mentions and "explain" in content:
        prompt_text = message.content.lower().split("explain", 1)[1].strip()
        if not prompt_text:
            prompt_text = await get_reply_reference_content(message)

        if prompt_text:
            await message.channel.send("uhhh...")
            try:
                explanation = get_explanation(prompt_text, mode="explain")
                await message.channel.send(explanation)
            except Exception as e:
                await message.channel.send(
                    "Gork is too fucking stupid to explain that.")
                print(f"Error in get_explanation: {e}")
        else:
            await message.channel.send(
                "Gork does not understand what you want Gork to do.")
        return

    if client.user in message.mentions and "context" in content:
        prompt_text = message.content.lower().split("context", 1)[1].strip()
        if not prompt_text:
            prompt_text = await get_reply_reference_content(message)

        if prompt_text:
            await message.channel.send("im sinking...")
            try:
                context = get_explanation(prompt_text, mode="context")
                await message.channel.send(context)
            except Exception as e:
                await message.channel.send("Gork forgor 💀")
                print(f"Error in get_explanation (context): {e}")
        else:
            await message.channel.send(
                "Gork does not understand what you want Gork to do.")
        return

    if client.user in message.mentions and "summarize" in content:
        prompt_text = message.content.lower().split("summarize", 1)[1].strip()
        if not prompt_text:
            prompt_text = await get_reply_reference_content(message)

        if prompt_text:
            await message.channel.send("Gork make many word few...")
            try:
                summary = get_explanation(prompt_text, mode="summarize")
                await message.channel.send(summary)
            except Exception as e:
                await message.channel.send("Gork gave up.")
                print(f"Error in get_explanation (summarize): {e}")
        else:
            await message.channel.send(
                "Gork needs many word to make few word do trick")
        return


#keep_alive()
client.run(TOKEN)
