# twitter_autobase
Twitter bot that can reads your dm, then tweets dm like Twitter autobase.<br>
Note: This project is a recode from https://github.com/ydhnwb/autodm_base with many improvements and fixed bug.

## New Features & Fixed Bug
- Only list & delete dm message that contains keyword (constants.py), so another dm would not deleted
- Simplified scripts
- Send dm to admin account
- Auto reply dm to sender
- Support gif and video
- Edited media for Twitter API requirements
- Thread in tweets
- Tweets quoted image
- Upload simple database(txt) with push on github repo for backup

## Requirements
- Python 3.7+
- Twitter Developer Account
- Github Account
- Heroku Account

## Instructions
- Install pip3, virtualenv, git, git lfs
- Do Installation
- Edit values in constants.py
- Push to Github
- Deploy to Heroku

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

## Push to Github
```bash
git init
git lfs install
git add .gitattributes
git add .
git remote add origin ((your repo))
git commit -m "first commit"
git push origin master
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

