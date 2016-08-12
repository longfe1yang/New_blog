from . import db
from . import ReprMixin

import time


class Comment(db.Model, ReprMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    sender_name = db.Column(db.String())
    reply_id = db.Column(db.Integer, default=0)
    blog_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    created_time = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
"""
时间问题没有解决，依旧是只用了一个时间
"""
