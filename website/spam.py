# Module for collecting ( pre-collected ) spam
import settings, random, os

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

    return {"spam_id" : spam_id,
            "spam_txt" : spam_txt,
            "emotion" : emotion} 
   
def save_spam_recording(spam_id, emotion, url):
    with open("recordings.csv", "a") as f:
        f.write(spam_id + "," + emotion + "," + url + "\n")

def get_recordings():
    with open("recordings.csv", "r") as f:
        return f.read()
        
        
    
    
    
    
    
    
    

    
