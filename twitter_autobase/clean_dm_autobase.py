def clean_private_autobase(selfAlias, message, media_idsAndTypes, list_attchmentUrlsMedia) -> str:
    '''
    :return: message
    '''
    for media_tweet_url in list_attchmentUrlsMedia:
        list_mediaIdsAndTypes = selfAlias.upload_media_tweet(media_tweet_url[1])
        if len(list_mediaIdsAndTypes):
            media_idsAndTypes.extend(list_mediaIdsAndTypes)
            message = message.split()
            message.remove(media_tweet_url[0])
            message = " ".join(message)
    
    return message


def clean_main_autobase(selfAlias, message, attachment_urls) -> str:
    '''
    :return: message
    '''
    # Keyword Deleter
    if selfAlias.credential.Keyword_deleter:
        list_keyword = [j.lower() for j in selfAlias.credential.Trigger_word]
        
        for word in list_keyword:
            tmp_message = message.lower()
            pos = tmp_message.find(word)
            
            if pos != -1:
                replaced = message[pos : pos + len(word)]
                
                if pos == 0:
                    if len(word) == len(message):
                        pass
                        # Error will happen on post_tweet method. If the message only contains trigger
                        # that will be deleted on replaced variable
                    elif message[pos+len(word)] == " ":
                        # when trigger is placed on the start of text and there is a space after it
                        replaced += " "

                elif message[pos-1] == " ":
                    # when trigger is placed on the middle or the end of text
                    replaced = " " + replaced
                
                message = message.replace(replaced, "")

    # Cleaning attachment_url
    if attachment_urls != (None, None):
        message = message.split()
        if attachment_urls[0] in message:
            message.remove(attachment_urls[0])
        message = " ".join(message)
                            
    # Cleaning hashtags and mentions
    message = message.replace("#", "#/")
    message = message.replace("@", "@/")

    return message