from flask import render_template, flash, redirect, url_for, session
from model import Model
from user import User
from datetime import datetime, date

class Inventory(object):
    User = User()
    Model = Model()
    
    def __init__(self):
        super(Inventory, self).__init__()

    def add(self, name, category, qty, amount, uom):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'IV','_CREATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))


        # Get User Count
        row_len = self.Model.read('iv01')
        row_len = len(row_len) + 1 if row_len else '1'

        self.Model.insert(
            'iv01', 
            {
                'IV_ID':f'IV-{row_len}',
                'IV_NAME':name if bool(name) else f'IV-{row_len}',
                'IV_CATEGORY':category if str(category) != 'None' else 3,
                'IV_QTY':qty if bool(qty) else 0,
                'IV_AMOUNT':amount if bool(amount) else 0,
                'IV_UOM':uom if str(uom) != 'None' else 2,
                'CRTD_DT':datetime.date(datetime.now()),
                'CRTD_BY':session_id
            }
        )

        return redirect(url_for('inventory'))

    def read(self, id=None):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'IV','_READ')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        data = []

        if id is None:
            # All Users
            data = self.Model.read('iv01',['IV_ID','IV_NAME','IV_QTY','IV_AMOUNT'])
            return_path = 'inventory/index.html'
        else:
            data.append(id)

            # Check if Exists
            db_ret = self.Model.read('iv01','*',{'IV_ID':id})

            if db_ret == []:
                flash('ID Not Found')
                return redirect(url_for('inventory'))

            # Append Summary
            (*summary,) = db_ret[0]
            data.append(summary)

            # Append Details
            data.append(self.Model.read('po11','*',{'PO_CUSTOMERID':id}))
            return_path = 'inventory/detail.html'

        return render_template(return_path, message=data)

    def update(self, id, name, category, qty, amount, uom):
        session_id = self.User.get_session_id()
        # Status Check
        account_status = self.User.is_active(session_id)
        if not account_status:
            flash("Account is Deactivated")
            return redirect(url_for('login'))

        # Access Check
        access_permission = self.User.is_allowed(session_id,'IV','_UPDATE')
        if not access_permission:
            flash("No Access Allowed")
            return redirect(url_for('index'))

        # Check if ID Exists
        db_ret = self.Model.read('iv01', ['IV_ID'],{'IV_ID':id})
        if db_ret == []:
            flash('ID Not Found')
            return redirect(url_for('inventory'))

        # Update New Value
        self.Model.update('iv01',
            {
                'IV_NAME':name if bool(name) else f'IV-{row_len}',
                'IV_CATEGORY':category,
                'IV_QTY':qty if bool(qty) else 0,
                'IV_AMOUNT':amount if bool(amount) else 0,
                'IV_UOM':uom,
                'UPDT_DT':datetime.date(datetime.now()),
                'UPDT_BY':session_id
            },
            {'IV_ID':id}
        )

        return redirect(url_for('inventory'))

# End Class/Method