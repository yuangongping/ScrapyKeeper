from ScrapyKeeper.model import Base


class BaseSrv(object):
    def __init__(self, orm: "Base"):
        self.orm = orm

    def save(self, **kwargs):
        return self.orm.save(kwargs)

    def all(self, _to_dict: bool = True):
        return self.orm.all(_to_dict)

    def delete(self, **kwargs):
        return self.orm.delete(kwargs)
