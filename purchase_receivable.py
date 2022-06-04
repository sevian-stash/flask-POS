from flask import render_template, flash, redirect, url_for, session
from model import Model
from user import User
from datetime import datetime, date

class Purchase_Receivable(object):
    User = User()
    Model = Model()

    def __init__(self):
        super(Purchase_Receivable, self).__init__()
        self.detail_row_len = 200

    def add(self, data):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'PO','_CREATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Supplier Check
        supplier = self.Model.read('ap01', ['AP_ID'], {'AP_ID':data['pr11']['PR_CUSTOMERID']})
        if supplier == []:
            flash("Supplier not Found")
            return redirect(url_for('purchase_receivable'))

        # Supplier Check
        purchase_order_id = self.Model.read('po11', ['PO_ID'], {'PO_ID':data['pr11']['PR_PURCHASEORDERID']})
        if supplier == []:
            flash("Purchase Order ID not Found")
            return redirect(url_for('purchase_receivable'))

        # Get User Count
        row_len = self.Model.read('pr11')
        row_len = len(row_len) + 1 if row_len else '1'

        # Insert Summary
        model_status = self.Model.insert(
            'pr11', 
            {
                'PR_ID':f'GRN-{row_len}',
                'PR_PURCHASEORDERID': data['pr11']['PR_PURCHASEORDERID'],
                'PR_CUSTOMERID': data['pr11']['PR_CUSTOMERID'],
                'PR_QTY': data['pr11']['PR_QTY'] if bool(data['pr11']['PR_QTY']) else 0,
                'PR_AMOUNT': data['pr11']['PR_AMOUNT'] if bool(data['pr11']['PR_AMOUNT']) else 0,
                'PR_STATUS': data['pr11']['PR_STATUS'] if str(data['pr11']['PR_STATUS']) != 'None' else '1',
                'CRTD_DT':datetime.date(datetime.now()),
                'CRTD_BY':session_id
            }
        )

        if model_status != 0:
            flash(f'Failed to Add Purchase Receivable')
            return redirect(url_for('purchase_receivable'))

        # Insert Detail
        for key in data['pr12']:
            # Item Check
            item = self.Model.read('iv01', ['IV_ID'], {'IV_ID':data['pr12'][key]['PR_ITEMID']})
            
            if item != []:
                model_status = self.Model.insert(
                    'pr12', 
                    {
                        'PR_ID':f'GRN-{row_len}',
                        'PR_ITEMID': data['pr12'][key]['PR_ITEMID'],
                        'PR_ITEMNAME': data['pr12'][key]['PR_ITEMNAME'],
                        'PR_ITEMPRICE': data['pr12'][key]['PR_ITEMPRICE'] if bool(data['pr12'][key]['PR_ITEMPRICE']) else 0,
                        'PR_ITEMQTY': data['pr12'][key]['PR_ITEMQTY'] if bool(data['pr12'][key]['PR_ITEMQTY']) else 0,
                        'CRTD_DT':datetime.date(datetime.now()),
                        'CRTD_BY':session_id
                    }
                )

                if model_status != 0:
                    flash(f'Failed to Add Purchase Receivable')
                    return redirect(url_for('purchase_receivable'))

        flash(f'GRN-{row_len} has been Created')

        return redirect(url_for('purchase_receivable'))

    def read(self, id=None):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'PO','_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        data = []

        if id is None:
            # All Users
            data = self.Model.read(
                'pr11 pr LEFT JOIN ap01 ap ON pr.PR_CUSTOMERID = ap.AP_ID',
                ['pr.PR_ID','ap.AP_NAME','pr.PR_AMOUNT', 'pr.CRTD_DT'])

            return_path = 'purchase_receivable/index.html'

        else:
            data.append(id)

            # Check if Exists
            db_ret = self.Model.read('pr11','*',{'PR_ID':id})

            if db_ret == []:
                flash('ID Not Found')
                return redirect(url_for('purchase_receivable'))

            # Append Summary
            (*summary,) = db_ret[0]
            data.append(summary)

            # Append Details
            data.append(self.Model.read('pr12','*',{'PR_ID':id}))
            data.append(self.detail_row_len)

            print(data)

            return_path = 'purchase_receivable/detail.html'

        return render_template(return_path, message=data)

    def update(self, data):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'PO','_UPDATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Check if ID Exists
        db_ret = self.Model.read('pr11', ['PR_ID'],{'PR_ID':data['pr11']['PR_ID']})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('purchase_receivable'))

        # Update New Value
        model_status = self.Model.update('pr11',
            {
                'PR_PURCHASEORDERID':data['pr11']['PR_PURCHASEORDERID'],
                'PR_CUSTOMERID':data['pr11']['PR_CUSTOMERID'],
                'PR_QTY': data['pr11']['PR_QTY'] if bool(data['pr11']['PR_QTY']) else 0,
                'PR_AMOUNT': data['pr11']['PR_AMOUNT'] if bool(data['pr11']['PR_AMOUNT']) else 0,
                'PR_STATUS': data['pr11']['PR_STATUS'] if str(data['pr11']['PR_STATUS']) != 'None' else '1',
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'PR_ID':data['pr11']['PR_ID']}
        )

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('purchase_receivable'))

        model_status = self.Model.delete('pr12',{'PR_ID':data['pr11']['PR_ID']})

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('purchase_receivable'))

        for item in data['pr12']:
            model_status = self.Model.insert('pr12',
                {
                    'PR_ID':data['pr12'][item]['PR_ID'],
                    'PR_ITEMID':data['pr12'][item]['PR_ITEMID'],
                    'PR_ITEMNAME':data['pr12'][item]['PR_ITEMNAME'],
                    'PR_ITEMPRICE': data['pr12'][item]['PR_ITEMPRICE'] if bool(data['pr12'][item]['PR_ITEMPRICE']) else 0,
                    'PR_ITEMQTY': data['pr12'][item]['PR_ITEMQTY'] if bool(data['pr12'][item]['PR_ITEMQTY']) else 0,
                    'UPDT_DT':datetime.date(datetime.now()),
                    'UPDT_BY':session_id
                }
            )

            if model_status != 0:
                flash('Failed to Save')

        if model_status == 0:
            flash(f'{data["pr11"]["PR_ID"]} has been Updated')

        return redirect(url_for('purchase_receivable'))

    def activate(self, id):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'PO','_CREATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Check if ID Exists
        db_ret = self.Model.read('pr11', ['PR_ID'],{'PR_ID':id})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('purchase_receivable'))

        # Update New Value
        model_status = self.Model.update('pr11',
            {
                'PR_STATUS': '2',
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'PR_ID':id}
        )

        if model_status != 0:
            flash('Failed to Save')
            return redirect(url_for('purchase_receivable'))

        return redirect(url_for('purchase_receivable'))

