# twitter_autobase
Twitter bot that can reads your DMs, then tweets like Twitter autobase.<br>
- This project is a recode from https://github.com/ydhnwb/autodm_base with many improvements and fixed bug.<br>
- I know this bot is not perfect yet, so issues and pull requests are welcome.<br>
- Feel free to contact me on Twitter if you have any questions! <br>

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
- Thread in tweets
- Tweets quoted image
- Upload simple database(txt) with push on github repo for backup
- Set timezone from constants

## Requirements
- Good at basic python programming
- Python 3.7+
- Twitter Developer Account
- Github Account
- Heroku Account

## Instructions
- Install pip3, virtualenv, git
- Do Installation
- Edit values in constants.py
- Push to Github
- Deploy to Heroku

## Constants
- Github repo, a repo that will be simple database.
- First keyword, keyword for video, photo, and gif.
- Second keyword, keyword to make quote.
- Sub2 keyword, when menfess contains Second keyword and Sub2 keyword, the sender username will be added to quote.
- Third keyword, when DMs contains this keyword, the DMs will be sent to admin id.
- Muted words, when muted words in DMs. the DMs will be deleted.
- Admin id, used when DMs contains Third_keyword. You can find admin id when your admin account send message (when bot active) to autobase account. The sender id is an Admin id.
- Timezone, Heroku timezone is on UTC. So, when this bot running on heroku server, the timezone is 7 for Jakarta


## Installation on Linux
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
When follower_data.txt is empty, This bot will automatically fill all follower to follower_data. So it can't track new follower when bot was just started.<br>
The algorithms of auto accept message is:<br>
1. follower_data.txt is empty, fill all followers to follower_data.txt<br>
2. Follower not in follower_data.txt, send message to new follower<br>
3. Follower stop following, remove follower from follower_data.txt<br>


## Push to Github (If you deploy to Heroku with Github repo)
Make a private repo, because data in constants.py is important<br>
Add lib and bin to .gitignore
```bash
git init
git remote add origin ((your repo))
git add .
git commit -m "first commit"
git push origin master
```

## Deploy to Heroku, You can search it on google

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

