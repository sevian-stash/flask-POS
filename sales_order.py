import re
from flask import render_template, flash, redirect, url_for, current_app
from model import Model
from user import User
from account_receivable import Account_Receivable
from inventory import Inventory
from datetime import datetime, date, timedelta
from flask_mail import Message

class Sales_Order(object):
    User = User()
    Model = Model()
    Account_Receivable = Account_Receivable()
    Inventory = Inventory()
    
    def __init__(self):
        super(Sales_Order, self).__init__()
        self.detail_row_len = 200

    def add(self, data):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'SO','_CREATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Customer Check
        customer = self.Model.read('ar01', ['AR_ID'], {'AR_ID':data['iv11']['IV_CUSTOMERID']})
        if customer == []:
            flash("Customer not Found")
            return redirect(url_for('transaction'))

        sales_order_id = self.Model.read('iv11', ['IV_ID'], {'IV_ID':data['iv11']['IV_ID']})
        if sales_order_id != []:
            flash("Duplicate SO ID")
            return redirect(url_for('transaction'))

        # Get User Count
        row_len = self.Model.read('iv11')
        row_len = len(row_len) + 1 if row_len else '1'

        # Insert Summary
        model_status = self.Model.insert(
            'iv11', 
            {
                'IV_ID':f'SO-{row_len}',
                'IV_CUSTOMERID': data['iv11']['IV_CUSTOMERID'],
                'IV_QTY': data['iv11']['IV_QTY'] if bool(data['iv11']['IV_QTY']) else 0,
                'IV_AMOUNT': data['iv11']['IV_AMOUNT'] if bool(data['iv11']['IV_AMOUNT']) else 0,
                'CRTD_DT':datetime.date(datetime.now()),
                'CRTD_BY':session_id
            }
        )

        if model_status != 0:
            flash(f'Failed to Add Sales Order Summary')
            return redirect(url_for('transaction'))

        # Insert Detail
        for key in data['iv12']:
            # Item Check
            item = self.Model.read('iv01', ['IV_ID'], {'IV_ID':data['iv12'][key]['IV_ITEMID']})
            
            if item != []:
                model_status = self.Model.insert(
                    'iv12', 
                    {
                        'IV_ID':f'SO-{row_len}',
                        'IV_ITEMID': data['iv12'][key]['IV_ITEMID'],
                        'IV_ITEMNAME': data['iv12'][key]['IV_ITEMNAME'],
                        'IV_ITEMPRICE': data['iv12'][key]['IV_ITEMPRICE'] if bool(data['iv12'][key]['IV_ITEMPRICE']) else 0,
                        'IV_ITEMQTY': data['iv12'][key]['IV_ITEMQTY'] if bool(data['iv12'][key]['IV_ITEMQTY']) else 0,
                        'UPDT_DT':datetime.date(datetime.now()),
                        'UPDT_BY':session_id
                    }
                )

                if model_status != 0:
                    flash(f'Failed to Add Sales Order Detail')
                    return redirect(url_for('transaction'))

        flash(f'SO-{row_len} has been Created')

        if data['iv11']['IV_PAYMENT'] == '3':
            return self.account_receivable_add(f'SO-{row_len}', data)

        self.inventory_update(data)

        return redirect(url_for('transaction'))

    def read(self, id=None):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'SO','_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        data = []

        if id is None:
            # All Users
            data = self.Model.read(
                'iv11 iv LEFT JOIN ar01 ar ON iv.IV_CUSTOMERID = ar.AR_ID',
                ['iv.IV_ID','ar.AR_NAME','iv.IV_AMOUNT', 'iv.CRTD_DT'])

            return_path = 'sales_order/index.html'

        else:
            data.append(id)

            # Check if Exists
            db_ret = self.Model.read('iv11','*',{'IV_ID':id})

            if db_ret == []:
                flash('ID Not Found')
                return redirect(url_for('sales_order'))

            # Append Summary
            (*summary,) = db_ret[0]
            data.append(summary)

            # Append Details
            data.append(self.Model.read('iv12','*',{'IV_ID':id}))
            data.append(self.detail_row_len)

            return_path = 'sales_order/detail.html'

        return render_template(return_path, message=data)

    def update(self, data):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'SO','_UPDATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Check if ID Exists
        db_ret = self.Model.read('iv11', ['IV_ID'],{'IV_ID':data['iv11']['IV_ID']})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('sales_order'))

        # Update New Value
        model_status = self.Model.update('iv11',
            {
                'IV_CUSTOMERID':data['iv11']['IV_CUSTOMERID'],
                'IV_QTY': data['iv11']['IV_QTY'] if bool(data['iv11']['IV_QTY']) else 0,
                'IV_AMOUNT': data['iv11']['IV_AMOUNT'] if bool(data['iv11']['IV_AMOUNT']) else 0,
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'IV_ID':data['iv11']['IV_ID']}
        )

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('sales_order'))

        model_status = self.Model.delete('iv12',{'IV_ID':data['iv11']['IV_ID']})

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('sales_order'))

        for item in data['iv12']:
            model_status = self.Model.insert('iv12',
                {
                    'IV_ID':data['iv12'][item]['IV_ID'],
                    'IV_ITEMID':data['iv12'][item]['IV_ITEMID'],
                    'IV_ITEMNAME':data['iv12'][item]['IV_ITEMNAME'],
                    'IV_ITEMPRICE': data['iv12'][item]['IV_ITEMPRICE'] if bool(data['iv12'][item]['IV_ITEMPRICE']) else 0,
                    'IV_ITEMQTY': data['iv12'][item]['IV_ITEMQTY'] if bool(data['iv12'][item]['IV_ITEMQTY']) else 0,
                    'UPDT_DT':datetime.date(datetime.now()),
                    'UPDT_BY':session_id
                }
            )

            if model_status != 0:
                flash('Failed to Save')

        if model_status == 0:
            flash(f'{data["iv11"]["IV_ID"]} has been Updated')

        return redirect(url_for('sales_order'))

    #Sync with AR
    def account_receivable_add(self, id, data):
        # Get User Count
        row_len = self.Model.read('ar11')
        row_len = len(row_len) + 1 if row_len else '1'

        ar_data = dict()

        # Insert Summary
        ar_duedt = datetime.date(datetime.now() + timedelta(days=14))
        ar_duedt = datetime.strptime(str(ar_duedt),'%Y-%m-%d').strftime('%d/%m/%Y')
        ar_data.update({'ar11':
            {
                'AR_CUSTOMERID': data['iv11']['IV_CUSTOMERID'],
                'AR_SALESORDERID': id,
                'AR_AMOUNT': data['iv11']['IV_AMOUNT'] if bool(data['iv11']['IV_AMOUNT']) else 0,
                'AR_QTY': data['iv11']['IV_QTY'] if bool(data['iv11']['IV_QTY']) else 0,
                'AR_STATUS': '2',
                'AR_DUEDT': ar_duedt
            }
        })

        # Insert Detail
        ar_data.update({'ar12': {}})
        for idx,key in enumerate(data['iv12']):
            ar_data['ar12'].update({f'row_{idx}': {
                'AR_ITEMID':data['iv12'][key]['IV_ITEMID'],
                'AR_ITEMNAME':data['iv12'][key]['IV_ITEMNAME'],
                'AR_ITEMQTY':data['iv12'][key]['IV_ITEMPRICE'] if bool(data['iv12'][key]['IV_ITEMPRICE']) else 0,
                'AR_ITEMPRICE':data['iv12'][key]['IV_ITEMQTY'] if bool(data['iv12'][key]['IV_ITEMQTY']) else 0
                }
            })

        self.Account_Receivable.add(ar_data)

        return redirect(url_for('transaction'))

    # Sync with IV
    def inventory_update(self, data):
        for row in data['iv12']:
            (*previous_qty,) = self.Model.read('iv01',['IV_QTY'],{'IV_ID':data['iv12'][row]['IV_ITEMID']})[0]
            if previous_qty == []:
                flash('Item ID Not Found')

            previous_qty = int(previous_qty[0])
            new_qty = previous_qty - int(data['iv12'][row]['IV_ITEMQTY'])

            
            self.Model.update('iv01',{'IV_QTY':new_qty},{'IV_ID':data['iv12'][row]['IV_ITEMID']})
        return True

    def email(self, mail, data):

        so_id = data['iv11']['IV_ID']
        customer_id = data['iv11']['IV_CUSTOMERID']
        so_qty = data['iv11']['IV_QTY']
        so_amount = data['iv11']['IV_AMOUNT']

        (*customer,) = self.Model.read('ar01',['AR_NAME','AR_EMAIL'],{'AR_ID': customer_id})[0]
        name = customer[0]
        recipient = customer[1] if customer[1] else current_app.config['MAIL_DEFAULT_SENDER']

        message = Message(f'Transaksi Happy Pancing : {so_id}', recipients = [recipient])
        message.body = f'Halo {name}! Terima kasih sudah berbelanja di Toko Happy Pancing.'
        message.body += f"\nIni struk perbelanjaan kamu\nTotal Barang {so_qty} dan total harga {'Rp.{:,.2f}'.format(int(so_amount))}"

        for idx,row in enumerate(data['iv12']):
            message.body += f"\n{idx + 1}. "
            message.body += f"{data['iv12'][row]['IV_ITEMID']} "
            message.body += f"{data['iv12'][row]['IV_ITEMNAME']} "
            message.body += f"{data['iv12'][row]['IV_ITEMQTY']}x "
            message.body += f"{'Rp.{:,.2f}'.format(int(data['iv12'][row]['IV_ITEMPRICE']))} : "
            message.body += f"{'Rp.{:,.2f}'.format(int(data['iv12'][row]['IV_ITEMQTY']) * int(data['iv12'][row]['IV_ITEMPRICE']))}"

        message.body += '\n\nTertanda,\nToko Happy Pancing.'
        mail.send(message)

        return True


