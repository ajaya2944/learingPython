def age_finder(birth_year):
    age = 2024 - birth_year
    return age

# Call the function and print the result
birth_year = int(input("Enter your birth year: "))
age = age_finder(birth_year)
print(f"Age is {age}")
