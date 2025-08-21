class A:
    def __init__(self):
        self.name = "Class A"

    def display(self):
        print("This is class A")

class B(A):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class

    def display(self):
        super().display()  # Call the display method of the parent class
        print("This is class B",self.name)

class C(A):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class
        self.name = "Class C"
        print("This is class C",self.name)

    def display(self):
        super().display()  # Call the display method of the parent class
        print("This is class C",self.name)

# Example usage
refOfC = C()  # Create an instance of class C
refOfC.display()  # Call the display method of class C
refOfB = B()
refOfB.display()

