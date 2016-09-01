from . import db
from . import ReprMixin

import time


class Comment(db.Model, ReprMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    reply_username = db.Column(db.Integer)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    created_time = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = int(time.time())
        self.tweet_id = form.get('tweet_id', '')

    def json(self):
        self.id
        d = {k: v for k, v in self.__dict__.items() if k not in self.blacklist()}
        return d

    def blacklist(self):
        b = [
            '_sa_instance_state',
        ]
        return b

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
"""
时间问题没有解决，依旧是只用了一个时间
"""
