#Here n1,n2 and n3 are number1, number2 and number3

n1 = int(input("Enter First numbe: "))
n2 = int(input("Enter Second numbe: "))
n3 = int(input("Enter Third numbe: "))

if n1 > n2 and n1 > n3:
 print(f"{n1} is greater number.")
elif n2 > n1 and n2 > n3:
    print(f"{n2} is greater the number.")
elif n3 > n1 and n3 > n2:
   print(f"{n3} is greater the number.")
else:
    print("Something went wrong")