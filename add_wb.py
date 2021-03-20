import pandas as pd
import requests
import json
from time import sleep

class ADD_WB():
    headers = {'Authorization': 'OAuth AgAAAAAszdoSAAbdhMvpGWrx40BspYYiZm7Km6c'}

    def __init__(self):
        self.start()

    def getUserId(self):
        response = requests.get('https://api.webmaster.yandex.net/v4/user', headers=ADD_WB.headers)
        with open("wb_id.json", "w") as write_file:
            json.dump(response.json(), write_file)

        user_id = response.json()['user_id']

        return user_id

    def getSiteId(self):
        user_id = self.getUserId()
        response = requests.get('https://api.webmaster.yandex.net/v4/user/'+str(user_id)+'/hosts', headers=ADD_WB.headers)
        with open("wb_site.json", "w") as write_file:
            json.dump(response.json(), write_file)
        number = 1
        list_host = []

        for site in response.json()['hosts']:
            list_host.append(site['host_id'])
            number +=1

        return list_host

    def getDomain(self):
        urls = pd.read_excel('./поддомены.xlsx')

        user_id = self.getUserId()

        self.headers['Content-type'] = 'application/json;charset=UTF-8'  # Определение типа данных
        self.headers['Accept'] = 'text/plain'

        step = 1
        iter = len(urls)

        while iter > 0:
            param = {'host_url': urls['url'][step - 1]}

            response = requests.post('https://api.webmaster.yandex.net/v4/user/' + str(user_id) + '/hosts',
                                     data=json.dumps(param), headers=self.headers)

            with open("add_response.json", "w") as write_file:
                json.dump(response.json(), write_file)

            iter -= 1
            step += 1

    def getVer(self):
        print ("Получение кода верфикации")
        user_id = self.getUserId()
        host_id = self.getSiteId()
        dict_site = []
        dict_uin = []
        for site in host_id:
            response = requests.get(
                'https://api.webmaster.yandex.net/v4/user/' + str(user_id) + '/hosts/' + str(site) + '/verification/',
                headers=self.headers)

            dict_site.append(site)
            dict_uin.append('<meta name="yandex-verification" content="'+response.json()['verification_uin']+'" />')

        print (dict_site)
        print (dict_uin)
        df = pd.DataFrame({'site': dict_site,'uin': dict_uin})
        df.to_excel('./ver_uin.xlsx', index=False)

    def start(self):
        print("Добавление сайта в Яндекс Вебмастер")
        choise = int(input("Выберите действие:\nДобавить сайт -> 1;\nПолучить код подтверждения -> 2;\nПодтвердить права -> 3\n"))
        if choise == 1:
            self.getDomain()
        elif choise == 2:
            self.getVer()
        else:
            print ("Неправильно выбрали действие")


if __name__ == "__main__":
    add_wb = ADD_WB()