from Flask import flask 


app = flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to your dashboard</h1>"


if __name__ ==  "__main__":
    app.run(debug=True)
