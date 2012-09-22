# Module for collecting ( pre-collected ) spam
import spambot.website.settings
import random, os

def _get_spam_ids():
    return os.listdir(settings.DATA_PATH)

def _get_spam_txt(spam_id):
    with open(settings.DATA_PATH + os.path.sep + spam_id + os.path.sep + "message.txt") as f:
        return f.read()

def get_next_spam():
    """
    TODO: What should this do ?
    - should I check for ones that haven't been read already ?
    """
    spam_id = random.choice(_get_spam_ids())
    spam_txt = _get_spam_txt(spam_id)
    emotion = random.choice(settings.EMOTIONS)

    return {"id" : spam_id,
            "spam_txt" : spam_txt,
            "emotion" : emotion} 
   
def save_spam_recording(spam_id, emotion, url):
    with open(settings.RECORDINGS_PATH, "a") as f:
        f.write(spam_id + "," + emotion + "," + url + "\n")

def get_recordings_str():
    with open(settings.RECORDINGS_PATH, "r") as f:
        return f.read()

def get_recordings():
    with open(settings.RECORDINGS_PATH, 'rb') as csvfile:
        recordings = []
        for line in csvfile.readlines():
            recording_list = line.split(",")
            recordings.append({"spam_id" : recording_list[0],
                               "emotion" : recording_list[1],
                               "url": recording_list[2]})
        return recordings
            
def get_next_recording():
    return random.choice(get_recordings())
        


    

    
        
    
    
    
    
    
    
    

    
