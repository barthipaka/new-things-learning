#creation of class and object

#Class is a blueprint for creating objects it contains attributes and methods
#it is an plan for creating objects
class Student:
    #Constructor method to initialize attributes it will automatically be called when an object is created
    #self is a reference to the current instance of the class
    def __init__(self, nameofStudent, age):
        self.name = nameofStudent  # Instance variable for name
        self.age = age    # Instance variable for age

    #Method to display student information
    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")


#Creating an object of the Student class
student1 = Student("John", 20)  # Creating an instance of Student with name
student2= Student("Doe", 22)  # Creating another instance of Student with name
#Accessing attributes and methods of the object
print(student1.name)  # Output: John
print(student1.age)   # Output: 20
student1.display_info()  # Output: Name: John, Age: 20
student2.display_info()  # Output: Name: Doe, Age: 30


