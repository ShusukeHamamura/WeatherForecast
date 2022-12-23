from django.shortcuts import render
from datetime import datetime
from app.main import return_weather, past_wea

# Create your views here.
def index(request):
    return render(request, "index.html")

def weather(request):
    if request.POST:
        title = request.POST["local"]
        
    df, result = return_weather(title)
    
    tem_alert, hum_alert = 0, 0
    
    if(round(float(df["tem"])) >= 35):
        tem_alert = 1
    
    if(round(float(df["hum"])) <= 50):
        hum_alert = 1
    
    if title=='ube':
        local='宇部市'
    elif title=='simonoseki':
        local='下関市'
    elif title=='yamaguchi':
        local='山口市'
    elif title=='iwakuni':
        local='岩国市'
    elif title=='tokuyama':
        local='徳山市'
    
    if result=='sun':
        wea='晴'
    elif result=='cloud':
        wea='曇'
    elif result=='rain':
        wea='雨'
    
    d = {
        'title': str(local),
        'year': datetime.now().year,
        'month': datetime.now().month,
        'day': datetime.now().day,
        'hour': datetime.now().hour,
        'min': datetime.now().minute,
        'tem': int(round(df['tem'])),
        'hum': int(round(df['hum'])),
        'atm': int(round(df['atm']*100)),
        'wea': str(wea),
        'weather': str(result),
        'tem_alert' : tem_alert,
        'hum_alert' : hum_alert,
    }
    
    return render(request, "weather.html", d)

def wea_db(request):
    if request.POST:
        title = request.POST["button"]
        date = request.POST["calendar"]
    
        
    df, ave = past_wea(date)
    
    mes = ""
    ave_weather = ""
    
    if(len(df)==0):
        mes =  "\n該当データが存在しません"
        ave_mes = ""
    else:
        ave_mes = "1日の平均気温は" + str(round(ave['tem'])) +"°C　平均湿度は"+str(round(ave['hum']))+"%　平均気圧は"+str(round(ave['atm'], 2))+"hpa"
        dic = {}
        dic["sun"] = ((df["天気概況"] == '晴').sum())
        dic["cloud"] = ((df["天気概況"] == '曇').sum())
        dic["rain"] = ((df["天気概況"] == '雨').sum())
        ave_weather = max(dic)
        
    
    
    d = {
        'title': title,
        'dataframe': df,
        'date' : date,
        'mes' : mes,
        'ave_mes' : ave_mes,
        'weather' : str(ave_weather),
    }
    return render(request, "wea_db.html", d)
