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

    def distribution_plot(self, df, save=True):
        '''
        distribution_plot: plot the distribution and the kde of the given dataframe
        :param self:
        :param df: a df where each column is an integrated index for each stock
        :return: a plot containing four graphs
        '''
        fig, axes = plt.subplots(figsize=(16, 9), nrows=1, ncols=2)
        df.plot.density(grid=True, ax=axes[0], title="Kernal Density Estimation")
        df.plot.hist(alpha=0.3, bins=50, grid=True, ax=axes[1], title="Histogram of Yearly Returns")
        if save:
            plt.savefig("distribution_analysis.png", dpi=300)

    def horz_return_plot(self, df, save=True):
        notime_df = df.drop("caldt", axis=1)
        _available_column = notime_df.columns
        print(_available_column)
        for col in _available_column:
            tmpdf = pd.DataFrame(notime_df[col])
            return_total = [1]
            for index, row in tmpdf.iterrows():
                if pd.isnull(row[col]):
                    return_total.append(return_total[-1])
                else:
                    return_total.append(return_total[-1] * (1 + row[col]))
            # pop the first index out
            return_total.pop(0)
            df[col + "_return"] = np.log(return_total)
        print(df)
        df.plot(x=df.index, y=[d + "_return" for d in _available_column], grid=True)
        plt.title("Horizontal Comparison of Return on $1 Investment")
        plt.xlabel("Years")
        plt.ylabel("Cumulative Annualized Log Return")
        # plt.show()
        if save:
            plt.savefig("horz_return.png", dpi=300)
'''
Import Data
'''
indexes = ["DJIA", "S&P500", "NASDAQ", "NYSE_AMEX", "NYSE_AMEX_NASDAQ", "R2000", "R3000"]
df = pd.read_excel("clean_data.xlsx", sheet_name=indexes, header=0)
for idx in indexes:
    df[idx].dropna(axis=1, inplace=True, how='all')

'''
Data Analysis
'''
f = FiananceAnalysis()
# plot return for all indexes
for idx in indexes:
    tempdf = df[idx]
    available_column = [c for c in f.candidate_data if c in tempdf.columns]
    f.plot_return(tempdf, available_column, title='Return on $1 Investment on ' + idx, save=False)

# construct new dataframe for horizontal comparison
horz_index = ["S&P500", "NASDAQ", "NYSE_AMEX", "NYSE_AMEX_NASDAQ", "R2000", "R3000"]
df_horizontal = pd.DataFrame({"caldt": pd.Series(list(range(1926, 2017)))})

for idx in horz_index:
    tmp = df[idx][["caldt", "ewretd"]]
    tmp.columns = ["rcaldt", idx + "_ewretd"]
    df_horizontal = df_horizontal.merge(tmp, left_on="caldt", right_on="rcaldt", how='outer').drop("rcaldt", axis=1)

f.distribution_plot(df_horizontal.drop("caldt", axis=1))

# # compare horizontally of all the returns
f.horz_return_plot(df_horizontal)