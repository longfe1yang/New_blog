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
    t = Tweet(form)
    t.user = u
    t.save()
    r = dict(
        success=True,
        next='/host',
    )
    log('jsonify成功')
    return jsonify(r)


@main.route('/tweet/update/<tweet_id>', methods=['POST'])
def tweet_update(tweet_id):
    # u = current_user()
    t = Tweet.query.filter_by(id=tweet_id).first_or_404()
    form = request.get_json()
    log(form)
    t.update(form)
    r = dict(
        success=True,
        # data=t.json(),
    )
    # r['next'] = request.args.get('next', url_for('controllers.host_view', user=u))
    r['next'] = '/details/{}'.format(tweet_id)
    log('r', r)
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
    log('debug r', r)
    return jsonify(r)


# 返回user自己的所有tweet
@main.route('/tweet/<user_id>')
# @login_required
def load_user_tweet(user_id):
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


# 返回tweet的详情
@main.route('/tweet/details/<tweet_id>')
def tweet_details(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first()
    data = t.json()
    r = dict(
        success=True,
        data=data
    )
    return jsonify(r)
