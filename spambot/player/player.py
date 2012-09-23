import subprocess
from spambot import spam
from spambot.website import settings
import time
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def _play_command(url):
    return ["mplayer", "-ao", "jack:name=spambot", url]

if __name__ == "__main__":
    
    while(True):
        try:
            recording = spam.get_next_recording()
            log.info("Playing %s" % (recording["spam_id"]))
            mp3_url = "%s.mp3" % recording["url"]
            subprocess.call(_play_command(mp3_url))
        except:
            log.exception("An error occurred during playback! - will sleep for 30secs before trying again.")
            time.sleep(30)
    
    
    
