from flask import render_template
from flask import session
from flask import Blueprint
from flask import jsonify

from ..models import User
from ..models import Tweet

from my_log import log

main = Blueprint('controllers', __name__)


# 通过 session 来获取当前登录的用户
def current_user():
    # print('session, debug', session.permanent)
    username = session.get('username', '')
    u = User.query.filter_by(username=username).first()
    return u


# 除了current_user()外的所有user
def other_users():
    u = current_user()
    all_users = User.query.all()
    return [i for i in all_users if i != u]


@main.route('/timeline')
def timeline_view():
    u = current_user()
    others = other_users()
    return render_template('tweet_timeline.html', user=u, others=others)


@main.route('/host')
def host_view():
    u = current_user()
    others = other_users()
    return render_template('tweet_host.html', user=u, others=others)


@main.route('/publish')
def publish():
    return render_template('tweet_publish.html', action='publish', b=None)


@main.route('/update/<tweet_id>')
def update_view(tweet_id):
    t = Tweet.query.filter_by(id=tweet_id).first_or_404()
    return render_template('tweet_update.html', t=t, action=True)


@main.route('/details/<tweet_id>')
def tweet_details(tweet_id):
    u = current_user()
    t = Tweet.query.filter_by(id=tweet_id).first()
    author = User.query.filter_by(id=t.user_id).first()
    d = dict(
        user=u,
        tweet=t,
        author=author.username
    )
    return render_template('tweet_details.html', **d)

# @main.route('/timeline/<username>')
# def user_timeline_view(username):
#     u = User.query.filter_by(username=username).first_or_404()
#     return render_template('tweet_timeline.html', user=u)
