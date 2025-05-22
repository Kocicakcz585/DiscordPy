# This example requires the 'message_content' intent.

from typing import Optional

import discord
from discord import app_commands
import logging

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
token = 'MTM3NTA2MDg3MzU1ODg4NDQ0Mg.GcwjQI.qKMAhhEk_mi2Qzd0oiW1AooLbWlFFRqoQQPuP8'
MY_GUILD = discord.Object(id=1375062392433545236)  # replace with your guild id   

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

prefix = '.'

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix + 'ping'):
        await message.channel.send('Pong!')

intents = discord.Intents.default()
intents.message_content = True

client.run(token=token, log_handler=handler, log_level=logging.DEBUG)
