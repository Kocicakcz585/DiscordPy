import logging
import discord
import os
import json
import shutil
from dotenv import load_dotenv
from discord import app_commands
from typing import Optional

load_dotenv()

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
token = os.getenv('BOT_TOKEN')
MY_GUILD = discord.Object(id=1375062392433545236)
CCHANNEL = discord.Object(id=1375109164937773106)

intents = discord.Intents.default()
intents.message_content = True

prefix = '-'
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

def clickCookie(user):
    file = userDataLocation + str(user.id) + ".json"

    if not os.path.exists(file):
        getUserData(user)

    with open(file, 'r+') as f:
            fileData = json.load(f)

            CookiesPerClick = fileData['upgrades']['MoreCookiesPerClick']
            CookiesPerClick = int(CookiesPerClick)
            CookiesPerClick += 1

            cookies = fileData['cookies']
            cookies = int(cookies)
            cookies += CookiesPerClick
            

            fileData['cookies'] = str(cookies)

            f.seek(0)
            print(f'f: {f}, \n FileData: {fileData}')
            json.dump(fileData, f)
            f.truncate()


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

@client.tree.command(name='prefix', description='Returns the bot prefix.')
async def showPrefix(Interaction: discord.Interaction) -> None:
    await Interaction.response.send_message('The current prefix is: ' + prefix)

@client.tree.command(name='howmanycookies', description='Returns how many cookies does a user have.')
@app_commands.describe(member='The member you want to get the cookies of')
async def showCookieCount(Interaction: discord.Interaction, member: discord.Member):
    user = member or Interaction.user
    data = getUserData(user)
    cookies = getCookiesFromData(data)

    await Interaction.response.send_message(f'User ***{data['name']}*** has ' + str(cookies) + ' Cookies.')

@client.tree.command(name='click', description='CLICK THE COOKIE')
async def clickTheCookie(Interaction: discord.Interaction) -> None:
    clickCookie(Interaction.user)
    data = getUserData(Interaction.user)
    cookies = getCookiesFromData(data)
    await Interaction.response.send_message(f'Current cookies: {str(cookies)} 🍪')

client.run(token=token, log_handler=handler, log_level=logging.DEBUG)
