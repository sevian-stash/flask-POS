import re
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_mail import Mail
from user import User
from customer import Customer
from supplier import Supplier
from inventory import Inventory
from transaction import Transaction
from sales_order import Sales_Order
from purchase_order import Purchase_Order
from purchase_receivable import Purchase_Receivable
from account_payable import Account_Payable
from account_receivable import Account_Receivable
from markupsafe import escape

# App Config
app = Flask(__name__)
app.secret_key = b'\x87nO\x9bm\xe4Q"\x18\xf7F;\x0f\\v\xe0' # Session Secret Key
# Flask-Mail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'dapigeotto@gmail.com'
app.config['MAIL_PASSWORD'] = 'uymqlvxmigwrrvat'
app.config['MAIL_DEFAULT_SENDER'] = 'dapigeotto@gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Create the object first
User = User()
Customer = Customer()
Supplier = Supplier()
Inventory = Inventory()
Transaction = Transaction()
Sales_Order = Sales_Order()
Purchase_Order = Purchase_Order()
Purchase_Receivable = Purchase_Receivable()
Account_Payable = Account_Payable()
Account_Receivable = Account_Receivable()
Mail = Mail(app)


# Start Route
@app.template_filter()
def currency(value):
    value = float(value)
    return "Rp.{:,.2f}".format(value)

@app.route("/")
def index():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return render_template('dashboard/index.html')

@app.route("/login/")
def login():
    return render_template('login/index.html')

@app.route("/logout/")
def logout():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return User.logout(redirect(url_for('login')))

# Sales Order Transaction Route

@app.route("/transaction/")
def transaction():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Transaction.read()

# Sales Order Route

@app.route("/sales_order/")
def sales_order():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Sales_Order.read()

@app.route("/sales_order/add/", methods = ["POST"])
def sales_order_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    loop_len = Sales_Order.detail_row_len
    data = dict()

    # Summary
    data.update({'iv11': {
        'IV_ID': escape(request.form.get('IV_ID')),
        'IV_CUSTOMERID': escape((request.form.get('IV_CUSTOMERID')).upper()),
        'IV_PAYMENT': escape(request.form.get('IV_PAYMENT')),
        'IV_QTY': escape(request.form.get('IV_QTY')),
        'IV_AMOUNT': (escape(request.form.get('IV_AMOUNT'))).replace(',','')
        }
    })

    # Details
    data.update({'iv12': {}})
    for i in range(loop_len):
        if bool(request.form.get(f'IV_ID_{i}')):
            data['iv12'].update({f'row_{i}': {
                f'IV_ITEMID': escape(request.form.get(f'IV_ID_{i}')),
                f'IV_ITEMNAME': escape(request.form.get(f'IV_NAME_{i}')),
                f'IV_ITEMQTY': escape(request.form.get(f'IV_QTY_{i}')),
                f'IV_ITEMPRICE': (escape(request.form.get(f'IV_SELLPRICE_{i}'))).replace(',','')
                }
            })

    Sales_Order.email(Mail, data)
    return Sales_Order.add(data)

@app.route("/sales_order/read/", methods = ['POST'])
def sales_order_read():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['search_id'])

    return Sales_Order.read(id)

@app.route("/sales_order/update/", methods = ['POST'])
def sales_order_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    loop_len = Sales_Order.detail_row_len
    data = dict()

    # Summary
    data.update({'iv11': {
        'IV_ID': escape(request.form.get('IV_ID')),
        'IV_CUSTOMERID': escape(request.form.get('IV_CUSTOMERID')),
        'IV_QTY': escape(request.form.get('IV_QTY')),
        'IV_AMOUNT': re.sub('[^0-9,]',escape(request.form.get('IV_AMOUNT'))),
        }
    })

    # Details
    data.update({'iv12': {}})
    for i in range(loop_len):
        if request.form[f'IV_ID_{i}']:
            data_len = len(data['iv12'])
            data['iv12'].update({f'row_{data_len}': {
                'IV_ID': escape(request.form.get('IV_ID')),
                'IV_ITEMID': escape(request.form.get(f'IV_ID_{i}')),
                'IV_ITEMNAME': escape(request.form.get(f'IV_NAME_{i}')),
                'IV_ITEMQTY': escape(request.form.get(f'IV_QTY_{i}')),
                'IV_ITEMPRICE': escape(request.form.get(f'IV_BUYPRICE_{i}'))
                }
            })


    return Sales_Order.update(data)

