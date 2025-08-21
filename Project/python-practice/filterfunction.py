a=[10,20,30,40,50,60,70,80,90,100]


def filterfunction(a):
    if a>60:
        return a
    

b=list(filter(filterfunction, a))
print("Filtered list with values greater than 60:", b)