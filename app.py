from flask import Flask, render_template, flash, redirect, request, url_for
from user import User
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'\x87nO\x9bm\xe4Q"\x18\xf7F;\x0f\\v\xe0'

# Create the object first
User = User()

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

class Supplier(object):
    
    def __init__(self):
        super(Supplier, self).__init__()

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

# End Class/Method


# Start Route

@app.route("/")
def index():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    # With trx data
    return render_template('dashboard/index.html')

@app.route("/login/")
def login():
    # With trx data
    return render_template('login/index.html')

@app.route("/logout/")
def logout():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    # With trx data
    return User.logout(redirect(url_for('login')))

# Inventory Transaction Route

@app.route("/transaction/")
def transaction():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('transaction/index.html')

@app.route("/transaction/add/")
def transaction_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return IV_Transaction.add()

@app.route("/transaction/read/<id>/")
def transaction_read(id=None):
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return IV_Transaction.read(id)

@app.route("/transaction/update/")
def transaction_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return IV_Transaction.update()

@app.route("/transaction/delete/")
def transaction_delete():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return IV_Transaction.delete()

# End Inventory Transaction Route
# AR Transaction Route

@app.route("/account_receivable/")
def account_receivable():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('account_receivable/index.html')

@app.route("/account_receivable/add/")
def account_receivable_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return AR_Transaction.add()

@app.route("/account_receivable/read/<id>/")
def account_receivable_read(id=None):
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('account_receivable/detail.html')
    # return AR_Transaction.read(id)

@app.route("/account_receivable/update/")
def account_receivable_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return AR_Transaction.update()

@app.route("/account_receivable/delete/")
def account_receivable_delete():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return AR_Transaction.delete()

# End AR Transaction Route
# AP Transaction Route

@app.route("/account_payable/")
def account_payable():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('account_payable/index.html')

@app.route("/account_payable/add/")
def account_payable_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return AP_Transaction.add()

@app.route("/account_payable/read/<id>/")
def account_payable_read(id=None):
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('account_payable/detail.html')
    # return AP_Transaction.read(id)

@app.route("/account_payable/update/")
def account_payable_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return AP_Transaction.update()

@app.route("/account_payable/delete/")
def account_payable_delete():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return AP_Transaction.delete()

# End AP Transaction Route
# PO Transaction Route

@app.route("/purchase_order/")
def purchase_order():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('')

@app.route("/purchase_order/add/")
def purchase_order_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return PO_Transaction.add()

@app.route("/purchase_order/read/<id>/")
def purchase_order_read(id=None):
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return PO_Transaction.read(id)

@app.route("/purchase_order/update/")
def purchase_order_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return PO_Transaction.update()

@app.route("/purchase_order/delete/")
def purchase_order_delete():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return PO_Transaction.delete()

# End PO Transaction Route
# Purchase Receiving (GRN) Route

@app.route("/purchase_receiving/")
def purchase_receiving():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('')

@app.route("/purchase_receiving/add/")
def purchase_receiving_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return PR_Transaction.add()

@app.route("/purchase_receiving/read/<id>/")
def purchase_receiving_read(id=None):
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return PR_Transaction.read(id)

@app.route("/purchase_receiving/update/")
def purchase_receiving_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return PR_Transaction.update()

@app.route("/purchase_receiving/delete/")
def purchase_receiving_delete():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return PR_Transaction.delete()

# End Purchase Receiving (GRN) Route
# Inventory Route

@app.route("/inventory/")
def inventory():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('inventory/index.html')

@app.route("/inventory/add/")
def inventory_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Inventory.add()

@app.route("/inventory/read/<id>/")
def inventory_read(id=None):
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('inventory/detail.html')
    # return Inventory.read(id)

@app.route("/inventory/update/")
def inventory_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Inventory.update()

@app.route("/inventory/delete/")
def inventory_delete():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Inventory.delete()

# End Inventory Route
# Supplier Route

@app.route("/supplier/")
def supplier():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('supplier/index.html')

@app.route("/supplier/add/")
def supplier_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Supplier.add()

@app.route("/supplier/read/<id>/")
def supplier_read(id=None):
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('supplier/detail.html')
    # return Supplier.read(id)

@app.route("/supplier/update/")
def supplier_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Supplier.update()

@app.route("/supplier/delete/")
def supplier_delete():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Supplier.delete()

# End Supplier Route
# Customer Route

@app.route("/customer/")
def customer():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('customer/index.html')

@app.route("/customer/add/")
def customer_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Customer.add()

@app.route("/customer/read/<id>/")
def customer_read(id=None):
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('customer/detail.html')
    # return Customer.read(id)

@app.route("/customer/update/")
def customer_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Customer.update()

@app.route("/customer/delete/")
def customer_delete():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Customer.delete()

# End Customer Route
# User Route

@app.route("/user/")
def user():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return User.read()

@app.route("/user/login/", methods=['POST'])
def user_login():
    user = escape(request.form['username'])
    password = request.form['password']

    return User.login(user,password)

@app.route("/user/add/", methods = ["POST"])
def user_add():
    user = escape(request.form['username'])
    password = request.form['password']

    if len(password) < 8:
        flash('Please use longer password (Minimum 8 characters)')
        return redirect(url_for('login'))

    return User.add(user,password)

@app.route("/user/read/", methods = ["POST"])
def user_read():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['search_id']) if request.form['search_id'] else None
    return User.read(id)

@app.route("/user/update/", methods = ["POST"])
def user_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    module = ['AP','AR','IV','PR','US']
    user_id = escape(request.form['US_ID'])
    username = escape(request.form['US_NAME'])
    module_permission = dict()

    for id in module:
        module_permission.update({id: {
            '_CREATE':bool(request.form.get(f'{id}_CREATE')),
            '_READ':bool(request.form.get(f'{id}_READ')),
            '_UPDATE':bool(request.form.get(f'{id}_UPDATE')),
            '_DELETE':bool(request.form.get(f'{id}_DELETE'))
        }})

    return User.update(user_id, username, module_permission)

@app.route("/user/update/password/", methods = ["POST"])
def user_update_password():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = request.form['US_ID']
    password = request.form['US_PASSWORD']

    return User.update(id,None,None,password)


@app.route("/user/deactivate/", methods = ["POST"])
def user_deactivate():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    user_id = escape(request.form['US_ID'])
    return User.deactivate(user_id)

@app.route("/user/activate/", methods = ["POST"])
def user_activate():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    user_id = escape(request.form['US_ID'])
    return User.activate(user_id)

# End User Route

# Main 
if __name__ == '__main__':
	app.run(debug=True)