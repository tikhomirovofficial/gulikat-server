import random
import requests
import json


class ATC:
    def __init__(self):
        self.code = {
            1: "Ваш%20код%20авторизации:%20",
        }

        self.atc_url = "https://smsc.ru/rest/send/"
        self.login = "gm.mrk"
        self.password = "Mupreswedren-1"

    def request(self, message, phone):
        data = {
            "login": self.login,
            "psw": self.password,
            "phones": f"{phone}",
            "mes": message
        }
        print(data)
        url = f"https://smsc.ru/sys/send.php?login={self.login}&psw={self.password}&phones={phone}&mes={message}"
        print(url)
        response = requests.get(url)
        print(response.content)
        print("Запрос сделан!")
        return f"Запрос сделан!, {response.content}"

    def send_message(self, phone, psw, code=1):
        generate_code = psw
        message = f"{self.code[code]}{generate_code}"
        print(f"{message} - {phone}")
        # self.request(message, phone)
