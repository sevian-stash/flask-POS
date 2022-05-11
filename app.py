from flask import Flask, render_template, flash, redirect, request, url_for, session

app = Flask(__name__)

# Start Class/Method

class IV_Transaction(object):
    
    def __init__(self):
        super(IV_Transaction, self).__init__()

    def add():
        return 

    def read(id):
        if id is None:
            # Return all
            return 
        else:
            # return by id
            return
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

    def read(id):
        if id is None:
            # Return all
            return 
        else:
            # return by id
            return
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

    def read(id):
        if id is None:
            # Return all
            return 
        else:
            # return by id
            return
        return

    def update():
        return 

    def delete():
        return

class PO_Transaction(object):

    def __init__(self):
        super(PO_Transaction, self).__init__()
    
    def add():
        return 

    def read(id):
        if id is None:
            # Return all
            return 
        else:
            # return by id
            return
        return

    def update():
        return 

    def delete():
        return

class PR_Transaction(object):

    def __init__(self):
        super(PR_Transaction, self).__init__()
    
    def add():
        return 

    def read(id):
        if id is None:
            # Return all
            return 
        else:
            # return by id
            return
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

    def read(id):
        if id is None:
            # Return all
            return 
        else:
            # return by id
            return
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

    def read(id):
        if id is None:
            # Return all
            return 
        else:
            # return by id
            return
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

    def read(id):
        if id is None:
            # Return all
            return 
        else:
            # return by id
            return
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
    return render_template('dashboard/index.html')

# Inventory Transaction Route

@app.route("/transaction")
def transaction():
    return render_template('transaction/index.html')

@app.route("/transaction/add")
def transaction_add():
    return IV_Transaction.add()

@app.route("/transaction/read/<id>")
def transaction_read(id=None):
    return IV_Transaction.read(id)

@app.route("/transaction/update")
def transaction_update():
    return IV_Transaction.update()

@app.route("/transaction/delete")
def transaction_delete():
    return IV_Transaction.delete()

# End Inventory Transaction Route
# AR Transaction Route

@app.route("/account_receivable/add")
def account_receivable():
    return render_template('')

@app.route("/account_receivable/add")
def account_receivable_add():
    return AR_Transaction.add()

@app.route("/account_receivable/read/<id>")
def account_receivable_read(id=None):
    return AR_Transaction.read(id)

@app.route("/account_receivable/update")
def account_receivable_update():
    return AR_Transaction.update()

@app.route("/account_receivable/delete")
def account_receivable_delete():
    return AR_Transaction.delete()

# End AR Transaction Route
# AP Transaction Route

@app.route("/account_payable/add")
def account_payable():
    return render_template('')

@app.route("/account_payable/add")
def account_payable_add():
    return AP_Transaction.add()

@app.route("/account_payable/read/<id>")
def account_payable_read(id=None):
    return AP_Transaction.read(id)

@app.route("/account_payable/update")
def account_payable_update():
    return AP_Transaction.update()

@app.route("/account_payable/delete")
def account_payable_delete():
    return AP_Transaction.delete()

# End AP Transaction Route
# PO Transaction Route

@app.route("/purchase_order/add")
def purchase_order():
    return render_template('')

@app.route("/purchase_order/add")
def purchase_order_add():
    return PO_Transaction.add()

@app.route("/purchase_order/read/<id>")
def purchase_order_read(id=None):
    return PO_Transaction.read(id)

@app.route("/purchase_order/update")
def purchase_order_update():
    return PO_Transaction.update()

@app.route("/purchase_order/delete")
def purchase_order_delete():
    return PO_Transaction.delete()

# End PO Transaction Route
# Purchase Receiving (GRN) Route

@app.route("/purchase_receiving/add")
def purchase_receiving():
    return render_template('')

@app.route("/purchase_receiving/add")
def purchase_receiving_add():
    return PR_Transaction.add()

@app.route("/purchase_receiving/read/<id>")
def purchase_receiving_read(id=None):
    return PR_Transaction.read(id)

@app.route("/purchase_receiving/update")
def purchase_receiving_update():
    return PR_Transaction.update()

@app.route("/purchase_receiving/delete")
<<<<<<< HEAD
def purchase_receiving_delete():
=======
def purchase_order_delete():
>>>>>>> d5ef66652249fd52f08c9b80dd65bc245cab2731
    return PR_Transaction.delete()

# End Purchase Receiving (GRN) Route
# Inventory Route

@app.route("/inventory/add")
def inventory():
    return render_template('')

@app.route("/inventory/add")
def inventory_add():
    return Inventory.add()

@app.route("/inventory/read/<id>")
def inventory_read(id=None):
    return Inventory.read(id)

@app.route("/inventory/update")
def inventory_update():
    return Inventory.update()

@app.route("/inventory/delete")
def inventory_delete():
    return Inventory.delete()

# End Inventory Route
# Customer Route

@app.route("/customer/add")
def customer():
    return render_template('')

@app.route("/customer/add")
def customer_add():
    return Customer.add()

@app.route("/customer/read/<id>")
def customer_read(id=None):
    return Customer.read(id)

@app.route("/customer/update")
def customer_update():
    return Customer.update()

@app.route("/customer/delete")
def customer_delete():
    return Customer.delete()

# End Customer Route
# User Route

@app.route("/user/add")
def user():
    return render_template('')

@app.route("/user/add")
def user_add():
    return User.add()

@app.route("/user/read/<id>")
def user_read(id=None):
    return User.read(id)

@app.route("/user/update")
def user_update():
    return User.update()

@app.route("/user/delete")
def user_delete():
    return User.delete()

# End User Route

# Main 
if __name__ == '__main__':
	app.run(debug=True)