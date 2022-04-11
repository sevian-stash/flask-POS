from flask import Flask, render_template, flash, redirect, request, url_for, session

app = Flask(__name__)

# Start Class/Method

class IV_Transaction(object):
    
    def __init__(self):
        super(IV_Transaction, self).__init__()

    def add():
        return 

    def read():
        return

    def update():
        return 

    def delete():
        return

class AR_Transaction(object):

    def __init__(self):
        super(AR_Transaction, self).__init__()
    
    def add():
        return 

    def read():
        return

    def update():
        return 

    def delete():
        return

class AP_Transaction(object):

    def __init__(self):
        super(AP_Transaction, self).__init__()
    
    def add():
        return 

    def read():
        return

    def update():
        return 

    def delete():
        return

class Inventory(object):
    
    def __init__(self):
        super(Inventory, self).__init__()

    def add():
        return 

    def read():
        return

    def update():
        return 

    def delete():
        return

class Customer(object):
    
    def __init__(self):
        super(Customer, self).__init__()

    def add():
        return 

    def read():
        return

    def update():
        return 

    def delete():
        return

class User(object):
    
    def __init__(self):
        super(User, self).__init__()

    def add():
        return 

    def read():
        return

    def update():
        return 

    def delete():
        return

# End Class/Method
# Start Route

@app.route("/")
def main():
    # With trx data
    return render_template('view.html')

# Inventory Transaction Route

@app.route("/transaction/add")
def transaction_add():
    return IV_Transaction.add()

@app.route("/transaction/read")
def transaction_read():
    return IV_Transaction.read()

@app.route("/transaction/update")
def transaction_update():
    return IV_Transaction.update()

@app.route("/transaction/delete")
def transaction_delete():
    return IV_Transaction.delete()

# End Inventory Transaction Route
# AR Transaction Route

@app.route("/account_receivable/add")
def account_receivable_add():
    return AR_Transaction.add()

@app.route("/account_receivable/read")
def account_receivable_read():
    return AR_Transaction.read()

@app.route("/account_receivable/update")
def account_receivable_update():
    return AR_Transaction.update()

@app.route("/account_receivable/delete")
def account_receivable_delete():
    return AR_Transaction.delete()

# End AR Transaction Route
# AP Transaction Route

@app.route("/account_payable/add")
def account_payable_add():
    return AP_Transaction.add()

@app.route("/account_payable/read")
def account_payable_read():
    return AP_Transaction.read()

@app.route("/account_payable/update")
def account_payable_update():
    return AP_Transaction.update()

@app.route("/account_payable/delete")
def account_payable_delete():
    return AP_Transaction.delete()

# End AP Transaction Route
# Inventory Route

@app.route("/inventory/add")
def inventory_add():
    return Inventory.add()

@app.route("/inventory/read")
def inventory_read():
    return Inventory.read()

@app.route("/inventory/update")
def inventory_update():
    return Inventory.update()

@app.route("/inventory/delete")
def inventory_delete():
    return Inventory.delete()

# End Inventory Route
# Customer Route

@app.route("/customer/add")
def customer_add():
    return Customer.add()

@app.route("/customer/read")
def customer_read():
    return Customer.read()

@app.route("/customer/update")
def customer_update():
    return Customer.update()

@app.route("/customer/delete")
def customer_delete():
    return Customer.delete()

# End Customer Route
# User Route

@app.route("/user/add")
def user_add():
    return User.add()

@app.route("/user/read")
def user_read():
    return User.read()

@app.route("/user/update")
def user_update():
    return User.update()

@app.route("/user/delete")
def user_delete():
    return User.delete()

# End User Route
