from flask import Flask, render_template, request, session, redirect, url_for
import pickle as pk
app = Flask(__name__)
app.secret_key = "jiselectric"

try:
    f = open("user.db", "rb")
    users = pk.load(f)
    f.close()
except:
    users = {}

# Log In
@app.route('/login')
def login():
    return render_template('login.html')

# Verify Log In Data
@app.route('/login_check', methods=["POST"])
def login_check():
    id = request.form.get("id")
    pw = request.form.get("pw")

    if id not in users:
        return "No Matching Account."
    elif users[id] != pw:
        return "Wrong Password."
    else:
        session["login_id"] = id
        return "success"

# After Log In
@app.route('/main')
def main():
    if "login_id" not in session:
        return "<script>alert('Login Needed.');location.href='/login';</script>"
        # return redirect(url_for('login'))
    id = session["login_id"]
    return render_template('main.html', login_id=id)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/regist', methods=["POST"])
def regist():
    id = request.form.get("id")
    pw = request.form.get("pw")

    if id not in users:
        f = open("user.db", "wb")
        pk.dump(users, f)
        f.close()
        return "Account Created"
    else:
        return "Cannot Create"

# ID Check
@app.route('/id_check', methods=["POST"])
def id_check():
    id = request.form.get("id")
    if id in users:
        return "already"
    else:
        return "available"

# Check Users
@app.route('/users')
def getUsers():
    return str(users)

# Logout
@app.route('/logout')
def logout():
    session.pop('login_id', None)
    return 'success'



app.run()