from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
@app.route("/login/")
def start():
    return render_template('basic.html')

@app.route("/authenticate/", methods=["POST"])
def auth():
    uname = "fred"
    passwd = "42"
    if request.method == "POST":
        if request.form["user"] == uname and request.form["password"] == passwd:
            render_template("success.html")
        else:
            render_template("failure.html")
    else:
        "You shouldn't see this"
if __name__ == '__main__':
    app.run(debug = True)
