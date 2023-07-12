from flask import Flask, request, session
from flask_session import Session
from flask_bcrypt import Bcrypt
from datetime import timedelta
from models import connect_mysql, insert_to_db, login_to_app


app = Flask(__name__)
# app.secret_key = "petedaisy"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
bcrypt = Bcrypt(app)
Session(app)

conn = connect_mysql()
cursor = conn.cursor()

@app.route("/")
def home():
    user = session['user']
    return {"message": user}

@app.route("/register", methods=["GET", "POST"])
def register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    # bcrypt.hashpw(bytes, salt)

    insert_to_db(cursor, conn, first_name, last_name, email, hashed_password)

    return { "message": "Register" }


@app.route("/login", methods=["GET", "POST"])
def login():
    email = request.json['email']
    password = request.json['password']
    user = login_to_app(cursor, email)['user']
    print(user)
    if not user:
        logged_in_state = False
    else:
        password_from_db = user[4]
        logged_in_state = bcrypt.check_password_hash(password_from_db, password)
    
    if logged_in_state:
        session["user"] = user

    return { "message": user }


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user", None)
    return {"message": "Session expired"}

if __name__ == "__main__":
    app.run(port=7000, debug=True)