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
- Install pip3, virtualenv, git, git lfs. (git lfs is optional)
- Do Installation
- Edit values in constants.py
- Push to Github
- Deploy to Heroku

## Note: Constants
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

## Push to Github (If you deploy to Heroku with Github repo)
```bash
git init
git lfs install
git add .gitattributes
git add .
git remote add origin ((your repo))
git commit -m "first commit"
git push origin master
```

## Push to Heroku, I suggest you to push from heroku CLI. You can search it on google

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

