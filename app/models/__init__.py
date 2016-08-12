from .. import db


class ReprMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)


# 在 ReprMixin 后导入所有 model 类
# 这样从这里import出去的User和Tweet都是已经继承了ReprMixin的类
from .user import User
from .tweet import Tweet
