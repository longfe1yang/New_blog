from . import main

from flask import request
from flask import render_template
from flask import abort
from flask import redirect
from flask import url_for

from . import User
from . import current_user
from my_log import log


@main.route('/')
def index_view():
    # return render_template('avatar_upload.html')
    return '<h1>头像功能正在完善</h1>'


@main.route('/upload', methods=['POST'])
def upload_file():
    u = current_user()
    user = User.query.filter_by(id=u.id).first()
    file = request.files.get('uploaded')
    log('upload, ', request.files)
    if file:
        filename = file.filename
        path = 'app/static/img/' + filename
        portrait_path = '../static/img/{}.{}'.format(user.username, filename.split('.')[1])
        user.portrait = portrait_path
        user.save()
        log('头像地址', portrait_path)
        log(path)
        # 存储在path这个路径，save是file的属性
        file.save(path)
        return redirect(url_for('controller.timeline_view'))
    else:
        return abort(404)
