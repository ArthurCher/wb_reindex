import pandas as pd
import requests
import json
from time import sleep
import os


class Reindex():

    headers = {'Authorization': 'OAuth AgAAAAAszdoSAAbdhMvpGWrx40BspYYiZm7Km6c'}

    def __init__(self):
        self.start()

    def getUserId(self):
        response = requests.get('https://api.webmaster.yandex.net/v4/user', headers=Reindex.headers)
        with open("wb_id.json", "w") as write_file:
            json.dump(response.json(), write_file)

        user_id = response.json()['user_id']

        return user_id


    def getSiteId(self):
        user_id = self.getUserId()
        response = requests.get('https://api.webmaster.yandex.net/v4/user/'+str(user_id)+'/hosts', headers=Reindex.headers)
        with open("wb_site.json", "w") as write_file:
            json.dump(response.json(), write_file)
        number = 1
        list_host = []

        for site in response.json()['hosts']:
            print (number,'-',  site['host_id'])
            list_host.append(site['host_id'])
            number +=1

        host_number = int(input("Введите номер host_id -> "))

        return list_host[host_number-1]


    def getURLList(self):
        list_file = []
        for file in os.listdir():
            if '.xlsx' in file:
                print(file)
                list_file.append(file)

        while True:
            file = input("Введите название файла из представленных - > ")
            if file in list_file:
                urls = pd.read_excel(file)

                host_id = self.getSiteId()

                user_id = self.getUserId()

                self.headers['Content-type'] = 'application/json;charset=UTF-8'  # Определение типа данных
                self.headers['Accept'] = 'text/plain'

                step = 1
                iter = len(urls)

                while iter > 0:
                    param = {'url': urls['URL'][step-1]}

                    response = requests.post('https://api.webmaster.yandex.net/v4/user/'+str(user_id)+'/hosts/'+str(host_id)+'/recrawl/queue',
                                             data=json.dumps(param), headers=self.headers)
                    with open("wb_response.json", "w") as write_file:
                        json.dump(response.json(), write_file)

                    if 'quota_remainder' in response.json().keys():
                        print ("Количество урлов в очереди ->", iter)
                        print("Дневная квота", response.json()['quota_remainder'], 'урлов')
                        iter -= 1
                        step += 1
                        sleep(3)

                    else:
                        print ("Дневная квота закончилась")
                        sleep(3600)

                break

            else:
                print("Такого файла нет, введите имя имеющегося файла")



    def start(self):
        print ("Скрипт переобхода страниц")

        self.getURLList()


if __name__ == "__main__":
    ya_s = Reindex()
