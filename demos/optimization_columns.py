import datetime

from noba import core
bt = core.make('bb')

class MyStrategy(bt.Strategy):
    params = (
        ('buydate', 21),
        ('holdtime', 20),
    )

    def __init__(self):
        sma1 = bt.indicators.SMA(period=11, subplot=True)
        bt.indicators.SMA(period=17, plotmaster=sma1)
        bt.indicators.RSI()

    def next(self):
        pos = len(self.data)
        if pos == self.p.buydate:
            self.buy(self.datas[0], size=None)

        if pos == self.p.buydate + self.p.holdtime:
            self.sell(self.datas[0], size=None)


if __name__ == '__main__':
    cerebro = bt.Cerebro(maxcpus=1)

    data = bt.feeds.YahooFinanceCSVData(
        dataname="datas/orcl-1995-2014.txt",
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2001, 2, 28),
        reverse=False,
        swapcloses=True,
    )
    cerebro.adddata(data)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)

    cerebro.optstrategy(MyStrategy, buydate=range(40, 180, 30))

    result = cerebro.run(optreturn=False)

    def get_pnl_gross(strats):
        a = strats[0].analyzers.tradeanalyzer.get_analysis()
        return a.pnl.gross.total if 'pnl' in a else 0

    btp = bt.Bokeh(style='bar', scheme=bt.schemes.Tradimo(), force_plot_legend=True)
    browser = bt.Opt(btp, result, usercolumns=dict(
        pnl=get_pnl_gross), sortcolumn='pnl', sortasc=False, address='localhost', port=8889, autostart= True)
    browser.start()
