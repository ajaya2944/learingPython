atm_pin = "1456"

user_pin = ""
attempt = 5

while atm_pin != user_pin:
    if attempt <= 0:
        print("your account has been blocked due to too many incorrect attempts.")
        break
    
    user_pin = input("Enter ATM Pin:")
    
    if user_pin != atm_pin:
        attempt -= 1
        if attempt > 0:
          print(f"invaild pin code. Total Attempt {attempt}")
   
else:

    print("Access Granted. How much you want to withdraw?")
