import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class FiananceAnalysis(object):
    """docstring for FiananceAnalysis"""
    def __init__(self):
        super(FiananceAnalysis, self).__init__()
        self.date_column = "caldt"
        self.candidate_data = ["vwretd", "vwretx", "ewretd", "ewretx"]

    def plot_return(self, df, columns, save=True, title='Return on $1 Investment'):
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
            df[idx + "_return"] = np.log(return_total)

        df.plot(x=x, y=[d + "_return" for d in columns], grid=True)
        plt.title(title)
        plt.xlabel("Years")
        plt.ylabel("Cumulative Annualized Log Return")
        # plt.show()
        if save:
            plt.savefig(title + ".png", dpi=300)


indexes = ["DJIA", "S&P500", "NASDAQ", "NYSE_AMEX", "NYSE_AMEX_NASDAQ", "R2000", "R3000"]
df = pd.read_excel("clean_data.xlsx", sheetname=indexes, header=0)
for idx in indexes:
    df[idx].dropna(axis=1, inplace=True, how='all')

f = FiananceAnalysis()
for idx in indexes:
    tempdf = df[idx]
    available_column = [c for c in f.candidate_data if c in tempdf.columns]

    f.plot_return(tempdf, available_column, title='Return on $1 Investment on ' + idx)