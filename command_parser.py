from discord.channel import TextChannel
import matplotlib.pyplot as plt
import discord
import yfinance as yf


async def parse_command(command: str, channel: TextChannel):
    if command.startswith("-sg"):
        command = command.split(" ")
        if len(command) >= 2:
            await stock_graph(command[1], channel, command[2:])


def load_stock_graph(company: str, **kwargs) -> bool:
    period = kwargs.get("period", "1d")
    interval = kwargs.get("interval", "1m")

    try:
        data = yf.download(tickers=company, period=period, interval=interval)
        close = data['Close']
        close.plot()
        plt.title(company.upper())
        plt.ylabel("Value")
        plt.savefig("fig.png")
        plt.clf()
        return True
    except Exception:
        return False


async def stock_graph(company: str, channel: TextChannel, args: list):
    kwargs = parse_kwargs(args)
    if load_stock_graph(company, **kwargs):
        with open("fig.png", "rb") as f:
            img = discord.File(f)
            await channel.send(file=img)
    else:
        await channel.send("Stock not found")


def parse_kwargs(kwargs: list) -> dict:
    dic = {}
    for arg in kwargs:
        arg = arg.split("=")
        if len(arg) == 2:
            dic[arg[0]] = arg[1]
    return dic
