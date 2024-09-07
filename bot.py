import os
import re
import json
import httpx
import random
import asyncio
import argparse
import aiofiles.os
import aiofiles.ospath
from urllib.parse import parse_qs
from datetime import datetime
from colorama import init, Fore, Style
from fake_useragent import UserAgent
from base64 import urlsafe_b64decode

init(autoreset=True)
token_file = ".match_tokens.json"
log_file = "http.log"
data_file = "data.txt"
proxy_file = "proxies.txt"
ua_file = ".user-agent.json"
config_file = ".config.json"
red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
blue = Fore.LIGHTBLUE_EX
magenta = Fore.LIGHTMAGENTA_EX
white = Fore.LIGHTWHITE_EX
black = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL
line = white + "~" * 50


class Config:
    def __init__(
        self,
        auto_claim: bool,
        auto_solve_task: bool,
        auto_play_game: bool,
        low_point: int,
        high_point: int,
    ):
        self.auto_claim = auto_claim
        self.auto_solve_task = auto_solve_task
        self.auto_play_game = auto_play_game
        self.low_point = low_point
        self.high_point = high_point


class MatchTod:
    def __init__(self, id: int, query: str, proxies: list, config: Config):
        self.log(f"{green}start account number : {white}{id + 1}")
        marin = lambda data: {key: value[0] for key, value in parse_qs(data).items()}
        parser = marin(query)
        user = parser.get("user")
        self.valid = True
        self.config = config
        if user is None:
            self.valid = False
            return None
        self.user = json.loads(user)
        self.proxies = proxies
        self.query = query
        if len(proxies) > 0:
            proxy = self.get_random_proxy(id)
            self.ses = httpx.AsyncClient(proxy=proxy, verify=False)
        else:
            self.ses = httpx.AsyncClient(verify=False)
        self.headers = {
            "Host": "tgapp-api.matchain.io",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.79 Mobile Safari/537.36",
            "Content-Type": "application/json",
            "Origin": "https://tgapp.matchain.io",
            "X-Requested-With": "org.telegram.messenger",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://tgapp.matchain.io/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7",
        }

    def get_random_proxy(self, isself: int, israndom=False):
        if israndom:
            return random.choice(self.proxies)
        return self.proxies[isself % len(self.proxies)]

    async def http(self, url, headers, data=None):
        while True:
            try:
                if not await aiofiles.ospath.exists(log_file):
                    async with aiofiles.open(log_file, "w") as w:
                        await w.write("")
                logsize = await aiofiles.ospath.getsize(log_file)
                if logsize / 1024 / 1024 > 1:
                    async with aiofiles.open(log_file, "w") as w:
                        await w.write("")
                if data is None:
                    res = await self.ses.get(url, headers=headers, timeout=30)
                elif data == "":
                    res = await self.ses.post(url, headers=headers, timeout=30)
                else:
                    res = await self.ses.post(
                        url, headers=headers, timeout=30, data=data
                    )
                async with aiofiles.open(log_file, "a", encoding="utf-8") as hw:
                    await hw.write(f"{res.text}\n")
                return res
            except httpx.ProxyError:
                proxy = self.get_random_proxy(0, israndom=True)
                self.ses = httpx.AsyncClient(proxy=proxy)
                self.log(f"{red}proxy error")
                await asyncio.sleep(3)
                continue
            except httpx.NetworkError:
                self.log(f"{red}network error !")
                await asyncio.sleep(3)
                continue
            except httpx.TimeoutException:
                self.log(f"{red}connection timeout !")
                await asyncio.sleep(3)
                continue
            except httpx.RemoteProtocolError:
                self.log(f"{red}server disconnected without sending response")
                await asyncio.sleep(3)

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}")

    async def check_ip(self):
        url = "https://ipgeolocation.info/"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=0, i",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        }
        res = await self.http(url, headers)
        ip = re.search(r"\<li\>\"ip\"\, \"(.*?)\"\<\/li\>", res.text).group(1)
        country = re.search(r"\<li\>\"country\"\, \"(.*?)\"\<\/li\>", res.text).group(1)
        region = re.search(r"\<li\>\"region\"\, \"(.*?)\"\<\/li\>", res.text).group(1)
        self.log(f"{green}using ip proxy {white}{ip}")
        self.log(f"{green}country {white}{country} {green}region {white}{region}")

    def is_expired(self, token):
        if token is None or isinstance(token, bool):
            return True
        header, payload, sign = token.split(".")
        deload = urlsafe_b64decode(payload + "==")
        jeload = json.loads(deload)
        now = int(datetime.now().timestamp()) + 200
        if now > jeload.get("exp"):
            return True
        return False

    async def login(self):
        login_url = "https://tgapp-api.matchain.io/api/tgapp/v1/user/login"
        login_data = {
            "uid": self.user.get("id"),
            "first_name": self.user.get("first_name"),
            "last_name": self.user.get("last_name"),
            "username": self.user.get("username"),
            "tg_login_params": self.query,
        }
        res = await self.http(login_url, self.headers, json.dumps(login_data))
        if not self.check_code(res.json()):
            return False
        data = res.json().get("data", {})
        token = data.get("token")
        return token

    def check_code(self, data: dict):
        code = data.get("code")
        msg = data.get("msg", "")
        err = data.get("err", "")
        if "You've already made a purchase." in msg:
            return "buy"
        if "user not found" == err:
            self.log(
                f"{yellow}This telegram account has not been registered with the bot."
            )
            return False
        if code != 200:
            self.log(f"{red}code : {code}, {(msg if msg else err)}")
            return False
        return True

    async def start(self):
        uid = str(self.user.get("id"))
        first_name = self.user.get("first_name")
        self.log(f"{green}login {white}{first_name}")
        if len(self.proxies) > 0:
            await self.check_ip()
        async with aiofiles.open(token_file) as w:
            read = await w.read()
            tokens = json.loads(read)
        async with aiofiles.open(ua_file) as w:
            read = await w.read()
            uas = json.loads(read)
        ua = uas.get(uid)
        if ua is None:
            ua = UserAgent(platforms="mobile").random
            uas[uid] = ua
            async with aiofiles.open(ua_file, "w") as w:
                await w.write(json.dumps(uas, indent=4))
        self.headers["User-Agent"] = ua
        token = tokens.get(uid)
        if self.is_expired(token):
            token = await self.login()
            if not token:
                return
            async with aiofiles.open(token_file, "w") as w:
                tokens[uid] = token
                await w.write(json.dumps(tokens, indent=4))
        self.headers["Authorization"] = token
        self.log(f"{green}success login !")
        profile_url = "https://tgapp-api.matchain.io/api/tgapp/v1/user/profile"
        reward_url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward"
        reward_claim_url = (
            "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/claim"
        )
        farming_url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/farming"
        balance_url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/balance"
        tasks_url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/task/list"
        task_complete_url = (
            "https://tgapp-api.matchain.io/api/tgapp/v1/point/task/complete"
        )
        task_claim_url = "https://tgapp-api.matchain.io/api/tgapp/v1/point/task/claim"
        daily_task_url = "https://tgapp-api.matchain.io/api/tgapp/v1/daily/task/status"
        buy_booster_url = (
            "https://tgapp-api.matchain.io/api/tgapp/v1/daily/task/purchase"
        )
        basic_data = {"uid": int(uid)}
        res = await self.http(profile_url, self.headers, json.dumps(basic_data))
        code = res.json().get("code")
        if code != 200:
            err = res.json().get("err")
            self.log(f"{red}code : {code},{err}")
            return False
        data = res.json().get("data")
        is_bot = data.get("IsBot")
        balance = data.get("Balance") / 1000
        self.log(f"{green}balance : {white}{balance}")
        self.log(f"{green}bot flag : {white}{is_bot}")
        res = await self.http(daily_task_url, self.headers)
        if not self.check_code(res.json()):
            return False
        data = res.json().get("data")
        for da in data:
            current_count = da.get("current_count")
            task_count = da.get("task_count")
            point = da.get("point")
            dtype = da.get("type")
            if dtype == "quiz":
                continue
            if balance < point:
                continue
            if current_count == task_count:
                continue
            buy_data = {"uid": int(uid), "type": dtype}
            res = await self.http(buy_booster_url, self.headers, json.dumps(buy_data))
            cdr = self.check_code(res.json())
            if cdr == "buy":
                self.log(f"{yellow}has purchased a {dtype} booster")
            elif not cdr:
                return False
            else:
                self.log(f"{green}successful purchase of a {dtype} booster")

        next_claim_timestamp = 3600
        if self.config.auto_claim:
            while True:
                res = await self.http(reward_url, self.headers, json.dumps(basic_data))
                code = res.json().get("code")
                if not self.check_code(res.json()):
                    return False

                data = res.json().get("data", {})
                reward = data.get("reward")
                next_claim_timestamp = (
                    data.get(
                        "next_claim_timestamp",
                        (int(datetime.now().timestamp() + 1000) * 1000),
                    )
                    / 1000
                )
                now = int(datetime.now().timestamp())
                if reward == 0 or reward is None:
                    res = await self.http(
                        farming_url, self.headers, json.dumps(basic_data)
                    )
                    if not self.check_code(res.json()):
                        return False
                    self.log(f"{green}success start farming !")
                    continue
                if now > next_claim_timestamp:
                    res = await self.http(
                        reward_claim_url, self.headers, json.dumps(basic_data)
                    )
                    if not self.check_code(res.json()):
                        return False
                    self.log(f"{green}success claim farming !")
                    continue
                self.log(f"{yellow}not the time to claim farming")
                next_claim = datetime.fromtimestamp(next_claim_timestamp)
                self.log(f"{green}next claim : {white}{next_claim}")
                break
        if self.config.auto_solve_task:
            res = await self.http(tasks_url, self.headers, json.dumps(basic_data))
            if not self.check_code(res.json()):
                return False
            data = res.json().get("data", {})
            task_keys = list(data.keys())
            for key in task_keys:
                tasks = data.get(key)
                for task in tasks:
                    name = task.get("name")
                    complete = task.get("complete")
                    if complete:
                        self.log(f"{yellow}task {white}{name} {yellow}completed !")
                        continue
                    complete_data = {"uid": int(uid), "type": name}
                    res = await self.http(
                        task_complete_url, self.headers, json.dumps(complete_data)
                    )
                    if not self.check_code(res.json()):
                        continue
                    self.log(f"{green}success complete task {white}{name}")
                    await asyncio.sleep(5)
                    res = await self.http(
                        task_claim_url, self.headers, json.dumps(complete_data)
                    )
                    code = res.json().get("code")
                    if code != 200:
                        self.log(f"{red}failed claim task {white}{name}")
                        continue
                    self.log(f"{green}success claim task {white}{name}")
            res = await self.http(balance_url, self.headers, json.dumps(basic_data))
            if not self.check_code(res.json()):
                return False
            balance = res.json().get("data")
            self.log(f"{green}balance : {white}{balance}")
        if self.config.auto_play_game:
            game_url = "https://tgapp-api.matchain.io/api/tgapp/v1/game/play"
            game_claim_url = "https://tgapp-api.matchain.io/api/tgapp/v1/game/claim"
            while True:
                res = await self.http(game_url, self.headers)
                if not self.check_code(res.json()):
                    return False
                data = res.json().get("data", {})
                game_id = data.get("game_id")
                game_count = data.get("game_count")
                self.log(f"{green}available game tickets {white}{game_count}")
                if int(game_count) <= 0:
                    break
                await countdown(35)
                point = random.randint(self.config.low_point, self.config.high_point)
                game_claim_data = {
                    "game_id": game_id,
                    "point": point,
                }
                res = await self.http(
                    game_claim_url, self.headers, json.dumps(game_claim_data)
                )
                if not self.check_code(res.json()):
                    return False
                self.log(
                    f"{green}successfully played a game with {white}{point} {green}points"
                )
        return int(next_claim_timestamp)


