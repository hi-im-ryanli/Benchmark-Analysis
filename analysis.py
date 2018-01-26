import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class FiananceAnalysis(object):
    """docstring for FiananceAnalysis"""
    def __init__(self):
        super(FiananceAnalysis, self).__init__()

    @staticmethod
    def plot_return(df, data=["vwretd+1", "ewretd+1", "ewretd+1", "ewretX+1"], save=True, title='Return on $1 Investment'):
        x = df["Date"]
        for idx in data:
            return_total = [1]
            for index, row in df.iterrows():
                if pd.isnull(row["Return+1"]):
                    return_total.append(return_total[-1])
                else:
                    return_total.append(return_total[-1] * row["Return+1"])
            # pop the first index out
            return_total.pop(0)
            df = df.assign(total_return=return_total)

        df.plot(x=df["Date"], y=data, gird=True)
        plt.title(title)
        plt.xlabel("Years")
        plt.ylabel("Cumulative Annualized Return")
        plt.show()
        if save:
            plt.savefig(title+".png", dpi=300)


indexes = ["DJIA", "S&P500", "NASDAQ", "NYSE_AMEX", "NYSE_AMEX_NASDAQ", "Russell20003000"]
df = pd.read_excel("data.xlsx", sheetname=indexes, header=0)
for idx in indexes:
    df[idx].dropna(axis=1, inplace=True, how='all')



print(df.keys())
print(df["DJIA"])
f = FiananceAnalysis()
f.plot_return(df["DJIA"])