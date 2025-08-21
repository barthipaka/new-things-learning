class StudentDetails:
    def __init__(self, name, age, roll_no):
        self.name = name
        self.age = age
        self.roll_no = roll_no

    def display(self):
        print(f"Name: {self.name}, Age: {self.age}, Roll No: {self.roll_no}")

# Function to create StudentDetails from a tuple
def create_student(data):
    name, age, roll_no = data
    return StudentDetails(name, int(age), roll_no)

# Get number of students
n = int(input("Enter number of students: "))

# Collect input for each student
students_input = []
for i in range(n):
    print(f"\nEnter details for student {i+1}:")
    name = input("Name: ")
    age = input("Age: ")
    roll_no = input("Roll No: ")
    students_input.append((name, age, roll_no))

# Use map to create StudentDetails objects
students = list(map(create_student, students_input))

# [
#     StudentDetails(name='Rakesh', age=28, roll_no='19UK1A0528'),
#     StudentDetails(name='Anil', age=27, roll_no='19UK1A0529')
# ]

# Display all student details
print("\n--- All Students ---")
for student in students:
    student.display()
