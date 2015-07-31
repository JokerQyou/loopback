# coding: utf-8
from flask import Flask, request

import sae

app = Flask(__name__)
app.debug = False


@app.route('/generate_204', methods=('GET', 'POST', 'OPTIONS', 'DELETE', 'PUT', ))
def android_portal():
    app.logger.info(request)
    try:
        sae.taskqueue.add_task('log', '/log',
                               payload={
                                   'k': 'android_portal'
                                },
                               delay=1)
    except Exception as e:
        app.logger.error('添加统计任务时出错：%s', extract_traceback())
    finally:
        return '', 204


@app.route('/', methods=('GET', 'POST', 'OPTIONS', ))
def index():
    return 'lo', 200


@app.route('/log', methods=('GET', 'POST', ))
def log():
    try:
        kv = sae.kvdb.Client()
        key = request.form.get('k', None)
        if key is None:
            return '', 400
        count = kv.get(key)
        if count is None:
            kv.set(key, 0)
        else:
            kv.replace(key, count + 1)
    except Exception as e:
        app.logger.error('进行统计时发生错误：%s', extract_traceback())
    finally:
        if 'kv' in locals():
            kv.disconnect_all()
        return '', 200


application = sae.create_wsgi_app(app)
