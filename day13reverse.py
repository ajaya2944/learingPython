name = "RAM"

reverse_string =""
for i in range(len(name)-1,-1,-1):
    reverse_string = reverse_string + name[i]

print(f"Reverse is {reverse_string}")
