#-*- encoding: utf-8 -*-

import os
import json
import random

from flask import Flask, request, session, g, redirect, url_for, abort, \
                render_template, flash
from werkzeug.utils import secure_filename
from werkzeug.contrib.cache import SimpleCache

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def file_ext(filename):
    return filename.rsplit('.', 1)[1]

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='sfas90aua#F31#$@wqERQW',
    USERNAME='admin',
    PASSWORD='87238136',
    UPLOAD_FOLDER=UPLOAD_FOLDER,
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/ajax/get/update/')
def ajax_update():
    cache = SimpleCache()
    d = cache.get('layout')

    if not d:
        with open('delivery.json', 'r') as config_file:
            d = json.load(config_file)

    if not d:
        d = {'error': 'empty'}

    return json.dumps(d)

@app.route('/detail/')
def detail():
    return render_template('detail.html')

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
            flash(u'你已登录系统')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash(u'你已退出系统')
    return redirect(url_for('index'))

@app.route('/delivery/')
def delivery_choices():
    if not session['logged_in']:
        return redirect(url_for('login'))
    return render_template('delivery_choices.html')

# 只有图片
@app.route('/delivery/layout1/', methods=['GET', 'POST'])
def delivery_layout1():
    error = None
    if not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            error = u'请指定背景图片'
        else:
            file = request.files['file']
            if not file.filename:
                error = u'请指定背景图片'
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    save_to = 'bg.' + file_ext(filename)
                    save_to = os.path.join(app.config['UPLOAD_FOLDER'],
                                        'layout1', save_to)
                    file.save(save_to)

                    flash(u'文件上传成功。')
                    # save the config to a file and then store to cache
                    d = {'layout': 'layout1', 'image': '/' + save_to}
                    with open('delivery.json', 'w') as config_file:
                        json.dump(d, config_file)
                    cache = SimpleCache()
                    cache.set('layout', d)
                    return redirect(url_for('detail'))
    return render_template('delivery_layout1.html', error=error)
