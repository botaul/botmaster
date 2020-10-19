# twitter_autobase
Twitter bot that can reads your DMs, then tweets like Twitter autobase. This project is a recode from https://github.com/ydhnwb/autodm_base with many improvements and fixed bugs. I know this bot is not perfect yet, so issues and pull requests are welcome. Feel free to contact me on Twitter if you have any questions.

## New Features & Fixed Bug
- Wait ratelimit with tweepy
- Added muted words
- Only follower that can sends menfess
- Auto accept message requests (for open DM) by interacting sending DM to new follower
- Send DM to admin account
- Notify sender when the menfess sent or not
- Support gif and video
- Edited media for Twitter API requirements
- Fix moviepy when saving file
- Make (tweets) a Thread when characters > 280
- Tweets quoted image
- Upload simple database(txt) with push on github repo for backup
- Set timezone from constants
- Set muted_words from DM

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
- Push to Github
- Deploy to Heroku

## [Constants](https://github.com/fakhrirofi/twitter_autobase/blob/master/constants.py)
- Github_repo; a repo that will be simple database.
- First_keyword; keyword for video, photo, and gif.
- Second_keyword; keyword to make quote.
- Sub2_keyword; when menfess contains Second keyword and Sub2 keyword, the sender username will be added to quote.
- Third_keyword; when DMs contains this keyword, the DMs will be sent to admin id.
- Muted_words; when muted words in DMs. the DMs will be deleted.
- Set_keyword; when Set keywords in DMs, it will edit Muted_words.
- Dict_set_keyword; command that will be executed with exec.
- Admin_id, used when DMs contains Third_keyword. You can find admin id when your admin account send message (when bot active) to autobase account. The sender id is an Admin id.
- Timezone, Heroku timezone is on UTC. So, when this bot running on heroku server, the timezone is 7 for Jakarta


## Installation on Linux
Note: You can run this bot from Windows as well. But I didn't write those steps<br>
Open your linux terminal on specified folder<br>
```bash
git clone https://github.com/fakhrirofi/twitter_autobase.git
virtualenv twitter_autobase
cd twitter_autobase
. bin/activate
pip3 install -r requirements.txt
```
run app.py using syntax: python3 app.py

## Notes
When follower_data.txt is empty, This bot will automatically fill all follower to follower_data. So it can't track new follower when bot was just started. The algorithms of auto accept message is:<br>
1. follower_data.txt is empty, fill all followers to follower_data.txt<br>
2. Follower not in follower_data.txt, send message to new follower<br>
3. Follower stop following, remove follower from follower_data.txt<br>
<br>
### DMs examples (based on constants)
`fess! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.` #automatically make Thread<br>
`fess! Upload media` (then attach a media) #send dm with media attachment<br>
`set! add_muted covid corona anjay` #set muted words from DM<br>
`[quote] hello hai hello hai` #make quote inside image<br>
`[quote] -s hello hai hello` #add sender screen_name to quote<br>
`[ask] asking to admin` #send message to admin

## Push to Github (If you deploy to Heroku with Github repo) or Fork this repository
- Make a private repo, because data in constants.py is important
- Add lib and bin to .gitignore
```bash
git init
git remote add origin ((your repo))
git add .
git commit -m "first commit"
git push origin master
```

## Deploy to Heroku, You can search it on google
I suggest you to deploy it from Heroku CLI

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
