import subprocess, threading
from spambot import spam
from spambot.website import settings
import time
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            logging.info('Thread started')
            self.process = subprocess.Popen(self.cmd, shell=False)
            self.process.communicate()
            logging.info('Thread finished')

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            log.error('Terminating process')
            self.process.terminate()
            thread.join()
        log.info("Returned with %s" % self.process.returncode)

def _play_command(url):
    return Command(["mplayer", "-ao", "jack:name=spambot", url])

if __name__ == "__main__":
    
    while(True):
        try:
            recording = spam.get_next_recording()
            log.info("Playing %s" % (recording["spam_id"]))
            mp3_url = "%s.mp3" % recording["url"]
            command = _play_command(mp3_url)
            command.run(timeout=5*60)
            log.info("Sleeping for 10 secs before next play")
            time.sleep(10)
        except:
            log.exception("An error occurred during playback!")
            
    
    
    
