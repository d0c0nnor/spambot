import os
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


PROFILE = os.environ.get("SPAMBOT_SETTINGS_PROFILE", "DEV")
log.warn("Using settings profile: %s" % PROFILE)

ACCOUNT_SID = "ACe969e88fdc2000dc53581539404443d9"
AUTH_TOKEN = "f618e5cd5362c61e1ee43d134dc2cdcb"
OUR_NUMBER= "+442033221778"

EMOTIONS = ["angry",
            "happy",
            "sleepy",
            "bashful"]

if PROFILE == "PROD":
    DATA_PATH="/var/spambot/data"
    RECORDINGS_PATH="/var/spambot/recordings.csv"
    BASE_URL = "http://134.0.22.13"
    

elif PROFILE == "DEV":
    DATA_PATH=os.path.dirname(__file__) + "/../sample_data"
    RECORDINGS_PATH="recordings.csv"
    BASE_URL = "http://47rt.localtunnel.com"
    



