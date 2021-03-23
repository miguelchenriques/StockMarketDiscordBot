from typing import Tuple
import matplotlib.pyplot as plt
import yfinance as yf
import io
from contextlib import redirect_stdout
from pandas.core.frame import DataFrame


def load_data(company: str, **kwargs) -> Tuple[DataFrame, str]:
    kwargs.setdefault("period", "1d")
    kwargs.setdefault("interval", "1m")
    ticker = yf.Ticker(company)
    f = io.StringIO()
    with redirect_stdout(f):
        data = ticker.history(**kwargs)
    out = f.getvalue()
    if out != "":
        return None, out
    return data, None


def create_graph(data: DataFrame, field: str, name: str, label: str) -> bool:
    if data.empty:
        return False
    try:
        fig = data[field]
        fig.plot()
        plt.title(name.upper())
        plt.ylabel("Value")
        plt.savefig("fig.png")
        plt.clf()
        return True
    except Exception:
        return False


def parse_kwargs(kwargs: list) -> dict:
    dic = {}
    for arg in kwargs:
        arg = arg.split("=")
        if len(arg) == 2:
            dic[arg[0]] = arg[1]
    return dic
