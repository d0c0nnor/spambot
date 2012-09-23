# Module for collecting ( pre-collected ) spam
import random, os, codecs
from spambot.website import settings

def _get_ids():
    return os.listdir(settings.DATA_PATH)

def get_txt(spam_id):
    with codecs.open(settings.DATA_PATH + os.path.sep + spam_id + os.path.sep + "message.txt", encoding='utf-8') as f:
        return unicode(f.read())

def get_topic(spam_id):
    with open(settings.DATA_PATH + os.path.sep + spam_id + os.path.sep + "topic.txt") as f:
        return f.read()

def get(spam_id):
    spam_txt = get_txt(spam_id)
    spam_topic = get_topic(spam_id)
    emotion = random.choice(settings.EMOTIONS)

    return {"id" : spam_id,
            "text" : spam_txt,
            "emotion" : emotion,
            "topic" : spam_topic
            } 

def get_next():
    """
    TODO: What should this do ?
    - should I check for ones that haven't been read already ?
    """
    spam_id = random.choice(_get_ids())
    return get(spam_id)
   
def save_spam_recording(spam_id, topic, url):
    with open(settings.RECORDINGS_PATH, "a") as f:
        f.write(spam_id + "," + topic + "," + url + "\n")

def get_recordings_str():
    with open(settings.RECORDINGS_PATH, "r") as f:
        return f.read()

def get_recordings():
    with open(settings.RECORDINGS_PATH, 'rb') as csvfile:
        recordings = []
        for line in csvfile.readlines():
            recording_list = line.strip().split(",")
            recordings.append({"spam_id" : recording_list[0],
                               "topic" : recording_list[1],
                               "url": recording_list[2]})
        return recordings
            
def get_next_recording():
    return random.choice(get_recordings())


    
