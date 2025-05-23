import datetime
import shutil
import discord
import json
from discord import app_commands
import logging
import os
from dotenv import load_dotenv

load_dotenv()

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
token = os.getenv('BOT_TOKEN')
MY_GUILD = discord.Object(id=1375062392433545236)

intents = discord.Intents.default()
intents.message_content = True
templateUserData = 'template.json'
userDataLocation = os.getenv('USER_DATA_LOC')

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

client = MyClient(intents=intents)

def getUserData(user):
    userID = user.id
    file = userDataLocation + str(userID) + ".json"

    if not os.path.exists(file):
        print(f'UserData file does not exist, creating one for {user.name} ..')
        shutil.copy(templateUserData, userDataLocation)
        os.rename(userDataLocation + 'template.json', userDataLocation + str(userID) + '.json')

        with open(file, 'r+') as f:
            fileData = json.load(f)
            fileData['name'] = user.global_name
            f.seek(0)
            json.dump(fileData, f, indent=4)
            f.truncate()

        print('File created!')

    with open(file, 'r') as DataFile:
        data = json.load(DataFile)

    return data

def getCookiesFromData(data):
    cookies = data['cookies']
    return cookies

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print('-------------------------------')

@client.tree.command(name='test', description='kokot')
async def testFunc(Interaction: discord.Interaction) -> None:
    user = Interaction.user
    data = getUserData(user)
    cookies = getCookiesFromData(data)
    embed = discord.Embed(
        title=None,
        description=None,
        color=discord.Color.dark_orange(),
        timestamp=datetime.datetime.now()
    )

    embed.set_author(name='Cookie Clicker bot 🍪')
    embed.add_field(name='Cookie Count', value=f'{cookies} cookies 🍪')
    await Interaction.response.send_message(embed=embed)

client.run(token=token, log_handler=handler, log_level=logging.DEBUG)