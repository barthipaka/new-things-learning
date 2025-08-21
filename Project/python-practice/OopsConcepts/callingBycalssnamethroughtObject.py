class Studnets:
    overall_Grade= 100
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def display(self):
        print(f"Name: {self.name}, Age: {self.age}")
    
refOfStudnets = Studnets("Rakesh", 20)
refOfStudnets.display()

Studnets.display(refOfStudnets)#This is the way to call the by class name