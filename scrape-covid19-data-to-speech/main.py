from typing import Counter
import requests
import json
import pyttsx3
import speech_recognition as sr
import threading
import time
import re

API_KEY = "tZ-a3Y1OaSXq"
PROJECT_TOKEN = "t6JAbj33ATuB"
RUN_TOKEN = "tQAmqXscA1T9"


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": api_key
        }

        self.data = self.get_data()

    def get_data(self):
        respone = requests.get(
            f'https://parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params={'api_key': self.api_key})
        data = json.loads(respone.text)
        return data

    def get_total_cases(self):
        data = self.data['total']

        for i in data:
            if i['name'] == 'Coronavirus Cases:':
                return i['value']

    def get_total_deaths(self):
        data = self.data['total']

        for i in data:
            if i['name'] == 'Deaths:':
                return i['value']

    def get_country_data(self, country):
        data = self.data['country']

        for i in data:
            if i['name'].lower() == country.lower():
                return i
        return "0"

    def get_list_country(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())

        return countries

    def update_data(self):
        response = requests.post(
            f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated")
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


# print(data.get_list_country())


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Speak("Shivansh tum chutiya ho ,")


def get_audio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception", str(e))
        # try:
        #     # recognize speech using Google Speech Recognition
        #     print("You said " + r.recognize_google(audio))
        # except LookupError:                           # speech is unintelligible
        #     print("Could not understand audio")
    return said.lower()


def main():

    data = Data(API_KEY, PROJECT_TOKEN)
    print("started")
    END_PHRASE = "[\w\s]+ stop [\w\s]+"
    result = None
    country = None
    country_list = list(data.get_list_country())
    UPDATE = "update [\w\s]+"
    SEARCH_PATTERS_TOTAL = {
        re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
        re.compile("[\w\s]+ total cases"): data.get_total_cases,
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total deaths"): data.get_total_deaths,

    }

    SEARCH_PATTERS_COUNTRY = {
        re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
        re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths']

    }
    while True:
        print("Listening....")
        text = get_audio()
        print(text)

        for pattern, func in SEARCH_PATTERS_COUNTRY.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break
        for pattern, func in SEARCH_PATTERS_TOTAL.items():
            if pattern.match(text):
                result = func()
                break
        if result:
            speak(result)

        if text == UPDATE:
            result = "Data is being updated. This may take a moment!"
            data.update_data()

        if text.find(END_PHRASE) != -1:
            print("bbye")
            break


main()