async def countdown(t):
    for i in range(t, 0, -1):
        minute, second = divmod(i, 60)
        hour, minute = divmod(minute, 60)
        second = str(second).zfill(2)
        minute = str(minute).zfill(2)
        hour = str(hour).zfill(2)
        print(f"waiting {hour}:{minute}:{second} ", flush=True, end="\r")
        await asyncio.sleep(1)
    print("                       ", flush=True, end="\r")


async def main():
    banner = f"""
{magenta}┏┓┳┓┏┓  ┏┓    •      {white}BlumTod Auto Claim for {yellow}matchquest
{magenta}┗┓┃┃┗┓  ┃┃┏┓┏┓┓┏┓┏╋  {green}Author : {white}AkasakaID
{magenta}┗┛┻┛┗┛  ┣┛┛ ┗┛┃┗ ┗┗  {white}Github : {green}https://github.com/AkasakaID
{magenta}              ┛      {green}Note : {white}Every Action Has a Consequence
        """
    if not await aiofiles.ospath.exists(data_file):
        async with aiofiles.open(data_file, "a") as w:
            await w.write("")
    if not await aiofiles.ospath.exists(proxy_file):
        async with aiofiles.open(proxy_file, "a") as w:
            await w.write("")
    if not await aiofiles.ospath.exists(token_file):
        async with aiofiles.open(token_file, "w") as w:
            await w.write(json.dumps({}))
    if not await aiofiles.ospath.exists(ua_file):
        async with aiofiles.open(ua_file, "w") as w:
            await w.write(json.dumps({}))
    if not await aiofiles.ospath.exists(config_file):
        async with aiofiles.open(config_file, "w") as w:
            await w.write(
                json.dumps(
                    {
                        "auto_claim": True,
                        "auto_play_game": True,
                        "auto_solve_task": True,
                        "game_point": {"low": 100, "high": 150},
                    }
                )
            )
    arg = argparse.ArgumentParser()
    arg.add_argument("--data", "-D", default=data_file)
    arg.add_argument("--proxy", "-P", default=proxy_file)
    arg.add_argument("--action", "-A")
    args = arg.parse_args()
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(banner)
        print(line)
        if not await aiofiles.ospath.exists(args.data):
            print(f"{white}data file : {args.data} {red} file not found !")
            return
        async with aiofiles.open(args.data) as w:
            read = await w.read()
            datas = [i for i in read.splitlines() if len(i) > 0]
        if not await aiofiles.ospath.exists(args.proxy):
            print(f"{white}proxy file : {args.proxy} {red}file not found !")
            return
        async with aiofiles.open(args.proxy) as w:
            read = await w.read()
            proxies = [i for i in read.splitlines() if len(i) > 0]
        async with aiofiles.open(config_file) as w:
            read = await w.read()
            config = json.loads(read)
            cfg = Config(
                auto_claim=config.get("auto_claim", True),
                auto_solve_task=config.get("auto_solve_task", True),
                auto_play_game=config.get("auto_play_game", True),
                low_point=config.get("game_point", {}).get("low", 100),
                high_point=config.get("game_point", {}).get("high", 100),
            )

        menu = f"""
{white}data file :{green} {data_file}
{white}proxy file :{green} {proxy_file}
{line}
{green}total data : {white}{len(datas)}
{green}total proxy : {white}{len(proxies)}
{green}using proxy : {white}{(True if len(proxies) > 0 else False)}
{line}
Menu :
    1.) set on/off auto claim ({(green + 'active' if cfg.auto_claim else red + 'non-active')}{white})
    2.) set on/off auto play game ({(green + 'active' if cfg.auto_play_game else red + 'non-active')}{white})
    3.) set on/off auto solve task ({(green + 'active' if cfg.auto_solve_task else red + 'non-active')}{white})
    4.) set game point ({green}{cfg.low_point}-{cfg.high_point}{white})
    5.) start bot

{white}Note : ctrl + c to exit !
    """
        print(menu)
        opt = args.action
        if opt is None:
            opt = input("input number : ")
        print(line)
        try:
            if int(opt) not in [1, 2, 3, 4, 5]:
                print(f"{red}enter the correct number of menu !")
                input(f"{yellow}press enter to continue")
                continue
        except ValueError:
            print(f"{red}enter the correct number of menu !")
            input(f"{yellow}press enter to continue")
        if opt == "1":
            config["auto_claim"] = False if cfg.auto_claim else True
            async with aiofiles.open(config_file, "w") as w:
                await w.write(json.dumps(config, indent=4))
            print(f"{green}Successfully make auto_claim config changes")
            input(f"{yellow}press enter to continue")
            continue
        if opt == "2":
            config["auto_play_game"] = False if cfg.auto_play_game else True
            async with aiofiles.open(config_file, "w") as w:
                await w.write(json.dumps(config, indent=4))
            print(f"{green}Successfully make auto_play_game config changes")
            input(f"{yellow}press enter to continue")
            continue
        if opt == "3":
            config["auto_solve_task"] = False if cfg.auto_solve_task else True
            async with aiofiles.open(config_file, "w") as w:
                await w.write(json.dumps(config, indent=4))
            print(f"{green}Successfully make auto_solve_task config changes")
            input(f"{yellow}press enter to continue")
            continue

        if opt == "4":
            low_point = input("input lowest point : ")
            high_point = input("input highest point : ")
            try:
                if int(low_point) > int(high_point):
                    print(f"{red}the lowest point cannot exceed the highest point.")
                    input(f"{yellow}press enter to continue")
                    continue
            except ValueError:
                print(f"{red}enter the correct number dumbass")
                input(f"{yellow}press enter to continue")
                continue

            config["game_point"]["low"] = int(low_point)
            config["game_point"]["high"] = int(high_point)
            async with aiofiles.open(config_file, "w") as w:
                await w.write(json.dumps(config, indent=4))
            print(f"{green}Successfully make game_point config changes")
            input(f"{yellow}press enter to continue")
            continue
        if opt == "5":
            while True:
                countdowns = []
                _start = int(datetime.now().timestamp())
                for no, data in enumerate(datas):

                    matchq = MatchTod(id=no, query=data, proxies=proxies, config=cfg)
                    if not matchq.valid:
                        print(
                            f"{yellow}it looks like account {no + 1} data has the wrong format."
                        )
                        print(line)
                        continue
                    result = await matchq.start()
                    print(line)
                    if not result:
                        continue
                    countdowns.append(result)
                _end = int(datetime.now().timestamp())
                if len(countdowns) > 0:
                    _min = min(countdowns)
                else:
                    _min = 3600
                _total = ((_min - (_end - _start)) - _end) + 120
                await countdown(_total)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()
