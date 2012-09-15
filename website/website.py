from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from twilio.rest import TwilioRestClient
import twilio.twiml
import re
import logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "http://134.0.22.13"

ACCOUNT_SID = "ACe969e88fdc2000dc53581539404443d9"
AUTH_TOKEN = "f618e5cd5362c61e1ee43d134dc2cdcb"
OUR_NUMBER= "+442033221778"
VALID_PHONE_NUMBER = re.compile('^\+[0-9]*$')

app = Flask(__name__)

def _fqurl(path):
    return BASE_URL + path

@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/record")
def record():
    return render_template("record.html")


# Rest routes for recording through the browser / through the browser with the client.
@app.route("/make_call", methods=["POST"])
def make_call():
    to_number = request.form['number']

    if not VALID_PHONE_NUMBER.match(to_number):
        flash("Please enter a valid phone number, +[Country Code][Area Code][Number]")
        return redirect(url_for('record'))
    
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    call = client.calls.create(to=to_number,  
                           from_=OUR_NUMBER, 
                           url=_fqurl("/handle_call"))
    print call.sid
    print request.form['number']
    return render_template("thanks.html")


# TODO: Routes for handling a call with a text number ( it's a
# seperate number ).



# Methods that handle the actual recording from twilio
@app.route("/handle_call", methods=["POST"])
def handle_call():
    resp = twilio.twiml.Response()
    resp.say("Hello, please record your message.")
    resp.record(maxLength="30", action=_fqurl("/handle_new_recording"))
    return str(resp)

@app.route("/handle_new_recording", methods=['GET', 'POST'])
def handle_recording():
    recording_url = request.values.get("RecordingUrl", None)
    resp = twilio.twiml.Response()
    resp.say("Thanks, this is what you said.")
    resp.play(recording_url)
    resp.say("Goodbye.")
    return str(resp)

if __name__ == "__main__":
    app.secret_key = '\xe8Rd\xf3\xec\x8c\xd7\x12\x03J\xd2\xdb\x14\xa3\xa8\xdf\x11\x0b\xb1)\xd4g\xf4\xa5'
    app.run(host='0.0.0.0', port=80, use_reloader=True)



