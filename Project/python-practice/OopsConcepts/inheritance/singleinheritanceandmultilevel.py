class A:
    def __init__(self):
        self.name = "Class A"

    def display(self):
        print("This is class A")

class B(A):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.name = "Class B"

    def display(self):
        super().display()  # Call the display method of the parent class
        print("This is class B")



class C(B):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.name = "Class C"

    def display(self):
        super().display()  # Call the display method of the parent class
        print("This is class C")


ref=C()  # Create an instance of class C
ref.display()  # Call the display method of class C

