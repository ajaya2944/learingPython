# countries = ["Nepal","Japan","Korea","USA","Austraila"]

# countries.sort()
# countries.reverse()

# print(countries)

country_capital = {"Nepal":"Kathmandu",
                   "India":"New Delhi",
                   "Japan":"Tokyo",
                   "Bangaladesh":"Dhaka",
                   "Malasiya":"Kuala lumpur",
                   "Singapore":"Singapore"}

country = list(country_capital.keys())
country.sort()
capital = list(country_capital.values())
capital.sort()


print(country)
print(capital)
