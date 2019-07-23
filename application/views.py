from application import app, db
from flask import render_template, redirect, url_for, request
from pymongo import MongoClient


@app.route('/')
@app.route('/index')
def index():
    try:
        col = db['data']
        documents = col.find()
        docs = []
        count = 1
        for doc in documents:
            doc['序号'] = count
            count += 1
            docs.append(doc)
    except Exception as e:
        err_msg = '数据库操作失败：' + str(e)
        return render_template('error.html', message=err_msg)

    return render_template('main.html', docs=docs)


# @app.route('/insert', methods=['POST', 'GET'])
# def insert():
#     db.data.insert()


@app.route('/delete/<string:doc_id>', methods=['POST', 'GET'])
def delete(doc_id):
    db.data.remove({'病历号': doc_id})
    return redirect(url_for('index'))


@app.route('/update/<string:doc_id>', methods=['POST', 'GET'])
def update(doc_id):
    db.data.update({'病历号': doc_id}, {'医院': '省人民医院'})
    return redirect(url_for('index'))


@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route('/to_insert')
def to_insert():
    return render_template('insert.html')


@app.route('/insert', methods=['POST', 'GET'])
def insert():
    dict = {'医院': request.form['hospital'],
            '姓名': request.form['name'],
            '性别 ': request.form['gender'],
            '出生日期 ': request.form['bir'],
            '入院时间 ': request.form['in_time'],
            '病历号': request.form['record_id']
            }
    print(dict)
    db.data.insert(dict)
    return redirect(url_for('index'))

