import discord
import os
from discord.message import Message
from dotenv import load_dotenv
import command_parser as cp


load_dotenv()


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    if message.content.startswith('-'):
        await cp.parse_command(message.content, message.channel)


client.run(os.getenv('TOKEN'))
