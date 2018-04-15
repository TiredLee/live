from flask import Flask, render_template, request
from flask_script import Manager, Server
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql
from sqlalchemy import or_


app = Flask(__name__)
manager = Manager(app)
manager.add_command('runserver', Server('127.0.0.1', port=5000))
# 添加python链接数据库的驱动
pymysql.install_as_MySQLdb()
# 获取当前目录的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# 配置flask链接数据库的地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/live'
# 关闭警告 当数据库发生改变 警告就会出现
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 创建sqlalchemy对象
db = SQLAlchemy(app)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.String(20))
    rn = db.Column(db.String(200))
    nn = db.Column(db.String(100))
    ol = db.Column(db.Integer)
    preview = db.Column(db.String(300))
    url = db.Column(db.String(200))
    category = db.Column(db.String(100))
    live_category = db.Column(db.String(10))

    __tablename__ = 'room'


category_dict = {
    'lol': '英雄联盟',
    'dnf': 'DNF',
    'lscs': '炉石传说',
    'jdqs': '绝地求生',
    'zj': '主机游戏',
    'hw': '户外',
    'ms': '美食',
}


# 创建视图函数
@app.route('/')
def index():
    page = 1
    rooms = Room.query.filter_by(live_category='douyu').order_by(Room.ol.desc()).paginate(page, per_page=40,
                                                                                          error_out=True)
    return render_template('index.html', rooms=rooms, category='douyu')


# @app.route('/<category>/')
# def category_page(category):
#     rooms = Room.query.filter_by(live_category=category)
#     return render_template('index.html', rooms=rooms, category=category)


@app.route('/<category>/<int:page>/')
def category_page1(category, page):
    if category == 'all':
        rooms = Room.query.order_by(Room.ol.desc()).paginate(page, per_page=40, error_out=True)
    else:
        rooms = Room.query.filter_by(live_category=category).order_by(Room.ol.desc()).paginate(page, per_page=40,
                                                                                               error_out=True)
    return render_template('index.html', rooms=rooms, category=category)


@app.route('/<category1>/<category2>/<int:page>/')
def category_page2(category1, category2, page):
    category2 = category_dict[category2]
    if category1 == 'all':
        rooms = Room.query.filter_by(category=category2).order_by(Room.ol.desc()).\
            paginate(page, per_page=40, error_out=True)
    else:
        rooms = Room.query.filter_by(live_category=category1).filter_by(category=category2).\
            order_by(Room.ol.desc()).paginate(page, per_page=40, error_out=True)
    return render_template('index.html', rooms=rooms, category=category1)


@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        page = 1
        if keyword.isdigit():
            rooms = Room.query.filter(Room.rid.ilike('%{0}%'.format(keyword))).\
                order_by(Room.ol.desc()).paginate(page, per_page=40, error_out=True)
        else:
            rooms = Room.query.filter(or_(Room.rn.ilike('%{0}%'.format(keyword)),
                                          Room.nn.ilike('%{0}%'.format(keyword))))\
                .order_by(Room.ol.desc()).paginate(page, per_page=40, error_out=True)
        return render_template('index.html', rooms=rooms)


# 启动应用实例
if __name__ == '__main__':
    app.run(debug=True)

    # gunicorn -w 4 -b 127.0.0.1:8080 live:app







