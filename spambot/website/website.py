from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from twilio.rest import TwilioRestClient
from twilio.util import TwilioCapability
import twilio.twiml
import json
import re
import logging
from spambot.spam import get_next_spam, save_spam_recording, get_recordings_str, get_next_recording
import spambot.website.settings

logging.basicConfig(level=logging.INFO)

VALID_PHONE_NUMBER = re.compile('^[0-9]*$')

app = Flask(__name__)

def _fqurl(path):
    return settings.BASE_URL + path

@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        to_number = request.form['number']

        if(to_number.startswith("00")):
            to_number = to_number[2:]
        elif(to_number.startswith("+")):
            to_number = to_number[1:]
        else:
            flash("Please enter a valid phone number, +[Country Code][Area Code][Number]")
            return redirect(url_for('welcome'))

        if not VALID_PHONE_NUMBER.match(to_number):
            flash("Please enter a valid phone number, +[Country Code][Area Code][Number]")
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('record',to_number=to_number))

    return render_template("welcome.html")

@app.route("/recordings")
def recordings():
    return get_recordings_str()

# Rest routes for recording through the browser / through the browser with the client.

@app.route("/record/<to_number>", methods=["GET", "POST"])
def record(to_number):
    spam = get_next_spam()
    logging.info("Showing spam %s" %(spam["spam_id"]))
    return render_template('record.html', spam=spam, to_number=to_number)

# TODO: Routes for handling a call with a text number ( it's a
# seperate number ).

@app.route("/call", methods=["POST"])
def place_call():
    emotion = request.form["emotion"]
    spam_id = request.form["spam_id"]
    to_number = request.form["to_number"]

    if not VALID_PHONE_NUMBER.match(to_number):
        abort(400)
    else:
        client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        call = client.calls.create(to="+" + to_number,  
                               from_=settings.OUR_NUMBER, 
                               url=_fqurl("/handle_call/" + emotion + "/" + spam_id))
        logging.info("Started call: " +  call.sid)
        return "Success"


# Methods that handle the actual recording from twilio
@app.route("/handle_call/<emotion>/<spam_id>", methods=["POST"])
def handle_call(emotion, spam_id):
    resp = twilio.twiml.Response()
    resp.say("Hello, thanks for helping out. When you're finished just hang up, there's no need to say goodbye or anything.")
    resp.record(maxLength="300", action=_fqurl("/handle_new_recording/" + emotion + "/" + spam_id))
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

# Methods that handle the actual recording from twilio
@app.route("/dial_a_spam/", methods=["GET", "POST"])
def dial_a_spam():
    if request.method == "POST":
        to_number = request.form['number']
        if not VALID_PHONE_NUMBER.match(to_number):
            flash("Please enter a valid phone number, +[Country Code][Area Code][Number]")
            return redirect(url_for('dial_a_spam'))
        else:
            client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
            call = client.calls.create(to=to_number,  
                                       from_=settings.OUR_NUMBER, 
                                       url=_fqurl("/handle_dial_a_spam"))

            logging.info("Started call: " +  call.sid)
            return render_template("thanks.html")
    else:
        return render_template("dial_a_spam.html")



@app.route("/next_recording", methods=["GET"])
def next_recording():
    return json.dumps(get_next_recording())

    
# Methods that handle the actual recording from twilio
@app.route("/play_a_spam/", methods=["GET"])
def play_a_spam():
    recording_url = get_next_recording()["url"] + ".mp3"
    return render_template("play_a_spam.html", recording_url=recording_url)

@app.route("/handle_dial_a_spam/", methods=["GET"])
def handle_dial_a_spam():
    recording = get_next_recording()
    resp = twilio.twiml.Response()
    resp.play(recording["url"])
    return str(resp)

if __name__ == "__main__":
    app.secret_key = '\xe8Rd\xf3\xec\x8c\xd7\x12\x03J\xd2\xdb\x14\xa3\xa8\xdf\x11\x0b\xb1)\xd4g\xf4\xa5'
    app.run(host='0.0.0.0', port=80)


