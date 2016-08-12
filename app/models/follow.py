from . import db
from . import ReprMixin


class Follow(db.Model, ReprMixin):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    followed_id = db.Column(db.Integer)
    # 关注了哪些用户，配合user_id使用
    follows = db.relationship('User')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

"""
这里没有增加时间，所以不显示什么时候关注
"""