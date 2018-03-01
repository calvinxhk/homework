class Foo:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls,*args,**kwargs)
        return cls._instance


item = Foo()
item1 = Foo()
print(item is item1)