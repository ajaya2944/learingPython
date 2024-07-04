#wap tpo print even number between start and end using function

#if there is nothing inside braket(), it is called no parameter
#if there is no return keyword,it means function doesnt return any value

# def display_even(first,last):
#     for i in range(first,last+1):
#         if i % 2 != 0:
#             print(i)

       
# start = 100
# end = 150

# display_even(start,end)

## parameter & No Return Type
## Here n1 and n2 are parameters

# def add(n1,n2):
#     total = n1 + n2
#     print(f"total is {total}")

# add(50,60)

# def find_cube (number):
#     cube = number * number * number
#     return cube

# myvalue = find_cube(2)
# print(myvalue)

### no parameter and return Type
def minvoter_age():
    return 18

ram_age = 23
if ram_age >=minvoter_age():
    print("Ram is ready to votes.")