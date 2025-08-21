def get_average(marks_list):
    sum=0
    n=len(marks_list)
    for i in range(0,n):
        sum+=marks_list[i]
    return sum/n

def get_grade(avg_marks):
    if avg_marks >= 90:
        return 'A'
    elif avg_marks >= 80 and avg_marks < 90:
        return 'B'
    elif avg_marks >= 70 and avg_marks < 80:
        return 'C'
    elif avg_marks >= 60 and avg_marks < 70:
        return 'D'
    else:
        return 'E'


def main():
    no_student=int(input("Enter Number of students: "))
    name_list=[]
    avg_list=[]
    for i in range(0,no_student):
        name=input("Enter student name: ")
        marks_list=list(map(int,input("Enter 6 subjects marks: ").split(" ")))
        print("Marks List: ",type(marks_list),marks_list)
        name_list.append(name)
        avg_list.append(get_average(marks_list))


    for i in range(0,no_student):
        print("-----------------")
        print('Name: ',name_list[i])
        print('Avg Marks: ',avg_list[i])
        print("Grade: ",get_grade(avg_list[i]))


if __name__ == "__main__":
    main()