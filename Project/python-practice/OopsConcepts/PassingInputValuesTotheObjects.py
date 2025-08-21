class StudentDeatils:
    def __init__(self, name, age, roll_no):
        self.name = name
        self.age = age
        self.roll_no = roll_no

    def display(self):
        print(f"Name: {self.name}, Age: {self.age}, Roll No: {self.roll_no}")

name = input("Enter student's name: ")
age = int(input("Enter student's age: "))
roll_no = input("Enter student's roll number: ")

ref = StudentDeatils(name , age, roll_no)

ref.display()
print("This is the variable access inside the class ",ref.name)