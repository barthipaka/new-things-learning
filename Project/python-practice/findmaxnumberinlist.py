avg_marks=[45,76,87,44,67,87,88,97,98,65]

max_value=-1
n=len(avg_marks)

for i in range(0,n):
    if avg_marks[i]>max_value:    
        max_value=avg_marks[i]

print("Maximum value in the list is:", max_value)