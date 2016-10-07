from flask import Flask, render_template, request, url_for, session, redirect
from hashlib import sha512
import csv

app = Flask(__name__)
app.secret_key = '\x96\xfb"\xed\xcc\xa3J\xb1O\x8dGf\x916!\xa0\x9f#T2S\xb3a\xf0\xa7\xed\xb8\xb4\xa7\x08w\xe2'

def register(user, password):
    user_list = [row[0] for row in csv.reader(open("data/passwd.csv","r"))]
    if user in user_list:
        return render_template("home.html", message = "The username " + user + " is already taken")
    hashed_pw = sha512(password.encode("utf-8")).hexdigest()
    new_row = '"' + user + '","' + hashed_pw + '"\n'
    append_file = open("data/passwd.csv", "a")
    append_file.write(new_row)
    append_file.close()
    return render_template("home.html", message = "Your account has been created" )


def login(user, password):
    user_pw_dict ={row[0]:row[1] for row in csv.reader(open("data/passwd.csv", "r"))}
    if user in user_pw_dict:
        hashed_pw = sha512(password.encode("utf-8")).hexdigest()                
        if hashed_pw == user_pw_dict[user]:
            session['user'] = user
            return redirect(url_for('welcome'))
        else:
            return render_template("home.html", message = "Wrong Password")            
    else:
        return render_template("home.html", message = "That username is not registered (yet!)")
    

@app.route("/")
def root():
    if 'user' in session:
        return redirect(url_for('welcome'))
    else:
        return redirect(url_for('logregister'))


@app.route('/home/')
def welcome():
    if 'user' in session:
        return render_template('welcome.html', user = session['user'])
    else:
        return redirect(url_for('logregister'))

@app.route("/login/")
def logregister():
    if 'user' in session:
        return redirect(url_for('welcome'))
    else:
        return render_template('home.html')

@app.route("/logout/", methods=["POST"])
def logout():
    session.pop('user')
    return redirect(url_for('root'))

@app.route("/authenticate/", methods=["POST", "GET"])
def auth():

    if request.method == "GET":
        return render_template("home.html")

    elif request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]
        
        if user == "" or password == "":
            return render_template("home.html", message = "Username and/or password fields can't be empty")
        
        if 'register' in request.form:
            return register(user,password)
                        
        if "login" in request.form:
            return login(user,password)
    else: 
        return render_template("home.html")

if __name__ == "__main__":
    app.run(debug = True)