# End Inventory Transaction Route
# AR Transaction Route

@app.route("/account_receivable/")
def account_receivable():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Account_Receivable.read()

@app.route("/account_receivable/add/", methods = ['POST', 'GET'])
def account_receivable_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    loop_len = Account_Receivable.detail_row_len

    if request.method == 'GET':
        return render_template('account_receivable/add.html', message=loop_len)

    data = dict()

    # Summary
    data.update({'ar11': {
        'AR_CUSTOMERID': escape(request.form.get('AR_CUSTOMERID')),
        'AR_SALESORDERID': escape(request.form.get('AR_SALESORDERID')),
        'AR_AMOUNT': escape(request.form.get('AR_AMOUNT')),
        'AR_STATUS': escape(request.form.get('AR_STATUS')),
        'AR_DUEDT': escape(request.form.get('AR_DUEDT'))
        }
    })

    # Details
    data.update({'ar12': {}})
    for i in range(loop_len):
        if bool(request.form.get(f'IV_ID_{i}')):
            data['ar12'].update({f'row_{i}': {
                f'AR_ITEMID': escape(request.form.get(f'IV_ID_{i}')),
                f'AR_ITEMNAME': escape(request.form.get(f'IV_NAME_{i}')),
                f'AR_ITEMQTY': escape(request.form.get(f'IV_QTY_{i}')),
                f'AR_ITEMPRICE': escape(request.form.get(f'IV_BUYPRICE_{i}'))
                }
            })


    return Account_Receivable.add(data)

@app.route("/account_receivable/read/", methods = ['POST'])
def account_receivable_read():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['search_id'])

    return Account_Receivable.read(id)

@app.route("/account_receivable/update/", methods = ['POST'])
def account_receivable_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    loop_len = Account_Receivable.detail_row_len
    data = dict()

    # Summary
    data.update({'ar11': {
        'AR_ID': escape(request.form.get('AR_ID')),
        'AR_CUSTOMERID': escape(request.form.get('AR_CUSTOMERID')),
        'AR_SALESORDERID': escape(request.form.get('AR_SALESORDERID')),
        'AR_QTY': escape(request.form.get('AR_QTY')),
        'AR_AMOUNT': escape(request.form.get('AR_AMOUNT')),
        'AR_DUEDT': escape(request.form.get('AR_DUEDT')),
        'AR_STATUS': escape(request.form.get('AR_STATUS'))
        }
    })

    # Details
    data.update({'ar12': {}})
    for i in range(loop_len):
        if request.form[f'IV_ID_{i}']:
            data_len = len(data['ar12'])
            data['ar12'].update({f'row_{data_len}': {
                'AR_ID': escape(request.form.get('AR_ID')),
                'AR_ITEMID': escape(request.form.get(f'IV_ID_{i}')),
                'AR_ITEMNAME': escape(request.form.get(f'IV_NAME_{i}')),
                'AR_ITEMQTY': escape(request.form.get(f'IV_QTY_{i}')),
                'AR_ITEMPRICE': escape(request.form.get(f'IV_BUYPRICE_{i}'))
                }
            })


    return Account_Receivable.update(data)

@app.route("/account_receivable/activate/", methods = ["POST"])
def account_receivable_activate():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['AR_ID'])

    return Account_Receivable.activate(id)

# End AR Transaction Route
# AP Transaction Route

@app.route("/account_payable/")
def account_payable():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Account_Payable.read()

