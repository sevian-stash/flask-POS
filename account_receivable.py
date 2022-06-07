from flask import render_template, flash, redirect, url_for
from model import Model
from user import User
from datetime import datetime, date

class Account_Receivable(object):
    User = User()
    Model = Model()
    
    def __init__(self):
        super(Account_Receivable, self).__init__()
        self.detail_row_len = 200
    
    def add(self, data):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AR','_CREATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Customer Check
        supplier = self.Model.read('ar01', ['AR_ID'], {'AR_ID':data['ar11']['AR_CUSTOMERID']})
        if supplier == []:
            flash("Supplier not Found")
            return redirect(url_for('account_receivable_add'))

        sales_order_id = self.Model.read('iv11', ['IV_ID'], {'IV_ID':data['ar11']['AR_SALESORDERID']})
        if sales_order_id == []:
            flash("Sales Order ID not Found")
            return redirect(url_for('account_receivable_add'))

        # Get User Count
        row_len = self.Model.read('ar11')
        row_len = len(row_len) + 1 if row_len else '1'

        # Insert Summary
        due_dt = str(data['ar11']['AR_DUEDT'])
        model_status = self.Model.insert(
            'ar11', 
            {
                'AR_ID':f'AR-{row_len}',
                'AR_CUSTOMERID': data['ar11']['AR_CUSTOMERID'],
                'AR_SALESORDERID': data['ar11']['AR_SALESORDERID'],
                'AR_AMOUNT': data['ar11']['AR_AMOUNT'] if bool(data['ar11']['AR_AMOUNT']) else 0,
                'AR_STATUS': data['ar11']['AR_STATUS'] if str(data['ar11']['AR_STATUS']) != 'None' else '1',
                'AR_DUEDT':datetime.strptime(due_dt, "%d/%m/%Y").date(),
                'CRTD_DT':datetime.date(datetime.now()),
                'CRTD_BY':session_id
            }
        )

        if model_status != 0:
            flash(f'Failed to Add Account Receivable')
            return redirect(url_for('account_receivable'))

        # Insert Detail
        for key in data['ar12']:
            # Item Check
            item = self.Model.read('iv01', ['IV_ID'], {'IV_ID':data['ar12'][key]['AR_ITEMID']})
            
            if item != []:
                model_status = self.Model.insert(
                    'ar12', 
                    {
                        'AR_ID':f'AR-{row_len}',
                        'AR_ITEMID': data['ar12'][key]['AR_ITEMID'],
                        'AR_ITEMNAME': data['ar12'][key]['AR_ITEMNAME'],
                        'AR_ITEMPRICE': data['ar12'][key]['AR_ITEMPRICE'] if bool(data['ar12'][key]['AR_ITEMPRICE']) else 0,
                        'AR_ITEMQTY': data['ar12'][key]['AR_ITEMQTY'] if bool(data['ar12'][key]['AR_ITEMQTY']) else 0,
                        'UPDT_DT':datetime.date(datetime.now()),
                        'UPDT_BY':session_id
                    }
                )

                if model_status != 0:
                    flash(f'Failed to Add Account Receivable')
                    return redirect(url_for('account_receivable'))

        flash(f'AR-{row_len} has been Created')

        return redirect(url_for('account_receivable'))

    def read(self, id=None):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AR','_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        data = []

        if id is None:
            # All Users
            data = self.Model.read(
                'ar11 a1 LEFT JOIN ar01 a0 ON a1.AR_CUSTOMERID = a0.AR_ID',
                ['a1.AR_ID','a0.AR_NAME','a1.AR_AMOUNT', 'a1.CRTD_DT'])
            print(data)

            return_path = 'account_receivable/index.html'

        else:
            data.append(id)

            # Check if Exists
            db_ret = self.Model.read('ar11','*',{'AR_ID':id})

            if db_ret == []:
                flash('ID Not Found')
                return redirect(url_for('account_receivable'))

            # Append Summary
            (*summary,) = db_ret[0]
            data.append(summary)

            # Append Details
            data.append(self.Model.read('ar12','*',{'AR_ID':id}))
            data.append(self.detail_row_len)

            print(data)

            return_path = 'account_receivable/detail.html'

        return render_template(return_path, message=data)

    def update(self, data):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AR','_UPDATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Check if ID Exists
        db_ret = self.Model.read('ar11', ['AR_ID'],{'AR_ID':data['ar11']['AR_ID']})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('account_receivable'))

        # Update New Value
        due_dt = str(data['ar11']['AR_DUEDT'])
        model_status = self.Model.update('ar11',
            {
                'AR_CUSTOMERID':data['ar11']['AR_CUSTOMERID'],
                'AR_SALESORDERID':data['ar11']['AR_SALESORDERID'],
                'AR_QTY': data['ar11']['AR_QTY'] if bool(data['ar11']['AR_QTY']) else 0,
                'AR_AMOUNT': data['ar11']['AR_AMOUNT'] if bool(data['ar11']['AR_AMOUNT']) else 0,
                'AR_STATUS': data['ar11']['AR_STATUS'] if str(data['ar11']['AR_STATUS']) != 'None' else '1',
                'AR_DUEDT':datetime.strptime(due_dt, "%d/%m/%Y").date(),
                'AR_PAIDDT':datetime.date(datetime.now()) if str(data['ar11']['AR_STATUS']) == '3' else None,
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'AR_ID':data['ar11']['AR_ID']}
        )

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('account_receivable'))

        model_status = self.Model.delete('ar12',{'AR_ID':data['ar11']['AR_ID']})

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('account_receivable'))

        for item in data['ar12']:
            model_status = self.Model.insert('ar12',
                {
                    'AR_ID':data['ar12'][item]['AR_ID'],
                    'AR_ITEMID':data['ar12'][item]['AR_ITEMID'],
                    'AR_ITEMNAME':data['ar12'][item]['AR_ITEMNAME'],
                    'AR_ITEMPRICE': data['ar12'][item]['AR_ITEMPRICE'] if bool(data['ar12'][item]['AR_ITEMPRICE']) else 0,
                    'AR_ITEMQTY': data['ar12'][item]['AR_ITEMQTY'] if bool(data['ar12'][item]['AR_ITEMQTY']) else 0,
                    'UPDT_DT':datetime.date(datetime.now()),
                    'UPDT_BY':session_id
                }
            )

            if model_status != 0:
                flash('Failed to Save')

        if model_status == 0:
            flash(f'{data["ar11"]["AR_ID"]} has been Updated')

        return redirect(url_for('account_receivable'))

    def activate(self, id):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'AR','_CREATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Check if ID Exists
        db_ret = self.Model.read('ar11', ['AR_ID'],{'AR_ID':id})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('account_receivable'))

        # Update New Value
        model_status = self.Model.update('ar11',
            {
                'AR_STATUS': '2',
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'AR_ID':id}
        )

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('account_receivable'))

        flash(f'{id} Activated')

        return redirect(url_for('account_receivable'))

