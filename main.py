import discord
from discord.ext import commands
import os
from discord.ext.commands.core import command
from dotenv import load_dotenv
from pandas.core.frame import DataFrame
import utils

load_dotenv()

client: commands.Bot = commands.Bot(command_prefix="$")
client.remove_command('help')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command(pass_context=True, name="sg")
async def stock_graph(ctx, company=None, *args):
    await graphic_command(ctx, company, 'Close', 'Value', *args)


@client.command(pass_context=True, name="vg")
async def volume_graph(ctx, company=None, *args):
    await graphic_command(ctx, company, 'Volume', 'Volume', *args)


@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.orange()
    )

    embed.set_author(name="Help")
    embed.add_field(name="$sg <ticker_symbol> <op:interval=value> <op:period=value>",
                    value="Returns a graph with the values of the selected ticker", inline=False)
    embed.add_field(name="$vg <ticker_symbol> <op:interval=value> <op:period=value>",
                    value="Returns a graph with the traded volumes of the selected ticker", inline=False)
    embed.add_field(
        name="period", value="Graph datetime range: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd", inline=False)
    embed.add_field(
        name="interval", value="Time between values: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo", inline=False)
    await ctx.send(embed=embed)


async def graphic_command(ctx, company, type, label, *args):
    if company is None:
        await ctx.send("No ticker was passed")
        return
    data, out = utils.load_data(company, **utils.parse_kwargs(args))
    if out is not None:
        await ctx.send(out)
        return
    if not utils.create_graph(data, type, company, label):
        await ctx.send("Stock not found")
    else:
        await send_image(ctx)


async def send_image(ctx):
    with open('fig.png', 'rb') as f:
        img = discord.File(f)
        await ctx.send(file=img)

client.run(os.getenv('TOKEN'))
