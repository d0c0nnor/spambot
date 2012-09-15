from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

@app.route("/")
def record():
    return render_template("record.html")

@app.route("/add_recording", methods=["POST"])
def add_recording():
    request.form['number']
    print request.form['number']
    return render_template("thanks.html")


if __name__ == "__main__":
    app.run(debug=True)

