# twitter_autobase
Twitter bot that can reads your DMs, then tweets like Twitter autobase. This project is a recode of [autodm_base](https://github.com/ydhnwb/autodm_base)-[ydhnwb](https://github.com/ydhnwb) with many improvements and fixed bugs. I know this bot is not perfect yet, issues and pull requests are welcome. If you like my projects, support me by giving me star! Please report if you found a bug!

## New Features & Fixed Bugs
- Wait ratelimit with Tweepy
- Added muted words
- Only follower can sends menfess and message to admin
- Auto accept message requests (for open DM) by interacting sending DM to new follower
- Send DM to admin account
- Notify sender when the menfess sent or not
- Tweet gif and video
- Edit media for Twitter API requirements
- Fix moviepy when saving file
- Make (tweets) a Thread when characters > 280
- Tweet a quote image
- Upload simple database (txt) with push on github repo for backup
- Set timezone from constants
- Set muted_words from DM
- Upload 4 media

## Requirements
- Good at basic python programming
- Python 3.7+
- Twitter Developer Account
- Github Account
- Heroku Account

## How to run this bot
- Install pip3, virtualenv, git
- Do Installation
- Edit contents in constants.py
- Deploy to Heroku

## [Constants](https://github.com/fakhrirofi/twitter_autobase/blob/master/constants.py)
- Github_repo; a repo that will be simple database.
- First_keyword; keyword for video, photo, and gif.
- Sub1_keyword; when url tweet exists, it will be a retweet.
- Second_keyword; keyword to make quote.
- Sub2_keyword; when menfess contains Second keyword and Sub2 keyword, the sender username will be added to quote.
- Third_keyword; when DMs contains this keyword, the DMs will be sent to admin id.
- Muted_words; when muted words in DMs. the DMs will be deleted.
- Set_keyword; when Set keywords in DMs, it will edit Muted_words.
- Dict_set_keyword; command that will be executed with exec.
- Admin_id, used when DMs contains Third_keyword. You can find admin id when your admin account send message (when bot active) to autobase account. The sender id is an Admin id.
- Timezone, Heroku timezone is on UTC. So, when this bot running on heroku server, the timezone is 7 for Jakarta


## Installation on Linux
Note: You can run this bot from Windows as well. Search it on Google. <br>
Open your linux terminal on specified folder <br>
```bash
git clone https://github.com/fakhrirofi/twitter_autobase.git
virtualenv twitter_autobase
cd twitter_autobase
. bin/activate
pip3 install -r requirements.txt
```
Make .gitignore file <br>
```
lib/
bin/
__pycache__/
pyvenv.cfg
```
Run app.py using syntax: python3 app.py

## Notes
### Auto Accept message 
When follower_data.txt is empty, This bot will automatically fill all follower to follower_data. So it can't track new follower when bot was just started. The algorithms of auto accept message is:<br>
1. follower_data.txt is empty, fill all followers to follower_data.txt<br>
2. Follower not in follower_data.txt, send message to new follower<br>
3. Follower stop following, remove follower from follower_data.txt
### Addition
- admin can sends menfess although admin doesn't follow the bot


## DMs examples (based on constants)
### Upload 4 Media
tweet media with a sender account, then send tweet url by sending message to the bot. only support 4 photo, 1 video, or 1 gif. <br>
`fess! your message https://twitter.com/username/41890813214140?=19` <br>
if media in tweet url doesn't exists, automatically make quote-retweet.
### Quote-retweet
`fess! RT your message https://twitter.com/username/41890813214140?=19` (by attaching tweet url)
### Make a thread
All menfess keywords are supported with 'making a Thread' when more than 280 characters are given. <br>
`fess! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.` (by attaching media, tweet url, or not)
### Normal tweet
`fess! your message` (by attaching media, or not)
### Make quote image
limited to 500 characters <br>
`[quote] your quote` (media and url are not allowed) <br>
`[quote] -s your quote` (media and url are not allowed)
### Ask to admin
`[ask] your message` (by attaching media, tweet url, or not)
### Set muted words
`set! add_muted word1 word2 word3 word-n` (media and url are not allowed) <br>
`set! rm_muted word1 word2 word3 word-n` (media and url are not allowed)


## Deploy to Heroku
### Deploy with Heroku CLI
```bash
git add .
git commit -m "first commit"
heroku git:remote -a ((your heroku app name))
git push heroku master
```
### Push to Github (If you deploy to Heroku with Github repo) or Fork this repository
- Use a private repo, because data in constants.py is important
```bash
git init
git remote add origin ((your repo))
git add .
git commit -m "first commit"
git push origin master
```
Then deploy github repository to Heroku, search it on Google. <br>


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## [MIT License](https://github.com/fakhrirofi/twitter_autobase/blob/master/LICENSE)

Copyright (c) 2020 Fakhri Catur Rofi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
