class A:
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.name = "Class A"
        print("This is class A from class A")

class B():
    def __init__(self):
        self.name = "Class B"
        print("This is class B from class B")
    


class C(A,B):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.name = "Class C"
        print("This is class C")


ref = C()  
