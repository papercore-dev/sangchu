from warnings import warn
from threading import Thread

class DictSerializerMixin(object):
    def __init__(self, **d):
        __slots__ = "_kwds"
        self._kwds = d

        for key in d:
            if key in self.__slots__ if hasattr(self, "__slots__") else True:
                self.__setattr__(key, d[key])
            else:
                warn("%s라는 키가 %s라는 클래스에서 소실되다! 건너뛰기"%(key, self.__class__.__name__))

        if hasattr(self, "__slots__"):
            for attr in self.__slots__:
                if not hasattr(self, attr):
                    self.__setattr__(attr, None)

def run_on_low_level(func):
    def wrapper(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper
