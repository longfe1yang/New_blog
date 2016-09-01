from . import db
from . import ReprMixin

import time


class Tweet(db.Model, ReprMixin):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    update_time = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='tweet')

    def __init__(self, form):
        print('tweet init', form)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.created_time = int(time.time())
        self.update_time = int(time.time())

    def json(self):
        extra = dict(
            user_id=self.user_id,
        )
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        d.update(extra)
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
        ]
        return b

    def update(self, form):
        self.content = form['content']
        self.title = form['title']
        self.update_time = int(time.time())
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
"""
这里增加了title，因为原先是微博形式，这里换成了博客
没有增加Update暂时
"""
