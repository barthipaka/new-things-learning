class Employee:
    def __init__(self, empname, empid, emprole):
        self.empname = empname
        self.empid = empid
        self.emprole = emprole

    def emp_details(self):
        print(f"Employee details: {self.empid} {self.empname} {self.emprole}")

    def update_details(self, empname=None, empid=None, emprole=None):
        """Modify existing details (only the ones provided)."""
        if empname:
            self.empname = empname
        if empid:
            self.empid = empid
        if emprole:
            self.emprole = emprole

    def delete_details(self):
        """Delete the attributes of the employee."""
        del self.empname
        del self.empid
        del self.emprole
        print("Employee details deleted.")


# Create object
ref_object = Employee("Rakesh Barthiapka", "1714P", "Developer")
ref_object.emp_details()

# Modify object
ref_object.update_details(empname="Rakesh B.", emprole="Senior Developer")
ref_object.emp_details()

# Delete object data
ref_object.delete_details()

# Delete the whole object
del ref_object
