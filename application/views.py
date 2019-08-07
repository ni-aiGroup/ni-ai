from application import app, db
from flask import render_template, redirect, url_for, request


@app.route('/')
@app.route('/index/<int:page_num>', methods=['POST', 'GET'])
def index(page_num=1):
    try:
        col = db['data']
        tol_counts = col.count()
        per_page_counts = 20
        if tol_counts % per_page_counts == 0:
            pages = tol_counts//per_page_counts
        else:
            pages = (tol_counts//per_page_counts)+1
        documents = col.find().limit(per_page_counts).skip((page_num-1)*per_page_counts).sort('_id', -1) #得到集合中所有的文档
        # print(documents)
        docs = []
        count = ((page_num-1)*per_page_counts) + 1
        for doc in documents:
            doc['序号'] = count  #新增属性'序号'
            count += 1
            docs.append(doc)
    except Exception as e:
        err_msg = '数据库操作失败：' + str(e)
        return render_template('error.html', message=err_msg)

    return render_template('main.html', docs=docs, pages=pages)


@app.route('/go_to_page', methods=['POST', 'GET'])
def go_to_page():
    print(request.form['page_content'])
    page_num = request.form['page_content']
    return redirect('/index/'+page_num)


@app.route('/go_to_info/<string:doc_id>', methods=['POST', 'GET'])
def go_to_info(doc_id):
    documents = db.data.find({'病历号': doc_id})
    docs = {}
    for doc in documents:
        docs = doc
    return render_template('edit.html', docs=docs)


@app.route('/go_to_dyjz/<string:doc_id>', methods=['POST', 'GET'])
def go_to_dyjz(doc_id):
    documents = db.data.find({'病历号': doc_id})
    docs = {}
    for doc in documents:
        docs = doc
    return render_template('edit_dyjz.html', docs=docs)


@app.route('/go_to_rkxtz/<string:doc_id>', methods=['POST', 'GET'])
def go_to_rkxtz(doc_id):
    documents = db.data.find({'病历号': doc_id})
    docs = {}
    for doc in documents:
        docs = doc
    return render_template('edit_rkxtz.html', docs=docs)


@app.route('/edit/<string:doc_id>', methods=['POST', 'GET'])
def edit(doc_id):
    documents = db.data.find({'病历号': doc_id})
    docs = {}
    for doc in documents:
        docs = doc
    return render_template('edit.html', docs=docs)


@app.route('/update/<string:doc_id>', methods=['POST', 'GET'])
def update(doc_id):
    db.data.update({'病历号': doc_id},
                   {
                       "个人基本信息": {"医院": request.form['hospital'],
                                      "病历号": request.form['record_id'],
                                      "患者姓名": request.form['name'],
                                      "联系方式": request.form['tel'],
                                      "文件创建时间": request.form['create_time']},

                       "到院就诊": {"患者出现卒中症状时的场所": "",
                                    "患者由何种途径转运至本医院": "",
                                    "患者到院首诊科室": "",
                                    "到院日期和时间": "",
                                    "入院时间": "",
                                    "患者住院科室": "",
                                    "患者出院科室": "",
                                    "住院天数": ""},

                       "人口学特征": {"年龄": "",
                                     "性别": "",
                                     "民族": "",
                                     "医保类型": "",
                                     "文化程度": "",
                                     "家庭人均月收入": "",
                                     "身份证": "",
                                     "籍贯": "",
                                     "职业": "",
                                     "婚姻": ""}
                   })
    return redirect(url_for('index'))


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


@app.route('/delete/<string:doc_id>', methods=['POST', 'GET'])
def delete(doc_id):
    db.data.remove({'病历号': doc_id})
    return redirect(url_for('index'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    # print(request.form['search_content'])

    documents = db.data.find({"$or": [{"医院": {'$regex': request.form['search_content']}},
                                      {"姓名": {'$regex': request.form['search_content']}},
                                      {"性别": {'$regex': request.form['search_content']}},
                                      {"出生日期": {'$regex': request.form['search_content']}},
                                      {"入院日期": {'$regex': request.form['search_content']}},
                                      {"病历号": {'$regex': request.form['search_content']}},
                                      ]})
    docs = []
    for doc in documents:
        # print(doc)
        docs.append(doc)
    # print(docs)

    return render_template('search.html', docs=docs)
