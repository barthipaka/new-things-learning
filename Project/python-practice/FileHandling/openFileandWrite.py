with open("data.txt","w") as file:
    content=file.write("This is another line i how this line added in the file ")
    print(content)


with open("data.txt","r") as file:
    content=file.read()
    print(content)
    