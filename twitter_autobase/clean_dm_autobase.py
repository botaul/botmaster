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
        message = message.split()
        list_keyword = [j.lower() for j in selfAlias.credential.Trigger_word] + \
                    [j.upper() for j in selfAlias.credential.Trigger_word] + \
                    [j.capitalize() for j in selfAlias.credential.Trigger_word]

        [message.remove(j) for j in list_keyword if j in message]
        message = " ".join(message)

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