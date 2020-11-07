# twitter_autobase
A Twitter bot that can read your DMs, then tweets like Twitter autobase. This project is a re-code of [autodm_base](https://github.com/ydhnwb/autodm_base) by [Prieyudha Akadita S.](https://github.com/ydhnwb) with many improvements and fixed bugs. I know this bot is not perfect yet, issues and pull requests are welcome.

- **Read [Twitter rules](https://help.twitter.com/en/rules-and-policies/twitter-search-policies)** <br>
- **USING THIS BOT FOR 'ADULT' BASE IS STRICTLY PROHIBITED** <br>

## Notes
- Admin can send menfess although admin doesn't follow the bot
- Admin pass muted word filters
- If your followers are **less than 5K**, follower filter may work properly. Uncomment line 114-127 on twitter.py (deactivated)
- I have 'commented' (deactivated) some nonessential features for autobase. If you want to make it active, just delete the comments in the script code
- If you use github repository to deploy to heroku, make sure to set the repository to private. Github automatically will delete your github token if your repository is public

### Auto Accept message 
In the beginning, this bot will automatically fill all followers to follower_data. So it can't track new followers when the bot was just started. The algorithms of auto accept message is:
1. Truncate (delete contents) follower_data.txt, fill all followers to follower_data.txt
2. Follower not in follower_data.txt, send message to new follower
3. Follower stop following, remove follower from follower_data.txt <br>
If your followers didn't receive a message from the bot. Unfollow this bot for some minutes then follow it again.

## New Features & Fixed Bugs
- Added muted words
- Only follower can sends menfess and message to admin (deactivated)
- Auto accepts message requests (for open DM) by interacting sending a DM to new follower
- Send DM to admin account (deactivated)
- Notify sender when the menfess sent or not
- Tweet GIF and video
- Edit media for Twitter API requirements
- Make (tweets) a Thread when characters > 280
- Tweet a quote image (deactivated)
- Sync simple database (text) on github repository
- Set muted_words & update database from DM
- Upload more than one media
- fix attachment url 

## Requirements
- Good at basic python programming
- Python 3.7+
- Twitter Developer Account
- Github Account
- Heroku Account

## How to run this bot?
- Install pip3, virtualenv, git, heroku
- Do [Installation](https://github.com/fakhrirofi/twitter_autobase#installation-on-linux)
- Edit [contents](https://github.com/fakhrirofi/twitter_autobase#constants) in constants.py
- [Deploy to Heroku](https://github.com/fakhrirofi/twitter_autobase#deploy-to-heroku)

## [Constants](https://github.com/fakhrirofi/twitter_autobase/blob/master/constants.py)
- Github_token; a token to access your github. Get it from [here](https://github.com/settings/tokens) and set allow for editing repository.
- Github_repo; a repo that will be simple database.
- First_keyword; keyword for video, photo, and GIF.
- Second_keyword; keyword to make quote. (deactivated)
- Sub2_keyword; when menfess contains Second keyword and Sub2 keyword, the sender username will be added to quote. (deactivated)
- Third_keyword; when DMs contains this keyword, the DMs will be sent to admin id. (deactivated)
- Muted_words; when muted words in DMs. The DMs will be deleted.
- Set_keyword; when Set keywords in DMs, it will edit Muted_words.
- Dict_set_keyword; command that will be executed with exec.
- Admin_id; used when DMs contains Third_keyword. You can find the admin id when your admin account send message (when bot active) to autobase account. The sender id is an Admin id.

## Installation on Linux
Note: You can run this bot from Windows as well. Search it on Google. <br>
Open your Linux terminal on the specified folder <br>
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
Run app.py by using syntax: python3 app.py



## DMs examples (based on constants)
You can tweet more than one media with media link on tweet. Open your twitter app then tap (hold) the tweet. media link will automatically copied. then send the link to this bot from DM.
### Quote-retweet
`fess! your message https://twitter.com/username/41890813214140?=19` (by attaching tweet url)
### Make a thread
All menfess keywords are supported with 'making a Thread' when more than 280 characters are given. <br>
`fess! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.` (by attaching media, tweet url, url, or not)
### Normal tweet
`fess! your message` (by attaching media, url, or not)
### Make quote image (deactivated)
Limited to 500 characters <br>
`[quote] your quote` (media and url are not allowed) <br>
`[quote] -s your quote` (media and url are not allowed)
### Ask to admin (deactivated)
`[ask] your message` (by attaching media, url, or not)
### Set
`set! add_muted word1 word2 word3 word-n` (media are not allowed) <br>
`set! rm_muted word1 word2 word3 word-n` (media are not allowed) <br>
`set! db_update`


## Deploy to Heroku
### Deploy with Heroku CLI
Make sure you have deleted the local Database if you previously ran the bot on local.
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
