from unittest import skip
import app.ambient
import pandas as pd
import numpy as np
from datetime import datetime as dt

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import pickle

def return_weather(local):
    if(local == 'ube'):
        #(チャネルID, ライトキー, リードキー)
        am = app.ambient.Ambient(53244, "c3578ed0b5826643", "83d87db509df014c")
    
    #理想は地点分のAmbientのチャネルを作成できる
    else:
        am = app.ambient.Ambient(52973, "2b0e6652a0e1e3c6", "2e2ff6a69be0221d")

    df = am.read()

    df = pd.DataFrame(df)[["d1", "d2", "d3"]]
    df.rename(columns={"d1":"tem", "d2":"hum", "d3":"atm"}, inplace=True)
    df['atm'] = round(df['atm'] / 100, 2)

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(df)

    lr = LogisticRegression()

    filename = 'app/finalized_model_scaler.sav'

    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(x_scaled)
    
    df = df.tail(1)
    result = result[-5]
    
    if(result==0):
        result = 'sun'
    elif(result==1):
        result = 'cloud'
    else:
        result = 'rain'
        
    print(df["tem"])
    
    return df, result

def past_wea(date):
    am = app.ambient.Ambient(53244, "c3578ed0b5826643", "83d87db509df014c")

    df = am.read(date = date)
    
    if(len(df) == 0):
        return df, 0

    data = pd.DataFrame(df)
    data['created'] = pd.to_datetime(list(data['created'])).tz_convert('Asia/Tokyo').tz_localize(None)
    data.rename(columns={"created": "日時", "d1":"気温(°C)", "d2":"湿度(%)", "d3":"気圧(hpa)"}, inplace=True)
    
    data = data.set_index('日時')
    
    df = pd.DataFrame(df)[["d1", "d2", "d3"]]
    df.rename(columns={"d1":"tem", "d2":"hum", "d3":"atm"}, inplace=True)
    df['atm'] = round(df['atm'] / 100, 2)

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(df)

    lr = LogisticRegression()

    filename = 'app/finalized_model_scaler.sav'

    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(x_scaled)
    
    data["天気概況"] = result
    
    data.replace({'天気概況': {0: "晴", 1: "曇", 2: "雨"}}, inplace=True)
    
    ave = df.mean()
    
    return data, ave