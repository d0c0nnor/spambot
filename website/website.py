from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from twilio.rest import TwilioRestClient
import twilio.twiml
import json
import re
import logging
from spam import get_next_spam, save_spam_recording, get_recordings
import settings

logging.basicConfig(level=logging.INFO)

VALID_PHONE_NUMBER = re.compile('^\+[0-9]*$')

app = Flask(__name__)

def _fqurl(path):
    return settings.BASE_URL + path

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/recordings")
def recordings():
    return get_recordings()


# Rest routes for recording through the browser / through the browser with the client.
@app.route("/record", methods=["POST"])
def record():
    to_number = request.form['number']
    
    if not VALID_PHONE_NUMBER.match(to_number):
        flash("Please enter a valid phone number, +[Country Code][Area Code][Number]")
        return redirect(url_for('welcome'))

    spam = get_next_spam()
    spam_id = spam["spam_id"]
    emotion = spam["emotion"]

    client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
    call = client.calls.create(to=to_number,  
                           from_=settings.OUR_NUMBER, 
                           url=_fqurl("/handle_call/" + emotion + "/" + spam_id))

    logging.info("Started call: " +  call.sid)
    return render_template("record.html",spam = spam)

# TODO: Routes for handling a call with a text number ( it's a
# seperate number ).

# Methods that handle the actual recording from twilio
@app.route("/handle_call/<emotion>/<spam_id>", methods=["POST"])
def handle_call(emotion, spam_id):
    resp = twilio.twiml.Response()
    resp.say("Hello, thanks for helping out. When you're finished " )
    resp.record(maxLength="60", action=_fqurl("/handle_new_recording/" + emotion + "/" + spam_id))
    return str(resp)

@app.route("/handle_new_recording/<emotion>/<spam_id>", methods=['GET', 'POST'])
def handle_recording(emotion, spam_id):
    recording_url = request.values.get("RecordingUrl", None)
    resp = twilio.twiml.Response()
    save_spam_recording(spam_id, emotion, recording_url)
    resp.say("Thanks, this is what you said:")
    resp.play(recording_url)
    resp.say("Goodbye.")
    return str(resp)

if __name__ == "__main__":
    app.secret_key = '\xe8Rd\xf3\xec\x8c\xd7\x12\x03J\xd2\xdb\x14\xa3\xa8\xdf\x11\x0b\xb1)\xd4g\xf4\xa5'
    app.run(host='0.0.0.0', port=80, use_reloader=True)


