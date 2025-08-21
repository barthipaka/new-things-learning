class Animal:
    def eat(self):
        print("Animal eats food")

class Dog(Animal):
    def bark(self):
        print("Dog barks")

class Cat(Animal):
    def meow(self):
        print("Cat meows")
    
# Example usage
d = Dog()
c = Cat()
d.eat()   # Inherited from Animal
d.bark()
c.eat()   # Inherited from Animal
c.meow()
