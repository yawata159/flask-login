from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
@app.route("/login/")
def start():
    return render_template('basic.html')

@app.route("/authenticate/", methods=["POST"])
def auth():
    user = "fred"
    password = "42"
    if request.method == "POST":
        if request.form["user"] == user and request.form["password"] == password:
            return render_template("response.html", success = True)
        return render_template("response.html", success = False)
    else:
        "You shouldn't be here."
        
if __name__ == '__main__':
    app.run(debug = True)
