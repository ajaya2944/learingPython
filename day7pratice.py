import datetime
import nepali_datetime

year = int(input("Enter Nepali Year:"))
month = int(input("Enter Nepali Month:"))
day = int(input("Enter Nepali Day:"))

nepali_date = nepali_datetime.date(year, month, day)
gregorian_date = nepali_date.to_datetime_date()

print(f"The Converted Nepali Date is: {gregorian_date}")