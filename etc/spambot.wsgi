import sys, os
sys.path.insert(0, '/home/arthack/spambot')

os.environ["SPAMBOT_SETTINGS_PROFILE"] = "PROD"
activate_this = '/home/arthack/spambotpy/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from spambot.website.website import app as application