@app.route("/account_payable/add/", methods = ['POST', 'GET'])
def account_payable_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    loop_len = Account_Payable.detail_row_len

    if request.method == 'GET':
        return render_template('account_payable/add.html', message=loop_len)

    data = dict()

    # Summary
    data.update({'ap11': {
        'AP_CUSTOMERID': escape(request.form.get('AP_CUSTOMERID')),
        'AP_PURCHASEORDERID': escape(request.form.get('AP_PURCHASEORDERID')),
        'AP_AMOUNT': escape(request.form.get('AP_AMOUNT')),
        'AP_STATUS': escape(request.form.get('AP_STATUS')),
        'AP_DUEDT': escape(request.form.get('AP_DUEDT'))
        }
    })

    # Details
    data.update({'ap12': {}})
    for i in range(loop_len):
        if bool(request.form.get(f'IV_ID_{i}')):
            data['ap12'].update({f'row_{i}': {
                f'AP_ITEMID': escape(request.form.get(f'IV_ID_{i}')),
                f'AP_ITEMNAME': escape(request.form.get(f'IV_NAME_{i}')),
                f'AP_ITEMQTY': escape(request.form.get(f'IV_QTY_{i}')),
                f'AP_ITEMPRICE': escape(request.form.get(f'IV_BUYPRICE_{i}'))
                }
            })


    return Account_Payable.add(data)

@app.route("/account_payable/read/", methods = ['POST'])
def account_payable_read():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['search_id'])

    return Account_Payable.read(id)

@app.route("/account_payable/update/", methods = ['POST'])
def account_payable_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    loop_len = Account_Payable.detail_row_len
    data = dict()

    # Summary
    data.update({'ap11': {
        'AP_ID': escape(request.form.get('AP_ID')),
        'AP_CUSTOMERID': escape(request.form.get('AP_CUSTOMERID')),
        'AP_PURCHASEORDERID': escape(request.form.get('AP_PURCHASEORDERID')),
        'AP_QTY': escape(request.form.get('AP_QTY')),
        'AP_AMOUNT': escape(request.form.get('AP_AMOUNT')),
        'AP_DUEDT': escape(request.form.get('AP_DUEDT')),
        'AP_STATUS': escape(request.form.get('AP_STATUS'))
        }
    })

    # Details
    data.update({'ap12': {}})
    for i in range(loop_len):
        if request.form[f'IV_ID_{i}']:
            data_len = len(data['ap12'])
            data['ap12'].update({f'row_{data_len}': {
                'AP_ID': escape(request.form.get('AP_ID')),
                'AP_ITEMID': escape(request.form.get(f'IV_ID_{i}')),
                'AP_ITEMNAME': escape(request.form.get(f'IV_NAME_{i}')),
                'AP_ITEMQTY': escape(request.form.get(f'IV_QTY_{i}')),
                'AP_ITEMPRICE': escape(request.form.get(f'IV_BUYPRICE_{i}'))
                }
            })


    return Account_Payable.update(data)

@app.route("/account_payable/activate/", methods = ["POST"])
def account_payable_activate():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['AP_ID'])

    return Account_Payable.activate(id)

# End AP Transaction Route
# PO Transaction Route

@app.route("/purchase_order/")
def purchase_order():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Purchase_Order.read()

@app.route("/purchase_order/add/", methods = ["POST","GET"])
def purchase_order_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    loop_len = Purchase_Order.detail_row_len

    if request.method == 'GET':
        return render_template('purchase_order/add.html', message=loop_len)

    data = dict()

    # Summary
    data.update({'po11': {
        'PO_CUSTOMERID': escape(request.form.get('PO_CUSTOMERID')),
        'PO_QTY': escape(request.form.get('PO_QTY')),
        'PO_AMOUNT': escape(request.form.get('PO_AMOUNT')),
        'PO_STATUS': escape(request.form.get('PO_STATUS'))
        }
    })

    # Details
    data.update({'po12': {}})
    for i in range(loop_len):
        if bool(request.form.get(f'IV_ID_{i}')):
            data['po12'].update({f'row_{i}': {
                f'PO_ITEMID': escape(request.form.get(f'IV_ID_{i}')),
                f'PO_ITEMNAME': escape(request.form.get(f'IV_NAME_{i}')),
                f'PO_ITEMQTY': escape(request.form.get(f'IV_QTY_{i}')),
                f'PO_ITEMPRICE': escape(request.form.get(f'IV_BUYPRICE_{i}'))
                }
            })

    return Purchase_Order.add(data)

@app.route("/purchase_order/read/", methods = ["POST"])
def purchase_order_read():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['search_id'])

    return Purchase_Order.read(id)

