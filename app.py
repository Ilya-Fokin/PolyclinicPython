from flask import Flask
from flask import session, redirect, request, url_for, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        pass
    return redirect("/")


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    if request.method == 'POST':
        pass
    return redirect("/")


if __name__ == '__main__':
    app.run()
