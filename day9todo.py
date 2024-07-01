# Create progarm that ask user to enter n no of todo and 
todos = []

total_todo = int(input ("Enter total number of todo: "))

for i in range(1,total_todo+1):
    todo = input(f"Enter todo {i}:")
    todos.append(todo)

    print("----------")
    print("All todos are: ")


    for todo in todos:
      print(todo)
    


