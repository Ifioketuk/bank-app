from ast import Not
from pickle import NONE
from typing import Optional
from fastapi import FastAPI,Path
from pydantic import BaseModel


app= FastAPI()
#get=get something new
#post=create something new
#put = update
#delete= delete something

customers = [
    {"Customer_name": "Chinua Achebe", "Account_Balance": 5000.00, "Password": "firetrees", "Account_Number": "1002345678","debit":[],"credit":[]},
    {"Customer_name": "Wole Soyinka", "Account_Balance": 2500.75, "Password": "kongiharvest", "Account_Number": "2005678910","debit":[],"credit":[]},
    {"Customer_name": "Chimamanda Ngozi Adichie", "Account_Balance": 3871.25, "Password": "halfofayellowsun", "Account_Number": "3008912345","debit":[],"credit":[]},
    {"Customer_name": "Ahamefula Achebe", "Account_Balance": 1298.50, "Password": "thingsfall", "Account_Number": "4001234567","debit":[],"credit":[]},
    {"Customer_name": "Ngozi Okonjo-Iweala", "Account_Balance": 7542.00, "Password:": "okonjonomics", "Account_Number": "5004567890","debit":[],"credit":[]},
    {"Customer_name": "Ben Okri", "Account_Balance": 987.65, "Password": "invisiblecity", "Account_Number": "6007890123","debit":[],"credit":[]},
    {"Customer_name": "Adichie Ozumba", "Account_Balance": 2154.90, "Password": "purplehibiscus", "Account_Number": "7001123456","debit":[],"credit":[]},
    {"Customer_name": "Fela Kuti", "Account_Balance": 4328.10, "Password": "afrobeat", "Account_Number": "8004456789","debit":[],"credit":[]},
    {"Customer_name": "John Amaechi", "Account_Balance": 6789.50, "Password": "celtics", "Account_Number": "9007789012","debit":[],"credit":[]},
    {"Customer_name": "Asa", "Account_Balance": 1592.35, "Password": "jata", "Account_Number": "1001012345","debit":[],"credit":[]},
]


class customer(BaseModel):
    name:str
    
    password:str
     







@app.get("/")
def index():
    return {"rubies":"customer data"}

@app.get("/get-customer/")
def check_balance( *,customer_acct:str=Path(...,description="The customer account number"),customer_password:str):
        for customer in customers:
             if customer_acct == customer['Account_Number'] and customer_password== customer['Password']:

                 return {  "name": customer["Customer_name"],
                            "Account number":customer["Account_Number"],
                          "Balance": customer['Account_Balance']}
       
        return {"error":"Account number or password is incorrect."}    
               
#gt is greater than,lt is less than 

    
@app.post("/debit-customer/{Account_number}")
def withdraw_cash(*,Account_number : str,Password: str,amount:int):
    for customer in customers:
        if Account_number == customer['Account_Number'] and Password == customer['Password']:

            if amount > customer['Account_Balance']:
                
                
                
                return {"error":"Insuffcient balance","Balance":customer['Account_Balance']}
            customer['Account_Balance']=customer['Account_Balance'] - amount
            customer["debit"].append(amount)
            
    
            return {"Balance":customer['Account_Balance'],"debited":amount}
    return {"error":"Account number or password is incorrect."}

@app.post("/credit-customer/{Account_number}")
def deposit_cash(Account_number:str, Password:str, amount:int):
     for customer in customers:
            if Account_number == customer['Account_Number'] and Password == customer['Password']:


               if amount > 0:

                      customer['Account_Balance']=customer['Account_Balance'] + amount
                      
                      customer["credit"].append(amount)
                      return "Successfully credited with:${}".format(amount)
 
               return "Balance:${}".format(customer['Account_Balance'])

     return "Account number or password is incorrect."

@app.post("/add_account/{new_acct}")
def create_account(Customer:customer):
    new_account = [('Customer_name',Customer.name),('Account_Balance',0),('Password',Customer.password),('Account_Number',customers["Account_Number"]+1234)]
    customers.append(new_account)
    return "Account successfully created:{}".format(new_account)
    

@app.put("/update-password/{new_password}")
def change_Password(*,Account_number:str, Password:str,New_Password:str):
    for customer in customers:
        if Account_number == customer['Account_Number'] and Password == customer['Password']:
            customer['Password']=New_Password
            return "Password successfully changed\nNew password:{}".format(New_Password)


    return "Account number or password is incorrect."
        
        
@app.delete("/delete-Account/{Account_number}")
def delete_account(Account_number, Password):
    for customer in customers:
        if Account_number == customer['Account_Number'] and Password == customer['Password']:
            confirmation = input("Confirm you want to delete account yes or no: ")
            if confirmation == "yes":
                del customers[customer]
                print("Account has been deleted and is not recoverable")
            elif confirmation == "no":
                print("Account not deleted")
                return "Account Name:{}\nAccount Number:{}".format(customer['Customer_name'],customer['Account_Number'])
            return "Invalid Input"
  
    
    return "Account number or password is incorrect."


@app.post("/generate-bank-statment/{Account_number}")
def bank_statement(Account_number:str,Password:str):
    for customer in customers:
        if Account_number == customer['Account_Number'] and Password == customer['Password']: 
            
            if (customer['credit'] and customer['debit']) == 0:
                return "Account has no transaction history"

            return ("Account name:{} Account Balance:{}".format(customer['Customer_name'],customer['Account_Balance']),
            "credits:{}".format(customer['credit']),
            "debits:{}".format(customer['debit'])
            )
            

            
    
    return "Account number or password is incorrect."


