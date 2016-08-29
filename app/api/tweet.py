from ..models import User
from ..models import Tweet
from . import main
from . import current_user
from . import login_required

from flask import request
from flask import jsonify
from flask import abort


# 绝对路由是http://127.0.0.1:5000/api/tweet/add
@main.route('/tweet/add', methods=['POST'])
def tweet_add():
    u = current_user()
    form = request.get_json()
    t = Tweet(form)
    t.user = u
    t.save()
    r = dict(
        success=True,
        data=t.json(),
    )
    return jsonify(r)


@main.route('/tweet/delete/<tweet_id>')
def tweet_delete(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first()
    print('t.id', t.id)
    if t is None:
        print('这里有个404')
        abort(404)
    user = current_user()
    if user is None or user.id != t.user_id:
        abort(401)
    else:
        t.delete()
        r = {
            'id': t.id,
            'success': True,
            'message': '成功删除',
        }
        return jsonify(r)


# 发送所有人的tweet
@main.route('/tweet/deliver')
# @login_required
def tweet_deliver():
    tweets = Tweet.query.all()
    print('tweets', tweets)
    r = dict(
        success=True,
        data=[t.json() for t in tweets]
    )
    print('debug r', r)
    return jsonify(r)


# TODO
# delete
# update
