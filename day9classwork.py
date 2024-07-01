#Ask user to enter n number of fruits
# and display all fruits

fruits = []

total_fruit = int(input("Enter fruits number: "))

for i in range (1,total_fruit+1):
    fruit = input(f"Enter fruit {i}:")
    fruits.append(fruit)

    print("\n-----------\n")
    print("Total fruits are :")

    for fruit in fruits:
        print(fruit)
