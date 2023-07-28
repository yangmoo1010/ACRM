class Test:

    a = 6

    def __init__(self) -> None:
        self.b = 2

    @classmethod
    def class_func(cls):
        cls.a += 1
        return cls.a

    def obj_func(self):
        self.a += 1
        Test.a += 1
        self.b += 1
        return self.a, self.b, Test.a

c = Test()
f = Test()
f.a = 0
print(c.obj_func())
d = Test().class_func()

print(d)
e = Test().class_func()
print(e)
print(c.obj_func())
# print(f.a)
