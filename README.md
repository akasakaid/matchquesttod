# MatchQuestTod

Auto Claim for MatchQuest Telegram Bot

# Table of Contents

- [MatchQuestTod](#matchquesttod)
- [Table of Contents](#table-of-contents)
- [Warning](#warning)
- [Features](#features)
- [How to Use](#how-to-use)
  - [About Config.json](#about-configjson)
  - [Windows](#windows)
  - [Linux](#linux)
  - [Termux](#termux)
- [How to Get Data](#how-to-get-data)
- [Javascript Command to Get Telegram Data for Desktop](#javascript-command-to-get-telegram-data-for-desktop)
- [Run for 24/7](#run-for-247)
- [Discussion](#discussion)
- [Support](#support)
- [Thank you \< 3](#thank-you--3)

# Warning

All Risks are borne by the user!

# Features

- [x] Auto Claim
- [x] Use Daily Booster
- [x] Multi Account Support
- [x] Auto Playing Game Support, see [How to Use](#how-to-use)

# How to Use

## About Config.json

Here some key parameter to enable some feature

| parameter         | value        | description                           |
| ----------------- | ------------ | ------------------------------------- |
| use_daily_booster | (true/false) | use daily booster                     |
| auto_play_game    | (true/false) | use this for enable auto playing game |


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

5. Edit `data.txt`, input you data token in `data.txt`, find you token in [How to Get Data](#how-to-get-data). One line for one data account, if you want add you second account add in new line!

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

5. Edit `data.txt`, input you data token in `data.txt`, find you token in [How to Get Data](#how-to-get-data). One line for one data account, if you want add you second account add in new line!

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

5. Edit `data.txt`, input you data token in `data.txt`, find you token in [How to Get Data](#how-to-get-data). One line for one data account, if you want add you second account add in new line!

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
   1.query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxxxxxxxxxxxxxxxx
   2.query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxxxxxxxxxxxxxxxx
   ```

# Javascript Command to Get Telegram Data for Desktop

```javascript
copy(Telegram.WebApp.initData)
```

# Run for 24/7 

You can run the script bot for 24/7 using vps / rdp. You can use `screen` application in vps linux to running the script bot in background process

# Discussion

If you have an question or something you can ask in here : [@sdsproject_chat](https://t.me/sdsproject_chat)

# Support

To support me you can buy me a coffee via website in below

- Send IDR directly via QRIS : [https://s.id/nusanqr](https://s.id/nusanqr)
- https://trakteer.id/fawwazthoerif/tip
- https://sociabuzz.com/fawwazthoerif/tribe

# Thank you < 3