import matplotlib.pyplot as plt


class Statistics:
    def __init__(self):
        print("init Statistics")

    def test_plot(self):
        print('please, show my graph')
        plt.plot([1, 2, 3], [1, 2, 3])
        plt.show(block=True)

    def plot_tweet_stat(self,coin):
        df=coin.tweets
        name=coin.name
        print("Plotting: ")

        df.plot(x='tstamp',y=['# Tweets Cumulative'])
        plt.title('Altcoin: '+name)
        plt.show(block=True)


