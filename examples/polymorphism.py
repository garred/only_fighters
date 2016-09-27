class A(object):
    def __init__(self):
        super(A, self).__init__()
        self.x = 1
    def say_hi(self):
        print('I\'m A.')

class B(A):
    def __init__(self):
        super(B, self).__init__()
        self.x = 2
    def say_hi(self):
        print('I\'m B.')


b = B()
b.say_hi()
print(b.x)

print(isinstance(b, A))
a = A()
a.__dict__ = b.__dict__
a.say_hi()
print(a.x)