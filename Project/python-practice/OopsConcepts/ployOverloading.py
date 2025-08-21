class Example:
    def add(self, a=None, b=None, c=None):
        if a is not None and b is not None and c is not None:
            return a + b + c
        elif a is not None and b is not None:
            return a + b
        else:
            return a

obj = Example()
print(obj.add(10, 20, 30))  # Output: 60
print(obj.add(10, 20))      # Output: 30


# class Calculator:
#     def add(self, *args):
#         return sum(args)

# calc = Calculator()
# print(calc.add(1, 2))        # Output: 3
# print(calc.add(1, 2, 3))     # Output: 6
# print(calc.add(1, 2, 3, 4))  # Output: 10


# from multipledispatch import dispatch

# @dispatch(int, int)
# def add(a, b):
#     print(a + b)

# @dispatch(int, int, int)
# def add(a, b, c):
#     print(a + b + c)

# add(2, 3)      # Output: 5
# add(2, 3, 4)   # Output: 9
