from flask import Flask, request, make_response, render_template, redirect, url_for
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG') or 'CTF{placeholder_flag_here}'


@app.route('/')
def index():
    role = request.cookies.get('role', '')
    if role == 'admin':
        return render_template('admin.html', flag=FLAG)
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('role', 'guest', httponly=False)
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
