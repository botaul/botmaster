# twitter_autobase
A Twitter bot that can read your DMs, then tweets like Twitter autobase. This project is a re-code of
[autodm_base](https://github.com/ydhnwb/autodm_base) by [Prieyudha Akadita S.](https://github.com/ydhnwb)
with many improvements and fixed bugs. This project is under MIT License. You can try on my autobase account
[@autobase_reborn](https://twitter.com/autobase_reborn).

- **Read Twitter rules[[1]](https://help.twitter.com/en/rules-and-policies/twitter-search-policies)[[2]](https://developer.twitter.com/en/developer-terms/more-on-restricted-use-cases)[[3]](https://help.twitter.com/en/rules-and-policies/twitter-automation)** <br>
- **USING THIS BOT FOR 'ADULT' BASE IS STRICTLY PROHIBITED** <br>

All updates will be postponed until June 2021 (or sooner). Feel free to make issues or pull
requests if you have any questions, feature requests, or bugs.


## Table of Contents
- [New Features](#new-features)
- [Requirements](#requirements)
- [How to run this bot?](#how-to-run-this-bot)
- [DMs examples (based on administrator_data)](#dms-examples-based-on-administrator_data)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#mit-license)


## New Features
- Added blacklist words
- Only followed by account that can send menfess
- Auto accepts message requests
- Notify sender when the menfess sent or not
- Tweet GIF and video
- Post a Thread when characters > 280
- Sync simple database (json) on github repository
- Setting account from DM
- Upload more than 4 media
- Trigger words are not case-sensitive
- Trigger words are list
- etc. see on administrator_data


## Requirements
- Good at basic python programming
- Python 3.8.x
- Twitter Developer Account
- Github Account
- Heroku Account


## How to run this bot?
- Install pip3, virtualenv, git, heroku
- [Do Installation](#installation)
- Edit contents on administrator_data.py
- [Deploy to Heroku](#deploy-to-heroku)


## Installation
Note: You can run this bot on Windows and MacOS as well<br>
Open your Linux terminal on the specified folder <br>
```bash
# Clone this repository or download released version on https://github.com/fakhrirofi/twitter_autobase/releases
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
# add another, up to you
```
After modifying contents on administrator_data, run app by using syntax: python3 app.py


## Deploy to Heroku

### Deploy using Heroku CLI
Make sure you have deleted the local Database if you previously ran the bot on local.
```bash
git add .
git commit -m "first commit"
heroku git:remote -a your_heroku_app_name
git push heroku master
```

### Heroku limitations
- 550 free dyno hours, you can upgrade to 1000 hours by adding credit card to your account.
- Dyno cycling (restart), so `add_admin`, `rm_admin`, `add_blacklist`, `rm_blacklist`,
`switch on/off`, and all temporary db (including Github database) won't work perfectly. It would be better if
you use Heroku database services e.g. Postgres. Please setting `Blacklist_words`, `Admin_id`, and etc. before
deploying to Heroku. Database will be changed to Postgres in future updates.


## DMs examples (based on administrator_data)
You can tweet more than one media with media link on tweet. Open your twitter app then tap (hold) the tweet.
Media link automatically will be copied, then send the link to this bot from DM.

### Quote-retweet
`fess! your message https://twitter.com/username/1234567890?s=19` (by attaching media, url, or not)

### Make a thread
`fess! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.` (by attaching media, url, or not)

### Normal tweet
`fess! your message` (by attaching media, url, or not)

### Admin command
Note: Due to Heroku dyno cycling, some commands that use temporary data won't work perfectly. <br>
Only admin can access these commands. If user try to access this commands, the user will be notified that the
keyword is wrong. <br>
`#add_blacklist word1 word2 word-n` <br>
`#rm_blacklist word1 word2 word-n` <br>
`#db_update` not available when Database = False <br>
`#display_blacklist` <br>
`#rm_followed username1 username2 username-n` <br>
`#add_admin username1 username2 username-n` <br>
`#rm_admin username1 username2 username-n` <br>
`#who https://twitter.com/username/status/1234567890?s=19` check who was sent the menfess <br>
`#switch off` turn off the automenfess <br>
`#switch on` turn on the automenfess<br> <br>
For add_blacklist and rm_blacklist, you can add space into your words by giving underscore "_". Example: <br>
`#add_blacklist _word1_ word2_word3 word-n` <br>
This command will append " word1 ", "word2 word3", and "word-n" to Blacklist words list.

### User command
`#delete https://twitter.com/username/status/1234567890?s=19` <br>
Only sender who has sent the menfess that can delete the mentioned tweet link, admin pass this filter.


## Notes
- Admin pass all filters
- Only admin that can setting account with admin command
- All temporary data only available for one day (reset at midnight or heroku dyno cycling)
- If you use github repository to deploy to heroku, make sure to set the repository to private. Github
automatically will delete your github token if your repository is public
- Keywords are not case-sensitive (upper, lower, capitalize)
- See changelogs on [releases's notes](https://github.com/fakhrirofi/twitter_autobase/releases)
- I have written documentation in administrator_data

### Auto accept message requests
This works by sending welcome message to new followers, so Sender must follow the bot. In the beginning, it
fills 50 followers to tw.follower. So it can't track new followers when the bot was just started. If your
followers didn't receive a welcome message from the bot. Unfollow this bot for some minutes then follow it again.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to
change. To make a pull request, see the GitHub documentation on [creating a pull request](https://help.githubcom/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).


## MIT License

Copyright (c) 2020- Fakhri Catur Rofi

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
