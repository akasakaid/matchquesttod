import os
import sys
import time
import json
import random
import argparse
import requests
from datetime import datetime
from colorama import *
from urllib.parse import parse_qs

init(autoreset=True)
merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
hitam = Fore.LIGHTBLACK_EX
putih = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL


class MatchQuestTod:
    def __init__(self):
        self.headers = {
            "host": "tgapp-api.matchain.io",
            "connection": "keep-alive",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; Redmi 4A / 5A Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36",
            "content-type": "application/json",
            "origin": "https://tgapp.matchain.io",
            "x-requested-with": "tw.nekomimi.nekogram",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://tgapp.matchain.io/",
            "accept-language": "en,en-US;q=0.9"
        }
        self.marin_kitagawa = lambda data: {
            key: value[0] for key, value in parse_qs(data).items()}
        self.line = putih + "~" * 50

    def login(self, data):
        parser = self.marin_kitagawa(data)
        user = json.loads(parser['user'])
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/user/login"
        payload = json.dumps({
            "uid": user['id'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "username": user['username'],
            "tg_login_params": data
        })
        res = self.http(url, self.headers, payload)
        if res.status_code != 200:
            self.log(f"{merah}login failure !")
            self.log(
                f"{merah}something wrong ???, check http.log file for more info !")
            return False

        self.userid = user['id']
        self.log(f'{hijau}login successfully !')
        token = res.json()["data"]["token"]
        invite_limit = res.json()["data"]["user"]["invite_limit"]
        self.headers['authorization'] = token
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/balance"
        payload = json.dumps({
            "uid": self.userid
        })
        res = self.http(url, self.headers, payload)
        if res.status_code != 200:
            self.log(
                f"{merah}something wrong ???, check http.log file for more info !")
            return False

        balance = res.json()['data']
        self.log(f'{hijau}balance : {putih}{balance / 1000}')
        self.log(f'{hijau}invite limit : {putih}{invite_limit}')
        while True:
            url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward"
            res = self.http(url, self.headers, payload)
            if res.status_code != 200:
                self.log(
                    f"{merah}something wrong ???, check http.log for more info !")
                return False

            next_claim = res.json()['data']['next_claim_timestamp']
            if next_claim == 0:
                url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/farming"
                res = self.http(url, self.headers, payload)
                if res.status_code != 200:
                    self.log(
                        f'{merah}something wrong ???, check http.log for more info !')
                    return False
                continue

            if next_claim > round(time.time() * 1000):
                format_next_claim = datetime.fromtimestamp(
                    next_claim/1000).isoformat(" ").split(".")[0]
                self.log(f'{kuning}not time to claim !')
                self.log(
                    f'{kuning}next claim : {putih}{format_next_claim}')
                if self.autogame:
                    self.game()
                return round(next_claim / 1000 - round(time.time())) + 30

            url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/claim"
            res = self.http(url, self.headers, payload)
            if res.status_code != 200:
                self.log(
                    f'{merah}something wrong ???, check http.log file for more info !')
                return False

            _data = res.json()['data']
            self.log(f'{hijau}claim successfully')
            self.log(f'{hijau}balance : {putih}{balance + _data}')

    def game(self):
        url = "https://tgapp-api.matchain.io/api/tgapp/v1/game/play"
        while True:
            res = self.http(url, self.headers)
            if res.status_code != 200:
                self.log(
                    f"{merah}something wrong ???, check http.log file for more info !")
                return False

            game_id = res.json()["data"]["game_id"]
            game_count = res.json()["data"]["game_count"]
            self.log(f"{hijau}game count : {putih}{game_count}")
            if game_count <= 0:
                self.log(f'{kuning}you dont have game ticket !')
                return False

            self.countdown(30)
            point = random.randint(20, 50)
            payload = json.dumps({
                "game_id": game_id,
                "point": point
            })
            url_claim = "https://tgapp-api.matchain.io/api/tgapp/v1/game/claim"
            res = self.http(url_claim, self.headers, payload)
            if res.status_code != 200:
                self.log(f'{merah}playgame failure !')
                continue

            self.log(f'{hijau}playgame successfully, earn {putih}{point}')

    def load_data(self, file):
        data = open(file).read().splitlines()
        if len(data) <= 0:
            self.log(f"{merah}fill {file} first, there no account detected !")
            return False

        self.log(f'{hijau}total account detected : {putih}{len(data)}')
        print(self.line)
        return data

    def main(self):
        banner = f"""
    {hijau}Auto Farm and Claim for {biru}MatchQuestBot
    
    {hijau}By: {putih}AkasakaID
    {hijau}Github: {putih}@AkasakaID
    
    {hijau}Message: {putih}don't forget 'git pull' maybe the script have update !
    
        """
        arg = argparse.ArgumentParser()
        arg.add_argument('--marin', action="store_true")
        arg.add_argument('--data', default="data.txt",
                         help="set custom input file data (default: data.txt)")
        arg.add_argument('--autogame', action="store_true",
                         help="add this parameter to enable feature auto playing game !")
        args = arg.parse_args()
        if args.marin is False:
            os.system("cls" if os.name == "nt" else "clear")
        print(banner)
        self.autogame = args.autogame
        while True:
            list_countdown = []
            _start = int(time.time())
            for no, data in enumerate(self.load_data(args.data)):
                self.log(f"{hijau}account number : {putih}{no+1}")
                result = self.login(data)
                list_countdown.append(result)
                self.countdown(3)
                print(self.line)

            _end = int(time.time())
            _tot = _end - _start
            _min = min(list_countdown) - _tot
            if _min <= 0:
                continue

            self.countdown(_min)

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih}waiting {jam}:{menit}:{detik}     ",
                  flush=True, end='\r')
            time.sleep(1)
            t -= 1
        print("                                        ", flush=True, end="\r")

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {msg}{reset}")

    def http(self, url, headers, data=None):
        while True:
            try:
                if data is None:
                    res = requests.get(url, headers=headers, timeout=30)
                    open("http.log", "a",
                         encoding="utf-8").write(f"{res.text}\n")
                    return res

                if data == "":
                    res = requests.post(url, headers=headers, timeout=30)
                    open("http.log", "a",
                         encoding="utf-8").write(f"{res.text}\n")
                    return res

                res = requests.post(url, headers=headers,
                                    data=data, timeout=30)
                open("http.log", "a", encoding="utf-8").write(f"{res.text}\n")
                return res
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                self.log(f"{merah}connection error / connection timeout !")
                time.sleep(1)
                continue


if __name__ == "__main__":
    try:
        app = MatchQuestTod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
