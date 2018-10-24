import json 
import requests
import time
import urllib

TOKEN = "692350531:AAFpDknxKV0fphwg3oZBWhY3aMGsHPa9Fzw"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def report(text):
    data = get_json_from_url("https://api.openweathermap.org/data/2.5/weather?appid=5298723ed42f8852e7f0461f076ea257&q="+text)
    coordinates = data["coord"]
    temperature = data["main"]["temp"] - 273
    weather = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    temp_min = data["main"]["temp_min"] - 273
    temp_max = data["main"]["temp_max"] - 273
    a = ['The coordinates are ' + str(coordinates), 'Temperature in °C : ' + str(int(temperature)), weather, 'Humidity : ' + str(humidity),'Maximum Temperature in °C : ' + str(int(temp_max)), 'Minimum Temperature in °C : ' + str(int(temp_min))]
    return("\n".join(a))


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(report(text), chat_id)
    get_url(url)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

main()



