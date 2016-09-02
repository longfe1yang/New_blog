from ..models import Comment
from ..models import User
from . import main

from my_log import log

from flask import abort
from flask import jsonify


@main.route('/user/delete/<user_id>')
def user_delete(user_id):
    u = User.query.filter_by(id=user_id).first()
    log('u.id', u)
    if u is None:
        print('这里有个404')
        abort(404)
    u.delete()
    r = {
        'success': True,
        'message': '成功删除用户{}'.format(u.username),
    }
    log('这里是api中user', r)
    return jsonify(r)
