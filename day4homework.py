electric_expenses = {
    "Jan": 500,
    "feb":300,
    "mar":700,
    "april":800,
    "may":900,
    "jun":500,
    "july":800,
    "aug":400,
    "sep":600,
    "oct":600,
    "nov":670,
    "dec":1600,

}
total=sum(electric_expenses.values())


print(f"The total one year electric expenses is {total}")
print(f"Average expenses of one year electric expenses is {total/12}")
print(electric_expenses.keys())
print(electric_expenses.values())
