from flask import render_template, flash, redirect, url_for
from model import Model
from user import User
from datetime import datetime, date

class Account_Payable(object):
    User = User()
    Model = Model()

    def __init__(self):
        super(Account_Payable, self).__init__()
        self.detail_row_len = 200
    
    def add(self, data):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AP','_CREATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Supplier Check
        supplier = self.Model.read('ap01', ['AP_ID'], {'AP_ID':data['ap11']['AP_CUSTOMERID']})
        if supplier == []:
            flash("Supplier not Found")
            return redirect(url_for('account_payable_add'))

        # Supplier Check
        purchase_order_id = self.Model.read('po11', ['PO_ID'], {'PO_ID':data['ap11']['AP_PURCHASEORDERID']})
        if purchase_order_id == []:
            flash("Purchase Order ID not Found")
            return redirect(url_for('account_payable_add'))

        # Get User Count
        row_len = self.Model.read('ap11')
        row_len = len(row_len) + 1 if row_len else '1'

        # Insert Summary
        due_dt = str(data['ap11']['AP_DUEDT'])
        model_status = self.Model.insert(
            'ap11', 
            {
                'AP_ID':f'AP-{row_len}',
                'AP_CUSTOMERID': data['ap11']['AP_CUSTOMERID'],
                'AP_PURCHASEORDERID': data['ap11']['AP_PURCHASEORDERID'],
                'AP_AMOUNT': data['ap11']['AP_AMOUNT'] if bool(data['ap11']['AP_AMOUNT']) else 0,
                'AP_STATUS': data['ap11']['AP_STATUS'] if str(data['ap11']['AP_STATUS']) != 'None' else '1',
                'AP_DUEDT':datetime.strptime(due_dt, "%d/%m/%Y").date(),
                'CRTD_DT':datetime.date(datetime.now()),
                'CRTD_BY':session_id
            }
        )

        if model_status != 0:
            flash(f'Failed to Add Purchase Receivable')
            return redirect(url_for('account_payable'))

        # Insert Detail
        for key in data['ap12']:
            # Item Check
            item = self.Model.read('iv01', ['IV_ID'], {'IV_ID':data['ap12'][key]['AP_ITEMID']})
            
            if item != []:
                model_status = self.Model.insert(
                    'ap12', 
                    {
                        'AP_ID':f'AP-{row_len}',
                        'AP_ITEMID': data['ap12'][key]['AP_ITEMID'],
                        'AP_ITEMNAME': data['ap12'][key]['AP_ITEMNAME'],
                        'AP_ITEMPRICE': data['ap12'][key]['AP_ITEMPRICE'] if bool(data['ap12'][key]['AP_ITEMPRICE']) else 0,
                        'AP_ITEMQTY': data['ap12'][key]['AP_ITEMQTY'] if bool(data['ap12'][key]['AP_ITEMQTY']) else 0,
                        'UPDT_DT':datetime.date(datetime.now()),
                        'UPDT_BY':session_id
                    }
                )

                if model_status != 0:
                    flash(f'Failed to Add Purchase Receivable')
                    return redirect(url_for('account_payable'))

        flash(f'AP-{row_len} has been Created')

        return redirect(url_for('account_payable'))

    def read(self, id=None):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AP','_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        data = []

        if id is None:
            # All Users
            data = self.Model.read(
                'ap11 a1 LEFT JOIN ap01 a0 ON a1.AP_CUSTOMERID = a0.AP_ID',
                ['a1.AP_ID','a0.AP_NAME','a1.AP_AMOUNT', 'a1.CRTD_DT'])
            print(data)

            return_path = 'account_payable/index.html'

        else:
            data.append(id)

            # Check if Exists
            db_ret = self.Model.read('ap11','*',{'AP_ID':id})

            if db_ret == []:
                flash('ID Not Found')
                return redirect(url_for('account_payable'))

            # Append Summary
            (*summary,) = db_ret[0]
            data.append(summary)

            # Append Details
            data.append(self.Model.read('ap12','*',{'AP_ID':id}))
            data.append(self.detail_row_len)

            print(data)

            return_path = 'account_payable/detail.html'

        return render_template(return_path, message=data)

    def update(self, data):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AP','_UPDATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Check if ID Exists
        db_ret = self.Model.read('ap11', ['AP_ID'],{'AP_ID':data['ap11']['AP_ID']})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('account_payable'))

        # Update New Value
        due_dt = str(data['ap11']['AP_DUEDT'])
        model_status = self.Model.update('ap11',
            {
                'AP_CUSTOMERID':data['ap11']['AP_CUSTOMERID'],
                'AP_PURCHASEORDERID':data['ap11']['AP_PURCHASEORDERID'],
                'AP_QTY': data['ap11']['AP_QTY'] if bool(data['ap11']['AP_QTY']) else 0,
                'AP_AMOUNT': data['ap11']['AP_AMOUNT'] if bool(data['ap11']['AP_AMOUNT']) else 0,
                'AP_STATUS': data['ap11']['AP_STATUS'] if str(data['ap11']['AP_STATUS']) != 'None' else '1',
                'AP_DUEDT':datetime.strptime(due_dt, "%d/%m/%Y").date(),
                'AP_PAIDDT':datetime.date(datetime.now()) if str(data['ap11']['AP_STATUS']) == '3' else None,
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'AP_ID':data['ap11']['AP_ID']}
        )

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('account_payable'))

        model_status = self.Model.delete('ap12',{'AP_ID':data['ap11']['AP_ID']})

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('account_payable'))

        for item in data['ap12']:
            model_status = self.Model.insert('ap12',
                {
                    'AP_ID':data['ap12'][item]['AP_ID'],
                    'AP_ITEMID':data['ap12'][item]['AP_ITEMID'],
                    'AP_ITEMNAME':data['ap12'][item]['AP_ITEMNAME'],
                    'AP_ITEMPRICE': data['ap12'][item]['AP_ITEMPRICE'] if bool(data['ap12'][item]['AP_ITEMPRICE']) else 0,
                    'AP_ITEMQTY': data['ap12'][item]['AP_ITEMQTY'] if bool(data['ap12'][item]['AP_ITEMQTY']) else 0,
                    'UPDT_DT':datetime.date(datetime.now()),
                    'UPDT_BY':session_id
                }
            )

            if model_status != 0:
                flash('Failed to Save')

        if model_status == 0:
            flash(f'{data["ap11"]["AP_ID"]} has been Updated')

        return redirect(url_for('account_payable'))

    def activate(self, id):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AP','_CREATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Check if ID Exists
        db_ret = self.Model.read('ap11', ['AP_ID'],{'AP_ID':id})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('account_payable'))

        # Update New Value
        model_status = self.Model.update('ap11',
            {
                'AP_STATUS': '2',
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'AP_ID':id}
        )

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('account_payable'))

        flash(f'{id} Activated')

        return redirect(url_for('account_payable'))