@app.route("/purchase_order/update/", methods = ["POST"])
def purchase_order_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    loop_len = Purchase_Order.detail_row_len
    data = dict()

    # Summary
    data.update({'po11': {
        'PO_ID': escape(request.form.get('PO_ID')),
        'PO_CUSTOMERID': escape(request.form.get('PO_CUSTOMERID')),
        'PO_QTY': escape(request.form.get('PO_QTY')),
        'PO_AMOUNT': escape(request.form.get('PO_AMOUNT')),
        'PO_STATUS': escape(request.form.get('PO_STATUS'))
        }
    })

    # Details
    data.update({'po12': {}})
    for i in range(loop_len):
        if request.form[f'IV_ID_{i}']:
            data_len = len(data['po12'])
            data['po12'].update({f'row_{data_len}': {
                'PO_ID': escape(request.form.get('PO_ID')),
                'PO_ITEMID': escape(request.form.get(f'IV_ID_{i}')),
                'PO_ITEMNAME': escape(request.form.get(f'IV_NAME_{i}')),
                'PO_ITEMQTY': escape(request.form.get(f'IV_QTY_{i}')),
                'PO_ITEMPRICE': escape(request.form.get(f'IV_BUYPRICE_{i}'))
                }
            })

    return Purchase_Order.update(data)

@app.route("/purchase_order/activate/", methods = ["POST"])
def purchase_order_activate():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['PO_ID'])

    return Purchase_Order.activate(id)

# End PO Transaction Route
# Purchase Receiving (GRN) Route

@app.route("/purchase_receivable/")
def purchase_receivable():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Purchase_Receivable.read()

@app.route("/purchase_receivable/add/", methods = ["POST","GET"])
def purchase_receivable_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    loop_len = Purchase_Receivable.detail_row_len

    if request.method == 'GET':
        return render_template('purchase_receivable/add.html', message=loop_len)

    data = dict()

    # Summary
    data.update({'pr11': {
        'PR_PURCHASEORDERID': escape(request.form.get('PR_PURCHASEORDERID')),
        'PR_CUSTOMERID': escape(request.form.get('PR_CUSTOMERID')),
        'PR_QTY': escape(request.form.get('PR_QTY')),
        'PR_AMOUNT': escape(request.form.get('PR_AMOUNT')),
        'PR_STATUS': escape(request.form.get('PR_STATUS'))
        }
    })

    # Details
    data.update({'pr12': {}})
    for i in range(loop_len):
        if bool(request.form.get(f'IV_ID_{i}')):
            data['pr12'].update({f'row_{i}': {
                f'PR_ITEMID': escape(request.form.get(f'IV_ID_{i}')),
                f'PR_ITEMNAME': escape(request.form.get(f'IV_NAME_{i}')),
                f'PR_ITEMQTY': escape(request.form.get(f'IV_QTY_{i}')),
                f'PR_ITEMPRICE': escape(request.form.get(f'IV_BUYPRICE_{i}'))
                }
            })

    return Purchase_Receivable.add(data)

@app.route("/purchase_receivable/read/", methods = ["POST"])
def purchase_receivable_read():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['search_id'])

    return Purchase_Receivable.read(id)

@app.route("/purchase_receivable/update/", methods = ["POST"])
def purchase_receivable_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    loop_len = Purchase_Receivable.detail_row_len
    data = dict()

    # Summary
    data.update({'pr11': {
        'PR_ID': escape(request.form.get('PR_ID')),
        'PR_PURCHASEORDERID': escape(request.form.get('PR_PURCHASEORDERID')),
        'PR_CUSTOMERID': escape(request.form.get('PR_CUSTOMERID')),
        'PR_QTY': escape(request.form.get('PR_QTY')),
        'PR_AMOUNT': escape(request.form.get('PR_AMOUNT')),
        'PR_STATUS': escape(request.form.get('PR_STATUS'))
        }
    })

    # Details
    data.update({'pr12': {}})
    for i in range(loop_len):
        if request.form[f'IV_ID_{i}']:
            data_len = len(data['pr12'])
            data['pr12'].update({f'row_{data_len}': {
                'PR_ID': escape(request.form.get('PR_ID')),
                'PR_ITEMID': escape(request.form.get(f'IV_ID_{i}')),
                'PR_ITEMNAME': escape(request.form.get(f'IV_NAME_{i}')),
                'PR_ITEMQTY': escape(request.form.get(f'IV_QTY_{i}')),
                'PR_ITEMPRICE': escape(request.form.get(f'IV_BUYPRICE_{i}'))
                }
            })

    return Purchase_Receivable.update(data)

