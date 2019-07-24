from application import app, db
from flask import render_template, redirect, url_for, request


@app.route('/')
@app.route('/index/<int:index>')
def index(index=1):
    try:
        page = 20
        col = db['data']
        counts = col.count()
        if counts % page == 0:
            counts = counts//page
        else:
            counts = (counts//page)+1
        documents = col.find().limit(page).skip((index-1)*page) #得到集合中所有的文档
        docs = []
        count = ((index-1)*page) + 1
        for doc in documents:
            doc['序号'] = count  #新增属性'序号'
            count += 1
            docs.append(doc)
    except Exception as e:
        err_msg = '数据库操作失败：' + str(e)
        return render_template('error.html', message=err_msg)

    return render_template('main.html', docs=docs, counts=counts)


@app.route('/delete/<string:doc_id>', methods=['POST', 'GET'])
def delete(doc_id):
    db.data.remove({'病历号': doc_id})
    return redirect(url_for('index'))


@app.route('/update/<string:doc_id>', methods=['POST', 'GET'])
def update(doc_id):
    db.data.update({'病历号': doc_id},
                   {'医院': request.form['hospital'],
                    '姓名': request.form['name'],
                    '性别': request.form['gender'],
                    '出生日期': request.form['bir'],
                    '入院时间': request.form['in_time'],
                    '病历号': request.form['record_id']
                    })
    return redirect(url_for('index'))


@app.route('/edit/<string:doc_id>', methods=['POST', 'GET'])
def edit(doc_id):
    documents = db.data.find({'病历号': doc_id})
    docs = {}
    for doc in documents:
        docs = doc
    return render_template('edit.html', docs=docs)


@app.route('/to_insert', methods=['POST', 'GET'])
def to_insert():
    return render_template('insert.html')


@app.route('/insert', methods=['POST', 'GET'])
def insert():
    dict = {'医院': request.form['hospital'],
            '姓名': request.form['name'],
            '性别': request.form['gender'],
            '出生日期': request.form['bir'],
            '入院时间': request.form['in_time'],
            '病历号': request.form['record_id']
            }
    print(dict)
    db.data.insert(dict)
    return redirect(url_for('index'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    print(request.form['search_content'])

    documents = db.data.find({"$or": [{"医院": request.form['search_content']},
                                      {"姓名": request.form['search_content']},
                                      {"性别": request.form['search_content']},
                                      {"出生日期": request.form['search_content']},
                                      {"入院日期": request.form['search_content']},
                                      {"病历号": request.form['search_content']},
                                      ]})
    docs = []
    for doc in documents:
        print(doc)
        docs.append(doc)
    print(docs)

    return render_template('search.html', docs=docs)
