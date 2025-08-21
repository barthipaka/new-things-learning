list_numbers=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


def square_if_even(num):
    if num % 2 == 0:
        return num ** 2
    return num ** 3



result=map(square_if_even, list_numbers)
print("List of elements with even numbers squared and odd numbers cubed:", list(result))