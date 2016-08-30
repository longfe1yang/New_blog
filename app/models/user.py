from . import db
from . import ReprMixin

import time

"""
users表的信息，
id、username、password、note、created_time、
没有特别声明，created_time都是清真的time，想用什么格式就用什么格式
"""


class User(db.Model, ReprMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    note = db.Column(db.String(), nullable=True)
    sex = db.Column(db.String())
    role = db.Column(db.Integer, default=2)
    created_time = db.Column(db.Integer)
    # 这里为啥指代时间，因为下面初始化时间指定为time.time()
    # 外键关联
    tweets = db.relationship('Tweet', backref='user')

    @staticmethod
    # 下面这个是什么？静态方法！
    def user_by_name(username):
        return User.query.filter_by(username=username).first()

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.sex = form .get('sex', '')
        self.note = form.get('note', '')
        # 在初始化数据的时候写入 unixtime
        # 这样不依赖数据库的功能, 可以通用
        # 这个意思是可以按照自己需要的格式在需要显示的地方来显示
        self.created_time = int(time.time())

    def json(self):
        # Model 是延迟载入的, 如果没有引用过数据, 就不会从数据库中加载
        # 引用一下 id 这样数据就从数据库中载入了
        self.id
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
            'password',
        ]
        # _sa_instance_state 是db.modole自动加载进去的
        return b

    # 验证登录用户合法性
    def validate_auth(self, form):
        username = form.get('username', '')
        password = form.get('password', '')
        username_equals = self.username == username
        password_equals = self.password == password
        print('validate auth', username, password, username_equals, password_equals)
        return username_equals and password_equals

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # 验证注册用户的合法性
    def register_validate(self):
        min_len = 3
        valid_username = User.query.filter_by(username=self.username).first() == None
        valid_username_len = len(self.username) >= min_len
        valid_password_len = len(self.password) >= min_len
        msgs = []
        if not valid_username:
            message = '用户名已经存在'
            msgs.append(message)
        elif not valid_username_len:
            message = '用户名长度必须大于等于 3'
            msgs.append(message)
        elif not valid_password_len:
            message = '密码长度必须大于等于 3'
            msgs.append(message)
        else:
            message = '用户注册成功'
            msgs.append(message)
        status = valid_username and valid_username_len and valid_password_len
        return status, msgs
"""
这里没有增加管理员权限，
这里的时间是有区别的，没用彭彭的，暂时这么吧
"""
