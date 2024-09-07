# MatchQuestTod

Auto Claim for MatchQuest Telegram Bot

# Table of Contents

- [MatchQuestTod](#matchquesttod)
- [Table of Contents](#table-of-contents)
- [Warning](#warning)
- [Features](#features)
- [Support](#support)
- [How to Use](#how-to-use)
  - [Proxy configuration](#proxy-configuration)
  - [Windows](#windows)
  - [Linux](#linux)
  - [Termux](#termux)
- [How to Get Data](#how-to-get-data)
- [Javascript Command to Get Telegram Data for Desktop](#javascript-command-to-get-telegram-data-for-desktop)
- [Run for 24/7](#run-for-247)
- [Discussion](#discussion)
- [Thank you \< 3](#thank-you--3)

# Warning

All Risks are borne by the user!

# Features

- [x] Auto Claim
- [x] Use Daily Booster
- [x] Auto Solve Task
- [x] Multi Account Support
- [x] Proxy Support
- [x] Auto Playing Game Support

# Support

To support me you can buy me a coffee via website in below

- Send IDR directly via QRIS : [https://s.id/nusanqr](https://s.id/nusanqr)
- https://trakteer.id/fawwazthoerif/tip
- https://sociabuzz.com/fawwazthoerif/tribe


# How to Use

## Proxy configuration

If you want to use proxies you can simply add your proxy list to the `proxies.txt`` file or whatever file you want (if you use custom filenames for proxies you should call them with the additional argument --proxy and followed by the custom filename when running bot.py/main program)

Here's the format for writing proxies:

If using authentication:
```text
protocol://username:password@ipproxy:port
```

Example:
```text
http://user:user@69.69.69.69:8000
socks5://user:user@69.69.69.69:8000
```

If without authentication:
```text
protocol://ipproxy:port
```

Example:
```text
http://69.69.69.69:8000
socks5://69.69.69.69:8000
```

## Windows 

1. Make sure you computer was installed python and git.
   
   python site : [https://python.org](https://python.org)
   
   git site : [https://git-scm.com/](https://git-scm.com/)

2. Clone this repository
   ```shell
   git clone https://github.com/akasakaid/matchquesttod.git
   ```

3. goto matchquesttod directory
   ```
   cd matchquesttod
   ```

4. install the require library
   ```
   python -m pip install -r requirements.txt
   ```

5. Edit `data.txt`, input your query data in `data.txt`, find you token in [How to Get Data](#how-to-get-data). One line for one data account, if you want add you second account add in new line!

6. execute the main program 
   ```
   python bot.py
   ```

## Linux

1. Make sure you computer was installed python and git.
   
   python
   ```shell
   sudo apt install python3 python3-pip
   ```
   git
   ```shell
   sudo apt install git
   ```

2. Clone this repository
   
   ```shell
   git clone https://github.com/akasakaid/matchquesttod.git
   ```

3. goto matchquesttod directory

   ```shell
   cd matchquesttod
   ```

4. Install the require library
   
   ```
   python3 -m pip install -r requirements.txt
   ```

5. Edit `data.txt`, input your query data in `data.txt`, find you token in [How to Get Data](#how-to-get-data). One line for one data account, if you want add you second account add in new line!

6. execute the main program 
   ```
   python bot.py
   ```

## Termux

1. Make sure you termux was installed python and git.
   
   python
   ```
   pkg install python
   ```

   git
   ```
   pkg install git
   ```

2. Clone this repository
   ```shell
   git clone https://github.com/akasakaid/matchquesttod.git
   ```

3. goto matchquesttod directory
   ```
   cd matchquesttod
   ```

4. install the require library
   ```
   python -m pip install -r requirements.txt
   ```

5. Edit `data.txt`, input your query data in `data.txt`, find you token in [How to Get Data](#how-to-get-data). One line for one data account, if you want add you second account add in new line!

6. execute the main program 
   ```
   python bot.py
   ```

# How to Get Data
   
   1. Active web inspecting in telegram app, How to activate follow the video [https://youtu.be/NYxHmck_GjE](https://youtu.be/NYxHmck_GjE)
   2. Goto gamee bot and open the apps
   3. Press `F12` on your keyboard to open devtool or right click on app and select `Inspect`
   4. Goto `console` menu and copy [javascript code](#javascript-command-to-get-telegram-data-for-desktop) then paste on `console` menu
   5. If you don't receive error message, it means you successfully copy telegram data then paste on `data.txt` (1 line for 1 telegram data)
   
   Example telegram data

   ```
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxxxxxxxxxxxxxxxx
   ```

   6. If you want to add more account. Just paste telegram second account data in line number 2.
   
   Maybe like this sample in below

   ```
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxxxxxxxxxxxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxxxxxxxxxxxxxxxx
   ```

# Javascript Command to Get Telegram Data for Desktop

Copy javascript code in below and paste to console menu in dev tool / dev mode

```javascript
let x = Telegram.WebApp.initData;let y = JSON.parse(sessionStorage.__telegram__initParams).tgWebAppData;if (x === undefined) {if (y === undefined) {console.log("failed fetch query data")} else {copy(y);console.log("the data has been copied, please paste it with the ctrl + v keys")}} else {copy(x);console.log("the data has been copied, please paste it with the ctrl + v keys")}
```

# Run for 24/7 

You can run the script bot for 24/7 using vps / rdp. You can use `screen` application in vps linux to running the script bot in background process

# Discussion

If you have an question or something you can ask in here : [@sdsproject_chat](https://t.me/sdsproject_chat)


# Thank you < 3