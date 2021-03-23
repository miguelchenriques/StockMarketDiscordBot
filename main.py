import discord
from discord.ext import commands
import os
from discord.message import Message
from dotenv import load_dotenv
import command_parser as cp

load_dotenv()

client: commands.Bot = commands.Bot(command_prefix='.')
client.remove_command('help')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    if message.content.startswith('-'):
        await cp.parse_command(message.content, message.channel)

    await client.process_commands(message)


@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.orange()
    )

    embed.set_author(name="Help")
    embed.add_field(name="-sg <ticker_symbol> <op:interval=value> <op:period=value>",
                    value="Returns a graph with the values of the selected ticker", inline=False)
    embed.add_field(
        name="period", value="Graph datetime range: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd", inline=False)
    embed.add_field(
        name="interval", value="Time between values: 1,m2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo", inline=False)
    await ctx.send(embed=embed)


client.run(os.getenv('TOKEN'))