@app.route("/purchase_receivable/activate/", methods = ["POST"])
def purchase_receivable_activate():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['PR_ID'])

    return Purchase_Receivable.activate(id)

# End Purchase Receiving (GRN) Route
# Inventory Route

@app.route("/inventory/")
def inventory():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Inventory.read()

@app.route("/inventory/add/", methods = ["POST","GET"])
def inventory_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('inventory/add.html')

    name = escape(request.form.get('IV_NAME'))
    category = escape(request.form.get('IV_CATEGORY'))
    qty = escape(request.form.get('IV_QTY'))
    buy_price = escape(request.form.get('IV_BUYPRICE'))
    sell_price = escape(request.form.get('IV_SELLPRICE'))
    uom = escape(request.form.get('IV_UOM'))

    return Inventory.add(name, category, qty, buy_price, sell_price, uom)

@app.route("/inventory/read/", methods = ["POST"])
def inventory_read():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['search_id'])

    return Inventory.read(id)
    # return Inventory.read(id)

@app.route("/inventory/update/", methods = ["POST"])
def inventory_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form.get('IV_ID'))
    name = escape(request.form.get('IV_NAME'))
    category = escape(request.form.get('IV_CATEGORY'))
    qty = escape(request.form.get('IV_QTY'))
    buy_price = escape(request.form.get('IV_BUYPRICE'))
    sell_price = escape(request.form.get('IV_SELLPRICE'))
    uom = escape(request.form.get('IV_UOM'))

    return Inventory.update(id, name, category, qty, buy_price, sell_price, uom)

@app.route("/inventory/deactivate/", methods = ["POST"])
def inventory_deactivate():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form.get('IV_ID'))

    return Inventory.deactivate(id)

@app.route("/inventory/activate/", methods = ["POST"])
def inventory_activate():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form.get('IV_ID'))

    return Inventory.activate(id)
# End Inventory Route
# Supplier Route

@app.route("/supplier/")
def supplier():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Supplier.read()

@app.route("/supplier/add/", methods = ["POST","GET"])
def supplier_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('supplier/add.html')

    name = escape(request.form.get('AP_NAME'))
    address = escape(request.form.get('AP_ADDRESS'))
    phone = escape(request.form.get('AP_PHONE'))
    email = escape(request.form.get('AP_EMAIL'))

    return Supplier.add(name, address, phone, email)

@app.route("/supplier/read/", methods = ["POST"])
def supplier_read():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['search_id'])

    return Supplier.read(id)

@app.route("/supplier/update/", methods = ["POST"])
def supplier_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form.get('AP_ID'))
    name = escape(request.form.get('AP_NAME'))
    address = escape(request.form.get('AP_ADDRESS'))
    phone = escape(request.form.get('AP_PHONE'))
    email = escape(request.form.get('AP_EMAIL'))

    return Supplier.update(id, name, address, phone, email)

# End Supplier Route
# Customer Route

@app.route("/customer/")
def customer():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    return Customer.read()

@app.route("/customer/add/", methods = ["POST","GET"])
def customer_add():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('customer/add.html')

    name = escape(request.form.get('AR_NAME'))
    address = escape(request.form.get('AR_ADDRESS'))
    phone = escape(request.form.get('AR_PHONE'))
    email = escape(request.form.get('AR_EMAIL'))

    return Customer.add(name, address, phone, email)

@app.route("/customer/read/", methods = ["POST"])
def customer_read():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form['search_id'])

    return Customer.read(id)

@app.route("/customer/update/", methods = ["POST"])
def customer_update():
    if not User.is_logged_in():
        return redirect(url_for('login'))

    id = escape(request.form.get('AR_ID'))
    name = escape(request.form.get('AR_NAME'))
    address = escape(request.form.get('AR_ADDRESS'))
    phone = escape(request.form.get('AR_PHONE'))
    email = escape(request.form.get('AR_EMAIL'))

    return Customer.update(id, name, address, phone, email)

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

    module = User.module_id
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