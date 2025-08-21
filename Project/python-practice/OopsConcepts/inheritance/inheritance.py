class driver:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print(f"Driver Name: {self.name}, Age: {self.age}")

class license(driver):
    def __init__(self, name, age, license_number):
        driver.__init__(self,name, age)  # Call the constructor of the parent class
        self.license_number = license_number

    def display(self):
        driver.display(self)  # Call the display method of the parent class
        print(f"License Number: {self.license_number}")

# Example usage
refOfLicense = license("John Doe", 30, "DL123456")
refOfLicense.display()