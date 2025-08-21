def palindrome_number(n:int):
    return str(n)==str(n)[::-1]


a=palindrome_number(1231)
if a:
    print("The number is a palindrome")
else:
    print("The number is not a palindrome") 

