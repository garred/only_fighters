'''Exercices with multiple inheritance.'''

class First(object):
  def __init__(self):
    super(First, self).__init__()
    print("first")

class Second(object):
  def __init__(self):
    super(Second, self).__init__()
    print("second")

class Third(First, Second):
  def __init__(self):
    super(Third, self).__init__()
    print("that's it")

Third()


class A(object):
    def __init__(self):
        super(A, self).__init__()
        print('A')

class B(A):
    def __init__(self):
        super(B, self).__init__()
        print('B')

class C(B):
    def __init__(self):
        super(C, self).__init__()
        print('C')

class D(B):
    def __init__(self):
        super(D, self).__init__()
        print('D')

class E(A):
    def __init__(self):
        super(E, self).__init__()
        print('E')

class F(C,D,E):
    def __init__(self):
        super(F,self).__init__()
        print('F')

F()


class G(object):
    def __init__(self):
        super(G, self).__init__()
        print('G')
class H(object):
    def __init__(self):
        super(H, self).__init__()
        print('H')
class I(object):
    def __init__(self):
        super(I, self).__init__()
        print('I')
class J(G,H):
    def __init__(self):
        super(J, self).__init__()
        print('J')
class K(J,H):
    def __init__(self):
        super(K, self).__init__()
        print('K')
class L(J,I):
    def __init__(self):
        super(L, self).__init__()
        print('L')

L()





