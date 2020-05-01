from flask import *
import pyrebase
import os


config = {
    "apiKey": "AIzaSyCDfuUFSrpBiajdbVYGZTh5WUYLcu6qFCI",
    "authDomain": "alpha-de070.firebaseapp.com",
    "databaseURL": "https://alpha-de070.firebaseio.com",
    "projectId": "alpha-de070",
    "storageBucket": "alpha-de070.appspot.com",
    "messagingSenderId": "994010362096",
    "appId": "1:994010362096:web:0be6bea2548d7eb031d235",
    "measurementId": "G-JMTCKRJP4K"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

app = Flask(__name__)
# Home page
app.secret_key = "karthick"


@app.route("/")
def index():
    return render_template("index.html")

# About page

@app.route("/about.html")
def about():
    return render_template("about.html")

#login page

@app.route("/login.html" , methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        user = auth.sign_in_with_email_and_password(email, password)
        a = auth.get_account_info(user['idToken'])
        b = a["users"][0]["localId"]
        session["email"] = b
        try:
            auth.sign_in_with_email_and_password(email, password)
            return redirect("/appcontent.html")

        except:
            return render_template("login.html", message="Wrong Credentials" )  
    return render_template("login.html")

#sign up page

@app.route("/signup.html" , methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        verify = "Please Check your Inbox to verify your email"
        email = request.form['email']
        password = request.form['pass']
        try:
            auth.create_user_with_email_and_password(email, password)
            return redirect("/login.html")
        except:
            return render_template("signup.html", message="The email is already taken, try another one, please" )
    return render_template("signup.html")    


#app contents

@app.route("/appcontent.html",methods = ['GET','POST'])
def appcontent():
    if "email" in session:
        email = session["email"]
        if request.method == "POST":
            if request.form["submit"] == "add":
                name = request.form["name"]
                db.child("todo").child(email).push(name)
                todo = db.child("todo").child(email).get()
                va = todo.val()
                return render_template("/appcontent.html",t=va.values())
            elif request.form["submit"] == "delete":
                db.child("todo").child(email).remove()
                return render_template("/appcontent.html")

        todo = db.child("todo").child(email).get()
        va = todo.val()
        if va == None:
            return render_template("/appcontent.html")
        else:
            return render_template("/appcontent.html",t=va.values())
    else:
        return redirect(url_for("login"))



#logout route
@app.route("/logout.html")
def logout():
    session.clear()
    return redirect("/")
    
# main 

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",8080)))
