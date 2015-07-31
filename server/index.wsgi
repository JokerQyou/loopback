# coding: utf-8
from datetime import datetime
import traceback
import sys
from urllib import urlencode

from flask import Flask, request

import sae
from sae.taskqueue import add_task
import sae.kvdb

app = Flask(__name__)
app.debug = True


def extract_traceback():
    e_type, e_value, tb = sys.exc_info()
    return '{0} - Exception happend! {1}"{2}\n{3}'.format(
        datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
        str(e_type), str(e_value), ''.join(traceback.format_tb(tb))
    )


@app.route('/generate_204', methods=('GET', 'POST', 'OPTIONS', 'DELETE', 'PUT', ))
def android_portal():
    try:
        add_task('log', '/log',
                 payload=urlencode({
                    'k': 'android_portal'
                 }),
                 delay=1)
    except Exception as e:
        app.logger.error('添加统计任务时出错：%s', extract_traceback())
    finally:
        return '', 204


@app.route('/', methods=('GET', 'POST', 'OPTIONS', ))
def index():
    text = 'lo'
    try:
        kv = sae.kvdb.Client()
        portal_count = kv.get('android_portal')
        if portal_count is not None:
            text += '\nandroid_portal: %d' % portal_count
        app.logger.debug(locals())
    except Exception as e:
        app.logger.error('取出统计数据时出错：%s', extract_traceback())
    finally:
        if 'kv' in locals():
            kv.disconnect_all()
        return text, 200


@app.route('/log', methods=('GET', 'POST', ))
def log():
    try:
        kv = sae.kvdb.Client()
        key = request.form.get('k', None)
        if key is None:
            return '', 400
        key = str(key)
        count = kv.get(key)
        if count is None:
            kv.set(key, 0)
        else:
            kv.replace(key, count + 1)
        app.logger.debug(locals())
    except Exception as e:
        app.logger.error('进行统计时发生错误：%s', extract_traceback())
    finally:
        if 'kv' in locals():
            kv.disconnect_all()
        return '', 200


application = sae.create_wsgi_app(app)
