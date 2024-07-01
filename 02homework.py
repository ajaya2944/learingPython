#Write down what you spend each day from Sunday to Saturday, add them up to find the total for the week, and figure out the average amount spent per day.
sun = 400
mon = 500
tues = 400
wed = 800
thur = 400
fri = 1600
sat = 2700

sum = sun + mon + tues + wed + thur + fri + sat
average = sum/7 

print(f"Total spent for the week Rs.{sum}")
print(F"Average spent per day rs. {average : .3f}")
