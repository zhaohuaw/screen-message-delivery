#-*- encoding: utf-8 -*-

import os
import json
import time

from flask import Flask, request, session, g, redirect, url_for, abort, \
                render_template, flash
from werkzeug.utils import secure_filename
from werkzeug.contrib.cache import SimpleCache


UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'gif'])

def file_ext(filename):
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='sfas90aua#F31#$@wqERQW',
    USERNAME='username',
    PASSWORD='password',
    UPLOAD_FOLDER=UPLOAD_FOLDER,
    DOWNLOAD_INTERVAL=5*60, # 5 minutes
))
app.config.from_envvar('SECRET_KEY', silent=True)
app.config.from_envvar('USERNAME', silent=True)
app.config.from_envvar('PASSWORD', silent=True)
app.config.from_envvar('DOWNLOAD_INTERVAL', silent=True)

cache = SimpleCache()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/ajax/get/update/')
def ajax_update():
    settings = cache.get('settings')

    if not settings:
        with open('delivery.json', 'r') as config_file:
            settings = json.load(config_file)

    if not settings:
        settings = {'error': 'empty'}

    if settings['layout'] == 'layout2': # 自动下载模式
        cached_etag = cache.get('layout2_etag')
        if cached_etag != settings['data']['etag']: # 要重新下载
            from  layout_handlers.layout2 import handler as h
            data = h()
            settings = {'layout': 'layout2', 'data': data }
            with open('delivery.json', 'w') as config_file:
                json.dump(settings, config_file)
            cache.set('settings', settings, 0) # cache forever
            cache.set('layout2_etag', data['etag'],
                    app.config['DOWNLOAD_INTERVAL'])# timeout 5m
            print 'file second'
    #elif settings['layout'] == 'layout1': # 单图主动设置
        #pass
    return json.dumps(settings)

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
                    file_folder = os.path.join(app.config['UPLOAD_FOLDER'],
                            'layout1')
                    # remove old files
                    for fn in os.listdir(file_folder):
                        os.remove(os.path.join(file_folder, fn))

                    #filename = secure_filename(file.filename)
                    filename = file.filename
                    # new random filename
                    save_to = "{0}.{1}".format(str(time.time()),
                            file_ext(filename))
                    save_to = os.path.join(file_folder, save_to)

                    file.save(save_to)

                    flash(u'文件上传成功。')
                    # save the config to a file and then store to cache
                    settings = {'layout': 'layout1', 'data': {'image': '/' +
                        save_to}}
                    with open('delivery.json', 'w') as config_file:
                        json.dump(settings , config_file)
                    cache.set('settings', settings , 0)
                    return redirect(url_for('detail'))
    return render_template('delivery_layout1.html', error=error)

# 自动从指定网站上下载多个图片内容
@app.route('/delivery/layout2/', methods=['GET', 'POST'])
def delivery_layout2():
    error = None
    if not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        settings = {'layout': 'layout2', 'data': {'etag': '', 'images': []}}
        with open('delivery.json', 'w') as config_file:
            json.dump(settings, config_file)
        cache.set('settings', settings, 0)
        return redirect(url_for('detail'))
    return render_template('delivery_layout2.html', error=error)
