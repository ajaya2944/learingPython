import random

# Generate 6 unique random numbers between 1 and 48
choose_lotoNo = int(input("Enter loto No:"))

random_numbers = random.sample(range(1, 49), choose_lotoNo)


# Sort the list of random numbers
sorted_random_numbers = sorted(random_numbers)

print(sorted_random_numbers)
