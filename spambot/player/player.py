import subprocess, threading

from spambot import spam
from spambot.website import settings
from multiprocessing import Process
import time
import logging
import OSC

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

TIMEOUT = 10*1000

def _play_command(url):
    return ["mplayer", '-ao', 'jack:name=spambot', url]
    #return ["mplayer", url]

if __name__ == "__main__":

    while(True):
        try:
            recording = spam.get_next_recording()
            log.info("Playing %s" % (recording["spam_id"]))
            mp3_url = "%s.mp3" % recording["url"]
            topic = recording["topic"]
            
            if topic in ["sex", "money"]:
                log.info("Sending %s osc message" % (recording["topic"]))
                c = OSC.OSCClient()
                c.sendto(OSC.OSCMessage("/%s" % topic), ("localhost",9998), 10)
                time.sleep(5)
            else:
                c.sendto(OSC.OSCMessage("/neutral"), ("localhost",9998), 10)
            
            p = subprocess.Popen(_play_command(mp3_url))
            starttime = time.time()
            
            while((time.time() - starttime) < TIMEOUT and p.poll() is None):
                time.sleep(1)

            if p.poll() is None:
                log.error("Appears to be hung .. terminating process")
                p.terminate()
            
            log.info("Sleeping for 2 secs before next play")
            time.sleep(2)
        except:
            log.exception("An error occurred during playback!")
            time.sleep(5)
    
    
    
