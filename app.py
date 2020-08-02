from flask import Flask, request, jsonify, render_template
import sqlite3
import time
import sched


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('root.html')


@app.route('/result/')
def result():
    get_id = request.args.get('id')
    return render_template('result.html')


@app.route('/search/')
def default():
    get_id = request.args.get('id')
    get_num = 100 if request.args.get('num') is None else request.args.get('num')
    return jsonify(search(get_id, get_num))


@app.route('/cookie/')
def cookie():
    cookies = request.args.get('cookie')
    file = open('static/cookie', 'w')
    file.write(cookies)


@app.route('/sql/')
def sql():
    content = request.args.get('sql')
    get_num = 100 if request.args.get('num') is None else request.args.get('num')
    conn = sqlite3.connect('walk.db')
    c = conn.cursor()
    c.execute(content)
    result = []
    for row in c.fetchmany(get_num):
        result.append(row)
    return jsonify(result)


def search(get_id: str, get_num: int):
    result = []
    try:
        conn = sqlite3.connect('walk.db')
        c = conn.cursor()
        c.execute('''
        select Time,Point from Walk where ID == {}
        '''.format(get_id))
        conn.commit()
    except sqlite3.OperationalError as e:
        print('reduce to name')
        c.execute('''
        select Time,Point from Walk where Name == '{}'
        '''.format(get_id))
        conn.commit()
    for row in c.fetchmany(get_num):
        result.append(row)
    return result


if __name__ == '__main__':
    app.run()
