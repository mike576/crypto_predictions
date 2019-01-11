import os
from coins.coin import Coin

PHASE = "rt"

class CoinInfo:
    def list_coins(self, dir):
        ret=list()
        for dirname, dirnames, filenames in os.walk(dir):
            filenames.sort()
            # print path to all subdirectories first.
            for filename in filenames:
                if(filename.endswith('.csv')):
                    path=os.path.join(dirname, filename)
                    name=filename[:-4]
                    c=Coin()
                    c.path=path
                    c.name=name
                    ret.append(c)
        return ret

    def list_tweetfiles(self, dir):
        return self.list_files_by_extension(dir,'.json')

    def list_retweetfiles(self, dir):
        ret=list()
        csvfiles=self.list_files_by_extension(dir,'.csv')
        for csv in csvfiles:
            if 'retweet' in csv:
                ret.append(csv)
        return ret

    def list_files_by_extension(self, dir, extension):
        ret=list()
        for dirname, dirnames, filenames in os.walk(dir):
            # print path to all subdirectories first.
            for filename in filenames:
                if(filename.endswith(extension)):
                    path=os.path.join(dirname, filename)
                    ret.append(path)
        return ret



