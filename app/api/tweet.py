from ..models import User
from ..models import Tweet
from . import main
from . import current_user
from . import login_required
from my_log import log

from flask import request
from flask import jsonify
from flask import abort
from flask import url_for


def content_cutter(data):
    content_limit = 150
    for i in data:
        content_len = len(i['content'])
        if content_len >= content_limit:
            i['content'] = i['content'][:content_limit] + '......'
    return data


def insert_author(data):
    for i in data:
        user = User.query.filter_by(id=i['user_id']).first()
        i['author'] = user.username
    return data


# 绝对路由是http://127.0.0.1:5000/api/tweet/add
@main.route('/tweet/add', methods=['POST'])
def tweet_add():
    u = current_user()
    form = request.get_json()
    log('get 到数据没', form)
    t = Tweet(form)
    t.user = u
    t.save()
    log('save成功')
    r = dict(
        success=True,
        next='/host',
        # data=t.json(),
    )
    log('jsonify成功')
    return jsonify(r)


@main.route('/tweet/update/<tweet_id>', methods=['POST'])
def update(tweet_id):
    u = current_user()
    t = Tweet.query.filter_by(id=tweet_id).first_or_404()
    form = request.get_json()
    print(form)
    t.update(form)
    print(t)
    r = dict(
        success=True,
        data=t.json(),
    )
    r['next'] = request.args.get('next', url_for('controllers.host_view', user=u))
    print('r', r)
    return jsonify(r)


@main.route('/tweet/delete/<tweet_id>')
def tweet_delete(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first()
    log('t.id', t.id)
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
        log('这个是r', r)
        return jsonify(r)


# 发送所有人的tweet
@main.route('/tweet/deliver')
# @login_required
def tweet_deliver():
    tweets = Tweet.query.all()
    print('tweets', tweets)
    data = [t.json() for t in tweets]
    content_cutter(data)
    insert_author(data)
    r = dict(
        success=True,
        data=data,
    )
    print('debug r', r)
    return jsonify(r)


@main.route('/tweet/<user_id>')
# @login_required
def load_user_blog(user_id):
    tweets = Tweet.query.filter_by(user_id=user_id).all()
    log('user_id', user_id)
    log('tweets', tweets)
    data = [t.json() for t in tweets]
    content_cutter(data)
    insert_author(data)
    r = dict(
        success=True,
        data=data,
    )
    print('debug r', r)
    return jsonify(r)

