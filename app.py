from flask import Flask, render_template, request
from hashlib import sha512
import csv

app = Flask(__name__)


@app.route("/")
@app.route("/login/")
def start():
    return render_template("home.html")

@app.route("/authenticate/", methods=["POST"])
def auth():
    user = request.form["user"]
    password = request.form["password"]

    if user == "" or password == "":
        return render_template("home.html", empty_field = True)
    
    if request.method == "POST":
        if 'register' in request.form:
            user_list = [row[0] for row in csv.reader(open("data/passwd.csv","r"))]
            
            if user in user_list:
                return render_template("home.html", user_exists = True, user = user)

            hashed_pw = sha512(password.encode("utf-8")).hexdigest()
            new_row = '"' + user + '","' + hashed_pw + '"\n'

            append_file = open("data/passwd.csv", "a")
            append_file.write(new_row)
            append_file.close()

            return render_template("home.html", user_created = True)
            
        if "login" in request.form:

            user_pw_dict ={row[0]:row[1] for row in csv.reader(open("data/passwd.csv", "r"))}
            if user in user_pw_dict:
                hashed_pw = sha512(password.encode("utf-8")).hexdigest()                
                if hashed_pw == user_pw_dict[user]:
                    return render_template("loginattempt.html", success = True)
                else:
                    return render_template("loginattempt.html", wrong_passwd = True)
            else:
                return render_template("loginattempt.html", wrong_user = True)            
    else:
        return render_template("home.html")
        
if __name__ == "__main__":
    app.run(debug = True)
