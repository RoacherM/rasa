# -*- coding: utf-8 -*- 

'''
Author: ByronVon
Email: sir.housir@gmail.com
Version: 
Date: 2020-12-25 11:52:06
LastEditTime: 2020-12-29 11:30:02
'''
import os
import json
import requests


# KEY = os.getenv("SENIVERSE_KEY","") ## API key
KEY = "SEVOTmsVQaYKFrrGp"
UID = "" ##

LOCATION = "beijing"
API = "https://api.seniverse.com/v3/weather/now.json"
UNIT = "c"
LANGUAGE = "zh-Hans"

def fetch_weather(location):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT, 
    }, timeout=20)
    return result.json()


def get_weather_by_day(location):
    result = fetch_weather(location)
    normal_result = {
        "location": result["results"][0]["location"],
        "result": result["results"][0]["now"]
    }

    return normal_result


if __name__ == '__main__':
    default_location = "合肥"
    result = fetch_weather(default_location)
    print(json.dumps(result, ensure_ascii=False))

    default_location = "合肥"
    result = get_weather_by_day(default_location)
    print(json.dumps(result, ensure_ascii=False))


