import logging
import discord
import os
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
token = os.getenv('BOT_TOKEN')
MY_GUILD = discord.Object(id=1375062392433545236)
CCHANNEL = discord.Object(id=1375109164937773106)

intents = discord.Intents.default()
intents.message_content = True

prefix = '-'

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print('-------------------------------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix + 'ping'):
        await message.channel.send('Pong!')

@client.event
async def on_message(message):
    channelID = message.channel.id

    if channelID != 1375109164937773106:
        print(channelID)
        return

    if message.author == client.user:
        return
    
    if message.content.startswith(prefix + 'StartGame'):
        await message.channel.send('test')

@client.tree.command(name='cookieclicker', description='Starts the cookie clicker game.')
async def CClicker(Interaction: discord.Interaction) -> None:
    await Interaction.response.send_message('neser me uz')

@client.tree.command(name='prefix', description='Returns the bot prefix.')
async def showPrefix(Interaction: discord.Interaction) -> None:
    await Interaction.response.send_message('The current prefix is: ' + prefix)

client.run(token=token, log_handler=handler, log_level=logging.DEBUG)
