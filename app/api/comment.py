from ..models import User
from ..models import Tweet
from ..models import Comment
from . import main
from . import current_user
from my_log import log

from flask import request
from flask import jsonify
from flask import abort
from flask import url_for

# 绝对路由是/api/comment/


@main.route('/comment/add/<tweet_id>', methods=['POST'])
def comment_add(tweet_id):
    user = current_user()
    form = request.get_json()
    c = Comment(form)
    # 设置是谁评论的
    # print('c', c.comment_content)
    c.reply_username = user.username
    # c.tweet_id = tweet_id
    c.save()
    counts = Comment.query.filter_by(tweet_id=tweet_id).count()
    r = dict(
        success=True,
        data=c.json(),
        counts=counts,
        next='/details/' + tweet_id,
    )
    print('r', r)
    # print('json', jsonify(r))
    return jsonify(r)


@main.route('/comment/delete/<comment_id>')
def comment_delete(comment_id):
    c = Comment.query.filter_by(id=comment_id).first()
    log('comment.id', c)
    if c is None:
        print('这里有个404')
        abort(404)
    c.delete()
    r = {
        'success': True,
        'message': '成功删除',
    }
    log('这个是r', r)
    return jsonify(r)
