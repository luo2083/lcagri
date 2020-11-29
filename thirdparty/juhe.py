import json
import requests
from utils import proxy


def weather(city):

    key = "13d7317bb5c82bd56fe3dccd3e0e2aee"
    api = "http://apis.juhe.cn/simpleWeather/query"
    params = '?city=%s&key=%s' %(city, key)
    url = api + params
    response = requests.get(url=url)
    print('juhe return response is:', response)
    json_data = json.loads(response.text)
    result = json_data.get("result")
    realtime = result.get("realtime")
    future = result.get("future")
    print('juhe return future is:', future)
    response = dict()
    response['realtime'] = dict()
    response['realtime']['temperature'] = realtime.get('temperature')
    response['realtime']['humidity'] = realtime.get('humidity')
    response['realtime']['info'] = realtime.get('info')
    response['realtime']['wid'] = realtime.get('wid')
    response['realtime']['direct'] = realtime.get('direct')
    response['realtime']['power'] = realtime.get('power')
    response['realtime']['aqi'] = realtime.get('aqi')

    response['future'] = []
    future_data = dict()
    for k in range(len(future)):
        future_data['date'] = future[k].get('date')
        future_data['temperature'] = future[k].get('temperature')
        future_data['weather'] = future[k].get('weather')
        future_data['direct'] = future[k].get('direct')
        response['future'].append(future_data)
    print('juhe return response is: ', response)
    return response


if __name__ == "__main__":
    data = weather("南山")
