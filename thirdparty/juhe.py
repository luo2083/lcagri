import json
import requests
from utils import proxy


def weather(city):

    key = "13d7317bb5c82bd56fe3dccd3e0e2aee"
    api = "http://apis.juhe.cn/simpleWeather/query"
    params = '?city=%s&key=%s' %(city, key)
    url = api + params
    print(url)
    response = requests.get(url=url)
    json_data = json.loads(response.text)
    print(json_data)
    result = json_data.get("result")
    realtime = result.get("realtime")
    response = dict()
    response['city'] = result.get("city")
    response['temperature'] = realtime.get('temperature')
    response['humidity'] = realtime.get('humidity')
    response['info'] = realtime.get('info')
    response['wid'] = realtime.get('wid')
    response['direct'] = realtime.get('direct')
    response['power'] = realtime.get('power')
    response['aqi'] = realtime.get('aqi')

    print(response)
    return response

def constellation(consName):
    key = 'fed29157ba4d3fb9aec2f0625d07838d'
    api = 'http://web.juhe.cn:8080/constellation/getAll'
    types = ('today','tomorrow','week','month','year')
    type = types[0]
    params = '?consName=%s&type=%s&key=%s' %(consName, type, key)
    url = api + params
    print(url)
    response = requests.get(url, proxies=proxy.proxy())
    data = json.loads(response.content)
    print(data['summary'])
    return {
        "name": consName,
        "text": data['summary']
    }

if __name__ == "__main__":
    data = constellation("白羊座")
