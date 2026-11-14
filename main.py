import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'
    data = []
    
    
    try:
        if Path(database).exists():
    
          with open(database) as fs:
              data = json.loads(fs.read())
              
        else:
            print("No Such file Exist")
    except Exception as err:
        print(f"an exception occured as {err}")
    
    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(Bank.data))
            
    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters,k =3)
        num = random.choices(string.digits,k = 3)
        spchar = random.choices("!@#$%^&*",k = 1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)
    
        
    
    
    
    def Createaccount(self):
        info ={
            "Name": input("Tell your Name :-"),
            "Age": int(input("Tell your Age :- ")),
            "Email": input("Tell your Email :-"),
            "Pin": int(input("Enter your PIN")),
            "Account_Number": Bank.__accountgenerate(),
            "Balance": 0
        }
        if info['Age'] < 18 or len(str(info['Pin'])) !=4:
            print("Sorry you cannot create an account")
        else:
            print("account has be created successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("Please Note down your account Number")
            
            Bank.data.append(info)
            
            Bank.__update()
            
    def Depositmoney(self):
        Account_Number = input("Please Enter  your Account Number")
        Pin = int(input("Please Enter your Pin"))
        
        userdata = [i for i in Bank.data if i['Account_Number'] == Account_Number and i['Pin'] == Pin]
        
        if userdata == False:
            print("Oops No Data Found")
            
        else:
            Amount = int(input("How much you want to deposit"))
            if Amount > 10000 or Amount < 0:
                print("Daily amount deposit is only 10000 or below 10000")
            else:
                print(userdata)
                userdata[0]["Balance"] += Amount
                Bank.__update()
                print("Your amount is deposited successfully")
                
                
    def Withdrawmoney(self):
            Account_Number = input("Please Enter  your Account Number")
            Pin = int(input("Please Enter your Pin"))
            
            userdata = [i for i in Bank.data if i['Account_Number'] == Account_Number and i['Pin'] == Pin]
            
            if userdata == False:
                print("Oops No Data Found")
                
            else:
                Amount = int(input("How much you want to withdraw"))
                if userdata[0]['Balance'] < Amount:
                    print("Sorry your account have insufficient balance ")

                else:
                    print(userdata)
                    userdata[0]["Balance"] -= Amount
                    Bank.__update()
                    print("Cash withdrawal successfully")   
                  
    def Showdetails(self):
                Account_Number = input("Please Enter  your Account Number")
                Pin = int(input("Please Enter your Pin"))
                
                userdata = [i for i in Bank.data if i['Account_Number'] == Account_Number and i['Pin'] == Pin]
                print("Your information are \n\n\n")
                for i in userdata[0]:
                    print(f"{i} : {userdata[0][i]}")
                    
                    
    def Updatedetails(self):
                Account_Number = input("Please Enter  your Account Number")
                Pin = int(input("Please Enter your Pin"))
                                
                userdata = [i for i in Bank.data if i['Account_Number'] == Account_Number and i['Pin'] == Pin]
                
                if userdata == False:
                    print("No user found")
                else:
                    print("You cannot change the age, account number, balance")
                    
                    print("Fill the details for Change else keep empty")
                    
                    newdata = {
                        "Name": input("Please enter the new Name or press enter to skip : "),
                        "Email": input("Please enter your new Email or press enter to skip : "),
                        "Pin":input("Enter the new Pin or press enter to skip : ")
                    }
                    
                    if newdata["Name"] == "":
                        newdata["Name"] = userdata[0]['Name']
                    if newdata["Email"] == "":
                        newdata["Email"] = userdata[0]['Email']
                    if newdata["Pin"] == "":
                        newdata["Pin"] = userdata[0]['Pin']
                        
                    newdata["Age"] = userdata[0]["Age"]
                    
                    newdata["Account_Number"] = userdata[0]["Account_Number"]
                
                    newdata["Balance"] = userdata[0]["Balance"]
                    
                    if type(newdata["Pin"]) == str:
                        newdata["Pin"] = int(newdata["Pin"])
                        
                    for i in newdata:
                        if newdata[i] == userdata[0][i]:
                            continue
                        else:
                            userdata[0][i] = newdata[i]
                    
                    Bank.__update()
                    print("Details updated successfully")
                    
    def Delete(self):
            Account_Number = input("Please Enter  your Account Number")
            Pin = int(input("Please Enter your Pin"))
                                            
            userdata = [i for i in Bank.data if i['Account_Number'] == Account_Number and i['Pin'] == Pin]
            
            if userdata == False:
                print("No data Exist")
            else:
                check = input(" Press Y if you want to delete the Account or Press N ")
                if check == 'N' or check == 'N':
                    print("Bypassed")
                else:
                    index = Bank.data.index(userdata[0])
                    Bank.data.pop(index)
                    print("Account  deleted Successfully")
                    Bank.__update()
                
                
user = Bank()
print("Press 1 for Creating an Account")
print("Press 2 for Despositing the Money in the Bank")
print("Press 3 for Withdrawing the Money")
print("Press 4 for Details")
print("Press 5 for Updating the Details")
print("Press 6 for Deleting your Account")

check = int(input("Tell your Response :- "))

if check == 1:
    user.Createaccount()
    
if check == 2:
    user.Depositmoney()
    
if check ==3:
    user.Withdrawmoney()
    
if check ==4:
    user.Showdetails()
    
if check ==5:
    user.Updatedetails()
    
if check ==6:
    user.Delete()
    