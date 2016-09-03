#-*- encoding: utf-8 -*-

import os

from flask import Flask, request, session, g, redirect, url_for, abort, \
                render_template, flash

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='sfas90aua#F31#$@wqERQW',
    USERNAME='admin',
    PASSWORD='87238136'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = u'用户名或密码不正确'
        elif request.form['password'] != app.config['PASSWORD']:
            error = u'用户名或密码不正确'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
