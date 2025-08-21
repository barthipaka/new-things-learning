#if you are using the two **kwargs then it means keywords arguments 


def twoStartArguments(*args, **kwargs):
    """
    This function takes any number of positional arguments and keyword arguments.
    It prints the positional arguments and the keyword arguments.
    """
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)


# Example usage
twoStartArguments(1, 2, 3, name="Alice", age=25, city="Wonderland")