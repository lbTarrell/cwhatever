
from __future__ import print_function

from flask_qrcode import QRcode
import re

import pandas as pd
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha

from flask import Flask, flash, redirect, render_template, request, session, abort,make_response, Response,url_for
app=Flask(__name__)
qrcode = QRcode(app)
app.config["SECRET_KEY"] = uuid.uuid4()
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 1
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SESSION_TYPE'] = 'sqlalchemy'
Session(app)
captcha = FlaskSessionCaptcha(app)
class DataStore():

    pp=None
    yy=None
    zza=None
    rr=None
    
data = DataStore()


@app.route("/reset", methods=['POST','GET'])
def reset():
    if captcha.validate():
        data.zza=2
        session['counter']=0
        return redirect('/')
    else:
        return render_template('loginfail.html')

@app.route("/qrcode", methods=["GET"])
def get_qrcode():
    data = request.args.get("data", "")
    return send_file(qrcode(data, mode="raw"), mimetype="image/png")
@app.route('/')
def home():
    if not session.get('logged_in'):
        a=7
        return render_template('login.html',a=a)
    else:
        return render_template("index.html")

@app.route('/login', methods=['POST','GET'])
def do_admin_login():

    if data.zza ==2:
        session['counter'] =3
        data.zza-=1
    if 'counter' not in session:
        session['counter'] = 3
        data.zza=3
    if session.get('counter')>0:
        if request.form['password'] == '111' and request.form['username'] == 'admin' and captcha.validate():
            session['logged_in'] = True
            return render_template("index.html")
        elif request.form['password'] == '111' and request.form['username'] == 'agent' and captcha.validate():
            session['logged_in'] = True
            return render_template("index1.html")
        elif request.form['password'] == '111' and request.form['username'] == 'agent1' and captcha.validate():
            session['logged_in'] = True
            return render_template("index2.html")
        else:
            flash('wrong password!')
            session['counter'] = session.get('counter') - 1
            num=session['counter'] 
            num1='你還有'+str(num)+'次機會嘗試！'
            return render_template('login.html',num1=num1)
    else:
        # session.pop('counter', None)
        return render_template('loginfail.html')
      

@app.route("/logout", methods=['POST','GET'])
def logout():
        session['logged_in'] = False
        return redirect('/')

@app.route("/general", methods=['POST','GET'])
def general():
        return render_template('general.html')
@app.route("/data1", methods=['POST','GET'])
def data1():
        return render_template('data.html')

@app.route("/general1", methods=['POST','GET'])
def general1():
        return render_template('general1.html')
@app.route("/data2", methods=['POST','GET'])
def data2():
        return render_template('data1.html')
@app.route("/general2", methods=['POST','GET'])
def general2():
        return render_template('general2.html')
@app.route("/data3", methods=['POST','GET'])
def data3():
        return render_template('data2.html')
@app.route("/login", methods=['POST','GET'])
def login():
        return render_template('login.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(20)
    app.run()


