 ### write that print 70 to 100 but not 77,78,81
for i in range(1,101):
    if i == 77 or i == 78 or i == 81:
        continue
    print(i)