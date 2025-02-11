from Flask import flask, render_template
from flask-login import UserMixin, login_required, login_user, logout_user, current_user
import sqlite

app = flask(__name__)
app.secret_key = "6924[j)zm>;%?(C4dyh~,dj<%"

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(Self, Id, Username, Password):
        self.id = Id
        self.username = Username
        self.password = Password

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route('/')
@app.route('/dashboard')
def home():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")


if __name__ ==  "__main__":
    app.run(debug=True, host="0.0.0.0")
