'''Stupid example of properties'''

class MyClass(object):
    def __init__(self):
        self.__x = None

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if value > 0:
            self.__x = value
        else:
            self.__x = -(2*value)

a = MyClass()
a.x = 2
print(a.x)
a.x = -3
print(a.x)
print(a.__x)

