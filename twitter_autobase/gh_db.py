from json import dump, load
from html import unescape
from os.path import exists
from datetime import datetime, timedelta, timezone
from time import sleep
from os import remove


def update_local_file(selfAlias, sender_id, message, postid):
    screen_name = selfAlias.get_user_screen_name(sender_id)
    if exists(selfAlias.AdminCmd.filename_github):
        with open(selfAlias.AdminCmd.filename_github, 'r+') as f:
            data = load(f)
            for x in range(len(data)):
                if int(data[x]['id']) == int(sender_id):
                    data[x]['username'] = screen_name
                    data[x]['menfess'].append({'postid': postid, 'text': unescape(message)})
                    break
            else:
                data.append({'username': screen_name, 'id': int(sender_id),
                            'menfess': [{'postid': postid, 'text': unescape(message)}]})
            f.seek(0)
            dump(data, f, indent=4)
            f.truncate()
            f.close()
    else:
        with open(selfAlias.AdminCmd.filename_github, 'w+') as f:
            data = [{'username': screen_name, 'id': int(sender_id),
                    'menfess': [{'postid': postid, 'text': unescape(message)}]}]
            f.seek(0)
            dump(data, f, indent=4)
            f.truncate()
            f.close()


def check_file_github(selfAlias, new=True):
    '''
    :param new: True when bot was just started, download & save file from github -> bool
    False when bot is running. If file exists, doesn't save the file from github.
    'new' parameter used if you update database not every midnight on Database method
    '''
    print("checking github file...")
    try:
        datee = datetime.now(timezone.utc) + \
            timedelta(hours=selfAlias.credential.Timezone)
        selfAlias.AdminCmd.filename_github = "{} {}-{}-{}.json".format(
            selfAlias.bot_username, datee.year, datee.month, datee.day)
        contents = selfAlias.AdminCmd.repo.get_contents("")

        if any(selfAlias.AdminCmd.filename_github == content.name for content in contents):
            # If filename exists in github. But, when midnight,
            # filename automatically changed.
            print(f"filename_github detected, new: {str(new)}")
            if new == False:
                return
            for content in contents:
                if selfAlias.AdminCmd.filename_github == content.name:
                    contents = content.decoded_content.decode()
                    break
        else:
            print("filename_github not detected")
            contents = "[]"
            selfAlias.AdminCmd.repo.create_file(selfAlias.AdminCmd.filename_github, "first commit",
                            contents)

        if exists(selfAlias.AdminCmd.filename_github) == False:
            with open(selfAlias.AdminCmd.filename_github, 'w') as f:
                f.write(contents)
                f.close()
        else:
            pass

        old_filename = "{} {}-{}-{}.json".format(
                selfAlias.bot_username, datee.year, datee.month, datee.day - 1)

        if exists(old_filename):
            remove(old_filename)
            print("Heroku yesterday's Database has been deleted")
        else:
            print("Heroku yesterday's Database doesn't exist")

    except Exception as ex:
        pass
        print(ex)


def gh_database(selfAlias, Github_database=True):
    while True:
        try:
            # update every midnight, you can update directly from DM with 'db_update'
            # check on config.py
            datee = datetime.now(timezone.utc) + timedelta(hours=selfAlias.credential.Timezone)
            if selfAlias.AdminCmd.filename_github != f"{selfAlias.bot_username} {datee.year}-{datee.month}-{datee.day}.json":
                if Github_database is True:
                    print("Github threading active...")
                    contents = selfAlias.AdminCmd.repo.get_contents(selfAlias.AdminCmd.filename_github)
                    with open(selfAlias.AdminCmd.filename_github) as f:
                        selfAlias.AdminCmd.repo.update_file(contents.path, "updating Database", f.read(), contents.sha)
                        f.close()
                    selfAlias.check_file_github(new=False)
                    print("Github Database updated")
                
                else:
                    selfAlias.AdminCmd.filename_github = f"{selfAlias.bot_username} {datee.year}-{datee.month}-{datee.day}.json"

            else:
                sleep(60)

        except Exception as ex:
            print(ex)
            print("Github threading failed..")
            sleep(720)
            pass