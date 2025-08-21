class A:
    def __init__(self):
        self.a="This is from A class"
        print(f'{self.a}')


class B(A):
    def __init__(self):
        A.__init__(self)
        self.b="This is from B class"
        print(f'{self.b}')


class C(B):
    def __init__(self):
        B.__init__(self)
        self.c="This is from C class"

class D(C,B):
    def __init__(self):
        C.__init__(self)
        self.d="This is from D class"
        print(f'this is from D class{self.d, self.c} ')

 
refObj=D()
print(D.mro())



