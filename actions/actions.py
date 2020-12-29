# -*- coding: utf-8 -*- 

'''
Author: ByronVon
Email: sir.housir@gmail.com
Version: 
Date: 2020-12-25 13:44:03
LastEditTime: 2020-12-29 11:29:36
'''
from typing import Text, Dict, Any, List

from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from .api import get_weather_by_day

from rasa_sdk.forms import Action
from rasa_sdk.events import SlotSet
from requests import ConnectionError, HTTPError, TooManyRedirects, Timeout


class ActionReportWeather(Action):

    def name(self) -> Text:
        return "action_report_weather"

    def run(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = tracker.get_slot('location')
        contexts = tracker.latest_message['text']
            
        weather_data = "{}".format(get_text_weather_date(location))

        if weather_data is not None:
            dispatcher.utter_message(text= "查询结果为：{}".format(weather_data))
        
        return []

        # return [SlotSet("matches", weather_data if weather_data is not None else [])]


def get_text_weather_date(address):
    try:
        result = get_weather_by_day(address)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = """
            {}的天气情况为：{}，气温：{}-{} °C
        """
        text_message = text_message_tpl.format(
            result['location']['name'],
            result['result']['text'],
            result['result']['code'],
            result['result']["temperature"],
        )

    return text_message