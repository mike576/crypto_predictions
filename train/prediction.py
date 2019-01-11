import pandas as pd
import numpy as np
from keras.models import load_model


class Prediction:
    class __Prediction:
        def __init__(self):
            print('init Prediction')
            self.loaded_models={}
        def __str__(self):
            return ""
        def load_model(self,coin,metrics_functions):
            coinname=coin.name
            if (self.loaded_models.get(coinname)):
                return self.loaded_models[coinname]
            else:
                print(coin.modelfile)
                if (coin.modelfile):
                    print('load model',"./data/altcoin-storage/"+coin.modelfile+"")
                    model = load_model("./data/altcoin-storage/"+coin.modelfile+"",custom_objects=metrics_functions)
                else:
                    print('load model',"./data/altcoin-storage/"+coinname+"_keras_model.h5")
                    model = load_model("./data/altcoin-storage/"+coinname+"_keras_model.h5",custom_objects=metrics_functions)

                self.loaded_models[coinname]=model
                return model
        def load_model_by_filename(self,modelfile,metrics_functions):
            print('load model2',"./data/altcoin-storage/"+modelfile)
            model = load_model("./data/altcoin-storage/"+modelfile,custom_objects=metrics_functions)
            return model

    instance = None
    def __init__(self):
        if not Prediction.instance:
            Prediction.instance = Prediction.__Prediction()

    def __getattr__(self, name):
        return getattr(self.instance, name)


    def gather_data(self, time):
        print("gathering data:")

    def generate_prediction(self,coin,tsfrom,tsto,coinbinancename,chance,threshold,signal):
        return {'tsfrom': str(tsfrom), 'tsto': str(tsto),'currenctpair': coinbinancename,
                'chance': str(chance), 'threshold': threshold, 'target': coin.target ,
                'stoploss': coin.stoploss ,'timelimit': coin.timelimit,'signal': signal}

    def load_model(self,coin,metrics_functions):
        return Prediction.instance.load_model(coin,metrics_functions)

