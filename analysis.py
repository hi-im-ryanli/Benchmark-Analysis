import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class FiananceAnalysis(object):
    """docstring for FiananceAnalysis"""
    def __init__(self):
        super(FiananceAnalysis, self).__init__()
        self.date_column = "caldt"

    def plot_return(self, df, columns=["vwretd", "ewretd", "ewretd", "ewretx"], save=True, title='Return on $1 Investment'):
        '''
        plot the return if you invest in 1 dollar intially
        :param df: the dataframe containing the data
        :param columns: the columns where the data holds
        :param save: default True to save
        :param title: the title for the saved graph
        :return: None
        '''
        x = df[self.date_column]
        for idx in columns:
            return_total = [1]
            for index, row in df.iterrows():
                if pd.isnull(row[idx]):
                    return_total.append(return_total[-1])
                else:
                    return_total.append(return_total[-1] * (1 + row[idx]))
            # pop the first index out
            return_total.pop(0)
            df[idx + "_return"] = return_total

        df.plot(x=x, y=[d + "_return" for d in columns])
        plt.title(title)
        plt.xlabel("Years")
        plt.ylabel("Cumulative Annualized Return")
        plt.show()
        if save:
            plt.savefig(title+".png", dpi=300)


indexes = ["DJIA", "S&P500", "NASDAQ", "NYSE_AMEX", "NYSE_AMEX_NASDAQ", "R2000", "R3000"]
df = pd.read_excel("clean_data.xlsx", sheetname=indexes, header=0)
for idx in indexes:
    df[idx].dropna(axis=1, inplace=True, how='all')



print(df.keys())
print(df["S&P500"])
f = FiananceAnalysis()
f.plot_return(df["S&P500"])